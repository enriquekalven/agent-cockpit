from typer.testing import CliRunner
from agent_ops_cockpit.ops.ui_auditor import app

runner = CliRunner()

def test_ui_auditor_score_calculation(tmp_path):
    """Verify that deductions work correctly in UI Auditor."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    
    # Create a component missing surfaceId and Thinking feedback
    # Deductions: Missing 'surfaceId' (20) + Missing 'Thinking' feedback (15) = 35 deduction
    # Expected score: 100 - 35 = 65
    (ui_dir / "DashboardPage.tsx").write_text("export const Dashboard = () => <div>No surface id</div>")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "GenUI Readiness Score" in result.stdout
    assert "65/100" in result.stdout
    assert "⚠️ WARN" in result.stdout

def test_ui_auditor_perfect_score(tmp_path):
    """Verify a perfect 100/100 score."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    
    # Create a component that passes most checks
    (ui_dir / "Component.tsx").write_text("""
/* surfaceId: 'my-comp' */
/* loading: <Spinner /> */
/* legal: Copyright 2024 */
/* a11y: aria-label='test' */
export const MyComp = () => <div surfaceId='test'>Stable UI</div>
""")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "100/100" in result.stdout
    assert "✅ APPROVED" in result.stdout

def test_ui_auditor_hitl_detection(tmp_path):
    """Verify HITL gating detection."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    
    # File name contains 'Transfer' but content lacks HITL patterns
    # This will trigger: Missing surfaceId(20), Missing Thinking(15), Missing HITL(15)
    # Total deduction: 50. Score: 50
    (ui_dir / "TransferPage.tsx").write_text("export const Transfer = () => <button>Click me</button>")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "Missing HITL" in result.stdout
    assert "50/100" in result.stdout or "45/100" in result.stdout
    assert "REJECTED" in result.stdout
