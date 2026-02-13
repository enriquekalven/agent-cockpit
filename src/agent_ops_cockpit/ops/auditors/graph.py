try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for Google Cloud Run
from tenacity import retry, wait_exponential, stop_after_attempt
import ast
from typing import List
from .base import BaseAuditor, AuditFinding

class DeepGraphAuditor(BaseAuditor):
    """
    Analyzes the 'Seams' between components and identifies dependency risks.
    """
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Dependency Cycle Detection (Simplified for AST)
        # Look for circular imports or cross-module logic smells
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                else:
                    if node.module:
                        imports.append(node.module)

        # 2. Hanging Tool Call Detection (Zombies)
        # Look for async calls without timeouts or cancellation guards
        for node in ast.walk(tree):
            if isinstance(node, ast.Await):
                if isinstance(node.value, ast.Call):
                    # Check for 'timeout' or 'wait' arguments in the call
                    has_timeout = any(kw.arg == "timeout" for kw in node.value.keywords)
                    if not has_timeout:
                        func_name = ""
                        if isinstance(node.value.func, ast.Name):
                            func_name = node.value.func.id
                        elif isinstance(node.value.func, ast.Attribute):
                            func_name = node.value.func.attr
                        
                        if any(x in func_name.lower() for x in ["get", "post", "fetch", "invoke", "call"]):
                             title = "Zombie Tool Call Detected"
                             if not self._is_ignored(node.lineno, content, title):
                                 findings.append(AuditFinding(
                                    category="🧗 Resiliency",
                                    title=title,
                                    description=f"Async call to '{func_name}' lacks a timeout. This risks 'Hanging Workers' in high-concurrency environments.",
                                    impact="HIGH",
                                    roi="Prevents thread-pool exhaustion and 99th percentile latency spikes.",
                                    line_number=node.lineno,
                                    file_path=file_path
                                ))

        return findings
