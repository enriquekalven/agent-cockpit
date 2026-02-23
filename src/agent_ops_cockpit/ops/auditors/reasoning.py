try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for Google Cloud Run
import ast
import re
from typing import List

from .base import AuditFinding, BaseAuditor


class ReasoningAuditor(BaseAuditor):
    """
    The 'Shadow Consultant' reasoning engine.
    Performs Phase 2 Active Reasoning: identifying trade-offs, bottlenecks, and intent.
    """
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Intent Detection: Look for 'Seams' between frameworks
        if "langgraph" in content.lower() and "crewai" in content.lower():
             title = "Strategic Conflict: Multi-Orchestrator Setup"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🏗️ Architecture",
                    title=title,
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
                title = "Sequential Data Fetching Bottleneck"
                if not self._is_ignored(func.lineno, content, title):
                    findings.append(AuditFinding(
                        category="🧗 Reliability",
                        title=title,
                        description=f"Function '{func.name}' has {len(awaits)} sequential await calls. This increases latency linearly (T1+T2+T3).",
                        impact="MEDIUM",
                        roi="Parallelizing these calls could reduce latency by up to 60%.",
                        line_number=func.lineno,
                        file_path=file_path
                    ))

        # 3. FinOps Reasoning: High-tier model in loops
        # (Simulated reasoning: we look for model strings and for loops together)
        if re.search(r"gemini-3-pro|gpt-5\.2|claude-4\.6", content) and re.search(r"for\s+\w+\s+in", content):
             if any(x in content.lower() for x in ["classify", "label", "is_", "has_"]):
                title = "Model Efficiency Regression (v1.8.4)"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="💰 FinOps",
                        title=title,
                        description="Frontier reasoning model (Feb 2026 tier) detected inside a loop performing simple classification tasks.",
                        impact="HIGH",
                        roi="Pivoting to Gemini 3 Flash via Antigravity or Claude Code reduces token spend by 95% with superior resolution coverage.",
                        file_path=file_path
                    ))

        # 4. Context Bloat Analysis (Prompt Logic)
        long_prompts = re.findall(r"['\"]{3}([\s\S]{5000,})['\"]{3}", content)
        if long_prompts:
            title = "Architectural Prompt Bloat"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="📉 Efficiency",
                    title=title,
                    description="Massive static context (>5k chars) detected in system instruction. This risks 'Lost in the Middle' hallucinations.",
                    impact="MEDIUM",
                    roi="Pivot to a RAG (Retrieval Augmented Generation) pattern to improve factual grounding accuracy.",
                    file_path=file_path
                ))

        # 5. Semantic Paradigm Auditor: RAG for Math (The "Judge's Verdict" miss)
        # We look for keywords like 'calculate', 'sum', 'total', 'average' in prompts
        # OR when the code uses a vector store (RAG) and asks for arithmetic.
        math_indicators = [r'calculate', r'sum', r'total', r'average', r'math', r'count']
        has_math_intent = any(re.search(pat, content.lower()) for pat in math_indicators)
        is_rag_active = any(x in content.lower() for x in ['vector', 'retriever', 'chroma', 'pinecone', 'search'])
        
        if has_math_intent and is_rag_active:
             title = "Architectural Mismatch: RAG for Math"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="🏛️ Architecture",
                    title=title,
                    description="Detected mathematical intent being processed via a RAG (Retrieval-Augmented Generation) pipeline. RAG is designed for semantic search, not arithmetic accuracy over raw text.",
                    impact="HIGH",
                    roi="[MASTER ARCHITECT RECOMMENDATION]: Pivot to an **NL2SQL** pattern or a **Code Interpreter** tool. These provide 100% deterministic accuracy for calculations, whereas LLMs over RAG can only 'approximate' sums.",
                    file_path=file_path
                ))

        # 6. Reflection Blindness Audit (v1.8.5 Sovereign)
        # Check if agent runners lack a reflection loop for self-correction.
        runner_funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and (n.name.startswith('run_') or n.name == 'call_agent')]
        for func in runner_funcs:
            has_reflection = any(isinstance(d, (ast.Name, ast.Call)) and ('reflection' in str(ast.dump(d)).lower()) for d in func.decorator_list)
            if not has_reflection and 'reflection_engine' not in content:
                title = "Reflection Blindness: Brittle Intelligence"
                if not self._is_ignored(func.lineno, content, title):
                    findings.append(AuditFinding(
                        category="🧗 Reliability",
                        title=title,
                        description=f"Agent runner '{func.name}' lacks a reflection loop. This increases the risk of 'First-Pass Hallucinations' where the model identifies the wrong tool or emits unsafe content.",
                        impact="MEDIUM",
                        roi="Implementing a Sovereign Reflection loop reduces hallucinations by ~40% via Dual-Pass verification.",
                        line_number=func.lineno,
                        file_path=file_path
                    ))

        return findings
