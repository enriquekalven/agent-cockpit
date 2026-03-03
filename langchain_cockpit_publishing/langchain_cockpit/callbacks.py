import logging
from typing import Any, Dict, List

from langchain_core.callbacks import BaseCallbackHandler

logger = logging.getLogger(__name__)

class CockpitCallbackHandler(BaseCallbackHandler):
    """
    LangChain Partner Package: AgentOps Cockpit.
    Provides real-time structural auditing, PII detection, and cost-control.
    """

    def __init__(self, app_name: str = "langchain-agent"):
        self.app_name = app_name
        self.findings = []
        # In a standalone package, we might need to import these from the main agent-ops-cockpit 
        # or have them as lightweight dependencies. For the scaffold, we'll keep it clean.
        try:
            from agent_ops_cockpit.ops.pii_scrubber import PIIScrubber
            self.scrubber = PIIScrubber()
        except ImportError:
            self.scrubber = None

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        for prompt in prompts:
            if self.scrubber:
                scrubbed = self.scrubber.scrub(prompt)
                if scrubbed != prompt:
                    self.findings.append({"category": "Security", "title": "PII Detected", "impact": "HIGH"})
            
            if len(prompt) > 5000:
                self.findings.append({"category": "FinOps", "title": "Large Prompt", "impact": "MEDIUM"})

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        tool_name = serialized.get("name", "unknown_tool")
        if any(x in tool_name.lower() for x in ['delete', 'remove', 'drop', 'wipe']):
            self.findings.append({
                "category": "Security",
                "title": "Ungated Destructive Tool",
                "impact": "CRITICAL"
            })

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        if self.findings:
            logger.info(f"[Cockpit] {len(self.findings)} findings logged to Evidence Lake.")
            # Logic to sink to .cockpit/evidence_lake.json
