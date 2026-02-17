Authors: enriq
Proposed Date: 2026-02-06
Status: IMPLEMENTED v1.8.4.1
Approvers: 
Workstreams: Ecosystem - ADK
Links:

DO NOT EDIT ANYTHING ABOVE THIS LINE. SHARE EDIT ACCESS WITH HERMES-AUTOMATION@

# Orcas RFC: Governance as Code in ADK

## Summary
While the recently approved Agent Guardrails RFC (go/orcas-rfc-307) establishes the foundational tooling for safety—specifically ADK extensions and Model Armor—the challenge for the enterprise has now shifted from individual agent safety to **fleet-wide operations**. This RFC proposes the implementation of **Governance as Code (GaC)** within ADK to embed architectural integrity, financial guardrails, and adversarial resilience directly into the developer workflow. 

This initiative transforms ADK from a reasoning framework into a **production-ready distribution** that ensures system quality by default, preventing the proliferation of "shadow agents" that lack enterprise oversight.

## Motivation
As we scale agentic solutions across the organization, we are observing four systemic failures that existing guardrails do not address:

1.  **System-Blind Development**: Current agent development is hyper-focused on prompt engineering, often at the expense of operational overhead and sound system design.
2.  **Monolithic Anti-patterns**: Developers are mixing reasoning logic (Engine) with UI logic (Face). This results in tightly coupled, "black box" agents that are impossible to audit, reuse, or scale.
3.  **Token Inefficiency (Cost Drift)**: We lack a standardized mechanism to catch unoptimized token consumption—such as redundant system instructions or uncompressed context—before they reach production and impact the bottom line.
4.  **Static Security Gaps**: Traditional unit tests are insufficient for agents. They do not capture conversational drift, tool-execution non-determinism, or multi-turn adversarial pressure.

## Proposal 
I propose implementing the following high-fidelity governance capabilities directly into the ADK core, shifting governance from a "manual audit" phase to a "build-time" requirement.

### [P0] Structural Integrity Validator (Architecture-as-Code)
We must enforce a strict separation between **Engine** (Reasoning/Tools), **Face** (UX/A2UI), and **Governance/Ops**. 

*   **Capability**: ADK will natively verify that repository structures adhere to these boundaries. This is not just a linter; it’s a dependency-graph validator that prevents "Engine" code from importing UI components.
*   **Mechanism**:
    *   **Import Linting**: Any reasoning logic found generating HTML or React components directly will trigger a build failure. The Engine must return "Pure Knowledge" (JSON/Data).
    *   **Contract Enforcement**: Verification of mandatory entry points:
        *   `src/backend/main.py`: Valid ADK entry point.
        *   `src/a2ui/renderer.config.ts`: A2UI component registration.
        *   `config/policies.json`: Validated policy schema.
    *   **Operations Injection**: Static analysis will verify that mandatory middleware (e.g., `PIIScrubberMiddleware`, `SemanticCacheProvider`) is registered in the application instantiation.
*   **Trigger**: Integrated into `adk audit --structural` (local) and `adk deploy --verify-architecture` (CI/CD).

### [P0] Policy-as-Code Manifests
We will move away from bespoke "prompt engineering" for safety and adopt structured policy files.

*   **Standardized Schema**: Developers define guardrails (topic restrictions, token budgets, HITL requirements) in a structured manifest.
*   **CEL/Cedar Integration**: ADK will ingest policies encoded in Common Expression Language (CEL), ensuring dev-loop guardrails are mathematically identical to production governance.
*   **Policy Pull Sync**: ADK will implement a sync mechanism to pull global enterprise policies (e.g., "All BQ deletes require HITL") into the local validator automatically.

### [P1] Environment-Aware Optimization (The "Sovereign Scan")
Standard linters are environment-blind; Governance as Code requires awareness of the underlying silicon and stack.

*   **Logic-Based Optimization**:
    *   If **AlloyDB** is detected via SDK imports, ADK mandates Columnar Engine usage.
    *   If **Context Length > 32k** is detected, ADK enforces **Gemini Context Caching** to mitigate the 90% premium on repeated prefix costs.
*   **Developer Feedback**: Real-time identification of "Dead-on-Arrival" patterns (e.g., "ADK Tool defined without a Structured Schema will cause Tool-Execution Drift. [Fix]").

### [P1] Financial Intelligence Layer
Embed cost-transparency directly into the CLI.

