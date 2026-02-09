# --- AgentOps Cockpit Makefile ---

# Project Variables
PYTHON = $(shell if [ -f "./.venv/bin/python3.14" ]; then echo "./.venv/bin/python3.14"; elif [ -d ".venv" ]; then echo "./.venv/bin/python"; elif command -v python >/dev/null 2>&1; then echo "python"; else echo "python3"; fi)
PROJECT_ID ?= $(shell gcloud config get-value project)
REGION ?= us-central1
SERVICE_NAME = agent-ops-backend
IMAGE_TAG = us-central1-docker.pkg.dev/$(PROJECT_ID)/agent-repo/$(SERVICE_NAME):latest

.PHONY: help dev build deploy-cloud-run deploy-firebase deploy-gke audit audit-deep deploy-prod scan-secrets ui-audit watch mcp-serve email-report diagnose arch secrets face

help:
	@echo "Available commands:"
	@echo "  make dev                       - Start local development server"
	@echo "  make audit                     - [MASTER] Quick Audit (secrets, reliability, quality)"
	@echo "  make audit-deep                - [MASTER] Deep Audit (benchmarks, red-team, stress)"
	@echo "  make apply-fixes               - [PHASE 4] Auto-remediate detected gaps"
	@echo "  make propose-fixes             - [PHASE 5] Create fix branch and commit patches"
	@echo "  make deploy-prod               - [MASTER] Production Readiness Gate (Audit + Stress)"
	@echo "  make deploy-cloud-run          - Deploy to Google Cloud Run"
	@echo "  make deploy-firebase           - Deploy to Firebase Hosting"
	@echo "  make mcp-serve                 - Start MCP Server"
	@echo "  make diagnose                  - System health check"

dev:
	npm run dev

build:
	npm run build

# 🏁 Master Audit: Safe-Build
audit:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode quick

# 🚀 Deep Master Audit
audit-deep:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode deep

# 🚀 The Closer: Auto-remediation
apply-fixes:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review apply-fixes

# 🌿 The Ambassador: PR Factory
propose-fixes:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.arch_review propose-fixes

# 🩺 Diagnose: DevEx
diagnose:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main diagnose

# 🧪 Secrets: Scan
scan-secrets:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main secrets .

# 🎨 Face: UI Audit
ui-audit:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main face src

# 🚩 Security: Red Team
red-team:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main report --only red_team

# 🧗 Quality: Hill Climb
quality:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main quality .

arch:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main arch .

secrets: scan-secrets
face: ui-audit

# 🚀 Production Readiness
deploy-prod:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.ops.orchestrator --mode deep --summary
	@echo "\n✅ Production Readiness Audit Complete."

# 🚀 Cloud Run
deploy-cloud-run:
	gcloud run deploy $(SERVICE_NAME) --source . --region $(REGION) --allow-unauthenticated --port 80

# 🔥 Firebase
deploy-firebase: build
	firebase deploy --only hosting

# 🔌 MCP Server
mcp-serve:
	@PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main mcp-server

# 📧 Email Report
email-report:
	@read -p "Enter recipient email: " email; \
	PYTHONPATH=src $(PYTHON) -m agent_ops_cockpit.cli.main email-report $$email
