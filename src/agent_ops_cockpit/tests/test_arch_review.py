from typer.testing import CliRunner
from agent_ops_cockpit.ops.arch_review import app

runner = CliRunner()

def test_arch_review_score(tmp_path):
    # Set up a mock project directory
    project_dir = tmp_path / "my_agent"
    project_dir.mkdir()
    
    # Create a README to trigger a framework (e.g., Google)
    readme = project_dir / "README.md"
    readme.write_text("Uses Google Cloud and Vertex AI.")
    
    # Create a code file with some keywords to pass checks
    code_file = project_dir / "agent.py"
    code_file.write_text("""
def chat():
    # pii scrubbing
    text = scrub_pii(input)
    # cache enabled
    cache = redis.Cache()
    # iam auth
    auth = iam.Auth()
""")
    
    # Run the audit on the mock project directory
    # We need to ensure src is in PYTHONPATH if the test runner doesn't handle it
    # But usually, when running pytest from root, 'src' is handled or we rely on the import path
    
    result = runner.invoke(app, ["--path", str(project_dir)])
    assert result.exit_code == 0
    assert "ARCHITECTURE REVIEW" in result.stdout
    assert "Review Score:" in result.stdout
    # We expect some checks to pass because of the keywords
    assert "PASSED" in result.stdout

def test_arch_review_fail_on_empty(tmp_path):
    project_dir = tmp_path / "empty_agent"
    project_dir.mkdir()
    
    result = runner.invoke(app, ["--path", str(project_dir)])
    assert result.exit_code == 0
    assert "FAIL" in result.stdout
    assert "Review Score: 0/100" in result.stdout
