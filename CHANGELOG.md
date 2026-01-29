# 📜 Changelog

All notable changes to the **AgentOps Cockpit** will be documented in this file.

## [0.7.0] - 2026-01-28

### 🛡️ Guardrail Intelligence (RFC-307)
- **Declarative Policy Engine**: Introduced `policies.json` for managing agentic guardrails without prompt engineering.
- **Forbidden Topics Enforcement**: Real-time input validation against customizable restricted domains (e.g., medical advice, illegal activities).
- **HITL (Human-in-the-Loop) Tooling**: Declaratively flag sensitive tools (e.g., `transfer_funds`) for manual approval.
- **Dynamic Cost Guardrails**: Session-level budget and token-per-turn enforcement linked directly to the policy engine.

## [0.6.0] - 2026-01-28

### 🚀 major Features
- **Triple-State Situational Analysis**: The Optimizer now detects three states for your SDKs:
    - **Missing**: Detects logic calls without installed SDKs and provides install guides.
    - **Legacy**: Provides situational workarounds for older SDKs (e.g., manual pruning for pre-v1.70.0 Vertex AI).
    - **Modern**: Unlocks native high-performance features (e.g., Context Caching).
- **Cross-Package Validation (Conflict Guard)**: Intelligent detection of architectural conflicts (e.g., mixing CrewAI and LangGraph state loops) and synergistical pairings (ADK + MCP).
- **Quick-Safe Build Pipeline**: Added `--quick` mode to the auditor, resulting in a **12x reduction in dev-loop latency** (from 1.8s down to 0.15s) by optimizing situational evidence fetching.

### 🛠️ Fixes & Enhancements
- **Master Orchestrator Integration**: `make audit` now defaults to Quick Mode for instantaneous feedback.
- **Reliability Suite Update**: Added support for high-velocity build flags.
- **SDK Citation Evidence**: Live fetching of GitHub release notes (Atom feeds) for real-time compliance citations in Deep Mode.

## [0.5.0] - 2026-01-15
- Initial public release of the AgentOps Platform.
- Red Team Auditor, PII Scrubber, and Hive Mind Caching.
- Google Well-Architected Framework checks.