*   **Projected Savings**: During `adk audit`, the tool will calculate and display projected savings for missing optimizations (e.g., "Switching this bond to a Semantic Cache will save $0.05 per turn and 1.5s latency").
*   **Business Justification**: Enables developers to lead with ROI when proposing architectural refactors.

### [P2] Adversarial Resilience Benchmarking ("Self-Hack")
Implement a build-time resilience suite that goes beyond static filters.

*   **Dynamic Scoring**: ADK will simulate sequential conversational attacks (Gaslighting, Logic Bypass) to calculate a **Dynamic Resilience Score**. 
*   **Goal**: Identify logic leaks and persona drift that exist *within* the reasoning logic itself.

### [P2] The Evidence Bridge
Every governance failure must be educational, mapping back to the **Google Cloud Architecture Framework**.

*   **Capability**: Map every gap or breach to a specific Architecture Framework citation.
*   **Benefit**: Transforms the developer loop into a continuous "Excellence Loop," where the tool teaches the builder how to reach production-grade quality.

## Timeline 
*   **Phase 1 (Month 1)**: P0 Structural Validator and Policy Manifest Schemas.
*   **Phase 2 (Month 2)**: P1 Environment-Awareness and Financial CLI integrations.
*   **Phase 3 (Month 3)**: P2 Adversarial Benchmarking and Evidence Bridge citations.

## Cross-workstream Impacts
*   **ADK Extensions Team**: Integration of structural validators into the base `Agent` class.
*   **FinOps Central**: Syncing pricing matrices to the ADK Financial Intelligence layer.
*   **Governance Hub (Hermes)**: Finalizing the Policy Pull Sync protocol.

## Outcome 
1.  **Zero-Day Quality**: 100% of ADK agents meet "Well-Architected" standards before first deployment.
2.  **Infrastructure ROI**: Automated injection of Context Caching and Flash-routing reduces enterprise OpEx by an estimated 30-40%.
3.  **Governance Scalability**: Organizations can bulk-patch security gaps across hundreds of agents via centralized policy updates.

---

## 🏛️ Fundamental Differences: GaC vs. Policy Engines & Plugins

A critical question for stakeholders is: *How is Governance as Code within ADK different from a standard policy engine (like OPA) or a set of security plugins?* 

The differentiation lies in the **Scope of Enforcement** and the **Lifecycle Phase**.

| Feature | Traditional Policy Engine | Plugins / Middleware | ADK Governance as Code (GaC) |
| :--- | :--- | :--- | :--- |
| **Logic Layer** | **Data-Aware (JSON/Rego)**: Evaluates request/response schemas and identity tokens at the network boundary. | **Runtime-Aware (Shims)**: Wraps function calls to inject logging or security checks during execution. | **AST-Aware (Code Structure)**: Parses source code to enforce architectural boundaries and mandatory library patterns. |
| **Lifecycle Phase** | **Runtime (Post-Deployment)**: Operates as an external sidecar blocking malicious production traffic. | **Runtime (Middleware)**: Executed during the application processing loop in live/staging environments. | **Shift-Left (Build & CI Gate)**: Validates system integrity during the dev-loop and as a mandatory CI/CD blocking gate. |
| **Action** | **Passive Blocking**: Issues Deny/Allow verdicts without providing context or code-level remediation. | **Behavioral Hooking**: Intercepts active calls to modify variables or alter runtime application state. | **Proactive Remediation**: Synthesizes and injects code patches (e.g., `@retry`, `ContextCache`) to resolve gaps. |
| **Enforcement** | **External (Sidecar)**: Disconnected from the repository logic; requires external policy management. | **Optional (Opt-in)**: Relies on developers to manually install and configure the necessary extensions. | **Sovereign (Mandatory Gate)**: Embedded in the ADK distribution; failures block repository deployment. |
| **Optimization** | **Environment-blind**: Lacks visibility into the underlying cloud topology or actual token expenditure. | **Ad-hoc / Static**: Provides generic caching or rate-limiting regardless of reasoning load or infra version. | **Infra-Aware (KV-Cache/TTR)**: Links code patterns to specific Hardware/SDK performance and FinOps ROI. |

### 1. Structure over Syntax (The AST Advantage)
Traditional policy engines evaluate the **Syntax** of a request (is this user allowed to call this API?). GaC evaluates the **Structure** of the engine itself. By using AST (Abstract Syntax Tree) analysis, ADK can identify "Spaghetti Agents" where reasoning and UI are mixed—a failure mode that no runtime policy engine can detect.

