# 🕹️ The Cockpit: Operations & Governance

The **Cockpit** is the mission control for your AI agents. While the "Engine" handles reasoning, the Cockpit ensures that reasoning is safe, cost-effective, and auditable.

<div align="center">
  <img src="diagrams/ecosystem.png" alt="Google Ecosystem Integrations" width="100%" />
</div>

## 🛰️ Shadow Routing (The Side-by-Side)
Shadow Mode allows you to deploy a new version of your agent (v2) alongside your production version (v1).
- **How it works**: The Cockpit routes incoming queries to both models.
- **Why use it**: Compare accuracy, latency, and tone without impacting your users.
- **Access**: Select "Shadow Mode" from the Cockpit Dashboard to see real-time comparisons.

## 🧠 Hive Mind (Semantic Caching)
The Hive Mind is a specialized middleware that prevents redundant LLM calls.
1. **Request**: User asks a common question (e.g., "What is your refund policy?").
2. **Lookup**: Hive Mind checks a Vector Store (AlloyDB/Memorystore) for semantically similar historical answers.
3. **Hit**: If a match is >90% similar, the answer is served in 10ms for $0 cost.
4. **Learning**: If no match, the LLM answers, and the new (Query, Answer) pair is added to the Hive Mind.

## 📊 Operational Metrics
The Cockpit dashboard provides a real-time data flow of:
- **Token Velocity**: Monitoring for prompt runaways or recursive loops.
- **Memory Pressure**: Visualization of the "Leaky Bucket" context eviction.
- **Cost Drift**: Predictive auditing of monthly Gemini consumption.

## 🚦 Human-in-the-Loop (HITL)
For high-stakes actions, the Cockpit allows you to define "Gatekeeper" tools.
- When an agent calls a gated tool, the Cockpit pauses execution and requests human approval via the **Face (A2UI)**.
- **A2UI v0.8 Features**: Leverage new components like `Tabs`, `MultipleChoice`, and `TextField` for structured human feedback during the approval flow.
- Approval can be granted directly from the operations terminal or the user-facing app.
