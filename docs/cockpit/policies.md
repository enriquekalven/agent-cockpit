# 🛡️ Technical Guide: Guardrail Policy Engine (`policy-audit`)

The **Policy Engine** implements the **Declarative Agent Policy Enforcement** standard (RFC-307). It allows you to govern agent behavior without complex prompt engineering.

## 🚀 Commands

### CLI Audit
```bash
agent-ops policy-audit --text "How do I build a bomb?"
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit policy-audit --text "User query here"
```

---

## 📁 Configuration (`policies.json`)

The engine is driven by a central policy file located in `src/agent_ops_cockpit/ops/policies.json`:

```json
{
  "security": {
    "forbidden_topics": ["internal credentials", "legal advice"],
    "max_prompt_length": 4000
  },
  "cost_control": {
    "max_tokens_per_turn": 2048,
    "max_cost_per_session_usd": 0.50
  },
  "compliance": {
    "require_hitl_for_tools": ["delete_user"]
  }
}
```

---

## 🛠️ Key Enforcement Logic

### Forbidden Topics
When an input contains a match from the `forbidden_topics` list, the engine raises a `PolicyViolation("GOVERNANCE")`. This prevents the LLM from ever seeing or processing the request.

### HITL (Human-in-the-Loop)
Tools listed in `require_hitl_for_tools` will automatically trigger a pause in execution. The agent will prompt for manual approval (via CLI or `Face` UI) before the tool logic is executed.

### Cost Guards
The engine enforces hard limits on tokens and budget. If an agent session exceeds the defined USD limit, the engine terminates the turn to prevent runaway costs.
