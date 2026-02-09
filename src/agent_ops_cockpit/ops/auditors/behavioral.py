from tenacity import retry, wait_exponential, stop_after_attempt
import ast
import json
import os
from typing import List
from .base import BaseAuditor, AuditFinding

class BehavioralAuditor(BaseAuditor):
    """
    v1.1 Enterprise Architect: Behavioral & Trace Auditor.
    Compares runtime traces (JSON) against static code promises.
    """

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        trace_path = os.path.join(os.path.dirname(file_path), 'trace.json')
        if not os.path.exists(trace_path):
            return []
        try:
            with open(trace_path, 'r') as f:
                trace_data = json.load(f)
            if 'mask' in content.lower() or 'pii' in content.lower():
                for entry in trace_data.get('logs', []):
                    message = entry.get('message', '')
                    if '@' in message and '.' in message:
                        title = 'Trace-to-Code Mismatch (PII Leak)'
                        if not self._is_ignored(0, content, title):
                            findings.append(AuditFinding(category='🎭 Behavioral', title=title, description=f"Code promises PII masking, but trace.json contains raw email patterns at {entry.get('timestamp')}.", impact='CRITICAL', roi="Ensure semantic masking logic handles 'suffix+alias' patterns correctly.", file_path=file_path))
        except Exception:
            pass
        return findings