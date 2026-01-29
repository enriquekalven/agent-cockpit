import os
import re

# --- CHECKLISTS ---

GOOGLE_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (Google)",
        "checks": [
            ("Runtime: Is the agent running on Cloud Run or GKE?", "Critical for scalability and cost."),
            ("Framework: Is ADK used for tool orchestration?", "Google-standard for agent-tool communication."),
            ("Sandbox: Is Code Execution running in Vertex AI Sandbox?", "Prevents malicious code execution."),
            ("Backend: Is FastAPI used for the Engine layer?", "Industry-standard for high-concurrency agent apps."),
            ("Outputs: Are Pydantic or Response Schemas used for structured output?", "Ensures data integrity and reliable tool execution.")
        ]
    },
    {
        "category": "🛡️ Security & Privacy",
        "checks": [
            ("PII: Is a scrubber active before sending data to LLM?", "Compliance requirement (GDPR/SOC2)."),
            ("Identity: Is IAM used for tool access?", "Ensures least-privilege security."),
            ("Safety: Are Vertex AI Safety Filters configured?", "Protects against toxic generation."),
            ("Policies: Is 'policies.json' used for declarative guardrails?", "Enforces RFC-307 standards for forbidden topics and tool HITL.")
        ]
    },
    {
        "category": "📉 Optimization",
        "checks": [
            ("Caching: Is Semantic Caching (Hive Mind) enabled?", "Reduces LLM costs."),
            ("Context: Are you using Context Caching?", "Critical for prompts > 32k tokens."),
            ("Routing: Are you using Flash for simple tasks?", "Performance and cost optimization.")
        ]
    },
    {
        "category": "🌐 Infrastructure & Runtime",
        "checks": [
            ("Agent Engine: Are you using Vertex AI Reasoning Engine for deployment?", "Managed orchestration with built-in versioning and traces."),
            ("Cloud Run: Is 'Startup CPU Boost' enabled?", "Critical for reducing cold-start latency in Python agents."),
            ("GKE: Is Workload Identity used for IAM?", "Google-standard for secure service-to-service communication."),
            ("VPC: Is VPC Service Controls (VPC SC) active?", "Prevents data exfiltration by isolating the agent environment.")
        ]
    },
    {
        "category": "🎭 Face (UI/UX)",
        "checks": [
            ("A2UI: Are components registered in the A2UIRenderer?", "Ensures engine-driven UI protocol compliance."),
            ("Responsive: Are mobile-first media queries present in index.css?", "Ensures usability across devices (iOS/Android)."),
            ("Accessibility: Do interactive elements have aria-labels?", "Critical for inclusive design and automated testing."),
            ("Triggers: Are you using interactive triggers for state changes?", "Improves 'Agentic Feel' through reactive UI.")
        ]
    },
    {
        "category": "🧗 Resiliency & Best Practices",
        "checks": [
            ("Resiliency: Are retries with exponential backoff used for API/DB calls?", "Prevents cascading failures during downtime (e.g., using tenacity)."),
            ("Prompts: Are prompts stored in external '.md' or '.yaml' files?", "Best practice for separation of concerns and versioning."),
            ("Sessions: Is there a session/conversation management layer?", "Ensures context continuity and user state tracking."),
            ("Retrieval: Are you using RAG or Efficient Context Caching for large datasets?", "Optimizes performance vs. cost for retrieval-heavy agents.")
        ]
    },
    {
        "category": "⚖️ Legal & Compliance",
        "checks": [
            ("Copyright: Does every source file have a legal copyright header?", "IP protection and enterprise policy."),
            ("License: Is there a LICENSE file in the root?", "Mandatory for legal distribution."),
            ("Disclaimer: Does the agent provide a clear LLM-usage disclaimer?", "Liability mitigation for AI hallucinations."),
            ("Data Residency: Is the agent region-restricted to us-central1 or equivalent?", "Ensures data stays within geofenced boundaries.")
        ]
    },
    {
        "category": "📢 Marketing & Brand",
        "checks": [
            ("Tone: Is the system prompt aligned with brand voice (Helpful/Professional)?", "Consistency in agent personality."),
            ("SEO: Are OpenGraph and meta-tags present in the Face layer?", "Critical for discoverability and social sharing."),
            ("Vibrancy: Does the UI use the standard corporate color palette?", "Prevents ad-hoc branding in autonomous UIs."),
            ("CTA: Is there a clear Call-to-Action for every agent proposing a tool?", "Drives conversion and user engagement.")
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
            ("Tooling: Are Function Definitions schema-validated?", "Prevents runtime tool execution errors."),
            ("Routing: Are deterministic routers used for critical branches?", "Prevents LLM drift in sensitive workflows."),
            ("Outputs: Is 'Structured Outputs' enabled for tool calls?", "Ensures data integrity and prevents injection.")
        ]
    },
    {
        "category": "🛡️ Security & Safety",
        "checks": [
            ("Moderation: Is the OpenAI Moderation API active?", "Prevents policy violations in user inputs/outputs."),
            ("Secrets: Are API Keys managed via Env/Secret Manager?", "Prevents credential leakage."),
            ("PII: Are PII Guardrails configured to block sensitive leaks?", "Required for production data handling."),
            ("HITL: Is there a User Approval node for sensitive actions?", "Human-in-the-loop for non-idempotent changes.")
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

ANTHROPIC_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (Anthropic)",
        "checks": [
            ("Orchestration: Is an Orchestrator-Subagent pattern used?", "ANTHROPIC best practice for complex tasks."),
            ("Loop: Is a structured Context-Action-Verify loop implemented?", "Ensures deterministic agent behavior."),
            ("ACIs: Is the Agent-Computer Interface (ACI) well-documented?", "Detailed tool descriptions are critical for Claude.")
        ]
    },
    {
        "category": "🛡️ Security & Guardrails",
        "checks": [
            ("Sandbox: Are tool calls running in a sandboxed bash environment?", "Isolates host filesystem and network."),
            ("IAM: Is 'Least Privilege' IAM enforced for all tools?", "Treat tool access like production IAM permissions."),
            ("Confirmation: Are sensitive commands (git/rm) blocked or confirmed?", "Prevents accidental or malicious damage."),
            ("Swiss Cheese: Are multiple layers of guardrails (filters + logic) active?", "Anthropic's 'Swiss Cheese Defense' model.")
        ]
    },
    {
        "category": "📉 Reliability",
        "checks": [
            ("Circuit Breakers: Are rate limits and circuit breakers active?", "Prevents infinite loops and API exhaustion."),
            ("Human-in-the-Loop: Are critical file/env changes manual?", "Ensures safety in autonomous workflows."),
            ("Logging: Is every tool invocation logged with full context?", "Auditability for autonomous agent decisions.")
        ]
    }
]

