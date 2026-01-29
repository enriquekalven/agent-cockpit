# 🚀 Quickstart: Production-Grade AgentOps

"From `pip install` to `Well-Architected` in 60 seconds."

The **AgentOps Cockpit** is not just another monitoring tool—it's a developer distribution designed to move AI agents from local scripts to production-grade services.

---

## ⚡ 1. Install & Scaffold

Get the Cockpit CLI globally. Everything you need to build and audit is packed into this single package.

```bash
pip install agentops-cockpit --upgrade
```

### Create a new project (A2UI/React/FastAPI)
```bash
agent-ops create my-agent --ui a2ui
```
*This scaffolds a full Agentic Trinity: **Engine** (Logic), **Face** (UI), and the local **Operations** hub.*

---

## 🔍 2. The "Aha!" Moment: Your First Audit

Navigate to any existing agent repository (LangGraph, CrewAI, or simple scripts) and run the Mission Report.

```bash
make audit
```

### What happens?
1.  **Quick Arch Review**: Detects your framework and grades it against the [Google Well-Architected Framework](./google-architecture).
2.  **Fast Red-Team**: Checks for the most common prompt injections and PII leakage.
3.  **Token Optimization**: Identifies non-cached prompts and projects FinOps savings.

*For a full production-gate audit including benchmarks, use `make audit-deep`.*

---

## 🛠️ 3. Audit-to-Action (Auto-Fix)

Don't just read reports—fix your code. If the Auditor identifies cost waste (like missing Gemini Context Caching), apply the fix instantly.

```bash
# Proposes and applies production-best-practices directly to your source
agent-ops audit path/to/agent.py --apply
```

---

## 🎮 4. Operational Control Plane

Launch the local mission control dashboard to monitor traces, manage your [Hive Mind Cache](./cockpit) and visualize [MCP Tool connectivity](./cli-commands).

```bash
make dev
```
*Visit `localhost:5173/ops` to step into the flight deck.*

---

## 🏁 Next Steps
- [ ] **Lead Dev**: Integrate [A2A Communication Standards](./a2a) to coordinate swarms.
- [ ] **Security Lead**: Review the [Red Team Hardening Guide](./security).
- [ ] **Ops Engineer**: Deploy the full stack to [Google Cloud Run](./deployment).
