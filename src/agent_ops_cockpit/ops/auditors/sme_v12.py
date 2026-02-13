try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for Google Cloud Run
import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class HITLAuditor(BaseAuditor):
    """
    v1.2 Principal SME: Human-in-the-Loop (HITL) Policy Auditor.
    Flags high-risk "write" permissions that lack explicit approval gates.
    """
    SENSITIVE_ACTIONS = [
        (r"(?i)transfer", "Financial Transfer"),
        (r"(?i)delete", "Resource Deletion"),
        (r"(?i)update_policy", "Policy Modification"),
        (r"(?i)send_email", "External Communication"),
        (r"(?i)purchase", "Procurement")
    ]

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        for node in ast.walk(tree):
            # Check function definitions for sensitive names
            if isinstance(node, ast.FunctionDef):
                for pattern, category in self.SENSITIVE_ACTIONS:
                    if re.search(pattern, node.name):
                        # Look for 'human_approval' or 'require_approval' in arguments or decorator
                        has_gate = any(arg.arg in ["human_approval", "require_approval", "gate"] for arg in node.args.args)
                        
                        # Also check decorators
                        if not has_gate:
                            for decorator in node.decorator_list:
                                if isinstance(decorator, ast.Name) and "gate" in decorator.id.lower():
                                    has_gate = True
                                elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and "gate" in decorator.func.id.lower():
                                    has_gate = True

                        if not has_gate:
                            title = f"Ungated {category} Action"
                            if not self._is_ignored(node.lineno, content, title):
                                findings.append(AuditFinding(
                                    category="🛡️ HITL Guardrail",
                                    title=title,
                                    description=f"Function '{node.name}' performs a high-risk action but lacks a 'human_approval' flag or security gate.",
                                    impact="CRITICAL",
                                    roi="Prevents autonomous catastrophic failures and unauthorized financial moves.",
                                    line_number=node.lineno,
                                    file_path=file_path
                                ))

        return findings

class A2AAuditor(BaseAuditor):
    """
    v1.2 Principal SME: Agent-to-Agent (A2A) Efficiency Auditor.
    Detects "Chatter Bloat" where agents pass excessive state objects.
    """
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # Look for patterns like passing 'state' or 'full_context' in a2a calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Heuristic: passing a variable named 'state', 'context', or 'message_log'
                for arg in node.args:
                    if isinstance(arg, ast.Name) and arg.id in ["state", "full_context", "messages", "history"]:
                        # Detection of "Chatter Bloat"
                        title = "A2A Chatter Bloat Detected"
                        if not self._is_ignored(node.lineno, content, title):
                            findings.append(AuditFinding(
                                category="📉 A2A Efficiency",
                                title=title,
                                description=f"Passing entire variable '{arg.id}' to tool/agent call. This introduces high latency and token waste.",
                                impact="MEDIUM",
                                roi="Reduces token cost and latency by 30-50% through surgical state passing.",
                                line_number=node.lineno,
                                file_path=file_path
                            ))

        return findings
