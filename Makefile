
# ==============================================================================
# Installation & Setup
# ==============================================================================

# Install dependencies using uv package manager
install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.8.13/install.sh | sh; source $HOME/.local/bin/env; }
	uv sync

# ==============================================================================
# Playground Targets
# ==============================================================================

# Launch local dev playground
playground:
	@echo "==============================================================================="
	@echo "| 🚀 Starting your agent playground...                                        |"
	@echo "|                                                                             |"
	@echo "| 💡 Try asking: What's the weather in San Francisco?                         |"
	@echo "|                                                                             |"
	@echo "| 🔍 IMPORTANT: Select the 'my_super_agent' folder to interact with your agent.          |"
	@echo "==============================================================================="
	uv run adk web . --port 8501 --reload_agents

# ==============================================================================
# Backend Deployment Targets
# ==============================================================================

# Deploy the agent remotely
# Usage: make deploy [AGENT_IDENTITY=true] - Set AGENT_IDENTITY=true to enable per-agent IAM identity (Preview)
deploy:
	# Export dependencies to requirements file using uv export.
	(uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > my_super_agent/app_utils/.requirements.txt 2>/dev/null || \
	uv export --no-hashes --no-header --no-dev --no-emit-project > my_super_agent/app_utils/.requirements.txt) && \
	uv run -m my_super_agent.app_utils.deploy \
		--source-packages=./my_super_agent \
		--entrypoint-module=my_super_agent.agent_engine_app \
		--entrypoint-object=agent_engine \
		--requirements-file=my_super_agent/app_utils/.requirements.txt \
		$(if $(AGENT_IDENTITY),--agent-identity)

# Alias for 'make deploy' for backward compatibility
backend: deploy

# ==============================================================================
# Testing & Code Quality
# ==============================================================================

# Run unit and integration tests
test:
	uv sync --dev
	uv run pytest tests/unit && uv run pytest tests/integration

# ==============================================================================
# Agent Evaluation
# ==============================================================================

# Run agent evaluation using ADK eval
# Usage: make eval [EVALSET=tests/eval/evalsets/basic.evalset.json] [EVAL_CONFIG=tests/eval/eval_config.json]
eval:
	@echo "==============================================================================="
	@echo "| Running Agent Evaluation                                                    |"
	@echo "==============================================================================="
	uv sync --dev --extra eval
	uv run adk eval ./my_super_agent $${EVALSET:-tests/eval/evalsets/basic.evalset.json} \
		$(if $(EVAL_CONFIG),--config_file_path=$(EVAL_CONFIG),$(if $(wildcard tests/eval/eval_config.json),--config_file_path=tests/eval/eval_config.json,))

# Run evaluation with all evalsets
eval-all:
	@echo "==============================================================================="
	@echo "| Running All Evalsets                                                        |"
	@echo "==============================================================================="
	@for evalset in tests/eval/evalsets/*.evalset.json; do \
		echo ""; \
		echo "▶ Running: $$evalset"; \
		$(MAKE) eval EVALSET=$$evalset || exit 1; \
	done
	@echo ""
	@echo "✅ All evalsets completed"

# Run code quality checks (codespell, ruff, ty)
lint:
	uv sync --dev --extra lint
	uv run codespell
	uv run ruff check . --diff
	uv run ruff format . --check --diff
	uv run ty check .

# ==============================================================================
# Gemini Enterprise Integration
# ==============================================================================

# Register the deployed agent to Gemini Enterprise
# Usage: make register-gemini-enterprise (interactive - will prompt for required details)
# For non-interactive use, set env vars: ID or GEMINI_ENTERPRISE_APP_ID (full GE resource name)
# Optional env vars: GEMINI_DISPLAY_NAME, GEMINI_DESCRIPTION, GEMINI_TOOL_DESCRIPTION, AGENT_ENGINE_ID
register-gemini-enterprise:
	@uvx agent-starter-pack@0.35.1 register-gemini-enterprise
# ==============================================================================
# Sovereign Hub Hierarchy (v1.6 CLI)
# ==============================================================================

create-trinity: ## Scaffold a unified Cockpit project (Engine + Face)
	@PYTHONPATH=src uv run agentops-cockpit create trinity --project-name $(if $(NAME),$(NAME),my-agent)

audit-report: ## Launch Master Audit (Arch, Quality, Security, Cost)
	@PYTHONPATH=src uv run agentops-cockpit audit report --path $(if $(P),$(P),.)

audit-deep: audit-report ## [Alias] Launch Master Audit (Full Benchmarks)

audit-security: ## Run Red Team and Secret Scanning
	@PYTHONPATH=src uv run agentops-cockpit audit security --path $(if $(P),$(P),.)

audit-arch: ## Architecture Design Review
	@PYTHONPATH=src uv run agentops-cockpit audit arch --path $(if $(P),$(P),.)

deploy-sovereign: ## End-to-End Factory (Audit -> Fix -> Deploy)
	@PYTHONPATH=src uv run agentops-cockpit deploy sovereign --path $(if $(P),$(P),.) --target $(if $(TARGET),$(TARGET),google)

fleet-status: ## Display stateful registry of deployed agents
	@PYTHONPATH=src uv run agentops-cockpit fleet status

fleet-mothball: ## FinOps: Scale fleet to zero
	@PYTHONPATH=src uv run agentops-cockpit fleet mothball --cloud $(CLOUD)

fleet-resume: ## FinOps: Resume mothballed fleet
	@PYTHONPATH=src uv run agentops-cockpit fleet resume --cloud $(CLOUD)

fleet-tunnel: ## Inner Loop: Local-to-Cloud Bridge
	@PYTHONPATH=src uv run agentops-cockpit fleet tunnel --port $(if $(PORT),$(PORT),8080)

fleet-watch: ## Track ecosystem updates
	@PYTHONPATH=src uv run agentops-cockpit fleet watch

fleet-anomaly: ## Trace behavior anomalies
	@PYTHONPATH=src uv run agentops-cockpit fleet anomaly --name $(if $(NAME),$(NAME),my-agent) $(if $(ROGUE),--rogue,)

smoke-test: ## Run Trinity Smoke Tests (Hub-based validation)
	@PYTHONPATH=src uv run python3 -m agent_ops_cockpit.ops.reliability audit --smoke

test-regression: ## Run Full Regression Suite (Unit + Smoke)
	@PYTHONPATH=src uv run agentops-cockpit test regression

test-simulate: ## Run Persona-based User Simulation
	@PYTHONPATH=src uv run agentops-cockpit test simulate

upgrade: ## Upgrade all packages to latest stable versions
	uv sync --upgrade

certify: ## Launch Full Production Readiness Certification
	@PYTHONPATH=src uv run agentops-cockpit sys certify

lab-bootstrap: ## Setup the 'Broken Agent' for the Cockpit Lab
	@echo "🧪 Bootstrapping broken agent for lab..."
	@mkdir -p my_super_agent
	@echo 'import os\nimport vertexai\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n# INTENTIONAL DEBT: No retries, no timeouts, no structured types, PII exposure\ndef get_user_data(email: str):\n    return f"Extracting PII: {email}"\n\n@app.get("/task")\ndef solve_task(q: str):\n    # MISSING: Context Caching\n    model = vertexai.generative_models.GenerativeModel("gemini-1.5-pro")\n    return model.generate_content(q).text\n' > my_super_agent/agent.py
	@echo "google-cloud-aiplatform\nfastapi\nuvicorn" > my_super_agent/requirements.txt
	@echo "✅ Lab environment ready in ./my_super_agent"
