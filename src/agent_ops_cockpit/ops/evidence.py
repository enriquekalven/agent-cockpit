from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class EvidenceNode(BaseModel):
    """A single piece of evidence or source used by the agent."""
    source_id: str
    source_type: str  # e.g., "doc", "web", "tool_query"
    snippet: str
    relevance_score: float = Field(ge=0.0, le=1.0)

class AgentEvidencePacket(BaseModel):
    """
    Standard 'Evidence Packet' format. 
    Ensures every agent response has a clear, auditable trail of information.
    """
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    reasoning_path: List[str] = Field(default_factory=list)
    sources: List[EvidenceNode] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    token_usage: Optional[Dict[str, int]] = None

def pack_evidence(response_data: Dict[str, Any]) -> AgentEvidencePacket:
    """Utility to formalize agent debug data into a sharable evidence packet."""
    return AgentEvidencePacket(**response_data)
