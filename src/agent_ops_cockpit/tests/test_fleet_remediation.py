import os
from tenacity import retry, wait_exponential, stop_after_attempt
import tempfile
from agent_ops_cockpit.ops.orchestrator import workspace_audit

def setup_mock_agent(agent_dir, has_issue=True):
    os.makedirs(agent_dir, exist_ok=True)
    agent_code = os.path.join(agent_dir, 'agent.py')
    if has_issue:
        content = 'import asyncio\nimport aiohttp\n\nasync def run_query(query):\n    # This needs a retry\n    return await fetch_api_data(query)\n\nAPI_KEY = "AIzaSyD-1234567890abcdefghijklmnopqrstuv"\n'
    else:
        content = 'import asyncio\nfrom tenacity import retry\n\n@retry\nasync def run_query(query):\n    return "fixed"\n'
    with open(agent_code, 'w') as f:
        f.write(content)
    return agent_code

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_workspace_bulk_fix_apply():
    """Verify that workspace_audit with apply_fixes=True repairs multiple agents."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent1_dir = os.path.join(tmp_dir, 'agent_alpha')
        agent2_dir = os.path.join(tmp_dir, 'agent_beta')
        f1 = setup_mock_agent(agent1_dir)
        f2 = setup_mock_agent(agent2_dir)
        orig1 = open(f1).read()
        orig2 = open(f2).read()
        old_cwd = os.getcwd()
        old_pp = os.environ.get('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = f'{root}{os.pathsep}{old_pp}'
        os.chdir(tmp_dir)
        try:
            workspace_audit(root_path='.', mode='quick', apply_fixes=True, sim=True)
            new1 = open(f1).read()
            new2 = open(f2).read()
            assert new1 == orig1, 'Workspace audit in v1.6.7 should NOT modify files directly!'
            assert new2 == orig2
            
            patch_dir = os.path.join('.cockpit', 'patches')
            assert os.path.exists(patch_dir)
            patches = os.listdir(patch_dir)
            assert len(patches) >= 2, 'Applying fixes should generate patches for all agents!'
            lake_path = os.path.join('.cockpit', 'evidence_lake.json')
            assert os.path.exists(lake_path)
            dashboard_path = os.path.join('.cockpit', 'fleet_dashboard.html')
            assert os.path.exists(dashboard_path)
        finally:
            os.chdir(old_cwd)
            os.environ['PYTHONPATH'] = old_pp