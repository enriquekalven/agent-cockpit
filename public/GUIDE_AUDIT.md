# 🕹️ Technical Guide: Master Audit (`make audit`)

The **Master Audit** is the primary entry point for verifying the production-readiness of your AI agent. It orchestrates multiple specialized auditors to provide a high-level "Cockpit Score."

<div align="center">
  <img src="diagrams/workflow.png" alt="Operational Workflow" width="100%" />
</div>

## 🚀 Commands

### Local Installation
```bash
make audit         # Quick Safe-Build (Sub-second feedback)
make audit-deep    # Deep System Audit (Full benchmarks)
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit report --mode quick
uvx agentops-cockpit report --mode deep
```

---

## 🔍 What it Checks

| Auditor | Logic |
| :--- | :--- |
| **Architecture Review** | Verifies alignment with the Google Well-Architected Framework (IAM, VPC, Cloud Run settings). |
| **Policy Enforcement** | Validates the agent against declarative `policies.json` (Forbidden topics, HITL). |
| **Secret Scanner** | Scans code for hardcoded API keys, service accounts, and bearer tokens. |
| **Token Optimization** | Analyzes SDK usage to identify context caching and model routing opportunities. |
| **Reliability Audit** | Runs the regression suite to ensure no logic drift since the last "Golden Set" run. |
| **Red Team (Fast)** | Automated adversarial testing for rapid jailbreak detection. |

---

## 📊 Report Output
The audit generates a unified Markdown report at **`cockpit_final_report.md`**.

### Usage in CI/CD
We recommend integrating `make audit` into your GitHub Actions (provided in `.github/workflows/main.yml`) to block PRs that fail governance or security checks.
