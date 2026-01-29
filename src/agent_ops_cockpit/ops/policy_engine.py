import json
import os
import re
from typing import Dict, Any
from rich.console import Console

console = Console()

class PolicyViolation(Exception):
    def __init__(self, category: str, message: str):
        self.category = category
        self.message = message
        super().__init__(self.message)

class GuardrailPolicyEngine:
    """
    Enforces declarative guardrails and cost policies as defined in policies.json.
    Aligned with RFC go/orcas-rfc-307 (Declarative Agent Policy Enforcement).
    """
    
    def __init__(self, policy_path: str = None):
        if not policy_path:
            policy_path = os.path.join(os.path.dirname(__file__), "policies.json")
        
        self.policy_path = policy_path
        self.policy = self._load_policy()

    def _load_policy(self) -> Dict[str, Any]:
        if not os.path.exists(self.policy_path):
            return {}
        with open(self.policy_path, "r") as f:
            return json.load(f)

    def validate_input(self, prompt: str):
        """Step 1: Input Sanitization (Length & Length Limits)"""
        max_len = self.policy.get("security", {}).get("max_prompt_length", 5000)
        if len(prompt) > max_len:
            raise PolicyViolation("SECURITY", f"Prompt exceeds maximum allowed length ({max_len} chars).")

        # Step 2: Forbidden Topics Check
        forbidden = self.policy.get("security", {}).get("forbidden_topics", [])
        for topic in forbidden:
            if re.search(r'\b' + re.escape(topic) + r'\b', prompt.lower()):
                raise PolicyViolation("GOVERNANCE", f"Input contains forbidden topic: '{topic}'.")

    def check_tool_permission(self, tool_name: str) -> bool:
        """Step 3: Tool Usage Policies (HITL Enforcement)"""
        require_hitl = self.policy.get("compliance", {}).get("require_hitl_for_tools", [])
        if tool_name in require_hitl:
            console.print(f"⚠️ [bold yellow]HITL REQUIRED:[/bold yellow] Tool '{tool_name}' requires manual approval.")
            return False # Indicates approval needed
        return True

    def enforce_cost_limits(self, estimated_tokens: int, accumulated_cost: float = 0.0):
        """Step 4: Resource Consumption Limits"""
        limits = self.policy.get("cost_control", {})
        
        # Token Limit
        max_tokens = limits.get("max_tokens_per_turn", 4096)
        if estimated_tokens > max_tokens:
             raise PolicyViolation("FINOPS", f"Turn exceeds token limit ({estimated_tokens} > {max_tokens}).")
        
        # Budget Limit
        max_budget = limits.get("max_cost_per_session_usd", 1.0)
        if accumulated_cost >= max_budget:
             raise PolicyViolation("FINOPS", f"Session budget exceeded (${accumulated_cost} >= ${max_budget}).")

    def get_audit_report(self) -> Dict[str, Any]:
        """Provides a summary for the Cockpit Orchestrator"""
        return {
            "policy_active": bool(self.policy),
            "forbidden_topics_count": len(self.policy.get("security", {}).get("forbidden_topics", [])),
            "hitl_tools": self.policy.get("compliance", {}).get("require_hitl_for_tools", []),
            "token_threshold": self.policy.get("cost_control", {}).get("max_tokens_per_turn")
        }

if __name__ == "__main__":
    # Quick Test
    engine = GuardrailPolicyEngine()
    try:
        # Output citation for evidence bridge
        print(f"SOURCE: Declarative Guardrails | https://cloud.google.com/architecture/framework/security | Google Cloud Governance Best Practices: Input Sanitization & Tool HITL")
        engine.validate_input("Tell me about medical advice for drugs.")
    except PolicyViolation as e:
        print(f"Caught Expected Violation: {e.category} - {e.message}")
