from tenacity import retry, wait_exponential, stop_after_attempt
from typer.testing import CliRunner
from agent_ops_cockpit.ops.ui_auditor import app

runner = CliRunner()

def test_ui_auditor_score_calculation(tmp_path):
    """Verify that deductions work correctly in UI Auditor."""
    ui_dir = tmp_path / "src"
    ui_dir.mkdir()
    
    # Create a component missing surfaceId and Thinking feedback
    # Deductions: Missing 'surfaceId' (20) + Missing 'Thinking' feedback (15) + Missing 'Mobile' (10) = 45 deduction
    # Expected score: 100 - 45 = 55
    (ui_dir / "DashboardPage.tsx").write_text("export const Dashboard = () => <div>No surface id</div>")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "GenUI Readiness Score" in result.stdout
    assert "55/100" in result.stdout
    assert "REJECTED" in result.stdout

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
/* mobile: @media (max-width: 768px) */
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
    # Also missing 'Page' patterns if it's considered a Page
    # This will trigger: Missing surfaceId(20), Missing Thinking(15), Missing HITL(15), Missing Mobile(10)
    # Total deduction: 60. Score: 40
    (ui_dir / "TransferPage.tsx").write_text("export const Transfer = () => <button>Click me</button>")
    
    result = runner.invoke(app, ["audit", str(ui_dir)])
    assert "Missing HITL" in result.stdout
    assert "40/100" in result.stdout
    assert "REJECTED" in result.stdout
