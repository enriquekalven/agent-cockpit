import os
import json
import tempfile
import pytest
from agent_ops_cockpit.eval.red_team import audit

def test_red_team_golden_set_generation():
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_path = os.path.join(tmp_dir, "agent.py")
        # This agent has no security logic at all
        with open(agent_path, "w") as f:
            f.write("print('hello')")
            
        # Run audit (it will exit with 1 because of vulnerabilities)
        try:
            audit(agent_path)
        except:
            pass
            
        # Verify regression file exists
        regression_path = os.path.join(tmp_dir, ".cockpit", "vulnerability_regression.json")
        assert os.path.exists(regression_path)
        
        with open(regression_path, "r") as f:
            data = json.load(f)
            
        assert len(data) > 0
        # Check if PII Extraction is recorded
        names = [item['name'] for item in data]
        assert "PII Extraction" in names
