import ast
from typing import List
from .base import BaseAuditor, AuditFinding

class ComplianceAuditor(BaseAuditor):
    """
    v1.1 Enterprise Architect: Governance & Compliance Auditor.
    Maps code flaws to specific audit controls (SOC2, HIPAA, NIST).
    """
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Check for Structural Audit Logging (SOC2 CC6.1)
        # Scan for 'import logging' or usage of 'logger' objects
        has_logging = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if any(alias.name == 'logging' for alias in node.names) or getattr(node, 'module', '') == 'logging':
                    has_logging = True
                    break
            if isinstance(node, ast.Attribute) and node.attr in ['info', 'warning', 'error', 'debug', 'log']:
                has_logging = True
                break

        if not has_logging and "log" not in content.lower():
            findings.append(AuditFinding(
                category="⚖️ Compliance",
                title="SOC2 Control Gap: Missing Transit Logging",
                description="Structural logging (logger.info/error) not detected. SOC2 CC6.1 requires audit trails for all system access.",
                impact="HIGH",
                roi="Critical for passing external audits and root-cause analysis.",
                file_path=file_path
            ))

        # Check for HIPAA (Encryption at Rest - Simplified)
        if "sql" in content.lower() or "db" in content.lower():
            if "encrypt" not in content.lower() and "secret" not in content.lower():
                findings.append(AuditFinding(
                    category="⚖️ Compliance",
                    title="HIPAA Risk: Potential Unencrypted ePHI",
                    description="Database interaction detected without explicit encryption or secret management headers.",
                    impact="CRITICAL",
                    roi="Avoid legal penalties by enforcing encryption headers in database client configuration."
                ))

        return findings
