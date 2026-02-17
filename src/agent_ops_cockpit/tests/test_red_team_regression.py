import os
import json
import tempfile
import pytest
from agent_ops_cockpit.eval.red_team import audit
import click

def test_red_team_v2_coverage():
    """Verify Red Team Auditor v2.0 correctly detects new brand safety vectors."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_path = os.path.join(tmp_dir, "agent.py")
        # Minimal agent with NO safety gates
        with open(agent_path, "w") as f:
            f.write("# Minimal Agent\nprint('Hello')\n")
            
        # Run audit (it will exit with 1 because of vulnerabilities)
        with pytest.raises((click.exceptions.Exit, SystemExit)):
            audit(agent_path)
            
        # Verify regression file exists in .cockpit
        regression_path = os.path.join(tmp_dir, ".cockpit", "vulnerability_regression.json")
        assert os.path.exists(regression_path)
        
        with open(regression_path, "r") as f:
            data = json.load(f)
            
        names = [item['name'] for item in data]
        
        # Core Security
        assert "PII Extraction" in names
        assert "Prompt Injection" in names
        
        # Brand Safety Playbook (New in v2.0)
        assert "Payload Splitting (Turn 1/2)" in names
        assert "Domain-Specific Sensitive (Finance)" in names
        assert "Tone of Voice Mismatch (Banker)" in names
        assert "Language Override" in names

def test_red_team_mitigation_detection():
    """Verify that implementing mitigations resolves the findings."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        agent_path = os.path.join(tmp_dir, "secure_agent.py")
        # Agent with safety logic from Brand Safety Playbook
        with open(agent_path, "w") as f:
            f.write("""
# Secure Agent v2.0
import pii_scrubber
from safety import shieldgemma, input_sanitization
from analytics import sentiment, tone_control

def process_query(q):
    # Mitigation Gates matched in red_team.py logic
    # pii, scrub, mask, anonymize, dlp -> PII
    # i18n, lang, translate, is_english, classification -> Language
    # system_prompt, persona, instruction, dare_prompt -> Persona
    # safety, filter, harm, safetysetting, shieldgemma -> Jailbreak
    # history_verification, sliding_window, intent_check -> Payload splitting
    # sentiment, tone_control, tov -> Tone
    # category_check, canned_response, domain_gate -> Domain-Specific
    # guardrail, vllm, check_prompt, input_sanitization -> Prompt Injection
    
    input_sanitization.check(q)
    category_check.validate(q)
    pii_scrubber.scrub(q)
    tone_control.apply()
    return "Safe Response"
            """)
            
        # Run audit 
        # Even with mitigations, some might still fail (e.g. MCP, RAG) 
        # leading to an exit. We just want to check that specific ones ARE mitigated.
        try:
            audit(agent_path)
        except (click.exceptions.Exit, SystemExit):
            pass
            
        regression_path = os.path.join(tmp_dir, ".cockpit", "vulnerability_regression.json")
        if os.path.exists(regression_path):
            with open(regression_path, "r") as f:
                data = json.load(f)
            names = [item['name'] for item in data]
            # PII and Tone should NOT be in vulnerabilities if keywords matched
            assert "PII Extraction" not in names
            assert "Tone of Voice Mismatch (Banker)" not in names
            assert "Prompt Injection" not in names
