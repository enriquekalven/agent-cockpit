"""
Pillar: Economic Sustainability
SME Persona: Distinguished FinOps Fellow
Objective: Project TCO and identify caching/efficiency opportunities in agentic flows.
Taxonomy: Sovereign FinOps (v1.8.4)
"""
try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

import ast
import re
from typing import List, Dict
from .base import BaseAuditor, AuditFinding

class FinOpsAuditor(BaseAuditor):
    """
    Analyzes model pricing, inference loops, and token utilization to provide ROI-based pivots.
    Focuses on 'Architectural Waste' and 'Inference Over-Privilege'.
    """
    
    # v1.8.5 Pricing Index (Sovereign Rates - Feb 2026)
    MODEL_PRICES: Dict[str, float] = {
        'gemini-2.0-pro': 1.25, 
        'gemini-3-pro': 1.25, 
        'gemini-2.0-flash': 0.1, 
        'gemini-2.0-flash-lite': 0.05,
        'gpt-5': 10.0,
        'gpt-4o': 5.0, 
        'gpt-4o-mini': 0.15,
        'claude-3-5-sonnet': 3.0,
        'claude-3-5-haiku': 0.25
    }

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        content_lower = content.lower()
        
        # 1. Inference Loop Detection & TCO Projection (Efficiency Pillar)
        # Uses AST to find LLM calls inside for/while loops
        has_inference_loop = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                loop_code = ast.unparse(node).lower()
                if any(kw in loop_code for kw in ['invoke', 'generate', 'predict', 'query', 'llm(']):
                    has_inference_loop = True
                    
                    # TCO Calculation for Loop
                    model_match = re.search(r"['\"](.*?-pro.*?)['\"]", content_lower)
                    model_name = model_match.group(1) if model_match else "generic"
                    base_price = self.MODEL_PRICES.get(model_name, 1.25)
                    projected_tco = base_price * 10 * 2 # 10 iterations * multiplier
                    
                    findings.append(AuditFinding(
                        category="💰 FinOps",
                        title="Economic Risk: Inference Loop Detected",
                        description=f"""Detected LLM reasoning calls inside a standard Python loop.
[bold red]Strategic Waste:[/bold red] Linear loops scale token costs indefinitely. 
[bold yellow]LOOP DETECTED:[/bold yellow] Projected TCO: ${projected_tco:.2f} (Aggressive multiplier).
[bold green]RECOMMENDATION:[/bold green] Pivot to **Batch Inference** or a **Map-Reduce** pattern.""",
                        impact="HIGH (Cost)",
                        roi="Reduces per-token overhead by up to 50% via batch discounts.",
                        line_number=node.lineno,
                        file_path=file_path
                    ))
                    break
        
        if not has_inference_loop:
            # Check for high-cost single calls
            model_match = re.search(r"['\"](.*?-pro.*?)['\"]", content_lower)
            if model_match:
                model_name = model_match.group(1)
                base_price = self.MODEL_PRICES.get(model_name, 1.25)
                projected_tco = base_price * 2
                findings.append(AuditFinding(
                    category="💰 FinOps",
                    title="Economic Review: High-Cost Inference",
                    description=f"""Detected single call to a high-tier model.
[bold blue]SINGLE PASS:[/bold blue] Projected TCO: ${projected_tco:.2f}.
[bold green]RECOMMENDATION:[/bold green] Ensure this call cannot be mothballed or tiered down.""",
                    impact="LOW",
                    roi="Maintains visibility into per-turn unit economics.",
                    file_path=file_path
                ))

        # 2. Context Caching Opportunity (Prefix Pillar)
        # Check for large prompt strings (> 2000 chars) without caching config
        docstrings = re.findall(r'"""([\s\S]*?)"""|\'\'\'([\s\S]*?)\'\'\'', content)
        large_prompts = [d for d in docstrings if len(d[0] or d[1]) > 2000]
        if large_prompts and 'ContextCacheConfig' not in content:
            findings.append(AuditFinding(
                category="💰 FinOps",
                title="Economic Opportunity: Missing Context Caching",
                description="""Detected large instructions or few-shot examples (>2k tokens) without Context Caching.
[bold blue]Sovereign Cache (v1.8.5):[/bold blue] Re-sending the same prefix on every turn for long-lived agent sessions is 'Architectural Waste'.
[bold green]RECOMMENDATION:[/bold green] Implement **Vertex AI Context Caching** or **Sovereign Sliding Memory**.""",
                impact="HIGH",
                roi="Reduces repeated prefix costs by up to 90% and decreases TTFT by 40%.",
                file_path=file_path
            ))

        # 3. Model Over-Privilege (Tiering Pillar)
        high_tier_models = ['gpt-4o', 'pro', 'opus', 'sonnet']
        if any(m in content_lower for m in high_tier_models):
            # Check if task seems deterministic (regex/parsing/formatting)
            if any(kw in content_lower for kw in ['regex', 'parse', 'clean', 'format']):
                findings.append(AuditFinding(
                    category="💰 FinOps",
                    title="Economic Inefficiency: Model Over-Privilege",
                    description="""Using a High-Tier model (e.g., GPT-4o/Pro) for deterministic ETL or parsing tasks.
[bold yellow]Strategic Move:[/bold yellow] This task can be handled by a 'Flash' or 'Mini' tier model at 1/10th the cost.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Gemini 2.0 Flash** or **GPT-4o-mini** for metadata tasks.""",
                    impact="MEDIUM",
                    roi="Immediate 90%+ reduction in inference billing.",
                    file_path=file_path
                ))

        # 4. Naive Retry Burn (Resiliency Pillar)
        if 'retry' in content_lower and 'wait_fixed' in content_lower:
             findings.append(AuditFinding(
                category="💰 FinOps",
                title="Token Burn: Non-Exponential Retry",
                description="""Detected fixed-interval retries for LLM calls.
[bold red]Structural Friction:[/bold red] Naive retries during rate-limits burn tokens and budget without recovery.
[bold green]RECOMMENDATION:[/bold green] Pivot to **Exponential Backoff** with jitter via `tenacity`.""",
                impact="MEDIUM",
                roi="Protects budget during upstream service disruptions.",
                file_path=file_path
            ))

        # 5. Retrieval Overhead (RAG FinOps)
        if 'retrieve' in content_lower and ('top_k=100' in content_lower or 'limit=100' in content_lower):
             findings.append(AuditFinding(
                category="💰 FinOps",
                title="Economic Waste: Massive Retrieval K-Index",
                description="""Detected extremely high retrieval limits (K > 20) being fed into context.
[bold blue]Strategic Bloat:[/bold blue] Too much context leads to 'Lost in the Middle' reasoning and high token costs.
[bold green]RECOMMENDATION:[/bold green] Implement **Reranking (FlashRank)** and reduce initial retrieval limits to K <= 5.""",
                impact="MEDIUM",
                roi="Optimizes context window spending and improves reasoning precision.",
                file_path=file_path
            ))

        return findings