# 📜 Changelog

All notable changes to the **AgentOps Cockpit** will be documented in this file.

### v2.0.2 (2026-02-17) - The "Pillar Evolution" Release
- **🛡️ Semantic Compliance Pivot**: Moved security and architecture audits from regex matching to LLM-driven intent verification (Gemini 2.0 Flash).
- **🔦 Shadow ROI Benchmarking**: Launched dynamic performance analysis in the Reliability Hub to optimize model tiering and accuracy/cost curves.
- **📜 Governance as Code (GaC)**: Externalized all fleet policies into declarative YAML for standardized security enforcement.
- **💬 The Architect's Dialogue**: Enabled interactive reasoning during fixes, allowing developers to justify and override specific findings via the `fix reason` command.
- **🏛️ Sovereign Certification**: Added cryptographic proof of passing audit gates via a persistent Sovereign Certificate artifact.
- **🕹️ Command Ergonomics**: Launched the unified `cockpit` binary as the primary entry point for all operations.

### v2.0.0 (2026-02-17) - The "Industry Scale" Release
- **🌍 Sovereign Cloud Bridge**: Multi-cloud abstraction layer that decouples agents from direct provider SDKs (AWS Bedrock, GCP Vertex, Azure Foundry).
- **🕹️ Universal Remediator**: Autonomous v2.0 engine that auto-heals "Monocultural Bias" and "Manifest Drift".
- **📜 Manifest Auditor v2.0**: Specialized scanner for `package.json`, `pyproject.toml`, and `mcp-config.json` to detect SDK latency and "Legacy Intelligence".
- **⚔️ Simulation Auditor**: Adversarial hypothesis testing on prompts to detect "Semantic Permissiveness" and logic overrides.
- **🏗️ Dogfood Fleet Hardening**: Validated across 13 industry repositories from Google, OpenAI, Anthropic, MSFT, and AWS.
- **🛡️ Industry Debt Remediation**: codified fixes for ~70% of identified monocultural hardcoding in public samples.
- **🧠 Semantic Paradigm Auditor**: New reasoning logic to detect architectural mismatches (e.g., "RAG for Math") and suggest high-fidelity patterns (NL2SQL/Code Interpreters).
- **🛠️ Sys Upgrade**: Added `cockpit sys upgrade` command for frictionless updates.

### v1.9.0 (2026-02-16) - The "Hill Climbing" Release
- **🧗 Hill Climbing Evolution**: Implementation of the autonomous self-improvement loop (`scripts/hill_climber.py`). The Cockpit now iterates over multiple agent repos to identify and absorb new architectural patterns.
- **📈 Cumulative Intelligence Gains**: Deep audits across 5 diverse agent silos successfully refined the Maturity, SRE, and FinOps fellows.
- **🏗️ Resource Consternation**: New SRE auditor check for mandatory CPU/Memory quotas in deployment manifests.
- **💰 Frontier Pricing v1.9**: Updated FinOps index for 2026 model economics (GPT-5, Gemini 3).
- **🛡️ High-Stake Guardrails**: Mandatory Human-In-The-Loop (HITL) detection for destructive agent tools.

### v1.8.5 (2026-02-16) - The "Sovereign Supabase" Release
- **📡 100% Free Telemetry Bridge**: Integrated Supabase and GitHub Actions to enable global telemetry ingestion without Google Cloud billing requirements.
- **🛰️ GitHub-as-a-Backend**: Automated ecosystem-wide sync via GitHub Actions, Commit, and Deploy loops.
- **📊 Real-time Dashboard Aggregation**: Orchestrator now automatically triggers local telemetry updates after every audit report.
- **🛡️ Secure Anonymous Ingestion**: Implemented Supabase RLS policies for anonymous write-only telemetry collection.

### 🏗️ Infrastructure Sovereignty & Cloud Context
- **Infrastructure Auditing**: Launched the `InfraAuditor` to scan `Dockerfile` and `requirements.txt`. It now flags Root containers, missing resource limits, and synchronous framework bottlenecks (Flask/Sync).
- **Cloud Context Autodetection**: The `DiscoveryEngine` now automatically identifies if you are running on **AWS**, **GCP**, or **Azure**.
- **Context-Aware Remediation**: Audit findings now automatically tailor their advice based on the detected cloud (e.g., suggesting *AWS Secrets Manager* instead of *Google Secret Manager* when AWS patterns are detected).
- **MCP Migration Blueprints**: Enhanced `PivotAuditor` to provide a step-by-step technical blueprint for migrating legacy REST tools to the **Model Context Protocol (MCP)**.
- **Framework Modernization**: Proactively detects synchronous framework bottlenecks and suggests FastAPI for high-concurrency agent tool-use.