### 2. Proactive Remediation vs. Passive Blocking
A policy engine is passive; it blocks a request and waits for a developer to fix it. The GaC **"Closer Engine"** is proactive. If it detects a missing resiliency pattern or an unoptimized prompt, it doesn't just block the build; it **synthesizes the fix** (e.g., injecting `@retry` or `ContextCacheConfig`) directly into the codebase.

### 3. Simulation-Based Evaluation (Digital Twins)
Policy engines are deterministic. Agentic quality is non-deterministic. GaC introduces **Adversarial Simulations** to measure "Reasoning Stability." This isn't a policy you configure; it's a behavioral benchmark that measures how the agent reacts to 100x concurrent pressure—bridging the gap between "Security" and "SRE."

### 4. Continuous Evolution vs. Static Extensions (Plugins)
While a **Plugin** is typically an optional library that adds a specific feature at runtime (e.g., adding a logger), **Governance as Code** is an operational layer that owns the **Architectural Health** of the project.

*   **Plugins are "Opt-In"**: A developer can choose to ignore a security plugin. In GaC, the **Sovereign Gate** is mandatory. If your code doesn't meet the trinity separation standard, it simply does not deploy.
*   **Plugins modify Behavior; GaC modifies Code**: Plugins wrap your logic to change what it does at runtime. GaC uses the **Closer Engine** to refactor what your logic *is* at the source level. It ensures that resiliency and cost-optimization are permanent fixtures of the codebase, not just "shimmed" on top. 
*   **Holistic Context**: A plugin is usually scope-blind (e.g., a caching plugin doesn't know if you've mixed HTML into your reasoning logic). GaC has **Full-Project Awareness**, validating the boundaries between the Engine, Face, and Cockpit across the entire repository.

---

## 🛠️ Concrete Implementation: The Developer Experience

To ground these abstract concepts, here is a comparison of a typical "Day 1" agent versus the "Day 60" production standard enforced by GaC.

### The "Spaghetti Agent" (Rejected by ADK Validator)
This is what developers often build and deploy today. It is unscalable, expensive, and fragile.

```python
# file: agent.py
import openai

def get_user_data(user_id):
    # ❌ Problem 1: No Resiliency. If this fails, the whole agent crashes.
    # ❌ Problem 2: No Schema. The LLM will "hallucinate" the tool output.
    response = openai.ChatCompletion.create(model="gpt-4", messages=[...])
    
    # ❌ Problem 3: HTML mixed with Logic. This kills UI flexibility.
    return f"<html><body>User: {response.name}</body></html>"

# ❌ Problem 4: No Context Caching for large system prompts.
system_prompt = "You are a helpful assistant..." * 1000 
```

### The GaC Standard (Auto-Remediated by ADK)
When the developer runs `adk audit --apply-fixes`, the "Closer Engine" transforms the code into this production-grade structure.

```python
# file: src/backend/tools.py (Separation of Concerns)
from tenacity import retry, wait_exponential
from google.adk.agents.context_cache_config import ContextCacheConfig

@tool
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def get_user_data(user_id: str) -> dict: # ✅ Enforced Typed Schema
    """Fetches user metadata from the source system."""
    # Logic remains pure data. No HTML allowed.
    return db.fetch(user_id)

# file: src/backend/main.py
app = Agent(
    model="gemini-1.5-pro",
    # ✅ GaC Injected: Reduces prefix costs by 90%
    context_cache_config=ContextCacheConfig(min_tokens=2048, ttl_seconds=600)
)
```

### What the ADK Validator actually "sees":
The GaC engine doesn't just read strings; it parses the **Abstract Syntax Tree (AST)**.

| Code Pattern | GaC Action | Reasoning |
| :--- | :--- | :--- |
| `return f"<html>..."` | **BUILD FAIL** | Mixed Face/Engine logic detected in `backend/`. |
| `openai.Chat(...)` | **WARN / FIX** | Missing Sovereign Pivot: Gemini/Vertex recommended. |
| `def tool(): ...` | **FIX** | Injected Typed Hinting and `@retry` decorator. |
| `prompt = "..."` | **OPTIMIZE** | Large constant detected: Injected Context Caching. |

---

## Appendix
Concept Prototype & Implementation Reference: [https://github.com/enriquekalven/agent-cockpit](https://github.com/enriquekalven/agent-cockpit)
