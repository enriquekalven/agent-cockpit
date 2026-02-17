from agent_ops_cockpit.telemetry import TelemetryManager
from agent_ops_cockpit.ops.shadow import ProductionShadowRouter
from agent_ops_cockpit.ops.watcher import OperationalWatcher
from agent_ops_cockpit.ops.simulator import ToolProxy

def test_telemetry_export_empty():
    tm = TelemetryManager()
    res = tm.export_traces()
    # Check if it returns empty/message if no traces exist (likely in CI environment)
    assert "status" in res

def test_shadow_router_diversion():
    router = ProductionShadowRouter(diversion_percent=1.0)
    
    def base_fn(x): return "base"
    def cand_fn(x): return "cand"
    
    # In shadow.py, route returns the base response
    res = router.route("test", base_fn, cand_fn)
    assert res == "base"

def test_operational_watcher_logic():
    watcher = OperationalWatcher()
    metrics = {
        "avg_latency": "600ms",
        "recent_events": [{"event": "hallucination_detected"}]
    }
    findings = watcher.inspect_live_metrics(metrics)
    assert len(findings) == 2
    assert any(f["level"] == "CRITICAL" for f in findings)

def test_tool_proxy_chaos():
    proxy = ToolProxy(mode="chaos")
    res = proxy.execute_mock_tool("test_tool", {})
    assert res["status"] == "error"

def test_tool_proxy_nominal():
    proxy = ToolProxy(mode="nominal")
    res = proxy.execute_mock_tool("test_tool", {"arg": 1})
    assert res["status"] == "success"
    assert "Simulated output" in res["data"]
