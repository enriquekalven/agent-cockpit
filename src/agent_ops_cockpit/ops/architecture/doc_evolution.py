"""
Pillar: Autonomous Platform Evolution & Anti-Drift
SME Persona: Distinguished Platform Fellow
Objective: Resolves conflicting website, README, and workflow documentation by cross-referencing truth in source code.
"""

import os
import re
from typing import Dict, List

from google.genai import Client
from rich.console import Console

console = Console()


class DocEvolutionEngine:
    """
    DocEvolutionEngine: Inspects markdown files across the repository, identifies discrepancies,
    and invokes Gemini to surgically self-heal and resolve documentation drift.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = os.path.abspath(workspace_path)
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv(
            "GOOGLE_API_KEY"
        )
        self.is_vertex = (
            os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
        )
        self.client = Client() if (self.api_key or self.is_vertex) else None

    def read_file_safe(self, rel_path: str) -> str:
        """Reads a file securely from the workspace."""
        fpath = os.path.join(self.workspace_path, rel_path)
        if not os.path.exists(fpath):
            return ""
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception:
            return ""

    def write_file_safe(self, rel_path: str, content: str):
        """Writes content to a file securely."""
        fpath = os.path.join(self.workspace_path, rel_path)
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

    def extract_current_cli_commands(self) -> List[str]:
        """Extracts the registered CLI commands from main.py to serve as the ground truth."""
        main_py = self.read_file_safe("src/agent_ops_cockpit/cli/main.py")
        command_pattern = r'@(?:app|context_app|cockpit_app|audit_app|fleet_app|deploy_app|fix_app|test_app|sys_app|ops_app|create_app|release_app)\.command\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']'
        commands = re.findall(command_pattern, main_py)

        # Also extract app names
        app_pattern = r'app\.add_typer\s*\(\s*[a-zA-Z_0-9]+,\s*name\s*=\s*["\']([^"\']+)["\']'
        apps = re.findall(app_pattern, main_py)

        ground_truth = []
        for app in apps:
            ground_truth.append(f"cockpit {app}")
        for cmd in commands:
            ground_truth.append(f"Command: {cmd}")

        return sorted(list(set(ground_truth)))

    def evolve_documentation(
        self, target_rel_path: str, max_retries: int = 2
    ) -> bool:
        """Resolves discrepancies in a specific markdown file against the platform's ground truth."""
        if not self.client:
            console.print(
                "⚠️ [yellow]API Key missing. Cannot evolve documentation autonomously.[/yellow]"
            )
            return False

        target_content = self.read_file_safe(target_rel_path)
        if not target_content:
            console.print(
                f"❌ [red]Documentation target not found: {target_rel_path}[/red]"
            )
            return False

        # Gather truth
        from agent_ops_cockpit.config import config

        current_version = config.VERSION
        cli_commands = self.extract_current_cli_commands()
        self.read_file_safe("docs/PRD.md")
        pyproject_toml = self.read_file_safe("pyproject.toml")

        prompt = f"""
        You are the Distinguished Platform Fellow and Technical Writer for the AgentOps Cockpit.
        
        Your task is to analyze and surgically correct the following Markdown document to remove all discrepancies, outdated commands, and versioning drift:
        Target File: `{target_rel_path}`
        
        Here is the Ground Truth of the platform's actual implementation:
        - Current Semantic Version: `{current_version}`
        - Registered CLI Apps/Commands: {cli_commands}
        - Platform Requirements:
        ```toml
        {pyproject_toml[:1000]}
        ```
        
        Here is the original content of `{target_rel_path}`:
        ```markdown
        {target_content}
        ```
        
        Instructions for evolution:
        1. Replace all outdated references to `v2.0.20`, `2.0.21`, or older versions with `{current_version}`.
        2. Ensure that any example CLI commands in the document (e.g. `agent-ops context build`, `cockpit test drift`) EXACTLY match the ground-truth registered CLI apps. 
        3. Harmonize discrepancies between this file and the core PRD.
        4. Output the COMPLETE, SURGICALLY FIXED Markdown document. Do NOT include markdown code-block tick wrappers around the output. 
        """

        try:
            console.print(
                f"🧬 [cyan]Evolving & Healing Doc Drift: {target_rel_path}...[/cyan]"
            )
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            fixed_content = response.text.strip()
            if fixed_content.startswith("```markdown"):
                fixed_content = fixed_content.split("```markdown", 1)[1]
            if fixed_content.startswith("```"):
                fixed_content = fixed_content.split("```", 1)[1]
            if fixed_content.endswith("```"):
                fixed_content = fixed_content.rsplit("```", 1)[0]

            # Prevent destructive empty outputs
            if len(fixed_content) < 50:
                console.print(
                    f"❌ [red]Gemini returned invalid or truncated document for {target_rel_path}. Aborting fix.[/red]"
                )
                return False

            self.write_file_safe(target_rel_path, fixed_content.strip())
            console.print(
                f"✨ [green]Documentation Healed Successfully: {target_rel_path}[/green]"
            )
            return True

        except Exception as e:
            console.print(
                f"❌ [red]Documentation Evolution Failed for {target_rel_path}: {e}[/red]"
            )
            return False

    def evolve_all_documentation(self) -> Dict[str, bool]:
        """Iterates through all known public and core Markdown documentation files and self-heals them."""
        doc_targets = [
            "README.md",
            "ROADMAP.md",
            "workflows/zero2hero.md",
            "workflows/validate.md",
            "public/README.md",
            "docs/PRD.md",
        ]
        results = {}
        for target in doc_targets:
            if os.path.exists(os.path.join(self.workspace_path, target)):
                res = self.evolve_documentation(target)
                results[target] = res
        return results
