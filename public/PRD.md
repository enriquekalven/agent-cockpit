# 📄 Product Requirements Document (PRD): AgentOps Cockpit

**Version**: 1.0.0-rc1 (The Antigravity Hardening)
**Status**: Release Candidate / Enterprise-Scale
**Owner**: Enrique Kalven & Agentic AI Engineering Team

---

## 1. Executive Summary
The **AgentOps Cockpit** is a production-grade operations and governance platform for AI agents. It addresses the "Day 2" challenges of agentic development: cost management, security hardening, architectural alignment, and operational visibility. By implementing the **Agentic Trinity** (Engine, Face, Cockpit), it provides developers with a framework-agnostic "Mission Control" to transition agents from prototypes to reliable production services.

The **v1.0.0 "Antigravity" Milestone** focuses on resilience, fleet-scale orchestration, and frictionless integration into enterprise CI/CD pipelines.

---

## 2. Motivation
As AI agent fleets scale from single-digit prototypes to hundreds of production services (145–465+ agents), traditional manual governance fails. The motivation for the Antigravity update is to:
- **Minimize Friction**: Developers in restricted VPN or proxy environments often face registry auth failures (401/403). The cockpit must be resilient.
- **Scale Orchestration**: Monolithic logs fail at scale. Partitioned evidence is required for parallelized fleet audits.
- **Automate Remediation**: Finding issues is not enough; the cockpit must proactively suggest and apply code-level fixes (Auto-Healing).
- **Hardened Governance**: Security and Architecture violations must be first-class citizens in CI/CD, preventing unsafe deployments through deterministic exit codes.

---

## 3. Target Audience & Personas
- **The AI Engineer**: Needs instant feedback and auto-remediation to maintain velocity.
- **The SecOps Lead**: Requires deterministic blocking of deployments containing secrets or PII leaks.
- **The Platform Architect**: Standardizes "Well-Architected" patterns across massive monorepos using `.cockpitignore` and `cockpit.yaml`.
- **The DevOps/SRE**: Integrates the cockpit into pipelines via JSON/SARIF reporting and severity-based exit codes.

---

## 4. Critical User Journeys (CUJs)
- **CUJ 1: Zero-Friction Registry Failover**
  - *User:* Developer on a restricted corporate VPN.
  - *Action:* Runs an audit that requires dependency checks.
  - *Outcome:* The cockpit detects a 401 Unauthorized from the private registry and automatically fails over to the Public PyPI Mirror, unblocking the audit session.
- **CUJ 2: Fleet-Scale Workspace Audit**
  - *User:* Platform Architect.
  - *Action:* Runs `ops report --workspace` at the root of a 400+ agent monorepo.
  - *Outcome:* The **Smart Discovery Engine** respects `.cockpitignore`, audits all agents in parallel, and saves results to a **Partitioned Evidence Lake**.
- **CUJ 3: Automated Security Gate (CI/CD)**
  - *User:* DevOps Engineer.
  - *Action:* Integration of `ops report --format json` into a GitHub Action.
  - *Outcome:* Pipeline automatically fails with `EXIT 1` when a hardcoded secret is detected, or `EXIT 2` for architecture violations, while allowing `EXIT 0` for informational warnings.
- **CUJ 4: Dry-Run Remediation (Auto-Healing)**
  - *User:* AI Engineer.
  - *Action:* Runs `ops report --heal --dry-run`.
  - *Outcome:* Views a "Dry Run Dashboard" in the console showing exactly which decorators (e.g., `@retry`) would be injected, without modifying production code until approved.

---

## 5. Functional Requirements
### R1: Resilient Registry Resolver (Network Resilience)
- **Automatic Failover**: Must detect 401/403 registry errors and retry using public mirrors (PyPI).
- **Registry Awareness**: The `diagnose` command must verify connectivity to core indices.

### R2: Partitioned Evidence Lake (Scalability)
- **Partitioning**: Must move from a single `evidence_lake.json` to agent-specific folder partitioning (`evidence_lake/{agent_hash}/latest.json`).
- **Parallel Performance**: Support simultaneous writes from concurrent processes without file locking contention.

### R3: Smart Discovery Engine (Orchestration)
- **Hieuristic Detection**: Must identify the agent "brain" across `agent/agent.py`, `src/main.py`, etc.
- **Exclusion Logic**: Must respect `.cockpitignore` and `cockpit.yaml` "Sovereign Gates" to skip non-essential directories.

### R4: Severity-Based Exit Codes (Governance)
- **Deterministic Blocking**: 
  - `EXIT 0`: Pass
  - `EXIT 1`: Security Critical (Secrets)
  - `EXIT 2`: Architecture/Policy Violation
  - `EXIT 3`: General Failure

### R5: Machine-Readable Reporting
- **SARIF/JSON**: Must support `--format json` and `--format sarif` for direct integration with security dashboards (e.g., GitHub Advanced Security).

---

## 6. Success Criteria (KPIs)
- **Zero-Block Rate**: 100% of registry auth failures during audits must be resolved via path failover.
- **Fleet Scalability**: Auditing 400 agents in a workspace must not exceed **2 minutes** (using parallel orchestration).
- **Compliance Accuracy**: 100% of findings in the Persona Matrix should be categorized with a "Fixability" score (1-Click vs. Structural).
- **CI/CD Reliability**: Deterministic exit codes must correctly block 100% of identified security leaks in simulation tests.

---

## 7. Technical Stack
- **Engine**: Python 3.10+, FastAPI.
- **Config**: Centralized `config.py` Single Source of Truth.
- **CLI**: Typer + Rich (Standardized Binary: `ops`, `aops`).
- **Storage**: Multi-tier Evidence Lake (Local Partitioned + Cloud Aggregated).
- **UI**: React 18 / Vite / A2UI (v1.3 standards).

---

## 8. Roadmap: The Antigravity Path
- **v0.9.8**: [x] Sovereign Gate Enforcement, [x] Command Trinity Parity.
- **v0.9.9**: [x] Frictionless DX, [x] Fixability Badges, [x] Heal Aliases.
- **v1.0.0-rc1**: [x] Partitioned Lake, [x] Resilient Registry, [x] Severity Exit Codes.
- **v1.1.0 (Upcoming)**: [ ] Multi-Agent Consensus Audits (Audit-by-Committee).

---
*Generated by the AgentOps Cockpit Orchestrator (v1.0.0-rc1).*
