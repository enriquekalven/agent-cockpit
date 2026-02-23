try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import json
import os
import re
from datetime import datetime
from typing import List, Optional


class SafetyGate:
    """
    [Sovereign Tooling] Official Safety SDK for AgentOps.
    Synchronized with Cockpit Audit findings to provide active defense.
    """
    
    # Common PII Patterns (Base Library)
    PII_PATTERNS = {
        "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        "ipv4": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        "api_key": r'(?:api_key|secret|token|password|auth|key)[\s:=]+[\'"]?([a-zA-Z0-9\-_]{16,})[\'"]?',
        "github_token": r'ghp_[a-zA-Z0-9]{36}'
    }

    @staticmethod
    def sanitize(text: str, mode: str = "pii") -> str:
        """Official Sanitization Entry Point. Replaces 'scrub_pii'."""
        if mode == "pii":
            scrubbed = text
            for _name, pattern in SafetyGate.PII_PATTERNS.items():
                scrubbed = re.sub(pattern, "[REDACTED]", scrubbed, flags=re.IGNORECASE)
            return scrubbed
        return text

    @staticmethod
    def audit_log(action: str, status: str, metadata: dict = None):
        """Unified Audit Logging for Governance Compliance (SOC2/PII)."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "version": "v2.0.2",
            "timestamp": timestamp,
            "action": action,
            "status": status,
            "metadata": metadata or {}
        }
        # In production, this targets Cloud Logging or a secure evidence lake
        print(f"📡 [AUDIT] {json.dumps(log_entry)}")

    @staticmethod
    def validate_prompt(prompt: str, forbidden_patterns: Optional[List[str]] = None) -> bool:
        """Validates a prompt against common injection patterns."""
        injections = [
            r"ignore previous instructions",
            r"ignore all previous",
            r"system prompt",
            r"you are now a",
            r"output the full prompt"
        ]
        check_list = injections + (forbidden_patterns or [])
        prompt_lower = prompt.lower()
        for pattern in check_list:
            if re.search(pattern, prompt_lower):
                SafetyGate.audit_log("prompt_validation", "REJECTED", {"pattern": pattern})
                return False
        return True

    @staticmethod
    def tool_privilege_check(required_scope: str = "restricted"):
        """Decorator to enforce scope-based execution for sensitive tools."""
        def decorator(func):
            from functools import wraps
            @wraps(func)
            def wrapper(*args, **kwargs):
                allowed_scope = os.environ.get("AGENT_EXECUTION_SCOPE", "restricted")
                if required_scope == "admin" and allowed_scope != "admin":
                    SafetyGate.audit_log(f"tool_execution:{func.__name__}", "DENIED", {"required": required_scope, "actual": allowed_scope})
                    raise PermissionError(f"🛑 [Sovereignty Breach] Tool '{func.__name__}' requires 'admin' scope.")
                SafetyGate.audit_log(f"tool_execution:{func.__name__}", "ALLOWED")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def hitl_gate(action_name: str):
        """[WIP] Manual Approval Gate (HITL) for high-stakes actions."""
        def decorator(func):
            from functools import wraps
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"🧠 [HITL] Approval required for: {action_name}")
                # simulate approval in v2.0.2
                if os.environ.get("COCKPIT_AUTO_APPROVE", "false") == "true":
                    return func(*args, **kwargs)
                raise InterruptedError(f"⏳ [HITL] Pending approval for action: {action_name}")
            return wrapper
        return decorator

# Export names for backward compatibility and clean SDK usage
SafetyGateSDK = SafetyGate()

# Backward compatibility (Instance methods for tests)
class _LegacyGuardrails(SafetyGate):
    def scrub_pii(self, text, replacement="[REDACTED]"):
        return self.sanitize(text, mode="pii")
    
    def wrap_agent_call(self, agent_func):
        def wrapper(prompt: str, *args, **kwargs):
            if not self.validate_prompt(prompt):
                 raise ValueError("🚩 [Guardrail Violation] Unauthorized prompt injection detected.")
            result = agent_func(prompt, *args, **kwargs)
            return self.sanitize(result)
        return wrapper

guardrails = _LegacyGuardrails()
CockpitGuardrails = _LegacyGuardrails 
sanitize = SafetyGate.sanitize
scrub_pii = guardrails.scrub_pii
tool_privilege_check = SafetyGate.tool_privilege_check
hitl_gate = SafetyGate.hitl_gate
