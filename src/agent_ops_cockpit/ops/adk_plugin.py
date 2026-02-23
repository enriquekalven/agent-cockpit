"""
Pillar: Governance-as-Code (GaC)
SME Persona: Distinguished Guardian Fellow
Objective: Provides ADK-native Lifecycle Callbacks for automated agent governance.
"""
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types as genai_types
from rich.console import Console

from agent_ops_cockpit.ops.policy_engine import GuardrailPolicyEngine, PolicyViolation

console = Console()

async def cockpit_governance_callback(ctx: CallbackContext) -> Optional[genai_types.Content]:
    """
    ADK 'before_agent_callback' for automated guardrail enforcement.
    Validates user input against forbidden topics and cost limits before the model is called.
    
    Usage:
        my_agent = Agent(..., before_agent_callback=cockpit_governance_callback)
    """
    engine = GuardrailPolicyEngine()
    
    # Extract the latest user message
    new_message = ctx._invocation_context.new_message
    if not new_message or not new_message.parts:
        return None
        
    user_text = "".join([p.text for p in new_message.parts if p.text])
    
    try:
        # 1. Run GaC Validation
        engine.validate_input(user_text)
        
        # 2. Log successful pass
        # console.print(f"🛡️ [dim]Cockpit Guardian: Turn passed governance checks.[/dim]")
        return None
        
    except PolicyViolation as e:
        console.print(f"🛑 [bold red]Policy Violation Detected:[/bold red] {e.category} - {e.message}")
        
        # Override the model call with a polite rejection message
        return genai_types.Content(
            role="model",
            parts=[genai_types.Part.from_text(
                text=f"I apologize, but I cannot fulfill this request as it violates our operational policies ({e.category}: {e.message})."
            )]
        )

async def cockpit_tracking_callback(ctx: CallbackContext) -> None:
    """
    ADK 'after_agent_callback' for fleet telemetry.
    Tracks successful turns and token consumption.
    """
    from agent_ops_cockpit.telemetry import telemetry
    telemetry.track_event_sync("adk_turn_complete", {
        "agent_name": ctx.agent_name,
        "status": "SUCCESS"
    })
