# Development Guide

This guide covers how to extend and customize the Optimized Agent Stack for your specific agentic applications.

## 🏗️ Architecture Overview

The project is structured into three main layers:
1. **Core Renderer**: Located in `src/a2ui`, it processes JSON to React components.
2. **Component Library**: Located in `src/components`, contains the logic for Playground and Documentation.
3. **Design System**: Driven by `src/index.css`, using CSS variables for high-fidelity theming.

## 🎨 Customizing the UI

### Adding New Components
To add a new A2UI component:
1. Define the component in `src/a2ui/A2UIRenderer.tsx`.
2. Update the `COMPONENT_MAP` to include your new type.
3. Add any necessary styles to `index.css`.

### Theming
The app supports light and dark modes out of the box. Modify the `--accent-color` and other variables in `:root` and `[data-theme="light"]` in `index.css` to match your brand.

## 🤖 Integrating Agents

### Using ADK (Agent Development Kit)
We recommend using the ADK for Python-based agents. The starter pack includes a sample in `src/backend`.

```python
from a2ui import Surface, Card, Text

def get_welcome_ui():
    surface = Surface(surface_id="welcome")
    surface.add(Text("Dynamic Agent UI", variant="h1"))
    return surface.to_json()
```

### Protocol Standards
- **A2UI**: Best for structured, predictable interfaces.
- **GenUI**: Best for generative, fluid interfaces.

## 🛠️ Testing Workflows

Use the Playground to test individual components before integrating them with your agent's backend.

1. Open Playground.
2. Toggle "Agent Mode" to simulate real-time chat interactions.
3. Use "Editor Mode" for precise JSON crafting.

## 📜 Best Practices
- **Security**: Always sanitize agent-generated content.
- **Performance**: Keep A2UI payloads small to minimize latency.
- **State**: Prefer stateless components where possible; handle state in the agent logic.
