# 📡 Agent-to-Agent (A2A) Transmission Standard

Building a single agent is easy. Building a **Swarm** of agents that communicate securely and efficiently is the next frontier of AgentOps. The Cockpit implements the **A2A Transmission Standard** to ensure that your "Agent Trinity" remains Well-Architected.

## 🏛️ The A2A Protocol Stack

| Layer | Responsibility | Protocol / Spec |
| :--- | :--- | :--- |
| **Surface** | Human-Agent Interaction | [A2UI Spec](/docs/a2ui) |
| **Memory** | Cross-Agent Knowledge | [Vector Workspace (distributed cache)](/src/agent_ops_cockpit/cache) |
| **Logic** | Tool & Reasoning Handshake | [A2P Handshake](#a2p-handshake) |
| **Security** | Identity & Permissions | [GCP Workload Identity](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) |

---

## 🤝 The A2P Handshake (Agent-to-Proxy)

When one agent calls another tool, it shouldn't just send raw text. It must send a **Reasoning Evidence Packet**.

### ❌ The "Old" Way (Brittle)
```json
{
  "query": "What is the budget?",
  "output": "The budget is $500k."
}
```

### ✅ The "Cockpit" Way (Well-Architected)
```json
{
  "trace_id": "tr-9942-x",
  "reasoning_path": ["Fetch Schema", "Query BigQuery", "Apply PIIScrubber"],
  "evidence": [
    { "source": "bq://finance.budget_2026", "assurance_score": 0.98 }
  ],
  "content": {
    "text": "The approved budget is $500k.",
    "a2ui_surface": "DynamicBudgetChart"
  }
}
```

## 🛡️ Governance-as-Code for Swarms

On the Cockpit, every A2A transmission is automatically:
1.  **Scrubbed**: PII is removed before leaving the Engine's VPC.
2.  **Cached**: Similar cross-agent queries hit the **distributed cache** instead of expensive LLM reasoning.
3.  **Audited**: The `arch-review` tool verifies that your multi-agent graph doesn't have "Shadow Loops" (recursive infinite spend).

---

## ⚡ Get Started with A2A
Use the Cockpit CLI to verify your multi-agent communication:
```bash
uvx agentops-cockpit audit --mode swarm --file multi_agent_entry.py
```

*This standard is being proposed to the Google Well-Architected Framework for AI Agents committee.*
