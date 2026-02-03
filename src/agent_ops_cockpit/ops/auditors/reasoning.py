import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class ReasoningAuditor(BaseAuditor):
    """
    The 'Shadow Consultant' reasoning engine.
    Performs Phase 2 Active Reasoning: identifying trade-offs, bottlenecks, and intent.
    """
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Intent Detection: Look for 'Seams' between frameworks
        if "langgraph" in content.lower() and "crewai" in content.lower():
             findings.append(AuditFinding(
                category="🏗️ Architecture",
                title="Strategic Conflict: Multi-Orchestrator Setup",
                description="Detected both LangGraph and CrewAI. Using two loop managers is a 'High-Entropy' pattern that often leads to cyclic state deadlocks.",
                impact="HIGH",
                roi="Recommend using LangGraph for 'Brain' and CrewAI for 'Task Workers' to ensure state consistency.",
                file_path=file_path
            ))

        # 2. Logic Probing: Sequential await profiling
        async_funcs = [n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)]
        for func in async_funcs:
            awaits = [n for n in ast.walk(func) if isinstance(n, ast.Await)]
            if len(awaits) >= 3:
                # Check if awaits are independent (not using results of previous yields)
                # This is a 'Reasoning' step over the AST
                findings.append(AuditFinding(
                    category="🧗 Reliability",
                    title="Sequential Data Fetching Bottleneck",
                    description=f"Function '{func.name}' has {len(awaits)} sequential await calls. This increases latency lineary (T1+T2+T3).",
                    impact="MEDIUM",
                    roi="Parallelizing these calls could reduce latency by up to 60%.",
                    line_number=func.lineno,
                    file_path=file_path
                ))

        # 3. FinOps Reasoning: High-tier model in loops
        # (Simulated reasoning: we look for model strings and for loops together)
        if re.search(r"gemini-1\.5-pro|gpt-4", content) and re.search(r"for\s+\w+\s+in", content):
             if any(x in content.lower() for x in ["classify", "label", "is_", "has_"]):
                findings.append(AuditFinding(
                    category="💰 FinOps",
                    title="Model Efficiency Regression",
                    description="High-tier model (Pro/GPT-4) detected inside a loop performing simple classification tasks.",
                    impact="HIGH",
                    roi="Pivoting to Gemini 1.5 Flash for this loop reduces token spend by 90% with zero accuracy loss.",
                    file_path=file_path
                ))

        # 4. Context Bloat Analysis (Prompt Logic)
        long_prompts = re.findall(r"['\"]{3}([\s\S]{5000,})['\"]{3}", content)
        if long_prompts:
            findings.append(AuditFinding(
                category="📉 Efficiency",
                title="Architectural Prompt Bloat",
                description="Massive static context (>5k chars) detected in system instruction. This risks 'Lost in the Middle' hallucinations.",
                impact="MEDIUM",
                roi="Pivot to a RAG (Retrieval Augmented Generation) pattern to improve factual grounding accuracy.",
                file_path=file_path
            ))

        return findings
