try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import re
import os
from typing import List, Optional

class CockpitGuardrails:
    """
    Recommendation #1: Standardized 'Guardrail' Middleware.
    Provides verified patterns for PII scrubbing, prompt validation, and safety.
    """
    
    # Common PII Patterns (Base Library)
    PII_PATTERNS = {
        "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        "ipv4": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        "api_key": r'(?:api_key|secret|token|password|auth|key)[\s:=]+[\'"]?([a-zA-Z0-9\-_]{16,})[\'"]?',
        "github_token": r'ghp_[a-zA-Z0-9]{36}'
    }

    @staticmethod
    def scrub_pii(text: str, replacement: str = "[REDACTED]") -> str:
        """Scrubs common PII from the provided text."""
        scrubbed = text
        for name, pattern in CockpitGuardrails.PII_PATTERNS.items():
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        return scrubbed

    @staticmethod
    def validate_prompt(prompt: str, forbidden_patterns: Optional[List[str]] = None) -> bool:
        """
        Validates a prompt against common injection patterns or custom forbidden topics.
        Returns True if safe, False if a violation is detected.
        """
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
                return False
        return True

    @staticmethod
    def wrap_agent_call(agent_func):
        """
        Higher-Order Decorator for Agent Calls.
        Automatically applies PII scrubbing and prompt validation.
        """
        def wrapper(prompt: str, *args, **kwargs):
            if not CockpitGuardrails.validate_prompt(prompt):
                 raise ValueError("🚩 [Guardrail Violation] Unauthorized prompt injection detected.")
            
            result = agent_func(prompt, *args, **kwargs)
            return CockpitGuardrails.scrub_pii(result)
        return wrapper

    @staticmethod
    def tool_privilege_check(required_scope: str = "restricted"):
        """
        [Sovereign Governance] Decorator to enforce scope-based execution for sensitive tools.
        Prevents 'Lateral Movement' by verifying environment-level permissions before execution.
        """
        def decorator(func):
            from functools import wraps
            @wraps(func)
            def wrapper(*args, **kwargs):
                # In a real scenario, this would check against a secure vault or session context
                # For v2.0.2, we implement a 'Sovereign Check' against environment variables
                allowed_scope = os.environ.get("AGENT_EXECUTION_SCOPE", "restricted")
                if required_scope == "admin" and allowed_scope != "admin":
                    raise PermissionError(f"🛑 [Sovereignty Breach] Tool '{func.__name__}' requires 'admin' scope. Current scope: '{allowed_scope}'.")
                return func(*args, **kwargs)
            return wrapper
        return decorator

# Export singleton for easy import
guardrails = CockpitGuardrails()
tool_privilege_check = CockpitGuardrails.tool_privilege_check
