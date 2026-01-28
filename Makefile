# --- A2UI Starter Makefile ---

# Project Variables
PROJECT_ID ?= $(shell gcloud config get-value project)
REGION ?= us-central1
SERVICE_NAME = agent-ops-backend
IMAGE_TAG = us-central1-docker.pkg.dev/$(PROJECT_ID)/agent-repo/$(SERVICE_NAME):latest

.PHONY: help dev build deploy-cloud-run deploy-firebase deploy-gke audit deploy-prod

help:
	@echo "Available commands:"
	@echo "  make dev               - Start local development server"
	@echo "  make build             - Build production assets"
	@echo "  make audit             - Run Agent Optimizer audit"
	@echo "  make arch-review       - Run Google Well-Architected design review"
	@echo "  make red-team          - Run adversarial security audit"
	@echo "  make load-test         - Run base load test"
	@echo "  make deploy-prod       - Deploy to production (Cloud Run + Firebase)"
	@echo "  make deploy-cloud-run  - Deploy to Google Cloud Run"
	@echo "  make deploy-firebase   - Deploy to Firebase Hosting"

dev:
	npm run dev

build:
	npm run build

# 🔍 The Optimizer: Audit your agent for waste
audit:
	@python3 src/backend/optimizer.py src/backend/agent.py

# 🏛️ Architecture: Design review against Google Well-Architected Framework
arch-review:
	@python3 src/backend/ops/arch_review.py

# 🔥 Red Team: Unleash self-hacking security audit
red-team:
	@python3 src/backend/eval/red_team.py src/backend/agent.py

# ⚡ Load Test: Stress test your agent endpoint (Usage: make load_test REQUESTS=100 CONCURRENCY=10)
REQUESTS ?= 50
CONCURRENCY ?= 5
URL ?= http://localhost:8000/agent/query?q=healthcheck

load_test:
	@python3 src/backend/eval/load_test.py run --url $(URL) --requests $(REQUESTS) --concurrency $(CONCURRENCY)

# 🚀 Production: The Vercel-style 1-click deploy
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
