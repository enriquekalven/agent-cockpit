import ast
import sys
import os
import re

# Ensure we can import from src
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from agent_ops_cockpit.ops.auditors.paradigm import ParadigmAuditor

auditor = ParadigmAuditor()

def debug_audit(name, content, file_path):
    print(f"--- {name} ---")
    tree = ast.parse(content)
    findings = auditor.audit(tree, content, file_path)
    print(f"Findings count: {len(findings)}")
    for f in findings:
        print(f" - {f.title}")

# Test P6
debug_audit("P6", "from google.adk import Agent\nquery = 'Calculate average value'\n# RAG search below\nresults = search(query)", "math_rag.py")

# Test P7
debug_audit("P7", "from google.adk import Agent\nprompt = 'Instructions: format this text with regex: ' + text", "etl.py")

# Test P12
debug_audit("P12", "from google.adk import Agent\n" + "def tool_" + "(): pass\ndef tool_".join([str(i) for i in range(30)]) + "(): pass", "bloat.py")
