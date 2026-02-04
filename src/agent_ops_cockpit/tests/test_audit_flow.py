import os
import json
import tempfile
import hashlib
from agent_ops_cockpit.ops.orchestrator import run_audit

def setup_mock_agent(agent_dir):
    os.makedirs(agent_dir, exist_ok=True)
    agent_code = os.path.join(agent_dir, "agent.py")
    with open(agent_code, "w") as f:
        f.write('''
import asyncio
import aiohttp

async def run_query(query):
    # ACTION: Missing Timeout (Zombie Risk)
    async with aiohttp.ClientSession() as session:
        async with session.get("http://example.com") as resp:
            return await resp.text()

# ACTION: Hardcoded Secret
API_KEY = "AIzaSyD-1234567890abcdefghijklmnopqrstuv"
''')
    return agent_code

def test_full_audit_flow_integration():
    """E2E: Ensure orchestrator scans, audits, and generates artifacts correctly."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_dir = os.path.join(tmp_dir, "my_agent")
        setup_mock_agent(agent_dir)

        old_cwd = os.getcwd()
        old_pp = os.environ.get('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = f"{root}{os.pathsep}{old_pp}"
        os.chdir(tmp_dir)
        try:
            # Run in simulation mode
            # Note: We use -m pytest -s to see output
            run_audit(mode='quick', target_path='my_agent', sim=True)
            
            # Verify Artifacts
            agent_abs = os.path.abspath('my_agent')
            agent_hash = hashlib.md5(agent_abs.encode()).hexdigest()
            lake_json = os.path.join('evidence_lake', agent_hash, 'latest.json')
            
            assert os.path.exists(lake_json)
            with open(lake_json, 'r') as f:
                data = json.load(f)
            
            # Check for findings in results
            if "Secret Scanner" not in data['results'] or "Google API Key" not in data['results']['Secret Scanner']['output']:
                print(f"\nDEBUG: Secret Scanner output: {data['results'].get('Secret Scanner', {}).get('output', 'N/A')}")
            assert "Secret Scanner" in data['results']
            assert "Google API Key" in data['results']['Secret Scanner']['output']
            
            if "Architecture Review" not in data['results'] or "ACTION:" not in data['results']['Architecture Review']['output']:
                print(f"\nDEBUG: Arch Review output: {data['results'].get('Architecture Review', {}).get('output', 'N/A')}")
            
            assert "Architecture Review" in data['results']
            assert "ACTION:" in data['results']['Architecture Review']['output']
            
        finally:
            os.chdir(old_cwd)
            os.environ['PYTHONPATH'] = old_pp

def test_dry_run_does_not_modify_files():
    """E2E: Verify --dry-run shows diff but doesn't save changes."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_dir = os.path.join(tmp_dir, "fix_me")
        agent_file = setup_mock_agent(agent_dir)
        original_content = open(agent_file).read()

        old_cwd = os.getcwd()
        old_pp = os.environ.get('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = f"{root}{os.pathsep}{old_pp}"
        os.chdir(tmp_dir)
        try:
            # Run with dry_run=True, apply_fixes=True
            # We want to see if it WOULD fix but doesn't
            run_audit(mode='quick', target_path='fix_me', apply_fixes=True, dry_run=True, sim=True)
            
            # Verify file content is unchanged
            current_content = open(agent_file).read()
            assert current_content == original_content, "Dry run should NOT modify the file!"
            
            # Verification: Now run WITHOUT dry_run to ensure it DOES fix
            run_audit(mode='quick', target_path='fix_me', apply_fixes=True, dry_run=False, sim=True)
            
            # Verify Artifacts to see if it even ran
            agent_abs = os.path.abspath('fix_me')
            agent_hash = hashlib.md5(agent_abs.encode()).hexdigest()
            lake_json = os.path.join('evidence_lake', agent_hash, 'latest.json')
            
            with open(lake_json, 'r') as f:
                data = json.load(f)
            
            fixed_content = open(agent_file).read()
            if "@retry" not in fixed_content and "timeout=" not in fixed_content:
                print(f"\nDEBUG: fix_me results: {json.dumps(data['results'], indent=2)}")
            
            assert fixed_content != original_content, "Applying fixes should modify the file!"
            assert "@retry" in fixed_content or "timeout=" in fixed_content
            
        finally:
            os.chdir(old_cwd)
            os.environ['PYTHONPATH'] = old_pp
