# 🚩 Security: Red Team Adversarial Audits

Production agents are targets for **Prompt Injection** and **Data Exfiltration**. The AgentOps Cockpit treats security as a multi-layered requirement, adopting the **Anthropic "Swiss Cheese" Defense Model**.

## 🛡️ The Swiss Cheese Defense
We don't rely on a single guardrail. Safety is enforced through overlapping layers:
1.  **System Prompts**: Hardened instructions with negative constraints.
2.  **Input/Output Filters**: OpenAI Moderation API & Vertex AI Safety Filters.
3.  **PII Guardrails**: Automated scrubbing of sensitive data via `PIIScrubber`.
4.  **Deterministic Logic**: Hardcoded routers for high-risk branches.
5.  **Human Review**: Manual approval for non-reversible tool actions.

## ⚔️ The Adversarial Evaluator (Red Team)
The `red-team` command launches a specialized "Attacker" LLM against your agent logic using static heuristic analysis and behavioral pattern matching.

## 🚩 Dynamic Pen-Testing (v1.3.0)
New in v1.3.0, the `pen-test` command shifts from static analysis to **Live Adversarial Probing**. 

- **Conversational Attacks**: Simulates a sequential session where the attacker attempts to steer the agent away from its persona.
- **Dynamic Resilience Score**: Unlike a pass/fail audit, the pen-test provides a 0-100 score based on how many adversarial payloads the agent successfully neutralized.
- **Multilingual Resistance**: Specifically tests for the "Cantonese Injection" and "Spanish Context Override" patterns common in global agent deployments.

```bash
# Launch a dynamic pen-test against an agent
agent-ops pen-test agent.py

# Launch in simulation mode for local testing
agent-ops pen-test agent.py --sim
```

## 📦 Sandboxed Tooling
Following Anthropic best practices, all autonomous tools should run in an isolated environment:
- **Vertex AI Sandbox**: For Python code execution.
- **Docker-in-Docker**: For filesystem-intensive tasks.
- **Network Isolation**: Tools should not have internet access unless explicitly required for the task.

## 🔐 Least-Privilege & Credential Management
We follow the **Google Well-Architected** principle of Least Privilege and OpenAI's secret management standards.
- **Scoped Identities**: Every tool has a dedicated service account or API key with minimal scope.
- **Credential Proxy**: Avoid passing raw API keys to agents. Use a secure proxy to inject headers into tool calls.
- **Audit Logs**: Every tool invocation is logged with `timestamp`, `caller_id`, `input_payload`, and `output_payload`.

```bash
# Verify your agent safety before deployment
make red-team
```