MICROSOFT_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (Microsoft)",
        "checks": [
            ("Framework: Using Unified Microsoft Agent Framework?", "Merges AutoGen orchestration with Semantic Kernel stability."),
            ("Workflows: Are repeatable, graph-based processes defined?", "Semantic Kernel best practice for enterprise reliability."),
            ("Orchestration: Is a centralized orchestrator managing multi-agent handoffs?", "Critical for complex problem solving in AutoGen."),
            ("Maturity: Are features GA or Preview?", "Graduation process ensures production stability.")
        ]
    },
    {
        "category": "🛡️ Security & Governance",
        "checks": [
            ("Guardrails: Are real-time Semantic Guardrails active?", "Monitors prompts/responses for risky behavior."),
            ("Secrets: Is Azure KeyVault used for key management?", "Production-standard for credential security."),
            ("HITL: Are custom 'Guardrails Agents' active?", "AutoGen pattern for enforcing RAI policies."),
            ("Sandbox: Is code execution isolated in Docker?", "Prevents malicious instruction execution.")
        ]
    },
    {
        "category": "📉 Reliability",
        "checks": [
            ("Observability: Is message tracing enabled via Azure AI?", "Critical for debugging multi-agent message flows."),
            ("Testing: Are TypeChat or similar used for output validation?", "Ensures structured reliability in C#/Python.")
        ]
    }
]

