from llama_index.core.callbacks import BaseCallbackHandler, CBEventType, EventPayload
from typing import Any, Dict, List, Optional
import logging
from agent_ops_cockpit.ops.pii_scrubber import PIIScrubber

logger = logging.getLogger(__name__)

class CockpitLlamaIndexCallbackHandler(BaseCallbackHandler):
    """
    Sovereign Integration for LlamaIndex.
    Monitors data retrieval and PII leakage in query engines.
    """
    def __init__(self, app_name: str = "llamaindex-agent"):
        super().__init__(event_starts_to_ignore=[], event_ends_to_ignore=[])
        self.app_name = app_name
        self.scrubber = PIIScrubber()
        self.findings = []

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        # 1. LLM/Prompt Auditing (ASI-01: Prompt Injection)
        if event_type == CBEventType.LLM:
            prompts = payload.get(EventPayload.PROMPTS, [])
            for prompt in prompts:
                scrubbed = self.scrubber.scrub(str(prompt))
                if scrubbed != str(prompt):
                    logger.warning(f"[Cockpit] PII detected in LlamaIndex LLM call")
                    self.findings.append({
                        "category": "🛡️ Security", 
                        "title": "ASI-06: PII in Query Engine", 
                        "impact": "HIGH",
                        "description": "Sensitive data detected in contextual retrieval prompt."
                    })

        # 2. Functional Tool Auditing (ASI-02 / ASI-04)
        if event_type == CBEventType.FUNCTION_CALL:
            tool_name = payload.get(EventPayload.TOOL, {}).get("name", "unknown_tool")
            
            # Destructive Action detection
            if any(x in tool_name.lower() for x in ['delete', 'remove', 'drop', 'wipe', 'terminate']):
                self.findings.append({
                    "category": "🛡️ Security",
                    "title": "ASI-02: Ungated Destructive Query",
                    "impact": "CRITICAL",
                    "description": f"LlamaIndex Tool '{tool_name}' performs destructive operations without a HITL gate."
                })

            # MCP / System Access detection
            if any(x in tool_name.lower() for x in ['mcp', 'shell', 'exec', 'system']):
                self.findings.append({
                    "category": "🛡️ Security",
                    "title": "ASI-04: Excess Agency in Query Path",
                    "impact": "HIGH",
                    "description": "Tool provides direct system access via LlamaIndex. Mitigation: Sandbox required."
                })

        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        pass

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        pass

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        if self.findings:
             logger.info(f"[Cockpit] Audit complete for {self.app_name}. Syncing {len(self.findings)} snippets to Evidence Lake.")
             
             # Save to evidence lake
             lake_path = ".cockpit/evidence_lake.json"
             import os, json
             if not os.path.exists(".cockpit"):
                 os.makedirs(".cockpit", exist_ok=True)
                 
             try:
                 data = []
                 if os.path.exists(lake_path):
                     with open(lake_path, 'r') as f:
                         try:
                             content = json.load(f)
                             data = content if isinstance(content, list) else [content]
                         except: data = []
                 
                 data.append({
                     "timestamp": "v2.0.4-llamaindex",
                     "app": self.app_name,
                     "findings": self.findings
                 })
                 
                 with open(lake_path, 'w') as f:
                     json.dump(data, f, indent=2)
             except Exception as e:
                 logger.error(f"[Cockpit] Evidence Lake Sink Failure: {e}")
