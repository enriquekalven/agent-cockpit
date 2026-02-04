import os
import shutil
import tempfile
import pytest
from agent_ops_cockpit.ops.discovery import DiscoveryEngine

@pytest.fixture
def temp_workspace():
    tmp_dir = tempfile.mkdtemp()
    yield tmp_dir
    shutil.rmtree(tmp_dir)

def test_discovery_engine_default_exclusions(temp_workspace):
    os.makedirs(os.path.join(temp_workspace, "venv"))
    os.makedirs(os.path.join(temp_workspace, "node_modules"))
    with open(os.path.join(temp_workspace, "venv", "secret.py"), "w") as f:
        f.write("key = '123'")
    with open(os.path.join(temp_workspace, "agent.py"), "w") as f:
        f.write("print('hello')")
    
    discovery = DiscoveryEngine(temp_workspace)
    files = list(discovery.walk())
    
    # Relativize for easy comparison
    rel_files = [os.path.relpath(f, temp_workspace) for f in files]
    
    assert "agent.py" in rel_files
    assert "venv/secret.py" not in rel_files
    assert "node_modules" not in rel_files

def test_discovery_engine_gitignore(temp_workspace):
    with open(os.path.join(temp_workspace, ".gitignore"), "w") as f:
        f.write("ignored_file.txt\n")
        f.write("ignored_dir/\n")
    
    os.makedirs(os.path.join(temp_workspace, "ignored_dir"))
    with open(os.path.join(temp_workspace, "ignored_file.txt"), "w") as f:
        f.write("ignore me")
    with open(os.path.join(temp_workspace, "ignored_dir/data.txt"), "w") as f:
        f.write("ignore me too")
    with open(os.path.join(temp_workspace, "keep_me.txt"), "w") as f:
        f.write("keep me")
        
    discovery = DiscoveryEngine(temp_workspace)
    files = list(discovery.walk())
    rel_files = [os.path.relpath(f, temp_workspace) for f in files]
    
    assert "keep_me.txt" in rel_files
    assert "ignored_file.txt" not in rel_files
    assert "ignored_dir/data.txt" not in rel_files

def test_discovery_engine_cockpit_yaml(temp_workspace):
    with open(os.path.join(temp_workspace, "cockpit.yaml"), "w") as f:
        f.write("entry_point: 'custom/brain.py'\n")
        f.write("exclude: ['legacy/**']\n")
        f.write("threshold: 85\n")
        
    os.makedirs(os.path.join(temp_workspace, "custom"))
    os.makedirs(os.path.join(temp_workspace, "legacy"))
    with open(os.path.join(temp_workspace, "custom/brain.py"), "w") as f:
        f.write("import vertexai")
    with open(os.path.join(temp_workspace, "legacy/old.py"), "w") as f:
        f.write("print('old')")
        
    discovery = DiscoveryEngine(temp_workspace)
    
    assert discovery.config["entry_point"] == "custom/brain.py"
    assert discovery.config["threshold"] == 85
    assert discovery.find_agent_brain() == os.path.join(temp_workspace, "custom/brain.py")
    
    files = list(discovery.walk())
    rel_files = [os.path.relpath(f, temp_workspace) for f in files]
    assert "legacy/old.py" not in rel_files

def test_discovery_engine_ast_brain_detection(temp_workspace):
    os.makedirs(os.path.join(temp_workspace, "app"))
    # One file without AI
    with open(os.path.join(temp_workspace, "app/utils.py"), "w") as f:
        f.write("def add(a, b): return a + b")
    # One file with AI
    with open(os.path.join(temp_workspace, "app/logic.py"), "w") as f:
        f.write("import vertexai\nfrom google.cloud import aiplatform\ndef run(): pass")
        
    discovery = DiscoveryEngine(temp_workspace)
    brain = discovery.find_agent_brain()
    
    assert os.path.basename(brain) == "logic.py"

def test_library_isolation_detection(temp_workspace):
    discovery = DiscoveryEngine(temp_workspace)
    
    venv_file = os.path.join(temp_workspace, "venv/lib/python3.9/site-packages/package/file.py")
    user_file = os.path.join(temp_workspace, "src/agent.py")
    
    assert discovery.is_library_file(venv_file)
    assert not discovery.is_library_file(user_file)
