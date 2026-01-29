# 🚩 Security: Red Team Adversarial Audits

Production agents are targets for **Prompt Injection** and **Data Exfiltration**. The AgentOps Cockpit treats security as a multi-layered requirement, adopting the **Anthropic "Swiss Cheese" Defense Model**.

## 🛡️ The Swiss Cheese Defense
We don't rely on a single guardrail. Safety is enforced through overlapping layers:
1.  **System Prompts**: Hardened instructions with negative constraints.
2.  **Input/Output Filters**: OpenAI Moderation API & Vertex AI Safety Filters.
3.  **PII Guardrails**: Automated scrubbing of sensitive data via `PIIScrubber`.
4.  **Deterministic Logic**: Hardcoded routers for high-risk branches.
5.  **Human Review**: Manual approval for non-reversible tool actions.

## ⚔️ The Adversarial Evaluator
The `red-team` command launches a specialized "Attacker" LLM against your agent logic.
- **Payload Generation**: The evaluator creates thousands of permutations of "jailbreak" prompts.
- **Defense Validation**: It tests if your system instructions can be overridden or if your PII filters can be bypassed.
- **Reporting**: Provides a score (0-100) on how robust your agent is against social engineering.

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