AWS_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (AWS)",
        "checks": [
            ("Action Groups: Are Bedrock Action Groups used for tools?", "Standardizes tool execution via OpenAPI schemas."),
            ("Grounding: Is Contextual Grounding enabled in Knowledge Bases?", "Mitigates hallucinations by anchoring to facts."),
            ("Isolation: Is model customization running in a VPC?", "Ensures network security for specialized training.")
        ]
    },
    {
        "category": "🛡️ Security & Guardrails",
        "checks": [
            ("Guardrails: Are organization-level Bedrock Guardrails active?", "Enforces consistent RAI policies across apps."),
            ("Information: Are PII Redaction and Denied Topics configured?", "Protects sensitive data and prevents brand risk."),
            ("IAM: Are service roles scoped to least-privilege?", "Ensures agents cannot cross-service impersonate."),
            ("KMS: Is encryption enabled via Customer Managed Keys (CMK)?", "Production requirement for rest and transit.")
        ]
    },
    {
        "category": "📉 Operations",
        "checks": [
            ("Logging: Is Model Invocation Logging enabled?", "Mandatory for audit and compliance (Audit Manager)."),
            ("Tracing: Are Agent Traces used to monitor orchestration?", "Provides visibility into RAG and reasoning logic."),
            ("IaC: Is the agent deployed via CloudFormation or CDK?", "Ensures repeatable and stable deployments.")
        ]
    }
]

COPILOTKIT_CHECKLIST = [
    {
        "category": "🏗️ Core Architecture (CopilotKit)",
        "checks": [
            ("Platform: Is CopilotKit Cloud or Self-Hosted used?", "Determines control over infrastructure and state."),
            ("State: Is shared state used for UI-Agent sync?", "Ensures the 'Face' remains aligned with the 'Engine'."),
            ("Reconnection: Is reliable thread persistence enabled?", "Critical for long-running user sessions.")
        ]
    },
    {
        "category": "🛡️ Security & Guardrails",
        "checks": [
            ("Moderation: Is 'guardrails_c' configured in the Cloud?", "Uses OpenAI content moderation as a baseline."),
            ("Auth: Is MFA and Conditional Access enforced via Entra/IAM?", "Ensures only trusted users can trigger agent actions."),
            ("Labels: Are Microsoft Purview sensitivity labels applied?", "Controls what documents the Copilot can access."),
            ("HITL: Are 'Human-in-the-Loop' checkpoints defined?", "Empowers users to guide agents at critical junctures.")
        ]
    },
    {
        "category": "📉 Deployment",
        "checks": [
            ("Staging: Is a staged rollout (pilot program) active?", "Best practice for minimizing AI-driven risks."),
            ("Monitoring: Is activity logging integrated with SIEM?", "Provides anomalous activity detection (Sentinel).")
        ]
    }
]

LANGCHAIN_CHECKLIST = [
    {
        "category": "🏗️ LangChain / LangGraph Architecture",
        "checks": [
            ("State: Is a typed State Schema used for the graph?", "Ensures data integrity across complex agentic nodes."),
            ("Persistence: Is a Checkpointer (Sqlite/Postgres) active?", "Mandatory for long-running agents and cross-session resume."),
            ("Observability: Is LangSmith integrated for trace analysis?", "De-facto standard for debugging cyclic graph execution."),
            ("Tooling: Are custom tools wrapped in @tool decorators?", "Ensures schema extraction and LLM compatibility (OpenAI/Anthropic).")
        ]
    },
    {
        "category": "🛡️ Security & Guardrails",
        "checks": [
            ("Loop: Is a 'Max Iterations' limit set on the Graph?", "Prevents infinite loops and runaway API costs."),
            ("Secrets: Are API keys loaded via ChatOpenAI(api_key=...)?", "Ensures keys are injectable and not hardcoded."),
            ("Moderation: Is a moderation node active in the graph?", "Pattern for real-time safety filtering of agent thoughts.")
        ]
    }
]

GENERIC_CHECKLIST = [
    {
        "category": "🏗️ Zero-Shot Discovery (Unknown Tech)",
        "checks": [
            ("Reasoning: Does the code exhibit a core reasoning/execution loop?", "Detected Structural Pattern: Universal Agentic Loop."),
            ("State: Is there an identifiable state management or memory pattern?", "Ensures session continuity even in custom stacks."),
            ("Tools: Are external functions being called via a registry or dispatcher?", "Standard for tool-enabled agents."),
            ("Safety: Are there any input/output sanitization blocks?", "Basic security hygiene for any AI application.")
        ]
    }
]

