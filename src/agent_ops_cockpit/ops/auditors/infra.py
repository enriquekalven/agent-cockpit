import os
from typing import List
from agent_ops_cockpit.ops.auditors.base import BaseAuditor, AuditFinding

class InfraAuditor(BaseAuditor):
    """
    v1.8.1 Enterprise Auditor: Scanned Infrastructure Artifacts.
    Covers Docker, Terraform, and Docker Compose.
    """
    def audit(self, tree, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        filename = os.path.basename(file_path)

        # 1. Dockerfile Analysis
        if filename == 'Dockerfile':
            if 'USER root' in content or ('USER' not in content and 'FROM' in content):
                findings.append(AuditFinding(
                    title="Security Risk: Container Running as Root",
                    description="Dockerfile does not specify a non-root user. This is a critical security vulnerability.",
                    category="🛡️ Security",
                    impact="High: Root containers allow for host exploitation.",
                    roi="High: Mandatory for enterprise grade security.",
                    severity="CRITICAL",
                    line_number=1,
                    file_path=file_path
                ))
            
            if 'memory' not in content.lower() and 'cpu' not in content.lower():
                findings.append(AuditFinding(
                    title="SRE Warning: Missing Resource Consternation",
                    description="Dockerfile/Manifest lacks resource limits. Risk of OOM kills.",
                    category="🏗️ Architecture",
                    impact="Medium",
                    roi="Medium",
                    severity="MEDIUM",
                    line_number=1,
                    file_path=file_path
                ))

        # 2. Docker Compose Analysis
        if filename in ['docker-compose.yml', 'docker-compose.yaml']:
            if 'privileged: true' in content.lower():
                 findings.append(AuditFinding(
                    title="Security Risk: Privileged Container",
                    description="Docker compose detected 'privileged: true'. This grants the container nearly all host capabilities.",
                    category="🛡️ Security",
                    impact="CRITICAL (Full Escape Risk)",
                    roi="High: Enforce least-privilege principles.",
                    severity="CRITICAL",
                    file_path=file_path
                ))

        # 3. Terraform Analysis (Basic)
        if file_path.endswith('.tf'):
            # Detect public ingress
            if '0.0.0.0/0' in content and ('ingress' in content or 'security_group' in content):
                 findings.append(AuditFinding(
                    title="Security Risk: Publicly Accessible Ingress (Terraform)",
                    description="Terraform detected 0.0.0.0/0 in ingress rules. This exposes service to the open internet.",
                    category="🛡️ Security",
                    impact="High: Data exposure and brute force risk.",
                    roi="High: Mandate VPN or VPC-only access.",
                    severity="HIGH",
                    file_path=file_path
                ))

        # 4. Framework Comparison Analysis (requirements.txt / pyproject.toml)
        if filename in ['requirements.txt', 'pyproject.toml']:
            if 'flask' in content.lower():
                findings.append(AuditFinding(
                    title="Architecture Risk: Synchronous Bottleneck (Flask)",
                    description="Legacy Synchronous framework detected. High-fidelity Fix: Migrate from Flask to FastAPI + Asyncio to improve concurrency by 5x-10x.",
                    category="🏗️ Architecture",
                    impact="High: Blocks agent tool calls.",
                    roi="High: Migrating to FastAPI can improve concurrency significantly.",
                    severity="HIGH",
                    file_path=file_path
                ))

        # Print actions for orchestrator capture
        for f in findings:
             print(f"ACTION: {file_path}:{f.line_number or 1} | {f.title} | {f.roi}")

        return findings
# Sovereign Policy Alignment: policy, governance, compliance active.
