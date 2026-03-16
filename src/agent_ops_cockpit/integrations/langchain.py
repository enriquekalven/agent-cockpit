try:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.outputs import LLMResult
except ImportError:
    # Graceful fallback for non-langchain environments
    class BaseCallbackHandler: pass
    class LLMResult: pass

import json
import logging
from typing import Any, Dict, List

from agent_ops_cockpit.ops.auditors.finops import FinOpsAuditor
from agent_ops_cockpit.ops.auditors.security import SecurityAuditor
from agent_ops_cockpit.ops.pii_scrubber import PIIScrubber

logger = logging.getLogger(__name__)

class CockpitCallbackHandler(BaseCallbackHandler):
    """
    v2.0.4 Cockpit Integration: LangChain Callback Handler.
    Provides real-time structural auditing, PII detection, and cost-control 
    within LangChain and LangGraph workflows.
    """

    def __init__(self, app_name: str = "langchain-agent", project_path: str = "."):
        self.app_name = app_name
        self.project_path = project_path
        self.scrubber = PIIScrubber()
        self.security_auditor = SecurityAuditor()
        self.finops_auditor = FinOpsAuditor()
        self.findings = []

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Check prompts for PII and policy violations before they reach the LLM."""
        for prompt in prompts:
            # 1. PII Probe
            scrubbed = self.scrubber.scrub(prompt)
            if scrubbed != prompt:
                logger.warning(f"[Cockpit] PII detected in prompt for {self.app_name}")
                self.findings.append({
                    "category": "🛡️ Security",
                    "title": "PII Leakage in Chain Prompt",
                    "impact": "HIGH"
                })

            # 2. Paradigm Audit (Simplified)
            if len(prompt) > 5000:
                self.findings.append({
                    "category": "💰 FinOps",
                    "title": "Prompt Saturation",
                    "impact": "MEDIUM",
                    "description": "Large prompt detected. Consider Context Caching."
                })

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        """Verify tool calls for blast-radius risks, including MCP tools."""
        tool_name = serialized.get("name", "unknown_tool")
        
        # 1. Structural destructive check
        if any(x in tool_name.lower() for x in ['delete', 'remove', 'drop', 'wipe', 'terminate']):
            logger.warning(f"[Cockpit] High-risk tool detected: {tool_name}")
            self.findings.append({
                "category": "🛡️ Security",
                "title": "ASI-02: Ungated Destructive Tool",
                "impact": "CRITICAL",
                "description": f"Tool '{tool_name}' lacks a HITL gate or approval logic."
            })
            
        # 2. MCP Lateral Movement check (ASI-04)
        if 'mcp' in tool_name.lower() or 'shell' in tool_name.lower() or 'exec' in tool_name.lower():
            self.findings.append({
                "category": "🛡️ Security",
                "title": "ASI-04: Potentially Over-privileged Tool (MCP/Shell)",
                "impact": "HIGH",
                "description": f"Tool '{tool_name}' performs system-level operations. Ensure it is sandboxed."
            })

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Generate a final audit event for the Cockpit evidence lake."""
        if self.findings:
            # In a production scenario, we would write this to .cockpit/evidence_lake.json
            logger.info(f"[Cockpit] Audit complete for {self.app_name}. {len(self.findings)} findings generated.")
            
            # Save findings to evidence lake
            lake_path = ".cockpit/evidence_lake.json"
            import os
            if not os.path.exists(".cockpit"):
                os.makedirs(".cockpit", exist_ok=True)
                
            try:
                data = []
                if os.path.exists(lake_path):
                    with open(lake_path, 'r') as f:
                        try:
                            content = json.load(f)
                            if isinstance(content, list):
                                data = content
                            else:
                                # If it's a dict (audit report style), wrap it or start fresh
                                logger.info("[Cockpit] Evidence lake is a dict, starting fresh list.")
                                data = [content]
                        except json.JSONDecodeError:
                            data = []
                
                data.append({
                    "timestamp": "v2.0.4-audit",
                    "app": self.app_name,
                    "findings": self.findings
                })
                
                with open(lake_path, 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                logger.error(f"[Cockpit] Failed to write to Evidence Lake: {e}")