ORACLE_CHECKLIST = [
    {
        "category": "🏗️ Oracle Cloud Architecture",
        "checks": [
            ("Platform: Using OCI Generative AI or AI Agents?", "OCI-native managed agent orchestration."),
            ("Data: Is Oracle Database 23ai (Vector Search) used?", "Enterprise-grade vector grounding for RAG."),
            ("Compute: Is the agent running on OCI Container Instances or OCI Functions?", "Scale-to-zero and high-performance OCI compute options.")
        ]
    },
    {
        "category": "🛡️ Security & Governance (Oracle)",
        "checks": [
            ("Identity: Is OCI IAM with dynamic groups enabled?", "Ensures secure, credential-less access to OCI resources."),
            ("Secrets: Using OCI Vault for API/DB secrets?", "Production standard for key management on OCI."),
            ("Network: Is the agent isolated in an OCI VCN with Private Endpoints?", "Prevents internet exposure of internal agent tools.")
        ]
    }
]

CREWAI_CHECKLIST = [
    {
        "category": "🏗️ CrewAI Multi-Agent Architecture",
        "checks": [
            ("Orchestration: Is the 'Process' defined (Sequential/Hierarchical)?", "CrewAI best practice for complex team coordination."),
            ("Memory: Is Short-term or Long-term memory enabled?", "Critical for maintaining context across multi-agent tasks."),
            ("Tools: Are tools shared across the Crew or specific to Agents?", "Promotes agent specialization and efficiency.")
        ]
    },
    {
        "category": "🛡️ Security & Reliability",
        "checks": [
            ("Manager: Is a 'Manager Agent' used for hierarchical crews?", "Provides a central governance layer for agent handoffs."),
            ("Delegation: Is 'allow_delegation' configured per agent?", "Controls the communication flow between autonomous agents.")
        ]
    }
]

FIREBASE_CHECKLIST = [
    {
        "category": "🏗️ Firebase Infrastructure",
        "checks": [
            ("Hosting: Are security headers (HSTS, CSP) configured in firebase.json?", "Prevents cross-site scripting and hijacking."),
            ("Firestore: Are composite indexes used for complex agent queries?", "Ensures high-performance data retrieval for RAG."),
            ("Functions: Is 'Minimum Instances' set for critical agent tools?", "Reduces cold-start latency for backend tool execution."),
            ("Rules: Are security rules locked down to 'request.auth'?", "Prevents unauthorized database access.")
        ]
    }
]


# --- MULTI-LANGUAGE / FRONTEND CHECKLISTS ---

STREAMLIT_CHECKLIST = [
    {
        "category": "🏗️ Streamlit Architecture",
        "checks": [
            ("State Management: Using st.session_state for agent history?", "Critical for maintaining context in stateful agents."),
            ("Async: Are long-running agent calls wrapped in st.spinner?", "Improves UX by providing immediate feedback."),
            ("Secrets: Using .streamlit/secrets.toml instead of hardcoding?", "Standard for secure key management in Streamlit.")
        ]
    }
]

LIT_CHECKLIST = [
    {
        "category": "🏗️ Lit Web Components",
        "checks": [
            ("Protocol: Is A2UI BaseElement used for styling isolation?", "Ensures components work across different host apps."),
            ("Reactivity: Are agent updates handled via @property decorator?", "Standard for efficient Lite-element updates."),
            ("Shadow DOM: Are styles encapsulated to avoid platform leaking?", "Critical for distributing agent widgets to 3rd party sites.")
        ]
    }
]

ANGULAR_CHECKLIST = [
    {
        "category": "🏗️ Angular Enterprise Face",
        "checks": [
            ("Signals: Using Angular Signals for real-time agent updates?", "Modern reactive pattern for low-latency UIs."),
            ("Interceptors: Is there a global error handler for Agent API timeouts?", "Ensures graceful degradation when LLMs are slow."),
            ("DI: Is the Agent Engine abstracted as a Service?", "Promotes testability and clean architecture.")
        ]
    }
]

