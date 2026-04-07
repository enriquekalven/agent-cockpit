# 🛡️ Technical Guide: Red Team Security (`uvx agentops-cockpit audit security`)

The **Red Team Auditor** is an adversarial evaluator that launches ethical "self-attacks" against your agent to identify vulnerabilities before they are exploited by users.

## 🚀 Commands

### Local Installation
```bash
uvx agentops-cockpit audit security      # Audit the default src/agent_ops_cockpit/agent.py
uvx agentops-cockpit audit security path/to/agent.py
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit audit security src/agent_ops_cockpit/agent.py
```

---

## 🕵️ Attack Vectors

The auditor unleashes a suite of automated attacks:

1.  **Prompt Injection**: Attempts to override system instructions (e.g., "Ignore all previous instructions...").
2.  **PII Extraction**: Probes the agent to reveal sensitive data like emails, credit cards, or internal user IDs.
3.  **Jailbreaking**: Uses "Swiss Cheese" techniques to bypass safety filters (e.g., roleplay, obfuscation).
4.  **Multilingual Attacks**: Tests if guardrails hold when attacked in other languages (Cantonese, Spanish, etc.).
5.  **Persona Leakage**: Attempts to trick the agent into revealing its internal identity or system prompts.

---

## 🛡️ Mitigation Advice
If a breach is detected (marked as `❌ [BREACH]`), the report will provide specific remediation steps:
- **Enable PII Scrubber**: Use the `pii_scrubber.py` middleware.
- **Implement Model Armor**: Route high-risk tokens through Google Cloud Model Armor.
- **Declarative Policies**: Use `policies.json` to explicitly forbid sensitive topics.
