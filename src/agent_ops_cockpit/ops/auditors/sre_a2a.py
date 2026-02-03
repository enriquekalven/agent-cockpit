import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class SREAuditor(BaseAuditor):
    """
    v1.2 Principal SME: AI Infrastructure & Networking Auditor.
    Focuses on Networking Debt, Compute Efficiency, and CI/CD Audit Gates.
    Separates Infra from Agent Architecture logic.
    """
    
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Networking Debt: REST vs gRPC for Vector DBs
        if ("pinecone" in content.lower() or "alloydb" in content.lower()) and "grpc" not in content.lower():
            findings.append(AuditFinding(
                category="🌐 Networking",
                title="Sub-Optimal Vector Networking (REST)",
                description="Detected REST-based vector retrieval. High-concurrency agents should use gRPC to reduce 'Cognitive Tax' by 40% and prevent tail-latency spikes.",
                impact="MEDIUM",
                roi="Faster response times for RAG-heavy agents. Prevents P99 latency cascading.",
                file_path=file_path
            ))

        # 2. Compute Efficiency: Time-to-Reasoning (TTR) Cold Start
        if "cloud run" in content.lower():
            is_boosted = "startup_cpu_boost" in content.lower()
            findings.append(AuditFinding(
                category="🏗️ Infrastructure",
                title="Time-to-Reasoning (TTR) Risk",
                description=f"Cloud Run detected. {'Startup Boost active.' if is_boosted else 'MISSING startup_cpu_boost. High risk of 10s+ cold starts.'} A slow TTR makes the agent's first response 'Dead on Arrival' for users.",
                impact="HIGH" if not is_boosted else "INFO",
                roi="Reduces TTR by 50%. Ensures immediate 'Latent Intelligence' activation.",
                file_path=file_path
            ))

        # 3. CI/CD Governance: The Sovereign Gate
        if "github/workflows" in file_path and "make audit" not in content:
            findings.append(AuditFinding(
                category="🚀 CI/CD",
                title="Sovereign Gate: Bypass Detected",
                description="CI/CD pipeline allowing direct-to-prod without a mandatory 'make audit' score gate. This allows un-audited reasoning logic to touch production data.",
                impact="CRITICAL",
                roi="Enforces the 'Sovereign standard' (score > 90) as a blocking gate.",
                file_path=file_path
            ))

        # 4. Regional Proximity: Regional Affinity Routing
        if "us-central1" in content.lower() and ("europe-west1" in content.lower() or "asia-east" in content.lower()):
            findings.append(AuditFinding(
                category="📍 Networking",
                title="Regional Proximity Breach",
                description="Detected cross-region latency (>100ms). Reasoning (LLM) and Retrieval (Vector DB) must be co-located in the same zone to hit <10ms tail latency.",
                impact="HIGH",
                roi="Eliminates 'Reasoning Drift' caused by network hops.",
                file_path=file_path
            ))

        # 5. State Persistence: Short-Term Memory (STM) Audit
        if ("session" in content.lower() or "persistence" in content.lower() or "memory" in content.lower()) and "redis" not in content.lower() and "memorystore" not in content.lower():
            if "dict" in content.lower() or "self.history" in content.lower():
                findings.append(AuditFinding(
                    category="🧠 State",
                    title="Short-Term Memory (STM) at Risk",
                    description="Agent is storing session state in local pod memory (dictionaries). A GKE restart or Cloud Run scale-down wipes the agent's brain.",
                    impact="HIGH",
                    roi="Implementing Redis for STM ensures persistent agent context across pod lifecycles.",
                    file_path=file_path
                ))

        # 6. Observability: The 5th Golden Signal (TTFT)
        if "cloud trace" not in content.lower() and "ttft" not in content.lower():
            findings.append(AuditFinding(
                category="🚀 Observability",
                title="Missing 5th Golden Signal (TTFT)",
                description="No active monitoring for Time to First Token (TTFT). In agentic loops, TTFT is the primary metric for perceived intelligence.",
                impact="MEDIUM",
                roi="Allows proactive 'Latency Regression' alerts before users feel the slowness.",
                file_path=file_path
            ))

        # 7. KV-Cache Awareness: Resource Profile
        if "memory" not in content.lower() and "cloud run" in content.lower():
             findings.append(AuditFinding(
                category="🏗️ Compute",
                title="Sub-Optimal Resource Profile",
                description="LLM workloads are Memory-Bound (KV-Cache). Low-memory instances degrade reasoning speed. Consider memory-optimized nodes (>4GB).",
                impact="LOW",
                roi="Maximizes Token Throughput by preventing memory-swapping during inference.",
                file_path=file_path
            ))

        return findings

