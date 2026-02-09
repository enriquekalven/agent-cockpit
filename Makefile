# --- A2UI Starter Makefile ---

# Project Variables
PYTHON = $(shell if [ -f "./.venv/bin/python3.14" ]; then echo "./.venv/bin/python3.14"; elif [ -d ".venv" ]; then echo "./.venv/bin/python"; elif command -v python >/dev/null 2>&1; then echo "python"; else echo "python3"; fi)
PROJECT_ID ?= $(shell gcloud config get-value project)
REGION ?= us-central1
SERVICE_NAME = agent-ops-backend
IMAGE_TAG = us-central1-docker.pkg.dev/$(PROJECT_ID)/agent-repo/$(SERVICE_NAME):latest

.PHONY: help dev build deploy-cloud-run deploy-firebase deploy-gke audit deploy-prod scan-secrets ui-audit audit-all watch

help:
	@echo "Available commands:"
	@echo "  make dev                       - Start local development server"
	@echo "  make audit                     - [MASTER] Quick Safe-Build (uvx agentops-cockpit report --mode quick)"
	@echo "  make audit-deep                - [MASTER] Deep System Audit (uvx agentops-cockpit report --mode deep)"
	@echo "  make optimizer-audit           - [CODE] Quick code audit (uvx agentops-cockpit audit --quick)"
	@echo "  make arch-review               - [ARCH] Wisdom Store Maturity Audit (v1.4)"
	@echo "  make arch-review-export        - [ARCH] Generate Executive v1.4 HTML Report"
	@echo "  make arch-benchmark            - [ARCH] Run Reliability Waterfall (Stress Test)"
	@echo "  make apply-fixes               - [PHASE 4] Auto-remediate detected architectural gaps"
	@echo "  make propose-fixes             - [PHASE 5] Create fix branch and commit remediations"
	@echo "  make quality-baseline          - [QUALITY] Hill Climbing Optimization (v1.4)"
	@echo "  make rag-truth                 - [QUALITY] RAG Fidelity & Grounding Audit (v1.4)"
	@echo "  make red-team                  - [SECURITY] Brand Safety Playbook Audit (v1.4)"
	@echo "  make scan-secrets              - [SECURITY] Zero-Trust Hygiene Scanner"
	@echo "  make reliability               - Run unit tests and regression suite"
	@echo "  make smoke-test                - [E2E] End-to-End Persona Journey smoke tests"
	@echo "  make regression                - [FULL] Master Reliability + Smoke Tests"
	@echo "  make diagnose                  - [DevEx] System health check and env diagnosis"
	@echo "  make load-test                 - Run base load test"
	@echo "  make deploy-prod               - [MASTER] Production Readiness Auditor (v1.4.1)"
	@echo "  make deploy-cloud-run          - Deploy to Google Cloud Run"
	@echo "  make deploy-firebase           - Deploy to Firebase Hosting"
	@echo "  make watch                     - Track ecosystem updates (ADK, A2A, LangChain, etc.)"

dev:
	npm run dev

build:
	npm run build

# 🏁 Master Audit: Safe-Build (Essential for dev velocity)
audit:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode quick

# 🚀 Deep Master Audit: Full benchmarks and stress tests
audit-deep:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode deep

# 🌐 Global Audit: Point the Cockpit at an external repository
# Usage: make audit-all TARGET=/path/to/your/agent
TARGET ?= .
audit-all:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode quick --path $(TARGET)

# 🛡️ Reliability: Unit tests and regression suite
reliability:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.reliability audit

# 🧪 Smoke Test: E2E Persona Validation
smoke-test:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.reliability audit --smoke

# 🚀 Regression: The Full Suite (Unit + Smoke)
regression:
	@PYTHONPATH=src $(PYTHON) -c "from agent_ops_cockpit.ops.reliability import run_regression_suite; run_regression_suite()"

# 🩺 Diagnose: DevEx system check
diagnose:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main diagnose

# 🔍 The Optimizer: Audit specific agent file for code-level waste
optimizer-audit:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.optimizer audit src/agent_ops_cockpit/agent.py --quick

# 🔍 Deep Optimizer: Fetch live SDK evidence
optimizer-audit-deep:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.optimizer audit src/agent_ops_cockpit/agent.py

# 🏛️ Architecture: Design review against Google Well-Architected Framework
arch-review:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review audit

# 🏛️ Executive: Generate v1.4 HTML Summary
arch-review-export:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review audit --export

# 🌊 Reliability: v1.2 Automated Benchmarking
arch-benchmark:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review benchmark --count 50

# 🚀 The Closer: Auto-remediation engine for architecture gaps
apply-fixes:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review apply-fixes

# 🌿 The Ambassador: Autonomous PR Factory
propose-fixes:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review propose-fixes

# 🧗 Quality: Iterative Hill Climbing optimization
quality-baseline:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.eval.quality_climber climb

# 🧗 RAG Fidelity: Grounding & Citation Audit (v1.4)
rag-truth:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.rag_audit audit

# 🧪 Secrets: Scan for hardcoded credentials
scan-secrets:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.secret_scanner scan .

# 🎨 UI/UX: Face Auditor for frontend quality
ui-audit:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.ui_auditor audit $(TARGET)

# 🔥 Red Team: Unleash self-hacking security audit
red-team:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.eval.red_team audit src/agent_ops_cockpit/agent.py

# ⚡ Load Test: Stress test your agent endpoint (Usage: make load-test REQUESTS=100 CONCURRENCY=10)
REQUESTS ?= 50
CONCURRENCY ?= 5
URL ?= http://localhost:8000/agent/query?q=healthcheck

load-test:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.eval.load_test run --url $(URL) --requests $(REQUESTS) --concurrency $(CONCURRENCY)

# 🚀 Production Readiness Auditor: Final gate before shipping to the Sovereign Cloud
deploy-prod:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode deep --summary
	@echo "\n✅ Production Readiness Audit Complete. Review the findings in .cockpit/report.md before manual deployment."

# 🚀 Cloud Run: The fastest way to production
deploy-cloud-run:
	gcloud run deploy $(SERVICE_NAME) --source . --region $(REGION) --allow-unauthenticated --port 80

# 🔥 Firebase: Optimized for frontend hosting
deploy-firebase: build
	firebase deploy --only hosting

# ☸️ GKE: Enterprise container orchestration
deploy-gke:
	docker build -t $(IMAGE_TAG) .
	docker push $(IMAGE_TAG)
	@echo "Updating deployment.yaml..."
	sed -i '' 's|image: .*|image: $(IMAGE_TAG)|' deployment.yaml || true
	kubectl apply -f deployment.yaml || echo "No deployment.yaml found. Please create one based on DEPLOYMENT.md"

# 📡 Watch: Ecosystem sync check
watch:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.watcher

# 🔌 MCP: Start the Model Context Protocol server
mcp-serve:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.mcp_server

# 📧 Reporting: Email the latest audit results
email-report:
	@read -p "Enter recipient email: " email; \
	PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main email-report $$email

