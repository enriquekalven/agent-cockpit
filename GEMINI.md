# GEMINI.md - Agent Context & Instructions

This repository is optimized for **Gemini CLI** and agentic development. AI agents should use this file as the primary source of truth for understanding the architecture, tools, and constraints of this project.

## 🚀 Project Overview
The **Agent Ops Starter Pack** is a modern, high-performance foundation for building and testing agent-driven user interfaces. It supports multiple interface protocols including **A2UI** (Agent-to-User Interface) and **GenUI**.

## 🛠️ Tech Stack
- **Frontend**: React (Vite), TypeScript, Vanilla CSS (Modern aesthetic).
- **Protocols**: A2UI, GenUI, Web Components.
- **Backend (Optional)**: Python ADK (Agent Development Kit) compatible.
- **Deployment**: Firebase Hosting, Google Cloud Run.

## 📁 Repository Structure
- `/src/a2ui`: Implementation of the A2UI renderer and system components.
- `/src/components`: UI components (Playground, Home, ThemeToggle, etc.).
- `/src/docs`: Documentation system and layout.
- `/src/backend`: Sample Python agent using ADK.
- `index.css`: Global design system and theme tokens.

## 🤖 AI Agent Instructions
When assisting the user:
1. **Design First**: Always prioritize high-end, premium aesthetics. Use the CSS variables in `index.css`.
2. **A2UI Standard**: When generating JSON for interfaces, follow the schema defined in `src/a2ui/A2UIRenderer.tsx`.
3. **Proactive Debugging**: If the user experiences issues with backend connectivity, check the CORS settings in `src/backend/agent.py` and the URL in `src/App.tsx`.
4. **Tooling**: Use standard CLI commands for management.

## ⌨️ CLI Commands
- `npm run dev`: Starts the React frontend development server.
- `npm run build`: Builds the production bundle.
- `npm run deploy`: Deploys to Firebase Hosting.
- `uvx agent-ui-starter`: (Proposed) Quick initialization of the environment.

## 📜 Development Patterns
- **States**: Use React `useState` for local UI state.
- **Routing**: `react-router-dom` is used for navigation.
- **Responsive**: All interfaces must be mobile-first and responsive.

---
*For more detailed guides, see the `/docs` section on the live site.*
