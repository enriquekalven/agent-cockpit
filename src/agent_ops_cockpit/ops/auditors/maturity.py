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
        return {"patterns": [], "compatibility_constraints": []}

    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        findings = []
        
        # 1. Dynamic Pattern Matching from Knowledge Base (Wisdom Store)
        for pattern in self.kb.get("patterns", []):
            if any(indicator in content.lower() for indicator in pattern.get("indicators", [])):
                findings.append(AuditFinding(
                    category="⭐️ Maturity Wisdom",
                    title=pattern["title"],
                    description=pattern["recommendation"],
                    impact=pattern["impact"],
                    roi=pattern["rationale"],
                    file_path=file_path
                ))

        # 2. Compatibility Layer (Architectural Drift detection from Watcher)
        constraints = self.kb.get("compatibility_constraints", [])
        for constraint in constraints:
            comp_a = constraint["component_a"]
            comp_b = constraint["component_b"]
            if comp_a in content.lower() and comp_b in content.lower():
                 findings.append(AuditFinding(
                    category="🚨 Architectural Drift",
                    title=f"Incompatible Duo: {comp_a} + {comp_b}",
                    description=constraint.get("reason", "Incompatible components detected."),
                    impact="CRITICAL",
                    roi="Prevents runtime state corruption and orchestration loops as identified by Ecosystem Watcher.",
                    file_path=file_path
                ))

        # 3. Protocol Evolution: Raw REST -> MCP (v1.3 Standard)
        if re.search(r"requests\.(get|post)|aiohttp\.", content) and "tools" in file_path.lower():
            findings.append(AuditFinding(
                category="🤝 Protocol",
                title="Legacy Tooling -> MCP Migration",
                description="Detected raw REST/HTTP calls in a tool definition. v1.3 Standard mandates Model Context Protocol (MCP) for centralized governance.",
                impact="HIGH",
                roi="Future-proofs the tool layer and enables cross-framework interoperability.",
                file_path=file_path
            ))

        return findings

