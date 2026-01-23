# Agent UI Starter Pack

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/enriquekalven/agent-ui-starter-pack)

A high-performance, zero-dependency A2UI (Agentic-Adaptive User Interface) renderer built with React, TypeScript, and Vite.

![Agent UI Hero](/hero.png)

## 🚀 Overview

This project provides a foundational implementation of the **A2UI protocol**, allowing AI agents to dynamically generate and update user interfaces using a declarative JSON schema. It is designed to be lightweight, premium, and easy to extend.

## ✨ Unified Agent UI Ecosystem

This starter pack is designed to support the leading agentic UI standards:

- **A2UI (Agent-to-User Interface)**: The core protocol for adaptive, JSON-driven interfaces.
- **GenUI (Generative UI)**: Full support for generative patterns across Web and Flutter.
- **AG UI (Agentic UI)**: Integration-ready for CopilotKit and high-end React agent surfaces.

## ✨ Features

- **Zero-Dependency Renderer**: Recursive rendering engine that handles complex A2UI JSON trees without external SDKs.
- **Visual Analytics**: Built-in support for **StatBars**, **Images**, and **Dynamic Lists** for rich dashboard generation.
- **Interactive Playground**: A built-in sandbox with **Agent Mode** to simulate real-world AI-driven UI updates.
- **Premium Design System**: Dark-mode aesthetic with glassmorphism, smooth transitions, and professional typography (Inter).
- **Protocol Ready**: Native support for **A2UI** (Agent-to-User) and **A2A** (Agent-to-Agent) standards.

## 🛠️ Getting Started


```bash
# Standard Setup (A2UI / React / Vite)
uvx agentui-starter-pack create my-ui

# High-Fidelity Setup (AG UI / CopilotKit)
uvx agentui-starter-pack create my-ui --ui agui

# GenUI SDK (Flutter / Cross-Platform)
uvx agentui-starter-pack create my-ui --ui flutter

# Web Components (Lit / Zero-Dependency)
uvx agentui-starter-pack create my-ui --ui lit
```

### Prerequisites

- Node.js (v18+)
- Python (v3.10+) for the CLI
- git

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start the Vite development server
npm run dev
```

The application will be available at `http://localhost:8888`.

## 🚀 Deployment

The project includes one-line deployment commands via the `Makefile`.

| Platform | Command |
| :--- | :--- |
| **Cloud Run** | `make deploy-cloud-run` |
| **Firebase** | `make deploy-firebase` |
| **GKE** | `make deploy-gke` |

For more options and configuration details, see the [Deployment Guide](./DEPLOYMENT.md).

## 🏗️ Architecture & Frameworks

### Web Components (Lit)
A2UI's core repository is built with **Lit**. For the "Full Control" path, you can use the native Lit renderer to create standard Web Components that work in any framework (including Angular).

### Flutter (GenUI SDK)
A2UI is designed for developers building custom surfaces across Web, Mobile, and **Flutter**. The **GenUI SDK** pattern allows for "Native-First" rendering where the agent sends blueprints that are realized using high-performance Flutter widgets.

### AG UI (CopilotKit)
For high-end React implementations, we recommend **CopilotKit** (formerly AG UI). It provides a full-stack starter designed for A2A and A2UI, handling the streaming "pipes" so you can focus on building beautiful surfaces.

## 📡 A2A Protocol
The **Agent-to-Agent (A2A)** protocol enables agents to communicate over a network. See the [A2A_GUIDE.md](./A2A_GUIDE.md) for details on exposing agents as services and orchestrating multi-agent systems.

## 📜 A2UI Protocol
The renderer expects an `A2UISurface` object with the following structure:

```json
{
  "surfaceId": "unique-id",
  "content": [
    {
      "type": "Text",
      "props": { "text": "Hello World", "variant": "h1" }
    },
    {
      "type": "Card",
      "props": { "title": "System Meta" },
      "children": [...]
    }
  ]
}
```

## 📄 License

MIT
