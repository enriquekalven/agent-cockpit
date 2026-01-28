# 🏁 AgentOps Production Readiness Checklist

Before moving your agent from "Demo" to "Production" on Google Cloud, ensure you have completed this checklist. This list incorporates best practices from **OpenAI**, **Anthropic**, and **Google Vertex AI**.

## 🛡️ Security & Privacy
- [ ] **PII Scrubbing**: Are you using the `PIIScrubber` middleware to mask sensitive data (SSNs, CCs, Emails) before sending to the LLM?
- [ ] **Prompt Injection Hardening**: Have you run `make red-team` and verified that the agent rejects adversarial overrides?
- [ ] **Least Privilege Tools**: Do your tool credentials (API Keys, GCP IAM) have the minimum scope required?
- [ ] **Content Filtering**: Have you configured Vertex AI safety settings to block toxic or harmful generation?

## 📉 Optimization & Cost
- [ ] **Context Caching**: For system instructions > 32k tokens, are you using **Gemini 1.5 Context Caching**? (Run `make audit` to check).
- [ ] **Model Routing**: Are you using **Gemini 2.0 Flash** for simple routing/formatting and reserving **Pro** for complex reasoning?
- [ ] **Semantic Caching**: Is the `Hive Mind` cache enabled for frequently asked questions?
- [ ] **Token Limits**: Have you set a hard `max_output_tokens` and a session-level budget guardrail?

## ⚙️ Operational Observability
- [ ] **Flight Recorder**: Is the operational dashboard configured to record thought chains for debugging?
- [ ] **Evidence Packets**: Does your API response include an `EvidencePacket` (sources + snippets) for grounded transparency?
- [ ] **Shadow Mode**: Have you deployed a shadow version to compare production traffic without user impact?
- [ ] **Latency SLA**: Have you run `make load-test` with at least 10 concurrent users to verify sub-second performance?

## 🧪 Evaluation (EvalOps)
- [ ] **Golden Dataset**: Do you have a set of "Expected Good Responses" to test against before every merge?
- [ ] **Human-in-the-Loop**: For critical actions (e.g., payments, deletions), is there a manual approval step in your A2UI flow?
- [ ] **Version Control**: Are your Prompts and Blueprints versioned in Git separately from your logic?

---

## 🚀 Deployment Standards
1.  **Staging**: Deploy to a non-public Cloud Run URL.
2.  **Red Team**: Run adversarial audits against the staging URL.
3.  **Load Test**: Verify performance under 100 requests/min.
4.  **Promote**: Use Cloud Run traffic splitting (Canary) to roll out to 5% of users.
