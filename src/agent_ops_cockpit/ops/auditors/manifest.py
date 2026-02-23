import os
import re
from typing import List

from .base import AuditFinding, BaseAuditor


class ManifestAuditor(BaseAuditor):
    """
    v2.0 Phase 8: The Librarian.
    Audits Manifest files (package.json, pyproject.toml, mcp-config.json) 
    for SDK drift, protocol compliance, and security risks.
    """
    def audit(self, tree, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        filename = os.path.basename(file_path)
        
        # 1. SDK Drift & Deprecation (JSON-based)
        if filename == 'package.json' or filename == 'pyproject.toml':
            # Look for frontier models that have been superseded
            deprecated_patterns = [
                (r'gpt-3\.5', "GPT-3.5-Turbo detected. This model is 'Legacy Intelligence' as of Feb 2026."),
                (r'claude-2', "Anthropic Claude 2 detected. Recommend upgrading to Claude 4.5+ for superior reasoning density."),
                (r'gemini-1\.0', "Early Gemini 1.0 detected. Upgrade to Gemini 3 Flash for 10x ROI improvement.")
            ]
            for pat, reason in deprecated_patterns:
                if re.search(pat, content, re.I):
                    findings.append(AuditFinding(
                        category="💰 FinOps",
                        title="Legacy Intelligence SDK",
                        description=f"Detected reference to {pat}. {reason}",
                        impact="MEDIUM",
                        roi="Reduces token waste and improves 'First-Pass' accuracy.",
                        file_path=file_path
                    ))

        # 2. Protocol Health (MCP / A2UI)
        if 'mcp' in filename.lower() and filename.endswith('.json'):
            if '"capabilities"' not in content:
                findings.append(AuditFinding(
                    category="🌍 Sovereignty",
                    title="Malformed MCP Protocol",
                    description="MCP server manifest lacks explicit 'capabilities' block. This risks protocol-level rejection by host clients (like Claude Code or Cockpit).",
                    impact="HIGH",
                    roi="Mandatory for Agentic Interoperability.",
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
                    description=f"Manifest indicates exclusive dependency on '{found_providers[0]}'. This is a 'Strategic Blindness' pattern that creates high switching costs.",
                    impact="INFO",
                    roi="Abstracting model calls via Antigravity or LiteLLM enables 'Dynamic Sovereignty' (Multi-Cloud failover).",
                    file_path=file_path
                ))

        return findings
