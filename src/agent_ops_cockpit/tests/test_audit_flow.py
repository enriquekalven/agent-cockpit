from tenacity import retry, wait_exponential, stop_after_attempt
import os
import json
import tempfile
import hashlib
from agent_ops_cockpit.ops.orchestrator import run_audit

def setup_mock_agent(agent_dir):
    os.makedirs(agent_dir, exist_ok=True)
    agent_code = os.path.join(agent_dir, 'agent.py')
    with open(agent_code, 'w') as f:
        f.write('import asyncio\nimport aiohttp\n\nasync def run_query(query):\n    # This is line 4\n    return await fetch_api_data(query)\n\n# ACTION: Hardcoded Secret\nAPI_KEY = "AIzaSyD-1234567890abcdefghijklmnopqrstuv"\n')
    return agent_code

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_full_audit_flow_integration():
    """E2E: Ensure orchestrator scans, audits, and generates artifacts correctly."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_dir = os.path.join(tmp_dir, 'my_agent')
        setup_mock_agent(agent_dir)
        old_cwd = os.getcwd()
        old_pp = os.environ.get('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = f'{root}{os.pathsep}{old_pp}'
        os.chdir(tmp_dir)
        try:
            run_audit(mode='quick', target_path='my_agent', sim=True)
            agent_abs = os.path.abspath('my_agent')
            agent_hash = hashlib.md5(agent_abs.encode()).hexdigest()
            lake_json = os.path.join('.cockpit', 'evidence_lake', agent_hash, 'latest.json')
            assert os.path.exists(lake_json)
            with open(lake_json, 'r') as f:
                data = json.load(f)
            if 'Secret Scanner' not in data['results'] or 'Google API Key' not in data['results']['Secret Scanner']['output']:
                print(f"\nDEBUG: Secret Scanner output: {data['results'].get('Secret Scanner', {}).get('output', 'N/A')}")
            assert 'Secret Scanner' in data['results']
            assert 'Google API Key' in data['results']['Secret Scanner']['output']
            if 'Architecture Review' not in data['results'] or 'ACTION:' not in data['results']['Architecture Review']['output']:
                print(f"\nDEBUG: Arch Review output: {data['results'].get('Architecture Review', {}).get('output', 'N/A')}")
            assert 'Architecture Review' in data['results']
            assert 'ACTION:' in data['results']['Architecture Review']['output']
        finally:
            os.chdir(old_cwd)
            os.environ['PYTHONPATH'] = old_pp

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def test_dry_run_does_not_modify_files():
    """E2E: Verify --dry-run shows diff but doesn't save changes."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_dir = os.path.join(tmp_dir, 'fix_me')
        agent_file = setup_mock_agent(agent_dir)
        original_content = open(agent_file).read()
        old_cwd = os.getcwd()
        old_pp = os.environ.get('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = f'{root}{os.pathsep}{old_pp}'
        os.chdir(tmp_dir)
        try:
            run_audit(mode='quick', target_path='fix_me', apply_fixes=True, dry_run=True, sim=True)
            current_content = open(agent_file).read()
            assert current_content == original_content, 'Dry run should NOT modify the file!'
            # In v1.8.2, apply_fixes=True (with dry_run=False) generates a patch, it does NOT modify the file directly.
            run_audit(mode='quick', target_path='fix_me', apply_fixes=True, dry_run=False, sim=True)
            fixed_content = open(agent_file).read()
            assert fixed_content == original_content, 'Applying fixes in v1.8.2 should NOT modify the file directly (Plan-then-Execute)!'
            
            patch_dir = os.path.join('.cockpit', 'patches')
            assert os.path.exists(patch_dir)
            patches = os.listdir(patch_dir)
            assert len(patches) > 0, 'Applying fixes should generate a .patch file!'
            assert any(p.endswith('.patch') for p in patches)
        finally:
            os.chdir(old_cwd)
            os.environ['PYTHONPATH'] = old_pp