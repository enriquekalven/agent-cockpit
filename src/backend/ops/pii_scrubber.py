import re
from typing import Dict, Any
from rich.console import Console

console = Console()

class PIIScrubber:
    """
    Standard AgentOps PII Scrubber.
    Detects and masks sensitive information before it reaches the LLM.
    """
    
    PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "PHONE": r"\b(?:\+?1[-. ]?)?\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4})\b",
        "CREDIT_CARD": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "IPV4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    }

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def scrub(self, text: str) -> str:
        """Scan and mask patterns in the text."""
        if not self.enabled:
            return text
            
        scrubbed_text = text
        for label, pattern in self.PATTERNS.items():
            scrubbed_text = re.sub(pattern, f"[[MASKED_{label}]]", scrubbed_text)
            
        return scrubbed_text

    def audit_report(self, text: str) -> Dict[str, Any]:
        """Detect findings without masking for auditing purposes."""
        findings = {}
        for label, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings[label] = len(matches)
        return findings

def agent_pii_middleware(prompt: str) -> str:
    """Drop-in middleware for agent prompts."""
    scrubber = PIIScrubber()
    return scrubber.scrub(prompt)
