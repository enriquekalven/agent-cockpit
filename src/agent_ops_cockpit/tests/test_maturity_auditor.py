from tenacity import retry, wait_exponential, stop_after_attempt
import ast
import json
import os
import pytest
from agent_ops_cockpit.ops.auditors.maturity import MaturityAuditor, PATTERNS_PATH

def test_maturity_auditor_loading():
    """Verify the auditor correctly loads the knowledge base."""
    auditor = MaturityAuditor()
    assert isinstance(auditor.kb, dict)
    assert 'patterns' in auditor.kb
    assert 'compatibility_constraints' in auditor.kb

def test_maturity_pattern_matching_enterprise():
    """Verify indicators for Enterprise Cloud & Framework patterns."""
    auditor = MaturityAuditor()
    content = 'import chromadb'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'rag.py')
    titles = [f.title for f in findings]
    assert 'Vector Store Evolution (Chroma DB)' in titles
    assert 'Vertex AI Search' in findings[0].description
    assert 'Amazon Bedrock' in findings[0].description

def test_maturity_pattern_matching_orchestration():
    """Verify orchestration framework patterns (MP-014)."""
    auditor = MaturityAuditor()
    content = "while True:\n    # Custom orchestration loop\n    print('reasoning')"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'agent.py')
    titles = [f.title for f in findings]
    assert 'Orchestration Pattern Selection' in titles
    assert 'LangGraph' in findings[0].description
    assert 'CrewAI' in findings[0].description

def test_maturity_brand_safety_matching():
    """Verify Brand Safety Playbook patterns (MP-015, MP-016, MP-017)."""
    auditor = MaturityAuditor()
    content = "chat_history.append({'role': 'user', 'content': payload})"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'memory.py')
    titles = [f.title for f in findings]
    assert 'Payload Splitting (Context Fragmentation)' in titles
    content = 'def test_agent_behavior(): pass'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'tests/test_agent.py')
    titles = [f.title for f in findings]
    assert 'Adversarial Testing (Red Teaming)' in titles

def test_compatibility_drift_detection():
    """Verify that incompatible components are detected."""
    auditor = MaturityAuditor()
    content = 'import langgraph\nimport crewai'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'swarm.py')
    titles = [f.title for f in findings]
    assert 'Incompatible Duo: langgraph + crewai' in titles
    assert any((f.category == '🚨 Architectural Drift' for f in findings))

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_new_knowledge_ingestion_regression_v14():
    """Regression test: Verify knowledge from latest ingestion (v1.4) is present."""
    auditor = MaturityAuditor()
    kb = auditor.kb
    titles = [p['title'] for p in kb.get('patterns', [])]
    assert 'Model Resilience & Fallbacks' in titles
    assert 'Enterprise Identity (Identity Sprawl)' in titles
    assert 'Agentic Observability (Golden Signals)' in titles
    assert 'Payload Splitting (Context Fragmentation)' in titles
    assert 'Missing Safety Classifiers' in titles
    assert 'Adversarial Testing (Red Teaming)' in titles

def test_kb_schema_validity():
    """Ensure the maturity_patterns.json follows the required schema."""
    if not os.path.exists(PATTERNS_PATH):
        pytest.skip('maturity_patterns.json not found')
    with open(PATTERNS_PATH, 'r') as f:
        data = json.load(f)
    assert 'version' in data
    assert isinstance(data['patterns'], list)
    for p in data['patterns']:
        assert all((k in p for k in ['id', 'category', 'title', 'indicators', 'recommendation', 'impact']))
        assert isinstance(p['indicators'], list)

def test_v141_maturity_patterns():
    """Verify detection of v1.8.4 premium maturity patterns (MP-020 to MP-026)."""
    auditor = MaturityAuditor()
    content = 'def call_tool(name, args): pass'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'tools.py')
    assert any(('Excessive Agency' in f.title for f in findings))
    content = "print(f'Reasoning trace: {thought}')"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'agent.py')
    assert any(('Explainable Reasoning' in f.title for f in findings))
    content = 'class AgentCritic:\n    def check(self, x): pass'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'logic.py')
    assert any(('Multi-Agent Debate' in f.title for f in findings))
    content = 'results = vector_search(query)'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'rag.py')
    assert any(('Indirect Prompt Injection' in f.title for f in findings))
    content = 'from agent_starter_pack import StarterPack'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'main.py')
    assert any(('Agent Starter Pack' in f.title for f in findings))
    content = 'class MyWorkflow(Workflow): pass'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, 'flow.py')
    assert any(('LlamaIndex Workflows' in f.title for f in findings))