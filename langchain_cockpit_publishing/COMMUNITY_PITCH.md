# LangChain Community Listing Pitch 🦜🕹️

Use the following templates to announce the integration in the community.

## 💬 Option 1: Discord (#integrations or #announcements)

**Subject:** New Governance Integration: AgentOps Cockpit

Hey LangChain community! 🦜

We just released a new callback integration for **AgentOps Cockpit** (v2.0.4 Sovereign Evolution). 

We're focusing on "Governance as Code" — helping developers detect PII, monitor token density, and gate destructive tools automatically within their chains and graphs.

- **Check it out:** https://github.com/enriquekalven/agent-ops-cockpit
- **Docs:** https://github.com/enriquekalven/agent-ops-cockpit/blob/main/docs/LANGCHAIN_INTEGRATION.md

Would love to hear any feedback on how we can better support LangGraph's cyclic state governance!

---

## 🐙 Option 2: GitHub Issue (Ecosystem Submission)

**Title:** [Ecosystem Integration] AgentOps Cockpit: Sovereign Governance for LangChain

**Description:**
Hi LangChain Team,

I'd like to propose adding **AgentOps Cockpit** to the LangChain Ecosystem/Integrations page.

AgentOps Cockpit is a distribution focused on Agentic Governance (The Sovereign Standard). We've implemented a `BaseCallbackHandler` that provides:
1. **Real-time PII Scrubbing** for prompts.
2. **FinOps Auditing** (Context Caching suggestions).
3. **Safety Gating** for destructive tool calls.

We've already scaffolded the partner package and would love to be listed in the "Governance, Monitoring, and Operations" category.

**Repository:** https://github.com/enriquekalven/agent-ops-cockpit
**Integration Path:** `src/agent_ops_cockpit/integrations/langchain.py`

Thanks!
