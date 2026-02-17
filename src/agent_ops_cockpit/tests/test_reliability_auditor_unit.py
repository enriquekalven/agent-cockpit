import ast
from agent_ops_cockpit.ops.auditors.reliability import ReliabilityAuditor

def test_reliability_auditor_detects_missing_retry():
    code = """
import asyncio
import aiohttp

async def run_query(query):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://example.com") as resp:
            return await resp.text()
"""
    tree = ast.parse(code)
    auditor = ReliabilityAuditor()
    findings = auditor.audit(tree, code, "test.py")
    
    assert len(findings) > 0
    assert any("Missing Resiliency Logic" in f.title for f in findings)

if __name__ == "__main__":
    test_reliability_auditor_detects_missing_retry()
    print("Test Passed!")
