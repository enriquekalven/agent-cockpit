from unittest.mock import patch, MagicMock
import os
import pytest
from agent_ops_cockpit.ops.preflight import PreflightEngine

def test_preflight_registry_check():
    engine = PreflightEngine()
    # Pypi should be reachable
    success, detail = engine.check_registry_access("https://pypi.org/simple")
    assert success is True
    assert "Reachable" in detail

def test_preflight_tooling_check():
    engine = PreflightEngine()
    success, detail = engine.check_tooling()
    assert success is True
    assert "All base tools detected" in detail

def test_preflight_env_check(tmp_path):
    # Test with no .env
    engine = PreflightEngine(target_path=str(tmp_path))
    success, detail = engine.check_environment_consistency()
    assert success is True
    assert "No .env detected" in detail
    
    # Test with .env
    env_file = tmp_path / ".env"
    env_file.write_text("API_KEY=test")
    success, detail = engine.check_environment_consistency()
    assert success is True
    assert "Found environment config" in detail

def mock_subprocess_check_output(cmd, *args, **kwargs):
    if "get-value" in cmd:
        return "mock-project"
    if "services" in cmd:
        return '[{"config": {"name": "aiplatform.googleapis.com"}}]'
    return 'mock-account@example.com'

@patch('shutil.which')
@patch('subprocess.check_output', side_effect=mock_subprocess_check_output)
@patch('subprocess.run')
def test_preflight_run_all(mock_run, mock_check_output, mock_which, monkeypatch):
    mock_which.return_value = '/usr/bin/gcloud'
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = '{"billingEnabled": true}'
    engine = PreflightEngine()
    assert engine.run_all() is True
