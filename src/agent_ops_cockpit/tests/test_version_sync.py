import os
import json
import tomllib
from agent_ops_cockpit.config import config

def test_versions_are_in_sync():
    """Ensure version strings in python, pyproject.toml, and package.json match."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    
    # 1. Get Python Config Version
    py_version = config.VERSION
    
    # 2. Get pyproject.toml version
    pyproject_path = os.path.join(root, "pyproject.toml")
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)
    pyproject_version = pyproject_data["project"]["version"]
    
    # 3. Get package.json version (Face layer)
    package_path = os.path.join(root, "package.json")
    with open(package_path, "r") as f:
        package_data = json.load(f)
    package_version = package_data["version"]
    
    print(f"\nVersions detected -> Config: {py_version}, pyproject: {pyproject_version}, package: {package_version}")
    
    assert py_version == pyproject_version
    assert py_version == package_version
