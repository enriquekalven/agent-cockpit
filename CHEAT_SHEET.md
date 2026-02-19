# 🕹️ AgentOps Cockpit: Sovereign Cheat Sheet (v2.0.2)
*The Industry Standard Logic Layer for Production AI Agents*

---

## 🚀 1. Installation & Zero-Install Access
Whether you want a long-term install or a quick one-off run.

| Method | Command | Use Case |
| :--- | :--- | :--- |
| **Python Install** | `pip install agentops-cockpit` | Permanent install for power users. |
| **Zero-Install (uvx)** | `uvx agentops-cockpit <command>` | Remote/CI execution without installing. |
| **Dev Setup** | `make install` | Clone and sync for local contributors. |

> 💡 **Pro-Tip**: You can use `ops`, `aops`, or `agent-ops` interchangeably with `cockpit`. For example, `ops report` is the same as `cockpit audit report`.

---

## 🏛️ 2. The Sovereign Workflow
Follow this path to take an agent from prototype to enterprise-grade.

| Sequence | uvx / CLI Command | make Shortcut | Purpose |
| :--- | :--- | :--- | :--- |
| **1. Explore**| `cockpit` | `make cockpit` | Launch Master Dashboard & Fleet Status. |
| **2. Modernize**| `cockpit mcp blueprint` | `make mcp-blueprint` | Generate MCP Wrappers for Legacy Tools. |
| **3. Certify** | `cockpit certify` | `make certify` | Production Readiness Certification. |
| **4. Audit** | `ops report` | `make audit` | Deep Persona SME scan: Sec, ROI, & Arch. |
| **5. Fix** | `cockpit fix evolve` | `make apply-fixes` | Autonomous remediation & code hardening. |
| **6. Deploy** | `cockpit deploy sovereign`| `make deploy-prod`| End-to-End: Audit -> Fix -> Deploy. |
| **7. Monitor**| `cockpit fleet status` | `make fleet-status` | View global production state. |

---

## ⚙️ 3. Developer Tooling (The Inner Loop)
Shortcuts for local development and testing.

- **`make dev`**: 🎭 Launches the unified local stack (Face + Gateway).
- **`make playground`**: 🎡 Starts the interactive agent sandbox.
- **`make test`**: 🧪 Runs unit and integration tests.
- **`make eval`**: 🧗 Launches ADK-based quality evaluations.
- **`make upgrade`**: 🚀 Syncs all packages to latest stable sovereign versions.

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
| **Master Audit** | `ops report` |
| **Apply All Fixes** | `make apply-fixes` |
| **Certify Project** | `cockpit certify` |
| **Modernize Tools** | `make arch-review` |
| **Bypass Registry** | `cockpit audit report --public` |
| **System Diagnosis** | `cockpit sys doctor` |

---

## 🌑 Pro-Tip: Sovereignty (Privacy)
Disable anonymous telemetry for air-gapped or high-security environments:
`export AGENTOPS_TELEMETRY_ENABLED=false`

---
*For the complete technical manual: [agent-cockpit.web.app/docs](https://agent-cockpit.web.app/docs)*
