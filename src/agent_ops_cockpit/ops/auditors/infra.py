import os
import re
from typing import List, Optional
from agent_ops_cockpit.ops.auditors.base import BaseAuditor, Finding

class InfraAuditor(BaseAuditor):
    """
    v1.8.0 Enterprise Auditor: Scans Infrastructure Artifacts (Dockerfile, requirements.txt, etc).
    """
    def audit(self, tree, content: str, file_path: str) -> List[Finding]:
        findings = []
        filename = os.path.basename(file_path)

        if filename == 'Dockerfile':
            # Check for Root User
            if 'USER root' in content or ('USER' not in content and 'FROM' in content):
                findings.append(Finding(
                    title="Security Risk: Container Running as Root",
                    description="Dockerfile does not specify a non-root user. This is a critical security vulnerability in production environments (AWS ECS, Google Cloud Run).",
                    category="🛡️ Security",
                    impact="High: Root containers can lead to host-level exploitation.",
                    roi="High: Prevents deployment blocks in regulated industries.",
                    severity="CRITICAL",
                    line_number=1,
                    file_path=file_path
                ))
            
            # Check for Resource Limits (Missing Indicators)
            if 'memory' not in content.lower() and 'cpu' not in content.lower():
                findings.append(Finding(
                    title="SRE Warning: Missing Resource Consternation",
                    description="Dockerfile/Manifest lacks hints for CPU/Memory limits. This can lead to 'Noisy Neighbor' effects and unpredictable scaling latency.",
                    category="🏗️ Architecture",
                    impact="Medium: Risk of OOM kills or resource starvation.",
                    roi="Medium: Improves fleet stability and multi-agent density.",
                    severity="MEDIUM",
                    line_number=1,
                    file_path=file_path
                ))

        if filename in ['requirements.txt', 'pyproject.toml']:
            # Framework Bottleneck Check
            if 'flask' in content.lower():
                findings.append(Finding(
                    title="Architecture Risk: Synchronous Bottleneck (Flask)",
                    description="Legacy Synchronous framework detected. Agents with high I/O tool-use (Vertex AI, Search) will suffer from head-of-line blocking.",
                    category="🏗️ Architecture",
                    impact="High: One slow tool call blocks the entire agent thread.",
                    roi="High: Migrating to FastAPI can improve concurrency by 5x-10x.",
                    severity="HIGH",
                    line_number=1,
                    file_path=file_path
                ))

        return findings
