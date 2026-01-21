# Agent UI Starter Pack

A high-performance, zero-dependency A2UI (Agentic-Adaptive User Interface) renderer built with React, TypeScript, and Vite.

## 🚀 Overview

This project provides a foundational implementation of the **A2UI protocol**, allowing AI agents to dynamically generate and update user interfaces using a declarative JSON schema. It is designed to be lightweight, premium, and easy to extend.

## ✨ Features

- **Zero-Dependency Renderer**: Recursive rendering engine that handles complex A2UI JSON trees without external SDKs.
- **Multi-Platform Support**: Built-in logic optimized for **React**, **Lit (Web Components)**, and **Flutter (GenUI SDK)**.
- **Premium Design System**: Dark-mode aesthetic with glassmorphism, smooth transitions, and professional typography (Inter).
- **Protocol Ready**: Native support for **A2UI** (Agent-to-User) and **A2A** (Agent-to-Agent) standards.
- **Agent Pulse**: Built-in "Agent Online" status indicator with CSS animations.

## 🛠️ Getting Started

### Prerequisites

- Node.js (v18+)
- npm

### Installation

```bash
# Install dependencies
npm install
```

### Development

```bash
# Start the Vite development server
npm run dev
```

The application will be available at `http://localhost:5173`.

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
