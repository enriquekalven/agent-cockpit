try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

import ast
import re
from typing import List, Optional
from .base import BaseAuditor, AuditFinding

class ParadigmAuditor(BaseAuditor):
    """
    SME Persona: Principal Semantic Architect
    Objective: Detect 'Strategic Paradigm Mismatches' (e.g., RAG for Math, Prompt-Stuffed Structured Data).
    """

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        content_lower = content.lower()

        # 1. Pattern: Structured Data (CSV/JSON) + Analytics Task in Prompt
        structured_indicators = ['csv.reader', 'pd.read_csv', 'json.load', 'open(', '.read()']
        math_indicators = ['sum', 'count', 'average', 'calculate', 'total', 'math', 'arithmetic']
        prompt_indicators = ['prompt =', 'f"', 'f\'', 'template', 'render(']

        has_structured = any(ind in content for ind in structured_indicators)
        has_math_intent = any(ind in content_lower for ind in math_indicators)
        has_prompt = any(ind in content_lower for ind in prompt_indicators)

        if has_structured and has_math_intent and has_prompt:
             findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Pattern Mismatch: Structured Data Math via Prompt",
                description="""Detected arithmetic intent over raw file content (CSV/JSON) stuffed into a prompt. 
[bold red]Structural Blindspot:[/bold red] LLMs are unreliable for math over long unstructured text.
[bold green]RECOMMENDATION:[/bold green] Pivot to **NL2SQL** or a **Code Interpreter** (e.g., Vertex AI Extensions / Python Sandbox). 
Efficiency: Reduces latency by ~70% and increases precision to 99%.""",
                impact="HIGH (Accuracy & Cost)",
                roi="Critical for financial or analytical agents.",
                file_path=file_path
            ))

        # 2. Pattern: Flattened RAG for Fact-Heavy Data
        if 'openai' in content_lower or 'anthropic' in content_lower or 'vertexai' in content_lower:
            if 'search' in content_lower and 'context' in content_lower and ('.txt' in content_lower or '.pdf' in content_lower):
                if 'database' not in content_lower and 'sql' not in content_lower:
                     findings.append(AuditFinding(
                        category="🚀 Strategic Paradigm",
                        title="Low-Fidelity RAG (Context Stuffing)",
                        description="""Detected "Flattened Prompt RAG" where unstructured files are read into context for fact-retrieval.
[bold yellow]Paradigm Shift:[/bold yellow] For large datasets, linear context stuffing scales poorly ($$$).
[bold green]RECOMMENDATION:[/bold green] Pivot to **Vector DB (Pinecone/Chroma)** or a **Semantic Layer**.
Efficiency: Enables sub-second retrieval over TBs of data.""",
                        impact="MEDIUM",
                        roi="Reduces token burn and reasoning drift.",
                        file_path=file_path
                    ))

        # 3. Pattern: Manual State Machine (The "Loop of Doom")
        # Look for LLM calls inside for/while loops without a framework
        is_loop_llm = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                loop_content = ast.unparse(node)
                if any(kw in loop_content.lower() for kw in ['completion', 'generate_content', 'chat_completion']):
                    is_loop_llm = True
                    break
        
        if is_loop_llm and 'langgraph' not in content_lower and 'semantic_kernel' not in content_lower:
            findings.append(AuditFinding(
                category="🚀 Strategic Paradigm",
                title="Manual State Machine Detected",
                description="""LLM reasoning calls detected inside standard Python loops. This often leads to "Reasoning Collapse."
[bold purple]Architecture Suggestion:[/bold purple] Pivot to **State Machines (LangGraph)** for reliable multi-turn logic.
Benefit: Provides standard checkpoints, error handling, and cyclic reasoning loops.""",
                impact="HIGH (Reliability)",
                roi="Ensures deterministic agent behavior in complex tasks.",
                file_path=file_path
            ))

        # Print actions for orchestrator capture
        for f in findings:
             print(f"ACTION: {file_path}:{f.line_number or 1} | {f.title} | {f.roi}")

        return findings
