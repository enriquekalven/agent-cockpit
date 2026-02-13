"""
Pillar: Governance & Structural Wisdom
SME Persona: Distinguished Semantic Fellow
Objective: Provides base primitives for all auditing logic within the AgentOps Cockpit.
"""
from tenacity import retry, wait_exponential, stop_after_attempt
try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

import ast
import re
from abc import ABC, abstractmethod
from typing import List, Optional

class AuditFinding:
    """
    Representation of a single architectural or tactical finding.
    
    Attributes:
        category: The hub category (Security, FinOps, Architecture, etc.)
        title: Short descriptive title of the issue.
        description: Detailed explanation and strategic move.
        impact: Qualitative assessment of the risk (LOW, MEDIUM, HIGH, CRITICAL).
        roi: The business value or technical gain from fixing the issue.
        line_number: Source code line where the issue was detected.
        file_path: Absolute or relative path to the file.
        severity: Quantitative urgency for remediation.
    """
    def __init__(
        self, 
        category: str, 
        title: str, 
        description: str, 
        impact: str, 
        roi: str, 
        line_number: int = 0, 
        file_path: str = "", 
        severity: str = "MEDIUM"
    ):
        self.category = category
        self.title = title
        self.description = description
        self.impact = impact
        self.roi = roi
        self.line_number = line_number
        self.file_path = file_path
        self.severity = severity

class BaseAuditor(ABC):
    """
    Abstract base class for all Cockpit auditors.
    Enforces a standardized interface for AST and heuristic-based scanning.
    """
    @abstractmethod
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        """
        Performs the audit logic and returns a list of findings.
        
        Args:
            tree: The parsed Abstract Syntax Tree of the file.
            content: The raw string content of the file.
            file_path: The path to the file being audited.
        """
        pass

    def _is_ignored(self, line_number: int, content: str, title: str) -> bool:
        """
        Check if a finding on a specific line is ignored via '# cockpit-ignore'.
        Example: # cockpit-ignore: hardcoded-secret intentional-testing
        """
        lines = content.splitlines()
        # Clean title to create a reliable slug
        clean_title = re.sub(r"[^a-zA-Z0-9\s]", "", title.lower())
        issue_slug = clean_title.replace(" ", "-")

        # 1. Check for whole-file ignores (in the first 10 lines)
        for i in range(min(10, len(lines))):
            if "# cockpit-ignore" in lines[i]:
                comment_part = lines[i].split("# cockpit-ignore")[1].lower()
                # Check for "all" or if ANY part of the slug is in the comment
                if "all" in comment_part:
                    return True
                # Match against the slug or potential keywords
                for word in issue_slug.split("-"):
                    if word and len(word) > 3 and word in comment_part:
                        return True
                if issue_slug in comment_part:
                    return True

        if not line_number or line_number > len(lines):
            return False
            
        # 2. Check for inline ignore on the specific line
        target_line = lines[line_number - 1]
        if "# cockpit-ignore" in target_line:
            comment_part = target_line.split("# cockpit-ignore")[1].lower()
            if "all" in comment_part:
                return True
            for word in issue_slug.split("-"):
                if word and len(word) > 3 and word in comment_part:
                    return True
            if issue_slug in comment_part:
                return True
        return False

class SymbolScanner(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.functions = []
        self.classes = []
        self.assignments = []
        self.calls = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.imports.append(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.append(node.func.attr)
        self.generic_visit(node)
