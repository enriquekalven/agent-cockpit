import ast
import pytest
from agent_ops_cockpit.ops.auditors.security import SecurityAuditor

@pytest.fixture
def auditor():
    return SecurityAuditor()

def test_s1_sovereignty_gap(auditor):
    content = "def execute_payment(amt): \n    bank_api.transfer(amt)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "bank.py")
    assert any("Sovereignty Gap" in f.title for f in findings)

def test_s2_execution_trap(auditor):
    content = "def run_agent_code(c): eval(c)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "unsafe.py")
    assert any("Insecure Output Handling: Execution Trap" in f.title for f in findings)

def test_s3_pii_osmosis(auditor):
    content = "import salesforce\ndef process_lead(l): llm.generate(l)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "lead.py")
    assert any("PII Osmosis: Implicit Leakage Risk" in f.title for f in findings)

def test_s4_credential_proximity(auditor):
    content = "import os\nos.getenv('API_KEY')\n# Uses .env file locally"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "env_test.py")
    assert any("Credential Proximity: Shadow ENV Usage" in f.title for f in findings)

def test_s5_indirect_injection(auditor):
    content = "def search_and_chat(q):\n    context = retrieve(q)\n    return llm.generate(context)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "rag.py")
    assert any("Untrusted Context Trap: Indirect Injection" in f.title for f in findings)

def test_s6_tool_overprivilege(auditor):
    content = "import subprocess\nsubprocess.run('ls -R /', shell=True)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "shell_tool.py")
    assert any("Lateral Movement: Tool Over-Privilege" in f.title for f in findings)

def test_s7_kb_poisoning(auditor):
    content = "def update_knowledge(doc): \n    vector_store.upsert(doc)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "ingest.py")
    assert any("Knowledge Base Poisoning: Ungated Ingestion" in f.title for f in findings)

def test_s8_hardcoded_secret(auditor):
    content = "AWS_SECRET = 'AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5'"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "secrets.py")
    assert any("Hardcoded Secret Detected" in f.title for f in findings)
