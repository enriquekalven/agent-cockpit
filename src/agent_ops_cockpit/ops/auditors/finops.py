from tenacity import retry, wait_exponential, stop_after_attempt
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
        'gemini-1.5-pro': 3.5, 
        'gemini-1.5-flash': 0.35, 
        'gpt-4': 10.0, 
        'gpt-3.5': 0.5
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
                    roi=f"Switching to Flash-equivalent could reduce projected cost to ${0.35 * multiplier:.2f}."
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
                roi="Implement Vertex AI Context Caching to reduce repeated prefix costs by 90%."
            ))

        # Check for retry logic (ROI & Reliability cross-over)
        if 'retry' not in content.lower() and ('request' in content.lower() or 'invoke' in content.lower()):
            print(f"ACTION: {file_path} | Missing Resiliency Pattern | Add @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5)) to handle rate limits efficiently.")

        # Print actions for orchestrator capture
        for f in findings:
             if f.roi:
                  print(f"ACTION: {file_path} | {f.title} | {f.roi}")

        return findings