try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v2.0.7 cockpit Alignment: Optimized for Google Cloud Run
import ast
import re
from typing import List

from .base import AuditFinding, BaseAuditor


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

        for p1, _v1_min, p2, _v2_min, reason in self.KNOW_CONFLICTS:
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

        # Unpinned Dependency Check
        if file_path.endswith("requirements.txt"):
            for line in content.splitlines():
                if line and not line.startswith("#") and "==" not in line and ">=" not in line and "<=" not in line:
                    title = "Unpinned Dependency Trap"
                    if not self._is_ignored(0, content, title):
                        findings.append(AuditFinding(
                            category="📦 Dependency",
                            title=title,
                            description="Detected unpinned dependency in requirements.txt. [bold red]Risk:[/] Agents are highly sensitive to SDK drift.",
                            impact="MEDIUM",
                            roi="Ensures deterministic environment builds.",
                            file_path=file_path
                        ))
                        break
        elif file_path.endswith("pyproject.toml"):
            # Detect unpinned version strings or missing version specifiers in the list
            if '"*"' in content or "'*'" in content:
                 title = "Unpinned Dependency Trap"
                 if not self._is_ignored(0, content, title):
                     findings.append(AuditFinding(
                        category="📦 Dependency",
                        title=title,
                        description="Detected unpinned dependency (*) in pyproject.toml.",
                        impact="MEDIUM",
                        roi="Prevents 'Manifest Drift' and unexpected runtime failures.",
                        file_path=file_path
                    ))
            
            # Check for naked package names in dependencies list
            dep_section = re.search(r"dependencies\s*=\s*\[(.*?)\]", content, re.DOTALL)
            if dep_section:
                dep_list = dep_section.group(1)
                for dep in re.findall(r"['\"]([^'\"]+)['\"]", dep_list):
                    if not any(op in dep for op in [">=", "<=", "==", "~=", ">", "<"]):
                        title = "Unpinned Dependency Trap"
                        if not self._is_ignored(0, content, title):
                            findings.append(AuditFinding(
                                category="📦 Dependency",
                                title=title,
                                description=f"Detected naked dependency '{dep}' without version constraints. [bold red]Risk:[/] Agents are brittle to SDK major/minor updates.",
                                impact="MEDIUM",
                                roi="Ensures deterministic environment builds.",
                                file_path=file_path
                            ))
                            break

        return findings
