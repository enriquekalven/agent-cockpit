from typer.testing import CliRunner
from agent_ops_cockpit.eval.quality_climber import app

runner = CliRunner()

def test_quality_climber_steps():
    # We use runner.invoke which handles the event loop if typer supports it
    # or we might need to mock bits.
    result = runner.invoke(app, ["--steps", "1"])
    assert result.exit_code == 0
    assert "QUALITY HILL CLIMBING" in result.stdout
    assert "Iteration 1" in result.stdout

def test_quality_climber_threshold():
    # Testing with a very low threshold to ensure success
    result = runner.invoke(app, ["--steps", "1", "--threshold", "0.1"])
    assert result.exit_code == 0
    assert "SUCCESS" in result.stdout
