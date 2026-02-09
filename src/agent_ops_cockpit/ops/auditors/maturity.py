from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
import ast
import json
import os
import re
from typing import List
from .base import BaseAuditor, AuditFinding
PATTERNS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'maturity_patterns.json')

class MaturityAuditor(BaseAuditor):
    """
    v1.3 Principal SME: Architecture Maturity & Consolidation Judge.
    Dynamically loads architectural patterns from the Maturity Wisdom Store.
    """

    def __init__(self):
        self.kb = self._load_knowledge_base()

    def _load_knowledge_base(self):
        try:
            if os.path.exists(PATTERNS_PATH):
                with open(PATTERNS_PATH, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'patterns': [], 'compatibility_constraints': []}

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        for pattern in self.kb.get('patterns', []):
            # Framework-Native Detection: Suppress orchestration advice if already present
            if pattern['id'] == 'MP-014' and any(kw in content.lower() for kw in ['stategraph', 'crewai', 'agent(role=', 'workflow']):
                continue
                
            if any((indicator.lower() in content.lower() for indicator in pattern.get('indicators', []))):
                findings.append(AuditFinding(category='⭐️ Maturity Wisdom', title=pattern['title'], description=pattern['recommendation'], impact=pattern['impact'], roi=pattern['rationale'], file_path=file_path))
        constraints = self.kb.get('compatibility_constraints', [])
        for constraint in constraints:
            comp_a = constraint['component_a']
            comp_b = constraint['component_b']
            if comp_a in content.lower() and comp_b in content.lower():
                findings.append(AuditFinding(category='🚨 Architectural Drift', title=f'Incompatible Duo: {comp_a} + {comp_b}', description=constraint.get('reason', 'Incompatible components detected.'), impact='CRITICAL', roi='Prevents runtime state corruption and orchestration loops as identified by Ecosystem Watcher.', file_path=file_path))
        if re.search('requests\\.(get|post)|aiohttp\\.', content) and 'tools' in file_path.lower():
            findings.append(AuditFinding(category='🤝 Protocol', title='Legacy Tooling -> MCP Migration', description='Detected raw REST/HTTP calls in a tool definition. v1.3 Standard mandates Model Context Protocol (MCP) for centralized governance.', impact='HIGH', roi='Future-proofs the tool layer and enables cross-framework interoperability.', file_path=file_path))
        return findings