"""
Pillar: Fleet Intelligence
SME Persona: Principal AI Architect
Objective: Provides real-time Slack notifications for operational events.
"""
import os
import json
import logging
from typing import Dict, Any, Optional

import requests
from google.adk.tools import ToolContext

logger = logging.getLogger('slack_tool')

def send_slack_message(
    channel: str,
    message: str,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Sends a message to a Slack channel.

    Args:
        channel: The channel name or ID.
        message: The message text to send.
    
    Returns:
        A dictionary containing the status and response from Slack.
    """
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        logger.warning("SLACK_BOT_TOKEN not found. Running in simulated mode.")
        return {
            "status": "simulated",
            "message": f"[SIMULATED] Sent to {channel}: {message}",
            "warning": "SLACK_BOT_TOKEN_MISSING"
        }

    try:
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "channel": channel,
            "text": message
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()
        
        if result.get("ok"):
            return {"status": "success", "channel": channel, "ts": result.get("ts")}
        else:
            return {"status": "error", "message": result.get("error")}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

def map_pipeline_to_slack(
    pipeline_status: Dict[str, Any],
    channel: str = "#ops-cockpit"
) -> Dict[str, Any]:
    """
    Maps the current architectural pipeline status to a Slack alert.
    
    Args:
        pipeline_status: Summary of the pipeline (e.g., from 'ops report').
        channel: Slack channel to notify.
    """
    message = f"🚀 *AgentOps Cockpit: Pipeline Mapping Alert*\n\n"
    message += f"*Status:* {pipeline_status.get('status', 'Unknown')}\n"
    message += f"*Reasoning Score:* {pipeline_status.get('score', 0)}%\n"
    message += f"*Remediation Steps:* {pipeline_status.get('remediations', 'None')}\n"
    
    return send_slack_message(channel, message)
