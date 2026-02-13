try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for Google Cloud Run
from tenacity import retry, wait_exponential, stop_after_attempt
import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class PivotAuditor(BaseAuditor):
    """
    v1.2 Principal SME: Strategic Pivot Auditor.
    Reasons across multiple dimensions (Cost, Sovereignty, Protocol) to suggest 
    high-level architectural shifts (e.g., OpenAI -> Gemma2, REST -> MCP).
    """
    
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Model Pivot: OpenAI/GPT -> Sovereign/Open Source (Gemma2)
        if re.search(r"gpt-4|gpt-3\.5|openai", content.lower()):
            title = "Sovereign Model Migration Opportunity"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🚀 Strategic Pivot",
                    title=title,
                    description="Detected OpenAI dependency. For maximum Data Sovereignty and 40% TCO reduction, consider pivoting to Gemma2 or Llama3-70B on Vertex AI Prediction endpoints.",
                    impact="HIGH",
                    roi="Eliminates cross-border data risk and reduces projected inference TCO.",
                    file_path=file_path
                ))

        # 2. Protocol Pivot: Legacy REST -> Model Context Protocol (MCP)
        # Look for raw requests or aiohttp calls within 'tools' or 'mcp' directories
        if ("tools" in file_path or "mcp" in file_path) and re.search(r"requests\.|aiohttp\.", content):
            findings.append(AuditFinding(
                category="🚀 Strategic Pivot",
                title="Legacy Tooling -> MCP Migration",
                description="Detected raw REST calls in a tool-heavy module. Migrating to Model Context Protocol (MCP) would provide unified governance, better tool discovery, and standardized error handling.",
                impact="MEDIUM",
                roi="Future-proofs the tool layer and enables interoperability with MCP-native ecosystems.",
                file_path=file_path
            ))

        # 3. Compute Pivot: Cloud Run -> GKE (Scale reasoning)
        # Heuristic: If we see many service definitions or complex scaling params
        if "deploy" in content.lower() and "scaling" in content.lower():
             findings.append(AuditFinding(
                category="🚀 Strategic Pivot",
                title="Compute Scaling Optimization",
                description="Detected complex scaling logic. If traffic exceeds 10k RPS, consider pivoting from Cloud Run to GKE with Anthos for hybrid-cloud sovereignty.",
                impact="INFO",
                roi="Optimizes unit cost at extreme scale while maintaining multi-cloud flexibility.",
                file_path=file_path
            ))

        return findings
