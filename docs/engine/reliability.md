# 🧗 Technical Guide: Quality Hill Climbing (`make quality-baseline`)

**Quality Hill Climbing** is an iterative optimization process to ensure your agent's reasoning trajectory remains accurate as you update prompts and tools.

<div align="center">
  <img src="diagrams/workflow.png" alt="Operational Workflow" width="100%" />
</div>

## 🚀 Commands

### Local Installation
```bash
make quality-baseline  # Run baseline audit
agent-ops quality-baseline --steps 10
```

### Portable (Zero-Install)
```bash
uvx agentops-cockpit quality-baseline
```

---

## 🛠️ The Hill-Climbing Process

Following **Google ADK Evaluation** best practices, the auditor follows this loop:

1.  **Golden Dataset**: The agent is tested against a set of predefined "Golden Scenarios" (Ground Truth).
2.  **LLM-as-a-Judge**: A separate, high-fidelity model (Gemini 1.5 Pro) evaluates the agent's performance.
3.  **Metrics Captured**:
    *   **Response Match**: Does the final answer match the expected outcome?
    *   **Tool Trajectory**: Did the agent call the correct tools in the right order?
    *   **Logic Fidelity**: Is the reasoning chain sound?
4.  **Scoring**: The agent receives a percentage score. The goal is to "Climb the Hill" by iteratively refining prompts until the score hits >90%.

---

## 📊 When to Run
- After updating the **System Prompt**.
- After adding or removing **Tools**.
- Before a **Major Release** to ensure no reasoning regressions have occurred.
