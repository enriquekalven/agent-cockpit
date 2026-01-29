# 🎭 UI Development: The Face

The **Face** layer of our stack is built on the **A2UI (Agent-to-User Interface)** protocol. This transforms raw text responses into rich, interactive application surfaces.

## 🚀 The A2UI Advantage
Stop building custom UI for every agent tool. Our renderer dynamically manifests components based on the **Agentic JSON** returned by the Engine.

| Feature | Description |
| :--- | :--- |
| **Adaptive Surfaces** | UIs that change layout based on tool outputs. |
| **HITL Integration** | Built-in approval buttons for sensitive agent actions. |
| **Evidence Display** | One-click "Show Sources" visibility via Evidence Packets. |
| **Real-time Sync** | WebSocket/SSE streaming for "thought" visibility. |

## 🎨 Design System
We adhere to a high-fidelity, sleek aesthetic:
- **Style**: Dark-mode primary with neon accent glows (Purple/Teal).
- **Icons**: Standardized `lucide-react` set.
- **Glassmorphism**: Heavy use of translucent panels and frosted backgrounds.

## 🧱 Component Library
Common pre-built components in `src/components/a2ui/`:
- `ActionCard`: For tool approvals.
- `SourceList`: For grounding evidence.
- `ThoughtChain`: For showing the agent's internal reasoning.
- `StatusRibbon`: For cost/latency transparency.

## 🏗️ Building Custom Components
To add a new visual surface:
1. Define the schema in `src/agent_ops_cockpit/agent.py`.
2. Create the React component in `src/components/a2ui/custom/`.
3. Map the JSON `surfaceId` to your new component in the `A2UIRenderer`.

---
*Reference: [A2UI Official Specification](https://github.com/google/A2UI)*
