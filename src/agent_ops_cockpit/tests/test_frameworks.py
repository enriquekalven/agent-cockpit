from agent_ops_cockpit.ops.frameworks import detect_framework

def test_detect_google_framework(tmp_path):
    # Create a mock README with Google indicators
    d = tmp_path / "google_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("This project uses Vertex AI and ADK.")
    
    assert detect_framework(str(d)) == "google"

def test_detect_openai_framework(tmp_path):
    d = tmp_path / "openai_project"
    d.mkdir()
    reqs = d / "requirements.txt"
    reqs.write_text("openai>=1.0.0\nlangchain")
    
    assert detect_framework(str(d)) == "openai"

def test_detect_anthropic_framework(tmp_path):
    d = tmp_path / "anthropic_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("Powered by Anthropic Claude 3.5 Sonnet.")
    
    assert detect_framework(str(d)) == "anthropic"

def test_detect_microsoft_framework(tmp_path):
    d = tmp_path / "ms_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("Multi-agent system built with AutoGen.")
    
    assert detect_framework(str(d)) == "microsoft"

def test_detect_aws_framework(tmp_path):
    d = tmp_path / "aws_project"
    d.mkdir()
    reqs = d / "requirements.txt"
    reqs.write_text("boto3\naws-sdk")
    
    assert detect_framework(str(d)) == "aws"

def test_detect_copilotkit_framework(tmp_path):
    d = tmp_path / "copilot_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("Integrated using CopilotKit.ai sidebar.")
    
    assert detect_framework(str(d)) == "copilotkit"

def test_detect_generic_framework(tmp_path):
    d = tmp_path / "generic_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("A simple python script.")
    
    assert detect_framework(str(d)) == "generic"

def test_detect_go_framework(tmp_path):
    d = tmp_path / "go_project"
    d.mkdir()
    mod = d / "go.mod"
    mod.write_text("module agent-go\ngo 1.21")
    assert detect_framework(str(d)) == "go"

def test_detect_nodejs_framework(tmp_path):
    d = tmp_path / "node_project"
    d.mkdir()
    pkg = d / "package.json"
    pkg.write_text('{"name": "agent-node"}')
    assert detect_framework(str(d)) == "nodejs"

def test_detect_streamlit_framework(tmp_path):
    d = tmp_path / "streamlit_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("Uses streamlit for the UI.")
    assert detect_framework(str(d)) == "streamlit"

def test_detect_lit_framework(tmp_path):
    d = tmp_path / "lit_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("Web components with lit-element.")
    assert detect_framework(str(d)) == "lit"

def test_detect_angular_framework(tmp_path):
    d = tmp_path / "angular_project"
    d.mkdir()
    readme = d / "README.md"
    readme.write_text("Enterprise agent with @angular/core.")
    assert detect_framework(str(d)) == "angular"

def test_detect_firebase_framework(tmp_path):
    d = tmp_path / "firebase_project"
    d.mkdir()
    fb = d / "firebase.json"
    fb.write_text("{}")
    assert detect_framework(str(d)) == "firebase"
