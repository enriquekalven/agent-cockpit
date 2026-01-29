# --- A2UI Starter Makefile ---

# Project Variables
PYTHON = $(shell if [ -f "./.venv/bin/python3.14" ]; then echo "./.venv/bin/python3.14"; elif [ -d ".venv" ]; then echo "./.venv/bin/python"; else echo "python3"; fi)
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
	@echo "  make optimizer-audit-deep      - [CODE] Deep code audit (uvx agentops-cockpit audit)"
	@echo "  make reliability               - Run unit tests and regression suite"
	@echo "  make diagnose                  - [DevEx] System health check and env diagnosis"
	@echo "  make email-report              - [GOV] Email the latest Persona-Approved report"
	@echo "  make red-team                  - Run adversarial security audit"
	@echo "  make load-test                 - Run base load test"
	@echo "  make deploy-prod       - Deploy to production (All Audits -> Cloud Run + Firebase)"
	@echo "  make deploy-cloud-run  - Deploy to Google Cloud Run"
	@echo "  make deploy-firebase   - Deploy to Firebase Hosting"
	@echo "  make watch             - Track ecosystem updates (ADK, A2A, LangChain, etc.)"




dev:
	npm run dev

build:
	npm run build

# 🏁 Master Audit: Safe-Build (Essential for dev velocity)
audit:
	@$(PYTHON) src/agent_ops_cockpit/ops/orchestrator.py --mode quick

# 🚀 Deep Master Audit: Full benchmarks and stress tests
audit-deep:
	@$(PYTHON) src/agent_ops_cockpit/ops/orchestrator.py --mode deep

# 🌐 Global Audit: Point the Cockpit at an external repository
# Usage: make audit-all TARGET=/path/to/your/agent
TARGET ?= .
audit-all:
	@$(PYTHON) src/agent_ops_cockpit/ops/orchestrator.py --mode quick --path $(TARGET)

# 🛡️ Reliability: Unit tests and regression suite
reliability:
	@$(PYTHON) src/agent_ops_cockpit/ops/reliability.py

# 🩺 Diagnose: DevEx system check
diagnose:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main diagnose

# 🔍 The Optimizer: Audit specific agent file for code-level waste
optimizer-audit:
	@$(PYTHON) src/agent_ops_cockpit/optimizer.py src/agent_ops_cockpit/agent.py --quick

# 🔍 Deep Optimizer: Fetch live SDK evidence
optimizer-audit-deep:
	@$(PYTHON) src/agent_ops_cockpit/optimizer.py src/agent_ops_cockpit/agent.py

# 🏛️ Architecture: Design review against Google Well-Architected Framework
arch-review:
	@$(PYTHON) src/agent_ops_cockpit/ops/arch_review.py

# 🧗 Quality: Iterative Hill Climbing optimization
quality-baseline:
	@$(PYTHON) src/agent_ops_cockpit/eval/quality_climber.py climb

# 🧪 Secrets: Scan for hardcoded credentials
scan-secrets:
	@$(PYTHON) src/agent_ops_cockpit/ops/secret_scanner.py .

# 🎨 UI/UX: Face Auditor for frontend quality
ui-audit:
	@$(PYTHON) src/agent_ops_cockpit/ops/ui_auditor.py src

# 🔥 Red Team: Unleash self-hacking security audit

red-team:
	@$(PYTHON) src/agent_ops_cockpit/eval/red_team.py src/agent_ops_cockpit/agent.py

# ⚡ Load Test: Stress test your agent endpoint (Usage: make load_test REQUESTS=100 CONCURRENCY=10)
REQUESTS ?= 50

CONCURRENCY ?= 5
URL ?= http://localhost:8000/agent/query?q=healthcheck

load_test:
	@$(PYTHON) src/agent_ops_cockpit/eval/load_test.py run --url $(URL) --requests $(REQUESTS) --concurrency $(CONCURRENCY)

# 🚀 Production: The Vercel-style 1-click deploy (using Quick Audit for speed)
deploy-prod: audit build

	@echo "📦 Containerizing and deploying to Cloud Run..."
	gcloud run deploy $(SERVICE_NAME) --source . --region $(REGION) --allow-unauthenticated --port 80
	@echo "🔥 Deploying frontend to Firebase..."
	firebase deploy --only hosting

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
	@$(PYTHON) src/agent_ops_cockpit/ops/watcher.py

# 🔌 MCP: Start the Model Context Protocol server
mcp-serve:
	@$(PYTHON) src/agent_ops_cockpit/mcp_server.py

# 📧 Reporting: Email the latest audit results
email-report:
	@read -p "Enter recipient email: " email; \
	$(PYTHON) -m agent_ops_cockpit.cli.main email-report $$email

