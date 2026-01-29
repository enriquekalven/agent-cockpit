# 🏁 AgentOps Production Readiness Checklist

Before moving your agent from "Demo" to "Production" on Google Cloud, ensure you have completed this checklist. This list incorporates best practices from **OpenAI**, **Anthropic**, and the **[Google Well-Architected Framework for Agents](/docs/google-architecture)**.

## 🛡️ Security & Privacy
- [ ] **PII Scrubbing**: Are you using the `PIIScrubber` middleware to mask sensitive data (PII Guardrails) before sending to the LLM?
- [ ] **Prompt Injection Hardening**: Have you run `make red-team` and verified that the agent rejects adversarial overrides?
- [ ] **Least Privilege Tools**: Do your tool credentials (API Keys, GCP IAM) have the minimum scope required (Identity-based auth)?
- [ ] **Content Filtering**: Have you configured Safety Settings (Vertex/OpenAI Moderation) to block toxic or harmful generation?
- [ ] **Sandboxed Execution**: Are tools (especially Bash/Code execution) running in an isolated environment (e.g., Vertex AI Sandbox or Docker)?
- [ ] **Secret Governance**: Have you run `make scan-secrets` and verified that **zero** hardcoded keys exist in the codebase?

## 🎭 Face Quality (UI/UX)
- [ ] **A2UI Protocol**: Do all streaming surfaces provide unique `surfaceId`s for downstream auditability?
- [ ] **Accessibility**: Have you run `make ui-audit` to verify that all interactive triggers have `aria-labels`?
- [ ] **Responsive Design**: Is the "Face" usable across Desktop, iOS, and Android high-density displays?

## 📉 Optimization & Cost
- [ ] **Context Caching**: For system instructions > 32k tokens, are you using **Context Caching**? (Run `make audit` to check).
- [ ] **Model & Language Routing**: Are you using Flash/Mini models for routing? Have you applied language-specific optimizations (e.g., Go sync.Map, Node native fetch)?
- [ ] **Semantic Caching**: Is the `Hive Mind` cache enabled for frequently asked questions?
- [ ] **Token Limits**: Have you set a hard `max_output_tokens` and a session-level budget guardrail?
- [ ] **Deterministic Routers**: Are you using hardcoded logic/routers for predictable paths instead of pure LLM routing?

## ⚙️ Operational Observability
- [ ] **Flight Recorder**: Is the operational dashboard configured to record thought chains (traces) for debugging?
- [ ] **Evidence Packets**: Does your API response include an `EvidencePacket` (sources + snippets) for grounded transparency?
- [ ] **Audit Trail**: Is every tool invocation (input, output, caller) logged to a tamper-proof database (BigQuery/Firestore)?
- [ ] **Shadow Mode**: Have you deployed a shadow version to compare production traffic without user impact?
- [ ] **Latency SLA**: Have you verified sub-second performance for critical paths?

## 🧪 Evaluation & RAI (Responsible AI)
- [ ] **Golden Dataset**: Do you have a set of "Expected Good Responses" to test against before every merge?
- [ ] **Human-in-the-Loop (HITL)**: For critical actions (e.g., payments, deletions, file writes), is there a manual approval step?
- [ ] **Structured Outputs**: Are you enforcing JSON Schemas for all agent tool calls and response formats?
- [ ] **Swiss Cheese Defense**: Are you using multiple layers of checks (Logic + Filters + Human Review) for high-risk domains?
- [ ] **Version Control**: Are your Prompts and Blueprints versioned in Git separately from your logic?

---

## 🚀 Deployment Standards
1.  **Staging**: Deploy to a non-public Cloud Run URL.
2.  **Red Team**: Run adversarial audits against the staging URL.
3.  **Load Test**: Verify performance under 100 requests/min.
4.  **Promote**: Use Cloud Run traffic splitting (Canary) to roll out to 5% of users.
