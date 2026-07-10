try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v2.0.7 Cockpit Alignment: Optimized for AWS App Runner (Bedrock)
import re
from typing import Any, Dict

from rich.console import Console

console = Console()


class PIIScrubber:
    """
    Standard AgentOps PII Scrubber.
    Detects and masks sensitive information before it reaches the LLM.
    """

    PATTERNS = {
        "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
        "PHONE": r"\b(?:\+?1[-. ]?)?\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4})\b",
        "CREDIT_CARD": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|(?:4[0-9]{3}|5[1-5][0-9]{2})[- ]?[0-9]{4}[- ]?[0-9]{4}[- ]?[0-9]{4})\b",
        "SSN": r"\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b",
        "IPV4": r"\b(?<!\.)(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b(?!\.)",
        "AWS_KEY": r"\bAKIA[A-Z0-9]{16}\b",
        "STRIPE_KEY": r"\bsk_live_[0-9a-zA-Z]{24,}\b",
        "GCP_KEY": r"\"private_key\"\s*:\s*\"-----BEGIN\s+PRIVATE\s+KEY-----",
        "OPENAI_KEY": r"\bsk-[a-zA-Z0-9]{20,}\b",
    }

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def scrub(self, text: str) -> str:
        """Scan and mask patterns in the text."""
        if not self.enabled:
            return text

        scrubbed_text = text
        for label, pattern in self.PATTERNS.items():
            scrubbed_text = re.sub(
                pattern, f"[[MASKED_{label}]]", scrubbed_text
            )

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
