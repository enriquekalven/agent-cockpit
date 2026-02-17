import ast
import pytest
from agent_ops_cockpit.ops.auditors.finops import FinOpsAuditor

@pytest.fixture
def auditor():
    return FinOpsAuditor()

def test_f1_inference_loop(auditor):
    content = "for i in range(10):\n    res = llm.invoke(f'task {i}')"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "loop_cost.py")
    assert any("Inference Loop Detected" in f.title for f in findings)

def test_f2_caching_opportunity(auditor):
    content = '"""' + "Instruction content " * 200 + '"""'
    # Missing ContextCacheConfig import/usage
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "big_prompt.py")
    assert any("Missing Context Caching" in f.title for f in findings)

def test_f3_model_overpower(auditor):
    content = "model = 'gpt-4o'\ndef clean_text(t): return llm.generate(t) # with regex cleaning"
    content += "\n# regex parse clean"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "overpower.py")
    assert any("Model Over-Privilege" in f.title for f in findings)

def test_f4_retry_burn(auditor):
    content = "from tenacity import retry, wait_fixed\n@retry(wait=wait_fixed(1))\ndef call(): pass"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "retry_fail.py")
    assert any("Non-Exponential Retry" in f.title for f in findings)

def test_f5_massive_retrieval(auditor):
    content = "results = vector_db.retrieve(query, top_k=100)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "heavy_rag.py")
    assert any("Massive Retrieval K-Index" in f.title for f in findings)
