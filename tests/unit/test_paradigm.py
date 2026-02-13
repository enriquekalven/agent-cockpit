import ast
from agent_ops_cockpit.ops.auditors.paradigm import ParadigmAuditor

def test_paradigm_auditor_math_prompt():
    auditor = ParadigmAuditor()
    content = """
import csv
with open('data.csv') as f:
    data = f.read()
prompt = f"Calculate the average of this data: {data}"
"""
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "app.py")
    
    assert any("Pattern Mismatch: Structured Data Math via Prompt" in f.title for f in findings)
    assert "NL2SQL" in findings[0].description

def test_paradigm_auditor_manual_state_machine():
    auditor = ParadigmAuditor()
    content = """
while True:
    response = client.chat_completion(prompt)
    if 'DONE' in response:
        break
"""
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "logic.py")
    
    assert any("Manual State Machine Detected" in f.title for f in findings)
    assert "LangGraph" in findings[0].description

def test_paradigm_auditor_low_fidelity_rag():
    auditor = ParadigmAuditor()
    content = """
import openai
with open('manual.txt') as f:
    corpus = f.read()
context = f"Internal Docs: {corpus}"
response = openai.Completion.create(prompt=f"Search for fact in {context}")
"""
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, "rag.py")
    
    assert any("Low-Fidelity RAG (Context Stuffing)" in f.title for f in findings)
    assert "Vector DB" in findings[0].description
