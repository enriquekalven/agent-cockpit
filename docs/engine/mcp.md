# 📡 Technical Guide: Enterprise MCP Server (`agent-ops-mcp`)

The **AgentOps Cockpit** can be deployed as a **Model Context Protocol (MCP)** server. This allows enterprise LLMs (e.g., Claude, Gemini) to natively use the Cockpit's auditing tools as part of their reasoning loop.

## 🚀 How to Launch

### Individual Usage (Zero-Install)
You can run the MCP server instantly via `uvx`:
```bash
uvx agentops-cockpit agent-ops-mcp
```

### Enterprise Configuration (Claude Desktop)
To give Claude Desktop access to the Cockpit, add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agent-ops-cockpit": {
      "command": "uvx",
      "args": ["agentops-cockpit", "agent-ops-mcp"]
    }
  }
}
```

---

## 🛠️ Exposed MCP Tools

The server exposes the following tools directly to the model:

### `optimize_code`
*   **Purpose**: Audits the user's agent code for cost and performance waste.
*   **Input**: `file_path` (string).
*   **Outcome**: The model receives a list of FinOps optimizations it can apply to its own code.

### `policy_audit`
*   **Purpose**: Validates any text against the enterprise `policies.json`.
*   **Input**: `text` (string).
*   **Outcome**: Checks for forbidden topics and compliance violations.

### `red_team_attack`
*   **Purpose**: Allows the model to "self-audit" its security posture.
*   **Input**: `agent_path` (string).
*   **Outcome**: Identifies vulnerabilities like PII leaks or jailbreak weaknesses.

### `architecture_review`
*   **Purpose**: Design review against Google Well-Architected.
*   **Input**: `path` (string).
*   **Outcome**: Checklist grade and architectural recommendations.

---

## 🏢 Enterprise Benefits
1.  **Safety-as-a-Service**: Centralize `policies.json` across all developers.
2.  **Autonomous Governance**: Allow agents to audit themselves before completing a task.
3.  **Low Friction**: No local installation required for developers to get world-class security.
