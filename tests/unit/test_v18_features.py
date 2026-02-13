import os
import ast
import pytest
from agent_ops_cockpit.ops.discovery import DiscoveryEngine
from agent_ops_cockpit.ops.auditors.infra import InfraAuditor
from agent_ops_cockpit.ops.auditors.pivot import PivotAuditor
from agent_ops_cockpit.ops.secret_scanner import SECRET_PATTERNS
import re

def test_discovery_detect_context(tmp_path):
    # Setup mock project
    (tmp_path / "Dockerfile").write_text("FROM python:3.9\nUSER root")
    (tmp_path / "requirements.txt").write_text("flask\nboto3")
    (tmp_path / "agent.py").write_text("import os\napi_key = 'sk-ant-1234567890abcdef'")
    
    discovery = DiscoveryEngine(str(tmp_path))
    context = discovery.detect_context()
    
    assert context['is_containerized'] is True
    assert context['framework'] == 'flask'
    assert context['cloud'] == 'aws'
    assert context['has_secrets_risk'] is True

def test_infra_auditor_dockerfile():
    auditor = InfraAuditor()
    content = "FROM python:3.9\nUSER root"
    findings = auditor.audit(None, content, "Dockerfile")
    
    assert any("Security Risk: Container Running as Root" in f.title for f in findings)
    assert any("SRE Warning: Missing Resource Consternation" in f.title for f in findings)

def test_infra_auditor_terraform():
    auditor = InfraAuditor()
    content = 'resource "aws_security_group" "allow_all" {\n  ingress {\n    from_port = 0\n    to_port = 0\n    protocol = "-1"\n    cidr_blocks = ["0.0.0.0/0"]\n  }\n}'
    findings = auditor.audit(None, content, "main.tf")
    
    assert any("Security Risk: Publicly Accessible Ingress" in f.title for f in findings)

def test_infra_auditor_flask_bottleneck():
    auditor = InfraAuditor()
    content = "flask==2.0.1\nrequests"
    findings = auditor.audit(None, content, "requirements.txt")
    
    assert any("Architecture Risk: Synchronous Bottleneck (Flask)" in f.title for f in findings)

def test_pivot_auditor_mcp_blueprint():
    auditor = PivotAuditor()
    content = "import requests\ndef get_data():\n    return requests.get('http://api.com').json()"
    findings = auditor.audit(None, content, "src/tools/weather.py")
    
    assert any("Legacy Tooling -> MCP Migration" in f.title for f in findings)
    mcp_finding = next(f for f in findings if "Legacy Tooling -> MCP Migration" in f.title)
    assert "Migration Blueprint" in mcp_finding.description

def test_secret_scanner_patterns():
    # Test our regex patterns directly
    content = "openai_key = 'sk-123456789012345678901234'"
    match = re.search(SECRET_PATTERNS["OpenAI API Key"], content)
    assert match is not None
    
    content = "anthropic_key = 'sk-ant-123456789012345678901234'"
    match = re.search(SECRET_PATTERNS["Anthropic API Key"], content)
    assert match is not None
