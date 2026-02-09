import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class FinOpsAuditor(BaseAuditor):
    """
    v1.2 Principal SME: FinOps & Economic Sustainability Auditor.
    Projects TCO and identifies missed caching opportunities for high-volume agents.
    """
    MODEL_PRICES = {
        'gemini-3-pro': 2.5, 
        'gemini-3-flash': 0.1, 
        'gpt-5.2-pro': 8.0, 
        'claude-4.6-opus': 12.0,
        'claude-4.6-sonnet': 3.0
    }

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Model TCO Projection
        for model, price in self.MODEL_PRICES.items():
            if model in content.lower():
                has_loop = re.search(r'for\s+\w+\s+in', content)
                multiplier = 10 if has_loop else 1
                projected_cost = price * multiplier
                findings.append(AuditFinding(
                    category="💰 FinOps",
                    title=f"Inference Cost Projection ({model})",
                    description=f"Detected {model} usage. Projected TCO over 1M tokens: ${projected_cost:.2f}.",
                    impact="INFO",
                    roi=f"Pivot to Gemini 3 Flash via Antigravity/Cursor to reduce projected cost to ${0.10 * multiplier:.2f}."
                ))

        # 2. Context Caching Opportunity
        docstrings = re.findall(r'"""([\s\S]*?)"""|\'\'\'([\s\S]*?)\'\'\'', content)
        has_large_prompt = any(len(d[0] or d[1]) > 500 for d in docstrings)
        if has_large_prompt and 'CachingConfig' not in content:
            findings.append(AuditFinding(
                category="💰 FinOps",
                title="Context Caching Opportunity",
                description="Large static system instructions detected without CachingConfig.",
                impact="HIGH",
                roi="Implement Vertex AI Context Caching via Antigravity to reduce repeated prefix costs by 90%."
            ))

        # Check for retry logic (ROI & Reliability cross-over)
        if 'retry' not in content.lower() and ('request' in content.lower() or 'invoke' in content.lower()):
            print(f"ACTION: {file_path} | Missing Resiliency Pattern | Add @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5)) to handle rate limits efficiently.")

        # Print actions for orchestrator capture
        for f in findings:
             if f.roi:
                  print(f"ACTION: {file_path} | {f.title} | {f.roi}")

        return findings