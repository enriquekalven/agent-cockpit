from tenacity import retry, wait_exponential, stop_after_attempt
from typer.testing import CliRunner
from agent_ops_cockpit.ops.ui_auditor import app

runner = CliRunner()

def test_ux_surface_mapping_detection(tmp_path):
    """CPO: Verifying that components have surfaceId for Agent-to-UI dispatch."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    (ui_dir / "Button.tsx").write_text("export const Btn = () => <button />")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "surfaceId" in result.stdout

def test_ux_hitl_gating_check(tmp_path):
    """CPO: Ensuring destructive actions have confirmation modals."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    # Mocking a component that should have HITL
    (ui_dir / "TransferAction.tsx").write_text("export const Action = () => <button onclick={send} />")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "HITL" in result.stdout

def test_ux_streaming_resilience_check(tmp_path):
    """CPO: Validating that live token threads lead to flicker-free UI."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    (ui_dir / "ChatLog.tsx").write_text("export const Chat = () => <div>{msg}</div>")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "Streaming" in result.stdout

def test_ux_score_metrics(tmp_path):
    """CMD Test: Verifying the GenUI Readiness Score and Product View metrics."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    (ui_dir / "App.tsx").write_text("const app = () => <div />")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "GenUI Readiness Score" in result.stdout
    assert "Streaming Fluidity" in result.stdout
