import ast
import pytest
from agent_ops_cockpit.ops.auditors.paradigm import ParadigmAuditor

@pytest.fixture
def auditor():
    return ParadigmAuditor()

def test_p1_monolithic_fatigue(auditor):
    # Fixed parentheses in def
    content = "def tool_" + "(): pass\ndef tool_".join([str(i) for i in range(20)]) + "(): pass\n" + "print('hello')\n" * 600
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "monolith.py")
    assert any("Monolithic Fatigue Detected" in f.title for f in findings)

def test_p2_legacy_shadowing(auditor):
    content = "import requests\n# This is an MCP tool\ndef get(): requests.get('url')"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "mcp_tool.py")
    assert any("Legacy Shadowing: HTTP instead of MCP" in f.title for f in findings)

def test_p3_token_amnesia(auditor):
    content = "chat_history = []\ndef chat(msg): chat_history.append(msg)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "memory.py")
    assert any("Token Amnesia: Manual Memory Management" in f.title for f in findings)

def test_p4_reflection_blindness(auditor):
    content = "def write_complex_code(spec):\n    return llm.generate(f'Write code for {spec}')"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "coder.py")
    assert any("Reflection Blindness: Brittle Intelligence" in f.title for f in findings)

def test_p5_data_stuffing(auditor):
    content = "import pandas as pd\ndata = pd.read_csv('a.csv')\nprompt = f'Analyze this: {data}'"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "stuffing.py")
    assert any("Pattern Mismatch: Structured Data Stuffing" in f.title for f in findings)

def test_p6_rag_for_math(auditor):
    content = "query = 'Calculate the average price'\n# RAG search below\nresults = search(query)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "math_rag.py")
    assert any("Paradigm Drift: RAG for Math" in f.title for f in findings)

def test_p7_token_burning(auditor):
    content = "prompt = 'Instructions: Clean and format this text with regex: ' + text"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "etl.py")
    assert any("Token Burning: LLM for Deterministic Ops" in f.title for f in findings)

def test_p8_latency_trap(auditor):
    content = "import os\nfor r,d,f in os.walk('.'): \n    if 'query' in r: pass"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "local_search.py")
    assert any("Latency Trap: Brute-Force Local Search" in f.title for f in findings)

def test_p9_ungated_autonomy(auditor):
    content = "def execute_payment(amount):\n    bank_api.post_transaction(amount)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "wallet.py")
    assert any("Ungated High-Stake Action" in f.title for f in findings)

def test_p10_manual_state_machine(auditor):
    content = "while True:\n    res = llm.generate_content(p)\n    if 'DONE' in res: break"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "loop.py")
    assert any("Manual State Machine: Loop of Doom" in f.title for f in findings)

def test_p11_looming_latency(auditor):
    content = "def generate_report():\n    # Response generation for a long report\n    return llm.generate('long report content')"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "report.py")
    assert any("Looming Latency: Blocking Inference" in f.title for f in findings)

def test_p12_expert_bloat(auditor):
    # Fixed parentheses in def
    content = "def tool_" + "(): pass\ndef tool_".join([str(i) for i in range(30)]) + "(): pass"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "bloat.py")
    assert any("Expert Bloat: Linear Tool Selection" in f.title for f in findings)

def test_p13_instruction_fatigue(auditor):
    content = '"""' + "A" * 11000 + '"""'
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "heavy_prompt.py")
    assert any("Instruction Fatigue: Prompt Overloading" in f.title for f in findings)

def test_p14_policy_blindness(auditor):
    content = "prompt = 'Rules and Regulations for this agent: ...'"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "rules.py")
    assert any("Policy Blindness: Implicit Governance" in f.title for f in findings)

def test_p15_path_rigidness(auditor):
    content = "def complex_task_goal():\n    # Executing then step1 then step2 then step3 then step4\n    pass"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "linear.py")
    assert any("Path Rigidness: Sequential Blindness" in f.title for f in findings)

def test_p16_passive_retrieval(auditor):
    content = "def query(msg):\n    docs = retrieve(msg)\n    return llm(docs, msg)"
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "passive.py")
    assert any("Passive Retrieval: Context Drowning" in f.title for f in findings)
