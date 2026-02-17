try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for Google Cloud Run
import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class DependencyAuditor(BaseAuditor):
    """
    v1.1 Enterprise Architect: Dependency Fragility Auditor.
    Scans pyproject.toml and requirements.txt for version drift and known conflicts.
    """
    KNOW_CONFLICTS = [
        ("langchain", "0.1.0", "crewai", "0.30.0", "Breaking change in BaseCallbackHandler. Expect runtime crashes during tool execution.")
    ]

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # Only check dependencies once per audit root (if we detect we are in the root)
        if not file_path.endswith(("pyproject.toml", "requirements.txt")):
            return []

        # Simple regex for dependency parsing (v1.1)
        deps = re.findall(r"(['\"]?\w+['\"]?)\s*[>=<]{1,2}\s*([\d\.]*)", content)
        dep_map = {name.strip("'\""): version for name, version in deps}

        for p1, v1_min, p2, v2_min, reason in self.KNOW_CONFLICTS:
            if p1 in dep_map and p2 in dep_map:
                title = "Version Drift Conflict Detected"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="📦 Dependency",
                        title=title,
                        description=f"Detected potential conflict between {p1} and {p2}. {reason}",
                        impact="HIGH",
                        roi="Prevent runtime failures and dependency hell before deployment.",
                        file_path=file_path
                    ))

        # Licensing Check
        if "agpl" in content.lower():
             title = "Restrictive License Warning"
             if not self._is_ignored(0, content, title):
                 findings.append(AuditFinding(
                    category="⚖️ Compliance",
                    title=title,
                    description="AGPL-licensed dependency found. This may require full source disclosure for the entire project.",
                    impact="MEDIUM",
                    roi="Avoid legal risk by switching to MIT/Apache alternatives."
                ))

        return findings