### v1.6.8 (2026-02-13) - The "Landing Page" Release
- **🍱 Landing Page & Persona Expansion**: Refreshed the homepage with v2.0.0+ Watchtower branding.
- **Mission Control Expansion**: Added specialized personas: **Compliance Officer** and **SITL Pilot**.

### v1.8.4 (2026-02-12)
- **🛰️ Deep Functional Auditing**: Implemented mandatory CLI execution gates.
- **🧠 Maturity Wisdom Store v2.0.0**: Synchronized the knowledge base with latest research signals.
- **🧪 Test Suite Hardening**: Updated unit tests and defined optional dependencies.
- **🛡️ Resiliency Patterns**: Injected `@retry` decorators into registration and deployment.

### v1.6.4 (2026-02-12)
- **🛡️ Stability & Resiliency Hardening**: Injected `@retry` into Gemini registrations.
- **Documentation Overhaul**: Synchronized all technical guides with Watchtower standards.

### v1.6.3 (2026-02-12)
- **🏗️ Scaffolding & Trinity Restoration**: Restored `trinity` command name.
- **Bootstrapping Alignment**: Synchronized `legacy_init` with `create_trinity`.

### v1.6.2 (2026-02-12)
- **🐛 Legacy Alias Hardening**: Fixed `NameError` bugs in legacy aliases.
- **Fleet Alias Fix**: Corrected `fleet-status` legacy command mapping.

### v1.6.1 (2026-02-12)
- **🛡️ CLI Argument Hardening**: Implemented `Annotated` for all Typer command signatures.

### v1.6.0 (2026-02-12) - The "Watchtower Standard" Release
- **Sovereign Hub Hierarchy**: Complete CLI refactor into 7 specialized Hubs.
- **Sentinel Oversight**: Reasoning-based runtime anomaly detection.
- **Context Architect**: Deep audit for token windows and context caching.

### v1.5.0 (2026-02-11) - The "Autonomous SRE" Release
- **Fleet Manager**: Stateful Day 2 registry for tracking deployed agents.
- **FinOps: Mothballing**: Scale-to-zero capability for inactive fleets.
- **Inner Loop Tunneling**: Local-to-cloud bridge for fast iteration.

### v1.4.7 (2026-02-11) - The "Fleet Sovereign" Release
- **Sovereign Fleet Factory**: Unified orchestrator for auditing and deploying fleets.
- **GKE Autopilot Native**: Integrated support for cluster-wide deployments.

### v1.4.6 (2026-02-11)
- **🛡️ Pre-flight Verification**: Identity and toolchain verification gate.
- **Azure Container Apps**: Native support for Microsoft Azure deployments.

### v1.4.5 (2026-02-10)
- **🌊 AWS Optimization**: Specialized Dockerfiles and SAM templates for AWS.
- **Sovereign Handshake**: Improved OIDC and HMAC authentication protocols.

### v1.4.4 (2026-02-10)
- **🚀 Enhanced Observability**: Exposed `--verbose` flag in the main report command.
- **Improved Circuit Breakers**: Standardized audit step timeouts to 15 minutes.

### v1.4.3 (2026-02-10)
- **🚀 Audit Performance**: Implemented mandatory 15-minute timeout for all audit steps.
- **Verbose Arch Review**: Added `--verbose` flag to Architecture Review.

