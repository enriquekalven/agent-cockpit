"""
Pillar: Git & Architecture Attestation
SME Persona: Security & SRE
Objective: Computes and monitors layout-agnostic Structural Syntax Tree Hashes (Drift Detection) for critical workspace files.
"""

import ast
import hashlib
import json
import os
from typing import Dict, List, Optional

from rich.console import Console

console = Console()


class ASTStructuralHasher(ast.NodeVisitor):
    """
    AST Visitor that strips line numbers, column offsets, and docstrings
    to create a purely layout-agnostic structural string representation of code.
    """

    def __init__(self):
        self.structural_tokens = []

    def visit(self, node: ast.AST):
        # Skip docstring expressions entirely
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            return

        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            # Skip the literal string inside the docstring or inline string
            return

        # Record the type of the node
        self.structural_tokens.append(type(node).__name__)

        # Extract specific structural properties for critical nodes
        if isinstance(node, ast.Name):
            self.structural_tokens.append(f"Name:{node.id}")
        elif isinstance(node, ast.Constant):
            self.structural_tokens.append(f"Const:{repr(node.value)}")

        elif isinstance(node, ast.arg):
            self.structural_tokens.append(f"Arg:{node.arg}")
        elif isinstance(node, ast.FunctionDef) or isinstance(
            node, ast.AsyncFunctionDef
        ):
            self.structural_tokens.append(f"Func:{node.name}")
            # Visit decorators
            for dec in node.decorator_list:
                self.visit(dec)
        elif isinstance(node, ast.ClassDef):
            self.structural_tokens.append(f"Class:{node.name}")

        # Recursively visit children
        super().generic_visit(node)


class CodeDriftDetector:
    """
    Cockpit Drift Detection Engine: Tracks, Saves, and Compares
    Structural Syntax Identifiers (SSI) to catch drift in audited workspaces.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = workspace_path
        self.attestation_path = os.path.join(
            workspace_path, ".cockpit", "audit_attestation.json"
        )

    def compute_file_hash(self, file_path: str) -> Optional[str]:
        """Computes the layout-agnostic SHA-256 structural hash of a Python file."""
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            tree = ast.parse(content)
            hasher = ASTStructuralHasher()
            hasher.visit(tree)

            structural_string = "".join(hasher.structural_tokens)
            sha = hashlib.sha256(structural_string.encode("utf-8")).hexdigest()
            return sha
        except Exception as e:
            console.print(
                f"⚠️ [yellow]Could not compute AST hash for {file_path}: {e}[/yellow]"
            )
            return None

    def save_attestation(self, target_files: List[str]) -> Dict[str, str]:
        """Snapshots and saves the structural hashes of the target files to the Attestation Store."""
        registry = {}
        for fpath in target_files:
            full_path = (
                os.path.join(self.workspace_path, fpath)
                if not os.path.isabs(fpath)
                else fpath
            )
            rel_path = os.path.relpath(full_path, self.workspace_path)
            h = self.compute_file_hash(full_path)
            if h:
                registry[rel_path] = h

        os.makedirs(os.path.dirname(self.attestation_path), exist_ok=True)
        with open(self.attestation_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=4)

        console.print(
            f"🛡️ [green]Audit Attestation Saved for {len(registry)} files.[/green]"
        )
        return registry

    def detect_drift(self) -> Dict[str, str]:
        """
        Reads the saved attestation and compares with the live workspace.
        Returns a dict of drifted files mapping rel_path -> status ('drifted' or 'missing').
        """
        if not os.path.exists(self.attestation_path):
            console.print(
                "[yellow]⚠️ No audit attestation found. Run 'agent-ops attestation snapshot' first.[/yellow]"
            )
            return {}

        with open(self.attestation_path, "r", encoding="utf-8") as f:
            attestation = json.load(f)

        drifted_files = {}
        for rel_path, old_hash in attestation.items():
            full_path = os.path.join(self.workspace_path, rel_path)
            if not os.path.exists(full_path):
                drifted_files[rel_path] = "missing"
                continue

            new_hash = self.compute_file_hash(full_path)
            if new_hash != old_hash:
                drifted_files[rel_path] = "drifted"

        return drifted_files