NODEJS_CHECKLIST = [
    {
        "category": "🏗️ NodeJS / TypeScript Engine",
        "checks": [
            ("Runtime: Using Bun or Node 20+ for native fetch?", "Optimizes performance for high-frequency API calls."),
            ("Security: Is Helmet middleware active in the Face API?", "Hardens the Express/Hono server against common attacks."),
            ("Types: Are Zod/Pydantic-like schemas used for tool outputs?", "Ensures type-safety across the agent-tool boundary.")
        ]
    }
]

GO_CHECKLIST = [
    {
        "category": "🏗️ Go High-Perf Engine",
        "checks": [
            ("Concurrency: Using Goroutines for parallel tool execution?", "Leverages Go's performance for multi-agent orchestration."),
            ("Validation: Using struct tags for JSON schema enforcement?", "Standard for ensuring engine-face protocol compatibility."),
            ("Tracing: Using OpenTelemetry for multi-hop agent traces?", "Mandatory for observability in complex Go agents.")
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
    "anthropic": {
        "name": "Anthropic Claude / SDK",
        "checklist": ANTHROPIC_CHECKLIST,
        "indicators": [r"anthropic", r"claude", r"sonnet", r"opus", r"haiku"]
    },
    "microsoft": {
        "name": "Microsoft Agent Framework / AutoGen",
        "checklist": MICROSOFT_CHECKLIST,
        "indicators": [r"autogen", r"semantic-kernel", r"microsoft-agent", r"TypeChat"]
    },
    "aws": {
        "name": "AWS Bedrock Agents",
        "checklist": AWS_CHECKLIST,
        "indicators": [r"boto3", r"bedrock", r"aws-sdk", r"ActionGroup"]
    },
    "copilotkit": {
        "name": "CopilotKit.ai",
        "checklist": COPILOTKIT_CHECKLIST,
        "indicators": [r"copilotkit", r"Guardrails_c", r"CopilotSidebar"]
    },
    "langchain": {
        "name": "LangChain / LangGraph",
        "checklist": LANGCHAIN_CHECKLIST,
        "indicators": [r"langchain", r"langgraph", r"stategraph", r"checkpointer"]
    },

    "streamlit": {
        "name": "Streamlit (Python)",
        "checklist": STREAMLIT_CHECKLIST,
        "indicators": [r"streamlit", r"st\.", r"st_chat_message"]
    },
    "lit": {
        "name": "Lit / Web Components",
        "checklist": LIT_CHECKLIST,
        "indicators": [r"lit-element", r"lit-html", r"@customElement"]
    },
    "angular": {
        "name": "Angular Face",
        "checklist": ANGULAR_CHECKLIST,
        "indicators": [r"@angular/core", r"NgModule", r"RxJS"]
    },
    "nodejs": {
        "name": "NodeJS / TypeScript Engine",
        "checklist": NODEJS_CHECKLIST,
        "indicators": [r"package\.json", r"npm", r"node", r"express", r"hono"]
    },
    "go": {
        "name": "Go High-Perf Engine",
        "checklist": GO_CHECKLIST,
        "indicators": [r"go\.mod", r"goroutine", r"golang"]
    },
    "firebase": {
        "name": "Firebase / Google Cloud Hosting",
        "checklist": FIREBASE_CHECKLIST,
        "indicators": [r"firebase\.json", r"\.firebaserc", r"firestore"]
    },
    "oracle": {
        "name": "Oracle Cloud Infrastructure (OCI)",
        "checklist": ORACLE_CHECKLIST,
        "indicators": [r"oci", r"oracle", r"23ai"]
    },
    "crewai": {
        "name": "CrewAI",
        "checklist": CREWAI_CHECKLIST,
        "indicators": [r"crewai", r"Agent\(", r"Task\(", r"Crew\("]
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
            
    # Check requirements.txt, pyproject.toml, package.json, go.mod, or firebase.json
    for filename in ["requirements.txt", "pyproject.toml", "package.json", "go.mod", "firebase.json", ".firebaserc"]:


        file_path = os.path.join(path, filename)
        if os.path.exists(file_path):
            content += f" {filename} " # Include filename as indicator
            with open(file_path, "r") as f:
                content += f.read()

    # Match indicators
    for framework, data in FRAMEWORKS.items():
        for indicator in data["indicators"]:
            if re.search(indicator, content, re.IGNORECASE):
                return framework
                
    return "generic"
