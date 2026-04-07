"""
Pillar: Governance & Structural Wisdom
SME Persona: Distinguished Semantic Fellow
Objective: Provides base primitives for all auditing logic within the AgentOps Cockpit.
"""
try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

import ast
import re
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, Field


class AuditFinding(BaseModel):
    """
    Representation of a single architectural or tactical finding.
    Now serialized using Pydantic for robust Inter-Process Communication (IPC).
    """
    category: str = Field(description="The hub category (Security, FinOps, Architecture, etc.)")
    title: str = Field(description="Short descriptive title of the issue.")
    description: str = Field(description="Detailed explanation and strategic move.")
    impact: str = Field(default="MEDIUM", description="Qualitative assessment of the risk.")
    roi: str = Field(default="N/A", description="The business value or technical gain.")
    line_number: int = Field(default=0, description="Source code line where the issue was detected.")
    file_path: str = Field(default="", description="Path to the file.")
    severity: str = Field(default="MEDIUM", description="Quantitative urgency for remediation.")

    def emit_ipc(self):
        """Prints the JSON representation for the orchestrator to parse, alongside the legacy string fallback."""
        payload = self.model_dump_json()
        print(f"ACTION: {self.file_path}:{self.line_number or 1} | {self.title} | {self.description} | IPC_PAYLOAD: {payload}")


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

    def semantic_verify(self, code_snippet: str, objective: str) -> bool:
        """
        v2.0.7 Semantic Compliance (Beyond Regex): 
        Uses a Policy SME model to verify if the code functionally meets a security objective.
        """
        try:
            from google.adk.agents import Agent
            from google.genai import types as genai_types
            
            # Lightweight Policy SME
            sme = Agent(
                name="policy_sme",
                model="gemini-2.0-flash",
                instruction=f"You are a Distinguished Security SME. Your task is to verify if the following code functionally achieves the objective: '{objective}'."
            )
            
            prompt = f"Objective: {objective}\n\nCode:\n```python\n{code_snippet}\n```\n\nDoes this code functionally achieve the objective? Answer only 'YES' or 'NO'."
            # This is a synchronous-wrapped call for an auditor environment
            import asyncio

            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            
            async def _check():
                session_service = InMemorySessionService()
                await session_service.create_session("cockpit", "system", "audit_turn")
                runner = Runner(agent=sme, app_name="cockpit", session_service=session_service)
                resp = ""
                async for event in runner.run_async(
                    user_id="system", 
                    session_id="audit_turn",
                    new_message=genai_types.Content(role="user", parts=[genai_types.Part.from_text(text=prompt)])
                ):
                    if event.is_final_response():
                        resp = event.content.parts[0].text
                return "YES" in resp.upper()

            try:
                asyncio.get_running_loop()
                # If an event loop is currently running (e.g., pytest-asyncio or FastAPI),
                # we cannot use asyncio.run() without blocking the loop or raising RuntimeError.
                # Since Auditor is a sync hook, we degrade gracefully to heuristic/False.
                return False
            except RuntimeError:
                # No running event loop, safe to execute
                return asyncio.run(_check())
        except Exception:
            # Fallback to False (conservative) if model fails
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
