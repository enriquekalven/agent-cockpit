# 🏛️ Technical Guide: Architecture Review (`make arch-review`)

The **Architecture Review** tool audits your agent's repository against the **Google Well-Architected Framework for Agents**. It identifies design gaps across security, scalability, and lifecycle management.

## 🚀 Commands

### Local Installation
```bash
make arch-review     # Scans the current directory
agent-ops arch-review --path /path/to/project
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit architecture_review --path .
```

---

## 🔍 How it Works

1.  **Framework Detection**: The tool scans for common signatures (e.g., `LangChain`, `CrewAI`, `FastAPI`) to provide a tailored checklist.
2.  **Heuristic Scanning**: It performs a deep scan of your `.py`, `.ts`, and `.tsx` files looking for architectural evidence:
    *   **Governance**: Use of `policies.json` or `policy_engine.py`.
    *   **Security**: Implementation of PII scrubbers or Workload Identity.
    *   **Reliability**: Presence of `checkpointer` (for state persistence) or `recursion_limit`.
    *   **Connectivity**: Use of `A2UI` protocols or `MCP` tool registries.

---

## 📈 Rationale & Scoring
The review provides a **Score (0-100)** based on PASSED/FAIL checks. 
- **PASSED**: Evidence found in code for that best practice.
- **FAIL**: Missing architectural guardrail.

### Corrective Action
Each failed check includes a **Rationale** which explains *why* the standard is necessary (e.g., "PII Scrubber is a compliance requirement for GDPR/SOC2").
