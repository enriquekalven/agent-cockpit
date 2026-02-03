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
        
        # Check for Audit Logging (SOC2 CC6.1 - Access Monitoring)
        if "log" not in content.lower():
            findings.append(AuditFinding(
                category="⚖️ Compliance",
                title="SOC2 Control Gap: Missing Transit Logging",
                description="No logging detected in mission-critical file. SOC2 CC6.1 requires audit trails for all system access.",
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
