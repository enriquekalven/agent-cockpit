import os
import json
import tempfile
import shutil
from agent_ops_cockpit.ops.orchestrator import workspace_audit

def setup_mock_agent(agent_dir, has_issue=True):
    os.makedirs(agent_dir, exist_ok=True)
    agent_code = os.path.join(agent_dir, "agent.py")
    if has_issue:
        content = '''import asyncio
import aiohttp

async def run_query(query):
    # This needs a retry
    return await fetch_api_data(query)

API_KEY = "AIzaSyD-1234567890abcdefghijklmnopqrstuv"
'''
    else:
        content = '''import asyncio
from tenacity import retry

@retry
async def run_query(query):
    return "fixed"
'''
    with open(agent_code, "w") as f:
        f.write(content)
    return agent_code

def test_workspace_bulk_fix_apply():
    """Verify that workspace_audit with apply_fixes=True repairs multiple agents."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Scenario: Two agents with issues
        agent1_dir = os.path.join(tmp_dir, "agent_alpha")
        agent2_dir = os.path.join(tmp_dir, "agent_beta")
        
        f1 = setup_mock_agent(agent1_dir)
        f2 = setup_mock_agent(agent2_dir)
        
        orig1 = open(f1).read()
        orig2 = open(f2).read()

        old_cwd = os.getcwd()
        old_pp = os.environ.get('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = f"{root}{os.pathsep}{old_pp}"
        os.chdir(tmp_dir)
        
        try:
            # Run workspace audit with apply_fixes
            workspace_audit(root_path=".", mode='quick', apply_fixes=True, sim=True)
            
            # Verify Both Agents are modified
            new1 = open(f1).read()
            new2 = open(f2).read()
            
            assert "@retry" in new1 or "timeout=" in new1
            assert "@retry" in new2 or "timeout=" in new2
            assert new1 != orig1
            assert new2 != orig2
            
            # Verify Evidence Lake Presence
            lake_path = os.path.join('.cockpit', 'evidence_lake.json')
            assert os.path.exists(lake_path)
            
            # Verify Fleet Dashboard Presence
            dashboard_path = os.path.join('.cockpit', 'fleet_dashboard.html')
            assert os.path.exists(dashboard_path)
            
        finally:
            os.chdir(old_cwd)
            os.environ['PYTHONPATH'] = old_pp
