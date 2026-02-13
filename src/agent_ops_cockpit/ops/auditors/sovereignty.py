try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import ast
import re
from typing import List
from .base import BaseAuditor, AuditFinding

class SovereigntyAuditor(BaseAuditor):
    """
    v1.1 Phase 6: The Sovereign. 
    Audits for Multi-Cloud Portability and Data Residency (GDPR/EU Sovereign).
    Detects Vendor Lock-in (Hardcoded Provider Specifics).
    """
    VULNERABLE_PATTERNS = [
        (r"project[-_]id\s*=\s*['\"][\w-]+['\"]", "Hardcoded GCP Project ID. Use environment variables for portability."),
        (r"region\s*=\s*['\"]us-[\w-]+['\"]", "Hardcoded US Region. Risk to EU Data Sovereignty if not configured per environment."),
        (r"aws_[\w-]+\s*=\s*['\"]", "AWS-specific credential detected. Ensure abstraction layer for Multi-Cloud."),
        (r"azure_[\w-]+\s*=\s*['\"]", "Azure-specific endpoint detected. Risk of vendor lock-in.")
    ]

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []

        # 1. Vendor Lock-in Check (Hardcoded IDs/Regions)
        for pattern, reason in self.VULNERABLE_PATTERNS:
            matches = re.finditer(pattern, content)
            for match in matches:
                # Find the line number based on char offset
                line_no = content.count('\n', 0, match.start()) + 1
                title = "Vendor Lock-in Risk"
                if not self._is_ignored(line_no, content, title):
                    findings.append(AuditFinding(
                        category="🌍 Sovereignty",
                        title=title,
                        description=reason,
                        impact="MEDIUM",
                        roi="Enables Multi-Cloud failover and EU sovereignty compliance.",
                        line_number=line_no,
                        file_path=file_path
                    ))

        # 2. Data Residency Audit (Sovereign Cloud patterns)
        if "google.cloud" in content and "europe-" not in content.lower():
            if "gdpr" in content.lower() or "compliance" in content.lower():
                title = "EU Data Sovereignty Gap"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🌍 Sovereignty",
                        title=title,
                        description="Compliance code detected but no European region routing found. Risk of non-compliance with EU data residency laws.",
                        impact="HIGH",
                        roi="Prevents multi-million Euro GDPR fines.",
                        file_path=file_path
                    ))

        # 3. Cloud Agnostic Interface Audit
        direct_sdks = ["vertexai", "boto3", "azure-identity"]
        for sdk in direct_sdks:
            if f"import {sdk}" in content or f"from {sdk}" in content:
                title = "Direct Vendor SDK Exposure"
                if not self._is_ignored(0, content, title):
                    findings.append(AuditFinding(
                        category="🌍 Sovereignty",
                        title=title,
                        description=f"Directly importing '{sdk}'. Consider wrapping in a provider-agnostic bridge to allow Multi-Cloud mobility.",
                        impact="LOW",
                        roi="Reduces refactoring cost during platform migration.",
                        file_path=file_path
                    ))

        # 4. v1.3 Strategic Exit: TCO & Migration Plan
        if any(x in content.lower() for x in ["vertexai", "google.cloud"]):
            title = "Strategic Exit Plan (Cloud)"
            if not self._is_ignored(0, content, title):
                findings.append(AuditFinding(
                    category="🌍 Sovereignty",
                    title=title,
                    description="Detected hardcoded cloud dependencies. For a 'Category Killer' grade, implement an abstraction layer that allows switching to Gemma 2 on GKE.",
                    impact="INFO",
                    roi="Estimated 12% OpEx reduction via open-source pivot orchestrated by Antigravity. Exit effort: ~14 lines of code.",
                    file_path=file_path
                ))

        return findings
