# 🕹️ AgentOps Cockpit: Cockpit Cheat Sheet (v2.0.7 Premium Insights)
*The Industry Standard Logic Layer for Production AI Agents*

---

## 🚀 1. Installation & Zero-Install Access
Whether you want a long-term install or a quick one-off run.

| Method | Command | Use Case |
| :--- | :--- | :--- |
| **Python Install** | `pip install agentops-cockpit` | Permanent install for power users. |
| **Zero-Install (uvx)** | `uvx agentops-cockpit <command>` | Remote/CI execution without installing. |
| **Dev Setup** | `make install` | Clone and sync for local contributors. |

> 💡 **Pro-Tip**: You can use `ops`, `uvx agentops-cockpit`, or `uvx agentops-cockpit` interchangeably with `cockpit`. For example, `uvx agentops-cockpit audit report` is the same as `cockpit audit report`.

---

## 🏛️ 2. The Cockpit Workflow
Follow this path to take an agent from prototype to enterprise-grade.

| Sequence | uvx / CLI Command | make Shortcut | Purpose |
| :--- | :--- | :--- | :--- |
| **1. Explore**| `cockpit` | `make cockpit` | Launch Master Dashboard & Fleet Status. |
| **2. Modernize**| `uvx agentops-cockpit mcp blueprint` | `make mcp-blueprint` | Generate MCP Wrappers for Legacy Tools. |
| **3. Certify** | `uvx agentops-cockpit certify` | `uvx agentops-cockpit certify` | Production Readiness Certification. |
| **4. Audit** | `uvx agentops-cockpit audit report` | `uvx agentops-cockpit audit report` | Deep Persona SME scan: Sec, ROI, & Arch. |
| **5. Fix** | `uvx agentops-cockpit evolve` | `uvx agentops-cockpit evolve` | Autonomous remediation & code hardening. |
| **6. Deploy** | `uvx agentops-cockpit deploy prep`| `uvx agentops-cockpit deploy prep`| End-to-End: Audit -> Fix -> Deploy. |
| **7. Monitor**| `uvx agentops-cockpit fleet status` | `uvx agentops-cockpit fleet status` | View global production state. |

---

## ⚙️ 3. Developer Tooling (The Inner Loop)
Shortcuts for local development and testing.

- **`uvx agentops-cockpit cockpit`**: 🎭 Launches the unified local stack (Face + Gateway).
- **`make playground`**: 🎡 Starts the interactive agent sandbox.
- **`uvx agentops-cockpit test`**: 🧪 Runs unit and integration tests.
- **`make eval`**: 🧗 Launches ADK-based quality evaluations.
- **`make upgrade`**: 🚀 Syncs all packages to latest stable cockpit versions.

---

## 🛡️ 4. Principal SME Persona Audits
Invoke specific auditors directly for surgical focus.

*   **🛡️ Security (Red Team)**: `cockpit audit security` (PII leaks, Injections).
*   **🏗️ Architecture**: `cockpit audit arch` (Strategic paradigm review).
*   **💰 FinOps**: `cockpit audit roi` (Model tier & cost benchmarking).
*   **🧗 Quality**: `cockpit audit quality` (Hill-climbing & reasoning).

---

## 🕵️ 5. Post-Deployment Ops (Fleet Hub)
Manage your agents once they are live in the wild.

- **`cockpit fleet anomaly`**: Detect reasoning drift and rogue behavior.
- **`cockpit fleet tunnel`**: Bridge local code to cloud endpoints.
- **`cockpit fleet mothball`**: Scale fleet to zero to halt billing.
- **`cockpit fleet watch`**: Real-time tracker for ecosystem updates.

---

## 💡 6. Master Shortcuts & Pro Tips

| Action | Command / Shortcut |
| :--- | :--- | :--- |
| **Mission Control** | `cockpit` |
| **Master Audit** | `uvx agentops-cockpit audit report` |
| **Apply All Fixes** | `uvx agentops-cockpit evolve` |
| **Certify Project** | `uvx agentops-cockpit certify` |
| **Modernize Tools** | `uvx agentops-cockpit audit arch` |
| **Bypass Registry** | `cockpit audit report --public` |
| **System Diagnosis** | `uvx agentops-cockpit sys doctor` |

---

## 🌑 Pro-Tip: Cockpitty (Privacy)
Disable anonymous telemetry for air-gapped or high-security environments:
`export AGENTOPS_TELEMETRY_ENABLED=false`

---
*For the complete technical manual: [agent-cockpit.web.app/docs](https://agent-cockpit.web.app/docs)*
