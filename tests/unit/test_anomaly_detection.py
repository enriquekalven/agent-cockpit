import pytest
import os
import tempfile
from agent_ops_cockpit.ops.auditors.anomaly_auditor import AnomalySME
from agent_ops_cockpit.ops.fleet import FleetManager

def test_anomaly_sme_detection():
    auditor = AnomalySME()
    
    # Tool Misuse Telemetry
    telemetry_misuse = [
        {"timestamp": "2026-02-11T12:00:00", "tool_calls": 15, "payload": "Normal loop"}
    ]
    report = auditor.audit_telemetry("rogue-agent", telemetry_misuse)
    assert report["risk_score"] >= 0.4
    assert any(f["id"] == "AD-TOOL-MISUSE" for f in report["findings"])
    
    # Rogue PII Telemetry
    telemetry_pii = [
        {"timestamp": "2026-02-11T12:01:00", "tool_calls": 1, "payload": "Extracting PII: secret@data.com"}
    ]
    report = auditor.audit_telemetry("pii-agent", telemetry_pii)
    assert report["risk_score"] >= 0.5
    assert any(f["id"] == "AD-ROGUE-EXFIL" for f in report["findings"])
    
    # Critical Threshold
    telemetry_critical = telemetry_misuse + telemetry_pii
    report = auditor.audit_telemetry("critical-agent", telemetry_critical)
    assert report["risk_score"] >= 0.85
    assert report["auto_remediation_triggered"] is True

def test_fleet_manager_anomaly_enforcement():
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        manager = FleetManager(db_path=tmp.name)
        manager.register_agent("rogue-agent", "/tmp/path", "google", "https://rogue.url", "1.5.0")
        
        # Simulate critical telemetry
        telemetry = [
            {"timestamp": "now", "tool_calls": 20, "payload": "Normal reasoning loop"}
        ]
        # AD-TOOL-MISUSE provides 0.4. Let's make it hit critical (0.85) by repeating or adding PII.
        telemetry.append({"timestamp": "now", "payload": "PII exfiltration"})
        
        report = manager.monitor_agent_anomaly("rogue-agent", telemetry)
        assert report["auto_remediation_triggered"] is True
        
        # Verify it was mothballed automatically
        fleet = manager.list_fleet()
        agent = next(a for a in fleet if a["name"] == "rogue-agent")
        assert agent["status"] == "MOTHBALLED"

def test_mothball_by_name():
    with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
        manager = FleetManager(db_path=tmp.name)
        manager.register_agent("agent-1", "/p1", "google", "u1", "v1")
        manager.register_agent("agent-2", "/p2", "google", "u2", "v1")
        
        # Mothball only agent-2
        manager.mothball_fleet(agent_name="agent-2")
        
        fleet = manager.list_fleet()
        a1 = next(a for a in fleet if a["name"] == "agent-1")
        a2 = next(a for a in fleet if a["name"] == "agent-2")
        
        assert a1["status"] == "HEALTHY"
        assert a2["status"] == "MOTHBALLED"
