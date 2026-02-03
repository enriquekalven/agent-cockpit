import ast
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AuditFinding:
    def __init__(self, category: str, title: str, description: str, impact: str, roi: str, line_number: int = 0, file_path: str = ""):
        self.category = category
        self.title = title
        self.description = description
        self.impact = impact
        self.roi = roi
        self.line_number = line_number
        self.file_path = file_path

class BaseAuditor(ABC):
    @abstractmethod
    def audit(self, tree: ast.AST, content: str, file_path: str) -> List[AuditFinding]:
        pass

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
