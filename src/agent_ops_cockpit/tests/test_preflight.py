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

def test_preflight_run_all():
    engine = PreflightEngine()
    # Should pass in a standard dev environment
    assert engine.run_all() is True
