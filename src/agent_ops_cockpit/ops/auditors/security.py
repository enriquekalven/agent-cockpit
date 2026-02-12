try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.4.5 Sovereign Alignment: Optimized for Google Cloud Run
from tenacity import retry, wait_exponential, stop_after_attempt
import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class SecurityAuditor(BaseAuditor):
    """
    Reasoning-based Security Auditor.
    Scans for 'Seams' where unsanitized user input flows into LLM calls or Tool execution.
    """
    @retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # Track variables that might contain raw user input
        input_vars = set(["prompt", "user_input", "query", "request"])
        sanitized_vars = set()
        
        for node in ast.walk(tree):
            # Track sanitization calls
            if isinstance(node, ast.Assign):
                if isinstance(node.value, ast.Call):
                    # If we call a scrubber, mark the target as sanitized
                    func_name = ""
                    if isinstance(node.value.func, ast.Name):
                        func_name = node.value.func.id
                    elif isinstance(node.value.func, ast.Attribute):
                        func_name = node.value.func.attr
                    
                    if any(x in func_name.lower() for x in ["scrub", "mask", "sanitize", "guard", "filter"]):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                sanitized_vars.add(target.id)
            
            # Detect LLM invocations with unsanitized inputs
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                if any(x in func_name.lower() for x in ["invoke", "generate", "call", "chat", "predict"]):
                    # Check arguments
                    for arg in node.args:
                        if isinstance(arg, ast.Name) and (arg.id in input_vars) and (arg.id not in sanitized_vars):
                            title = "Prompt Injection Susceptibility"
                            if not self._is_ignored(node.lineno, content, title):
                                findings.append(AuditFinding(
                                    category="🛡️ Security",
                                    title=title,
                                    description=f"The variable '{arg.id}' flows into an LLM call without detected sanitization logic (e.g., scrub/guard).",
                                    impact="CRITICAL",
                                    roi="Prevents prompt injection attacks by 99%.",
                                    line_number=node.lineno,
                                    file_path=file_path
                                ))

        # Secret Scanning (v1.1)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if any(x in target.id.lower() for x in ["key", "token", "secret", "password", "auth"]):
                            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                                val = node.value.value
                                if len(val) > 16 and re.search(r"\d", val) and re.search(r"[a-zA-Z]", val):
                                    title = "Hardcoded Secret Detected"
                                    if not self._is_ignored(node.lineno, content, title):
                                        findings.append(AuditFinding(
                                            category="🛡️ Security",
                                            title=title,
                                            description=f"Variable '{target.id}' appears to contain a hardcoded credential.",
                                            impact="CRITICAL",
                                            roi="Prevent catastrophic credential leaks by using Google Secret Manager.",
                                            line_number=node.lineno,
                                            file_path=file_path
                                        ))

        # Look for TODOs in comments
        if "// todo" in content.lower() or "# todo" in content.lower():
            if "mask" in content.lower() or "pii" in content.lower():
                 title = "Incomplete PII Protection"
                 if not self._is_ignored(0, content, title):
                     findings.append(AuditFinding(
                        category="🛡️ Security",
                        title=title,
                        description="Source code contains 'TODO' comments related to PII masking. Active protection is currently absent.",
                        impact="HIGH",
                        roi="Closes compliance gap for GDPR/SOC2.",
                        file_path=file_path
                    ))

        return findings
