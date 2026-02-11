# Contributing to AgentOps Cockpit

First off, thank you for helping us build the future of **Autonomous Agent Operations**! 🚀 Evolving the **Trinity** standard requires high-fidelity engineering and the discipline of a professional logic layer.

## 🏛️ v1.4.7 Vision: The "Ecosystem Expansion"
In v1.4.7, we have evolved beyond simple compliance into a **Lifecycle Management Platform**. We are building the **Autonomous Patching Engine**—a system that not only detects architectural gaps but synthesizes remediation across RAG pipelines, analytical DBs (BigQuery/Snowflake), and multi-cloud architectures.

## 🏗️ Architecture Philosophy
We strictly follow the **Trinity Model**:
1.  **The Engine**: Reasoning trajectories and tool orchestrations.
2.  **The Face**: Reactive UX surfaces and GenUI (A2UI) protocols.
3.  **The Cockpit**: Our focus. Governance, cost control, semantic caching, and sovereign policy enforcement.

---

## 🛠️ Environment Setup

We use **[uv](https://docs.astral.sh/uv/)** for ultra-fast Python dependency management and **Node.js** for the Face (v17+).

### 1. Backend (The Cockpit Engine)
```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup virtual environment and install in editable mode
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### 2. Frontend (The Face)
```bash
npm install
```

---

## ⌨️ Operational Workflow

Don't wait for CI/CD to tell you there's a problem. Run the **Master Cockpit Audit** locally.

### Local Development
- `make dev`: Starts the local Engine + Face stack.
- `make audit`: Runs the **Quick Safe-Build** (Secrets, Reliability).
- `make audit-deep`: Runs the **Master Cockpit Audit** (Hill Climbing, Benchmarks).
- `make arch-review`: Runs the v1.4.7 Autonomous Architect review.
- `make maturity`: Runs the **Expertise Matrix** dashboard.

### Specialized Audits
- `make red-team`: Runs the Adversarial Evaluator against the codebase.
- `make finops`: Analyzes token efficiency and semantic caching TCO.
- `make rag-truth`: Audits RAG pipelines for grounding and citation fidelity.

---

## 🏛️ Contribution Standards

### 1. The Trinity Standard
Every PR should identify which pillar(s) it affects. If modifying the **Cockpit** logic (middleware/routing), ensure you update the corresponding **SME Auditor** in `src/agent_ops_cockpit/ops/auditors/`.

### 2. Poka-Yoke (Mistake-Proofing)
- **Absolute Paths**: All tool executions and file operations MUST use absolute paths.
- **Surface Verification**: New UI components must register a `surfaceId` via A2UI.
- **Cost Guardrails**: New tools must include a cost signature for the FinOps auditor.

### 3. Persona-Based Auditing
We use a **Multi-Persona Governance Board**. If you are adding a new feature, consider which SME would care:
- **Architect**: Does this maintain the Trinity separation?
- **FinOps**: Is there a caching strategy?
- **Security**: Is there persistent prompt injection risk?
- **Quality**: Is the RAG grounding logic robust?

---

## 🔍 Pull Request Checklist
Before submitting a PR, ensure:
1.  [ ] Your code passes `make audit` with a score > 90.
2.  [ ] You have run `make red-team` if adding new reasoning logic.
3.  [ ] You have updated `CHANGELOG.md` with your changes.
4.  [ ] Documentation in `/docs` reflects any new command or policy.

## 🤝 Ecosystem
We bridge specialized tools like the **Google ADK** and **LangGraph**. Contributions that improve integration with these frameworks are highly encouraged.

---
**License**: By contributing, you agree that your work will be licensed under the MIT License.
