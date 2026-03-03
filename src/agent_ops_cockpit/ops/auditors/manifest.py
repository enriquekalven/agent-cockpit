import os
import re
from typing import List

from .base import AuditFinding, BaseAuditor


class ManifestAuditor(BaseAuditor):
    """
    v2.0 Phase 8: The Librarian.
    Audits Manifest files for SDK drift, protocol compliance, and security risks.
    Aligned with ASI-07: Supply Chain Vulnerabilities.
    """
    def audit(self, tree, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        filename = os.path.basename(file_path)
        
        # 1. SDK Drift & Deprecation (JSON-based)
        if filename in ['package.json', 'pyproject.toml', 'requirements.txt']:
            # Look for frontier models and SDKs that have known vulnerabilities or are legacy
            vulnerability_patterns = [
                (r'langchain[<\s=]*0\.0', "ASI-07: Legacy LangChain version detected. Susceptible to early-stage prompt injection vectors."),
                (r'requests[<\s=]*2\.25', "ASI-07: Vulnerable 'requests' version. High-risk CVE for agent-to-agent SSRF."),
                (r'gpt-3\.5', "FinOps: GPT-3.5-Turbo detected. This model is 'Legacy Intelligence' as of Feb 2026."),
                (r'pickle|yaml\.load', "ASI-03: Insecure Serializer detected in dependencies. Recommend switching to safer alternatives.")
            ]
            for pat, reason in vulnerability_patterns:
                if re.search(pat, content, re.I):
                    findings.append(AuditFinding(
                        category="🛡️ SecOps" if "ASI" in reason else "💰 FinOps",
                        title="ASI-07: Vulnerable Supply Chain" if "ASI" in reason else "Legacy Intelligence SDK",
                        description=f"Detected reference to {pat}. {reason}",
                        impact="HIGH",
                        roi="Closes known CVE vectors and improves reasoning density.",
                        file_path=file_path
                    ))

        # 2. Protocol Health & Hardening (MCP / A2UI)
        if 'mcp' in filename.lower() and filename.endswith('.json'):
            # ASI-04: Tool Over-Privilege Check in MCP
            if '"capabilities"' not in content:
                findings.append(AuditFinding(
                    category="🌍 Sovereignty",
                    title="Malformed MCP Protocol",
                    description="MCP server manifest lacks explicit 'capabilities' block. This risks protocol-level rejection.",
                    impact="HIGH",
                    roi="Mandatory for Agentic Interoperability.",
                    file_path=file_path
                ))
            
            if '"allowExecute": true' in content and '"restricted": true' not in content:
                 findings.append(AuditFinding(
                    category="🛡️ SecOps",
                    title="ASI-04: Ungated MCP Execution",
                    description="Detected MCP server with execution enabled but without a `restricted` sandbox flag.",
                    impact="CRITICAL",
                    roi="Prevents lateral movement via hijacked MCP tools.",
                    file_path=file_path
                ))

        # 3. Hardcoded Provider Bias
        provider_indicators = {
            "azure": ["azure-openai", "semantic-kernel"],
            "aws": ["boto3", "bedrock-agent"],
            "google": ["vertexai", "google-adk"]
        }
        
        if filename in ['package.json', 'pyproject.toml', 'requirements.txt']:
            found_providers = []
            for p, indicators in provider_indicators.items():
                if any(ind in content.lower() for ind in indicators):
                    found_providers.append(p)
            
            if len(found_providers) == 1:
                findings.append(AuditFinding(
                    category="🌍 Sovereignty",
                    title="Monocultural Provider Bias",
                    description=f"Manifest indicates exclusive dependency on '{found_providers[0]}'. This creates high switching costs.",
                    impact="INFO",
                    roi="Enables 'Dynamic Sovereignty' (Multi-Cloud failover).",
                    file_path=file_path
                ))

        return findings