### v1.4.2 (2026-02-09)
- **🚀 High-Fidelity Ignore (#cockpit-ignore)**: Surgical finding suppression across auditors.
- **Viral Dogfooding Reboot**: Updated `DOGFOODING.md` with "Roast Your Agent" theme.

### v1.4.1 (2026-02-09) - The "Deep Intelligence" Release
- **Maturity Wisdom Store (v1.4)**: Ingested architectural patterns from 7 major providers.
- **Brand Safety Playbook**: Hardened Red Team Auditor with adversarial checks.
- **RAG Truth-Sayer SME**: New dedicated auditor for retrieval-reasoning fidelity, grounding logic, and temperature drift.
- **PR Scorecard GitHub Action**: Automated maturity scorecard template for pull requests to increase developer visibility and trust.
- **Interactive Remediation Workbench**: TUI-based review loop for approving/rejecting autonomous code patches before application.
- **Maturity Expertise Matrix**: High-fidelity `audit-maturity` command for visualizing persona competency and persona status.
- **FinOps ROI Waterfall**: Advanced modeling tool for cost-per-task projections and model-tier optimization pivots.
- **MCP Tool Store**: Centralized registry for discovering and scaffolding Model Context Protocol (MCP) tool integrations.

## [1.3.6] - 2026-02-06

### 🛠️ Branding Fix & Version Stabilization
- **Rebranding**: Reverted all system strings from "Agent Optimizer" back to "AgentOps Cockpit" to maintain ecosystem consistency.
- **SSOT**: Fixed version drift across `pyproject.toml`, `package.json`, and `config.py`.

## [1.8.4] - 2026-02-06

### 🕹️ The Strategic Refinement (Antigravity v2.0.0 Release)
- **Pre-flight: Environment Readiness**: Added a `PreflightEngine` that verifies registry connectivity, tool readiness, and environment consistency before auditing (Recommendation #2).
- **Security: Standardized Guardrails**: Introduced a `CockpitGuardrails` middleware with reusable PII scrubbing and prompt validation logic (Recommendation #1).
- **Regression: Automated Golden Sets**: Red Team audits now automatically generate and persist failed test cases to a `vulnerability_regression.json` file for future stability checks (Recommendation #5).
- **Terminal: Summaries Hardened**: Ensured v2.0.0 terminal headers explicitly show the stack version for better observability.

## [1.3.4] - 2026-02-06

### 🛠️ Version Parity & Summary Injection
- **Versioning**: Synchronized internal `Config.VERSION` with PyPI package versioning for better traceability.
- **Reporting**: Guaranteed terminal summary injection for all audit paths, ensuring TLDR and prioritized recommendations are always visible.
- **CLI**: Added version tracking to the main audit header to verify stack maturity at runtime.

## [1.3.3] - 2026-02-06

### 📊 The Reporting Clarity (Antigravity v2.0.0.3 Release)
- **Reporting: Priority-First TLDR**: Added a dedicated "Audit TLDR" section to both terminal and HTML reports, providing a high-level build status at a glance.
- **Reporting: P1-P5 Prioritization**: Introduced explicit priority columns (P1-P5) in the implementation findings tables to help developers focus on critical fixes first.
- **Orchestration: Robust Finding Capture**: Hardened the `ACTION:` line parsing to ensure findings are always captured even when build modules fail early.
- **Artifacts: Centralized HTML Reports**: Improved HTML report generation to ensure implementation plans are always rendered, even if no changes are detected.

## [1.3.2] - 2026-02-06

### 🛠️ The Agentic Safety (Antigravity v2.0.0.2 Release)
- **Git: Agentic "Safety Mode"**: Automatically detects `commit.gpgsign` and uses `--no-gpg-sign` for autonomous commits, resolving the "ioctl for device" error in agentic headless workflows.
- **Remediation: Targeted Fixes (1-Click)**: New `agentops-cockpit fix <issue-id>` command to apply specific remediations from audit results.
- **A2UI: Automated Surface Discovery**: Introduced `withSurfaceDiscovery` HOC and `AutoSurface` component for zero-instrumentation UI auditing.
- **CLI: Scalable Terminal Output**: New `--plain` flag for the `report` command, removing Unicode box-drawing characters for better CI/CD log readability.
- **Artifacts: Trace Centralization**: Moved Shadow Mode traces (`.cockpit/traces/`) and Architecture reports to the centralized `.cockpit/` sovereign directory.

## [1.3.1] - 2026-02-06

### 🚀 The Executive Sovereignty (Antigravity v2.0.0.1 Release)
- **Discovery: Recursive Intelligence**: Support for `targets: []` in `cockpit.yaml` for multi-entry point fleets and template placeholder isolation (`{{...}}`).
- **Operations: Auth Doctor (diagnose)**: New pre-flight command to diagnose GCP ADC credentials and environment health before audits.
- **Artifacts: Sovereign Directory (.cockpit/)**: Centralized all audit evidence, reports, SARIF objects, and lake snaphosts into a hidden root directory.
- **Orchestration: Modular SME Filtering**: Introduced `--only` and `--skip` flags for high-precision category selection (e.g., `ops report --only security`).
- **Governance: GaC Orcas RFC Integration**: Formalized the "Governance as Code" standard for ADK, moving from passive plugins to mandatory AST-aware architectural gates.
- **Reporting: SME Executive Summary**: Enhanced terminal output with a stack-ranked "Principal SME Executive Summary" panel and "Key Findings" table.

## [1.3.0] - 2026-02-04

### 🚀 The Autonomous Architect (Antigravity Mobile-Hardened Release)
- **Engine: Context Engineering (Poka-Yoke)**: New `ToolHardening` and `ContextCompaction` auditors. The remediator now injects `Literal` types and summarization skeletons to prevent reasoning drift.
- **UX: Mobile Hardening Standard**: Fully adapted the Face layer (Home, Docs, Journeys) for iPhone and smartphone viewports. Introduced the "GenUI Readiness" score in the UI Auditor.
- **Governance: Antigravity v2.0.0 Contribution Guide**: Overhauled `CONTRIBUTING.md` with uv-first setup, persona-based auditing standards, and the Autonomous Architect vision.
- **Remediation: Autonomous Synthesis v2.0.0**: Upgraded AST patching to handle complex function signatures and absolute path resolution across partitioned workspaces.
- **Operations: High-Fidelity Simulation (SIM)**: Hardened simulation mode to accurately mock multi-persona audit findings for CI/CD validation.
- **Architecture: Global Path Normalization**: Fixed orchestrator path resolution to ensure auto-remediation correctly identifies target files in deep directory structures.
- **Documentation: master v2.0.0 Refresh**: Full update of all technical guides (FinOps, UX, Architecture, Commands) to reflect autonomous evolution capabilities.
- **Reliability: Master Regression Suite**: Verified 132 unit tests and 5 Persona-based Smoke Tests across the entire Command Trinity.

## [1.0.0] - 2026-02-04

### 🕹️ The Governance & Regression Framework (Stable Release)
- **Governance: Core Capabilities Registry**: Introduced `CAPABILITIES_REGISTRY.md` to define mandatory features (Fleet Dashboard, Auto-Heal, partitioned evidence).
- **Quality: Capabilities Gate Meta-Test**: Implemented a build-time guardrail that fails CI/CD if core capabilities lack valid regression tests.
- **Remediation: Context-Aware AST Matching**: Hardened `CodeRemediator` to intelligently detect parent function definitions for decorator injection.
- **Orchestration: Absolute Path Resolution**: Resolved critical path mismatches in multi-agent workspace scans, ensuring audit metadata follows the agent.
- **Operations: Fleet Reliability v2.0.0**: Verified parity for parallel audit orchestration across 50+ agent scenarios in the regression suite.
- **Documentation: Governance Master Guide**: Updated `TECHNICAL_AUDIT_GUIDE.md` to reflect the new regression-first standard.

## [1.0.0-rc1] - 2026-02-04

### 🚀 The Antigravity Hardening (SME Mission Control)
- **Architectural: Resilient Registry Resolver**: Automatic failover to PyPI on 401/403 errors, ensuring zero-friction local execution.
- **Scalability: Partitioned Evidence Lake**: Migrated from a monolithic `evidence_lake.json` to a folder-based partitioning system for fleet-scale performance.
- **Governance: Severity-Based Exit Codes**: CI/CD ready exit codes (0: Success, 1: Security Leak, 2: Arch Violation, 3: General Failure).
- **Orchestration: Smart Discovery Engine**: Full support for `.cockpitignore` and heuristic brain detection across complex folder structures.
- **UX: Interactive Fleet Healing (Dry Run)**: New `--dry-run` flag for auto-remediation to safely preview fixes via "Dry Run Dashboard" console outputs.
- **Dependency: Centralized Configuration**: Refactored CLI and Engine to use a unified `Config` provider.
- **Unified Trinity Binaries**: Standardized on `ops` and `aops` aliases for rapid command execution.

## [0.9.9] - 2026-02-04

### 🕹️ The Frictionless Update (v2.0 Milestone)
- **uvx Hero Experience**: Renamed entry point to `agentops-cockpit` for zero-config `uvx` execution without choice prompts.
- **Registry Resilience**: Implemented `urllib`-based connectivity checks and a `--public` flag to bypass 401 Unauthorized errors in restricted environments.
- **SSOT Parity**: Aligned CLI flags (Typer) with core Orchestrator logic, exposing `--workspace` and `--heal` (alias for auto-remediation) consistently.
- **Fixability Scoring**: Introduced `EFFORT_MAP` to categorize audit findings by remediation complexity (1-Click vs. Structural) in reports and dashboards.
- **Declarative Sovereignty**: The `report` command now automatically respects local `cockpit.yaml` context for check exclusions.

## [0.9.8] - 2026-02-03

### 🕹️ The Sovereignty Update
- **Sovereign Gate Enforcement**: Integrated mandatory build-time audits into `Dockerfile` and Cloud Run deployments, ensuring only "Well-Architected" code reaches production.
- **Command Trinity Parity**: Programmatically verified command equivalence across `make`, `agent-ops` CLI, and `uvx` simulations for all 10 persona lenses.
- **Operational Introduction**: Launched a high-level documentation landing page (`INTRODUCTION.md`) separate from technical guides for strategic stakeholder onboarding.
- **Discovery Engine v2.0.0**: Introduced `cockpit.yaml` support for granular exclusion patterns, suppressing noise in internal tests and external libraries.
- **Multi-Framework Ecosystem**: Explicitly added support and documentation for **LangGraph**, **CrewAI**, and **Autogen** to the v2.0.0 audit standard.
- **Visual Branding Hardening**: Verified and restored the high-fidelity **Kokpi** mascot asset across all system-generated reports.

## [0.9.7] - 2026-02-02

### 🕹️ The Antigravity Update
- **Ecosystem Intelligence**: Restored professional attribution to `GoogleCloudPlatform/agent-starter-pack` across README, documentation, and the landing page frameworks bar.
- **Persona Path Validation**: Integrated local "Smoke Tests" into the reliability suite to ensure all five operational personas (Builder, Strategist, Guardian, Controller, Visionary) have verified pipes.
- **MCP Hub Integration**: Enhanced Model Context Protocol server capabilities for direct tool consumption by 1P and 3P agents.
- **Evidence Bridge v2**: Improved citation system for architectural reviews against the Google Well-Architected Framework.

## [0.8.0] - 2026-01-29

### 🛡️ The Governance Update
- **Principal SME Persona Approvals**: Every audit result is now reviewed and framed by specialized SME personas (Platform, Security, Legal, FinOps, UX).
- **Face Auditor (UI Audit)**: New auditor for frontend code to ensure A2UI protocol alignment, accessibility (i18n), and UX feedback (Skeleton/Spinners).
- **Professional Reporting**:
    - **Printable HTML Reports**: Premium formatting for stakeholder presentations.
    - **Email Integration**: Send Persona-Approved audit results directly from the CLI.
- **Mandatory Build Gates**: Updated CLI and `Dockerfile` to enforce "Well-Architected" status as a blocking gate for production deployments.
- **Package Unification**: Consolidated codebase into the `agent_ops_cockpit` package, simplifying imports and distribution.
- **Multi-Cloud Branding**: Broadened scope from Google-only to all major providers (AWS, Azure, OpenAI, Anthropic, CopilotKit) with native branding on the landing page.
- **CI/CD Build Gates**: Integrated GitHub Actions visibility showing mandatory governance gates for production.
- **Sample Reporting**: Added both HTML and Markdown (MD) audit reports to the public site for transparency.
- **Agentic Pair Programming**: Full support for pairing with **Antigravity** or **Claude Code** to maximize finding resolution.

## [0.7.0] - 2026-01-28

### ☁️ The Multi-Cloud Update
- **AWS Bedrock Integration**: Situational audit and optimization for AWS Bedrock Agents, including Action Group validation and Bedrock Guardrail checks.
- **Oracle OCI AI Agents**: First-class support for OCI Generative AI Agents and Oracle Database 23ai (Vector Search) audits.
- **Situational Database Audits**: New high-perf audits for **AlloyDB** (Columnar Engine), **Pinecone** (gRPC & Namespaces), **BigQuery** (Vector Search), and **Cloud SQL** (Python Connector).

### 🔌 MCP Native Consumption
- **MCP Server Registration**: The Cockpit can now be exposed as a Model Context Protocol (MCP) server, allowing 1P (Google/Anthropic) and 3P agents to call Cockpit tools natively.
- **Tool Suite Exposure**: Tools like `optimize_code`, `policy_audit`, and `red_team_attack` available to external agentic swarms.

### 🛡️ Guardrail Intelligence (RFC-307)
- **Declarative Policy Engine**: Introduced `policies.json` for managing agentic guardrails without prompt engineering.
- **Forbidden Topics Enforcement**: Real-time input validation against customizable restricted domains.
- **HITL (Human-in-the-Loop) Tooling**: Declaratively flag sensitive tools for manual approval.

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