class InteropAuditor(BaseAuditor):
    """
    v1.2 Principal SME: Ecosystem Interoperability Auditor (A2X).
    Scans for MCP, A2UI, UCP, AP2, and AGUI framework compliance.
    Ensures the agent ecosystem doesn't collapse into 'Chatter Bloat'.
    """
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Chatter Bloat (Existing check)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id in ["state", "full_context", "messages", "history"]:
                        findings.append(AuditFinding(
                            category="📉 A2A Efficiency",
                            title="A2A Chatter Bloat Detected",
                            description=f"Passing entire variable '{arg.id}' to tool/agent call. This introduces high latency and token waste.",
                            impact="MEDIUM",
                            roi="Reduces token cost and latency by 30-50% through surgical state passing.",
                            line_number=node.lineno,
                            file_path=file_path
                        ))

        # 2. Handshake Missing (Schema-less calls)
        if "agent_call" in content.lower() and "schema" not in content.lower():
             findings.append(AuditFinding(
                category="🤝 A2A Protocol",
                title="Schema-less A2A Handshake",
                description="Agent-to-Agent call detected without explicit input/output schema validation. High risk of 'Reasoning Drift'.",
                impact="HIGH",
                roi="Ensures interoperability between agents from different teams or providers.",
                file_path=file_path
            ))

        # 3. Recursive Loop Detection (Infinite Spend)
        if re.search(r"def\s+(\w+).*?\1\(", content, re.DOTALL):
             findings.append(AuditFinding(
                category="🛑 Protocol Logic",
                title="Potential Recursive Agent Loop",
                description="Detected a self-referencing agent call pattern. Risk of infinite reasoning loops and runaway costs.",
                impact="CRITICAL",
                roi="Prevents 'Infinite Spend' scenarios where agents gaslight each other recursively.",
                file_path=file_path
            ))

        # 4. MCP Compliance: Tools over Logic
        if "subprocess.run" in content.lower() or "requests.get" in content.lower():
            if "mcp" not in content.lower() and "tools" in file_path.lower():
                findings.append(AuditFinding(
                    category="🛠️ MCP Protocol",
                    title="Legacy Tooling detected (Non-MCP)",
                    description="Detected raw system/network calls in a tool module. Standardizing on Model Context Protocol (MCP) provides unified governance and discovery.",
                    impact="MEDIUM",
                    roi="Allows tools to be consumed by any MCP-native agent ecosystem.",
                    file_path=file_path
                ))

        # 5. A2UI / AGUI: Generative Interface Handshake
        if "return" in content.lower() and "html" in content.lower():
            if "surfaceid" not in content.lower() and "a2ui" not in content.lower():
                findings.append(AuditFinding(
                    category="🎭 A2UI Protocol",
                    title="Missing GenUI Surface Mapping",
                    description="Agent is returning raw HTML/UI strings without A2UI surfaceId mapping. This breaks the 'Push-based GenUI' standard.",
                    impact="HIGH",
                    roi="Enables proactive visual updates to the user through the Face layer.",
                    file_path=file_path
                ))

        # 6. UCP / AP2: Universal Context & Agent Protocol
        if "context" in content.lower() and "headers" not in content.lower():
             if "ap2" not in content.lower() and "ucp" not in content.lower():
                findings.append(AuditFinding(
                    category="🤝 Standard Protocols",
                    title="Proprietary Context Handshake (Non-AP2)",
                    description="Agent is using ad-hoc context passing. Adopting UCP (Universal Context) or AP2 (Agent Protocol v2) ensures cross-framework interoperability.",
                    impact="LOW",
                    roi="Prevents vendor lock-in and enables multi-framework swarms (e.g. LangChain + CrewAI).",
                    file_path=file_path
                ))

        return findings
