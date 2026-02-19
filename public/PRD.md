# 📄 Product Requirements Document (PRD): AgentOps Cockpit

**Version**: 2.0.2 (The Sovereign Master Build)
**Status**: Stable / Production-Ready
**Owner**: Enrique Kalven & Agentic AI Engineering Team

---

## 1. Executive Summary
The **AgentOps Cockpit** is a production-grade operations and governance platform for AI agents. It addresses the "Day 2" challenges of agentic development: cost management, security hardening, architectural alignment, and operational visibility. By implementing the **Agentic Trinity** (Engine, Face, Cockpit), it provides developers with a framework-agnostic "Mission Control" to transition agents from prototypes to reliable production services.

The **v2.0.2 "Sovereign Master Build" Milestone** focuses on **Engineering Resilience** (Venv Isolation, Cordon Mode), **Proactive Security** (AST Taint Tracking), **Architectural Hardening** (Structural Monolith Detection), and the official **Sovereign Safety SDK** (`SafetyGate`).

---

## 2. Motivation
As AI agent fleets scale from single-digit prototypes to hundreds of production services, traditional manual governance fails. The motivation for the v2.0.2 update is to:
- **Minimize Friction**: corporate environments often face registry auth failures (401/403). The cockpit must be resilient via **Cordon Mode**.
- **Environmental Independence**: Eliminate dependency "blind spots" by automatically provisioning and using isolated **Audit Venvs**.
- **Automate Remediation**: Move from "reporting" to providing the actual **Safety SDK** (`SafetyGate`) that handles PII, HITL, and Taint Protection.
- **Architectural Scalability**: Detect and remediate **Structural Monoliths** (large agent files) that degrade reasoning and increase latency.
- **Economic Visibility**: Provide real-time **Opex Simulations** to forecast the token impact of security and reliability hardening.

---

## 3. Target Audience & Personas
- **The AI Engineer**: Needs instant feedback and auto-remediation to maintain velocity.
- **The SecOps Lead**: Requires deterministic blocking of deployments containing secrets, PII leaks, or unsanitized input flows (Taint Tracking).
- **The Platform Architect**: Standardizes "Well-Architected" patterns across massive monorepos and enforces modular agent structures.
- **The DevOps/SRE**: Integrates the cockpit into pipelines via JSON/SARIF reporting, severity-based exit codes, and isolated audit environments.

---

## 4. Critical User Journeys (CUJs)
- **CUJ 1: Zero-Friction Registry Cordoning**
  - *User:* Developer on a restricted corporate VPN.
  - *Action:* Runs an audit that requires dependency checks.
  - *Outcome:* The cockpit's **Cordon Mode** isolates the registry environment, failing over to a Public PyPI Mirror and unblocking the session.
- **CUJ 2: Venv-Isolated Fleet Audit**
  - *User:* DevOps Engineer.
  - *Action:* Runs an audit in a CI environment with fragmented Python dependencies.
  - *Outcome:* The cockpit automatically provisions a **Managed Audit Venv**, ensuring 100% dependency discovery without polluting the host.
- **CUJ 3: Proactive Taint-Tracking Gate**
  - *User:* SecOps Lead.
  - *Action:* Code review of an agent tool call.
  - *Outcome:* The **Security Fellow** uses AST analysis to trace user-query flow to a sensitive shell call, flagging it as a "Sovereign Taint" if unsanitized.
- **CUJ 4: Structural Split Scaffold**
  - *User:* Platform Architect.
  - *Action:* Audits a large, monolithic agent file (>200 lines).
  - *Outcome:* The cockpit identifies the "Structural Monolith" risk and automatically injects a **Managed Router** scaffold to guide modularization.
- **CUJ 5: Opex Simulation Report**
  - *User:* FinOps Principal.
  - *Action:* Reviews proposed audit fixes (retries, logging, etc.).
  - *Outcome:* The cockpit generates an **Estimated Monthly Token Delta** (e.g., "+15% for resiliency") before the changes are committed.

---

## 5. Functional Requirements
### R1: Cordon Mode (Network Resilience)
- **Automatic Failover**: Must isolate SUBPROCESS env and force public index mirrors upon registry auth failure.
- **Status Visibility**: The cockpit header must clearly indicate `CORDONED` status during execution.

### R2: Venv Isolation Sidecar (Environment Purity)
- **Managed Venv**: Must automatically initialize and use a `.cockpit_venv` if present, ensuring a clean dependency path for auditors.
- **Binary Discovery**: Intelligently route `python`, `pytest`, and `uv` commands through the isolated sidecar.

### R3: Sovereign Safety SDK (`SafetyGate`)
- **Sanitization**: Provide a production-grade `sanitize()` utility for PII and data masking.
- **HITL Gating**: Implement a manual approval decorator (`@hitl_gate`) matched to audit findings.
- **Taint Tracking**: Utilize AST analysis to trace unsanitized input flow to high-stakes tool calls.

### R4: Structural Monolith Detection (Architecture)
- **Scale Analysis**: Flag any agent file exceeding 200 lines as a structural risk.
- **Remediation Scaffolding**: Automatically provide "Managed Router" templates for oversized agents.

### R5: Opex Simulation Engine (FinOps)
- **Token Forecasting**: Provide percentage-based impact estimates for proposed fixes.
- **Drivers Analysis**: Identify which hardening measures (Telemetry, Resiliency, Caching) are driving cost changes.

---

## 6. Success Criteria (KPIs)
- **Zero-Block Rate**: 100% of registry auth failures resolved via Cordon Mode.
- **Dependency Fidelity**: 0% "ModuleNotFoundError" during audits when Venv Isolation is enabled.
- **Remediation Density**: Move from 0% to 100% "Actionable Logic" for Security findings via the Safety SDK.
- **Audit Velocity**: Maintain sub-30s incremental audit speed for targeted personas.

---

## 7. Technical Stack
- **Engine**: Python 3.10+, FastAPI, AST/LibCST.
- **Protocols**: Model Context (MCP), A2UI, UCP, AP2.
- **CLI**: Typer + Rich (v2.0.2 Standards).
- **SDK**: `SafetyGate` Sovereign Safety SDK.
- **Cloud**: Unified Governance for GCP (Vertex), AWS (Bedrock), and Azure (OpenAI).

---

## 8. Roadmap: The Sovereign Path
- **v1.0.0**: [x] The Governance & Regression Framework.
- **v2.0.0**: [x] The Sovereign Orchestrator (Multi-Cloud Bridge).
- **v2.0.2**: [x] **The Sovereign Master Build** (Venv, Cordon, Structural, Safety SDK).
- **v3.0.0 (Upcoming)**: [ ] A2A Inter-Agent Simulation, Visual Face-Scan, Shadow Duel.

---
*Generated by the AgentOps Cockpit Orchestrator (v2.0.2).*
