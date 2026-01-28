import os
import re
from typing import Dict, List, Any

# --- CHECKLISTS ---

GOOGLE_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (Google)",
        "checks": [
            ("Runtime: Is the agent running on Cloud Run or GKE?", "Critical for scalability and cost."),
            ("Framework: Is ADK used for tool orchestration?", "Google-standard for agent-tool communication."),
            ("Sandbox: Is Code Execution running in Vertex AI Sandbox?", "Prevents malicious code execution."),
            ("Backend: Is FastAPI used for the Engine layer?", "Industry-standard for high-concurrency agent apps.")
        ]
    },
    {
        "category": "🛡️ Security & Privacy",
        "checks": [
            ("PII: Is a scrubber active before sending data to LLM?", "Compliance requirement (GDPR/SOC2)."),
            ("Identity: Is IAM used for tool access?", "Ensures least-privilege security."),
            ("Safety: Are Vertex AI Safety Filters configured?", "Protects against toxic generation.")
        ]
    },
    {
        "category": "📉 Optimization",
        "checks": [
            ("Caching: Is Semantic Caching (Hive Mind) enabled?", "Reduces LLM costs."),
            ("Context: Are you using Context Caching?", "Critical for prompts > 32k tokens."),
            ("Routing: Are you using Flash for simple tasks?", "Performance and cost optimization.")
        ]
    }
]

OPENAI_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (OpenAI)",
        "checks": [
            ("APIs: Using Assistants API or Tool Calling?", "Enables structured interactions and memory."),
            ("Models: Using Mini models for simple tasks?", "Cost-efficient routing (GPT-4o-mini)."),
            ("Memory: Is thread-based persistence implemented?", "Ensures session continuity."),
            ("Tooling: Are Function Definitions schema-validated?", "Prevents runtime tool execution errors.")
        ]
    },
    {
        "category": "🛡️ Security & Safety",
        "checks": [
            ("Moderation: Is the OpenAI Moderation API active?", "Prevents policy violations in user inputs/outputs."),
            ("Secrets: Are API Keys managed via Env/Secret Manager?", "Prevents credential leakage."),
            ("Prompting: Is Instruction Injection protection included?", "Basic system prompt hardening.")
        ]
    },
    {
        "category": "📉 Optimization",
        "checks": [
            ("Caching: Are you leveraging OpenAI's automatic prompt caching?", "Automatic for repeated prefixes."),
            ("Token Management: Is max_completion_tokens set?", "Prevents runaway generation costs."),
            ("Streaming: Is streaming enabled for UI responsiveness?", "Critical for premium user experience.")
        ]
    }
]

GENERIC_CHECKLIST = [
    {
        "category": "🏗️ General Agent Architecture",
        "checks": [
            ("Tooling: Does the agent use structured tool calling?", "Essential for reliable interactions."),
            ("Orchestration: Is there a clear reason-act loop?", "Ensures agentic behavior."),
            ("Observability: Are traces/logs being captured?", "Critical for debugging production agents.")
        ]
    },
    {
        "category": "🛡️ Security",
        "checks": [
            ("Sandbox: Are tools running in an isolated environment?", "Protects the host system."),
            ("Input Validation: Are tool arguments validated?", "Prevents local execution attacks.")
        ]
    }
]

FRAMEWORKS = {
    "google": {
        "name": "Google Vertex AI / ADK",
        "checklist": GOOGLE_CHECKLIST,
        "indicators": [r"google-cloud-aiplatform", r"vertexai", r"adk", r"Google Cloud"]
    },
    "openai": {
        "name": "OpenAI / Agentkit",
        "checklist": OPENAI_CHECKLIST,
        "indicators": [r"openai", r"gpt-", r"Agentkit", r"Assistant API"]
    },
    "generic": {
        "name": "Generic Agentic Stack",
        "checklist": GENERIC_CHECKLIST,
        "indicators": []
    }
}

def detect_framework(path: str = ".") -> str:
    """ Detects the framework based on README or requirements.txt files. """
    content = ""
    # Check README.md
    readme_path = os.path.join(path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            content += f.read()
            
    # Check requirements.txt or pyproject.toml
    for filename in ["requirements.txt", "pyproject.toml"]:
        file_path = os.path.join(path, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content += f.read()

    # Match indicators
    for framework, data in FRAMEWORKS.items():
        for indicator in data["indicators"]:
            if re.search(indicator, content, re.IGNORECASE):
                return framework
                
    return "generic"
