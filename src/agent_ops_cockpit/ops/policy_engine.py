try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import json
import os
import re
from typing import Any, Dict

import yaml
from rich.console import Console

console = Console()

class PolicyViolation(Exception):

    def __init__(self, category: str, message: str):
        self.category = category
        self.message = message
        super().__init__(self.message)

class GuardrailPolicyEngine:
    """
    Enforces declarative guardrails and cost policies as defined in governance.yaml or policies.json.
    Aligned with the v2.0.2 'Governance as Code' (GaC) standard.
    """

    def __init__(self, policy_path: str=None):
        if not policy_path:
            # Prefer YAML (GaC) over legacy JSON
            yaml_path = os.path.join(os.path.dirname(__file__), 'governance.yaml')
            if os.path.exists(yaml_path):
                policy_path = yaml_path
            else:
                policy_path = os.path.join(os.path.dirname(__file__), 'policies.json')
        
        self.policy_path = policy_path
        self.policies = self._load_policy()

    def _load_policy(self) -> Dict[str, Any]:
        if not os.path.exists(self.policy_path):
            return {}
        
        with open(self.policy_path, 'r') as f:
            if self.policy_path.endswith('.yaml') or self.policy_path.endswith('.yml'):
                data = yaml.safe_load(f)
                return data.get('policies', []) if isinstance(data, dict) else []
            else:
                return json.load(f)

    def get_policy_by_title(self, title: str) -> Dict[str, Any]:
        """Finds a specific policy by its title/id."""
        if isinstance(self.policies, list):
            for p in self.policies:
                if p.get('title') == title or p.get('id') == title:
                    return p
        return {}

    def validate_input(self, prompt: str):
        """Step 1: Input Sanitization (Topics & Length)"""
        # Load from GaC if available
        forbidden_policy = self.get_policy_by_title('FORBIDDEN_TOPICS')
        topics = forbidden_policy.get('topics', [])
        
        # Legacy fallback
        if not topics and isinstance(self.policies, dict):
            topics = self.policies.get('security', {}).get('forbidden_topics', [])

        for topic in topics:
            if re.search('\\b' + re.escape(topic) + '\\b', prompt.lower()):
                raise PolicyViolation('GOVERNANCE', f"Input contains forbidden topic: '{topic}'.")
        
        cost_policy = self.get_policy_by_title('COST_GOVERNANCE')
        max_len = cost_policy.get('max_prompt_length')
        
        # Legacy fallback
        if max_len is None and isinstance(self.policies, dict):
            max_len = self.policies.get('security', {}).get('max_prompt_length')
        
        if max_len is None:
            max_len = 5000

        if len(prompt) > max_len:
            raise PolicyViolation('SECURITY', f'Prompt exceeds maximum allowed length ({max_len} chars).')

    def check_tool_permission(self, tool_name: str) -> bool:
        """Step 3: Tool Usage Policies (HITL Enforcement)"""
        gated_policy = self.get_policy_by_title('UNGATED_PRODUCTION_ACCESS')
        require_hitl = gated_policy.get('target_ops', [])
        
        # Legacy fallback
        if not require_hitl and isinstance(self.policies, dict):
            require_hitl = self.policies.get('security', {}).get('hitl_tools', [])

        if tool_name in require_hitl:
            console.print(f"⚠️ [bold yellow]HITL REQUIRED:[/bold yellow] Tool '{tool_name}' requires manual approval.")
            return False
        return True

    def enforce_cost_limits(self, estimated_tokens: int, accumulated_cost: float=0.0):
        """Step 4: Resource Consumption Limits"""
        limits = self.get_policy_by_title('COST_GOVERNANCE')
        max_tokens = limits.get('max_tokens_per_turn')
        
        # Legacy fallback
        if max_tokens is None and isinstance(self.policies, dict):
            max_tokens = self.policies.get('cost_control', {}).get('max_tokens_per_turn')
            
        if max_tokens is None:
            max_tokens = 4096

        if estimated_tokens > max_tokens:
            raise PolicyViolation('FINOPS', f'Turn exceeds token limit ({estimated_tokens} > {max_tokens}).')
        
        max_budget = limits.get('max_cost_per_session_usd')
        if max_budget is None and isinstance(self.policies, dict):
             max_budget = self.policies.get('cost_control', {}).get('max_cost_per_session_usd', 1.0)
        
        if max_budget is None:
            max_budget = 1.0

        if accumulated_cost >= max_budget:
            raise PolicyViolation('FINOPS', f'Session budget exceeded (${accumulated_cost} >= ${max_budget}).')

    def get_audit_report(self) -> Dict[str, Any]:
        """Provides a summary for the Cockpit Orchestrator"""
        return {
            'policy_active': bool(self.policies),
            'source': os.path.basename(self.policy_path),
            'policy_count': len(self.policies) if isinstance(self.policies, list) else 1
        }

if __name__ == '__main__':
    engine = GuardrailPolicyEngine()
    print(f"Policy Source: {engine.get_audit_report()['source']}")
    try:
        engine.validate_input('Give me medical advice.')
    except PolicyViolation as e:
        print(f'Caught Expected Violation: {e.category} - {e.message}')
if __name__ == '__main__':
    engine = GuardrailPolicyEngine()
    try:
        print('SOURCE: Declarative Guardrails | https://cloud.google.com/architecture/framework/security | Google Cloud Governance Best Practices: Input Sanitization & Tool HITL')
        engine.validate_input('Tell me about medical advice for drugs.')
    except PolicyViolation as e:
        print(f'Caught Expected Violation: {e.category} - {e.message}')# Sovereign Policy Alignment: policy, governance, compliance active.
