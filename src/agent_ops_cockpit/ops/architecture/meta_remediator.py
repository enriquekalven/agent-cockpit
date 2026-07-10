"""
Pillar: Meta-Evolutionary Architecture
SME Persona: Master Architect
Objective: Synthesizes layout-preserving LibCST transformers directly from Natural Language instructions, executing and self-healing them until Pytests pass.
"""

import ast
import os
import traceback
from typing import Any, Dict

from google.genai import Client
from rich.console import Console

console = Console()


class MetaRemediator:
    """
    Meta-Remediator: Invokes Gemini to dynamically generate Python 'libcst.CSTTransformer'
    classes from natural language, sandboxing, executing, and self-repairing them.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = workspace_path
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv(
            "GOOGLE_API_KEY"
        )
        self.is_vertex = (
            os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "false").lower() == "true"
        )
        self.client = Client() if (self.api_key or self.is_vertex) else None

    def synthesize_transformer_code(self, instruction: str) -> str:
        """Invokes Gemini to write the raw Python code for a valid LibCST Transformer class."""
        if not self.client:
            raise ValueError(
                "MetaRemediator requires a valid Gemini API Key to synthesize transformers."
            )

        prompt = f"""
        You are an elite Python software engineer specializing in Concrete Syntax Trees (CSTs) using the 'libcst' library.
        
        Write a complete, standalone Python code block containing:
        1. All necessary LibCST imports (e.g. 'import libcst as cst', 'from libcst.metadata import PositionProvider', etc.).
        2. A single class named 'DynamicCSTTransformer' which inherits from 'cst.CSTTransformer'.
        
        The transformer MUST execute the following natural language instruction layout-preservingly:
        "{instruction}"
        
        Rules for the generated code:
        - Must NOT include any markdown code block ticks. Output RAW Python code ONLY.
        - Must be perfectly syntactically correct.
        - Any inserted keyword arguments like 'timeout' must use 'cst.AssignEqual(whitespace_before=cst.SimpleWhitespace(""), whitespace_after=cst.SimpleWhitespace(""))'.
        - Do not modify or destroy user comments or indentation.
        - The class MUST expose a boolean attribute 'self.modified = False' to track if any node was mutated.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            raw_code = response.text.strip()
            # Sanitize potential markdown ticks
            if raw_code.startswith("```python"):
                raw_code = raw_code.split("```python", 1)[1]
            if raw_code.endswith("```"):
                raw_code = raw_code.rsplit("```", 1)[0]
            return raw_code.strip()
        except Exception as e:
            console.print(
                f"❌ [red]Gemini Transformer Synthesis Failed: {e}[/red]"
            )
            raise

    def repair_transformer_code(
        self, bad_code: str, error_traceback: str, instruction: str
    ) -> str:
        """Self-heals a synthesized transformer using the execution error context."""
        if not self.client:
            raise ValueError(
                "MetaRemediator requires a valid Gemini API Key to repair transformers."
            )

        prompt = f"""
         You are an elite Python software engineer. You generated the following LibCST Transformer code to fulfill this instruction:
         Instruction: "{instruction}"
         
         Code:
         ```python
         {bad_code}
         ```
         
         However, when we executed or unit-tested this code, it failed with the following traceback:
         ```
         {error_traceback}
         ```
         
         Please analyze the traceback, fix the LibCST usage or python syntax error, and output the COMPLETE, CORRECTED Python code block.
         Output RAW Python code ONLY (no markdown blocks!).
         """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )
            raw_code = response.text.strip()
            if raw_code.startswith("```python"):
                raw_code = raw_code.split("```python", 1)[1]
            if raw_code.endswith("```"):
                raw_code = raw_code.rsplit("```", 1)[0]
            return raw_code.strip()
        except Exception as e:
            console.print(
                f"❌ [red]Gemini Transformer Self-Healing Failed: {e}[/red]"
            )
            raise

    def execute_transformer_safely(
        self, target_code: str, transformer_code: str
    ) -> Dict[str, Any]:
        """
        Executes a synthesized CST Transformer against a target code string in a local namespace sandbox.
        Returns {"success": bool, "modified_code": str, "modified": bool, "error": str}.
        """
        namespace = {}
        try:
            # Validate transformer syntax
            ast.parse(transformer_code)

            # Exec the transformer into the namespace
            exec(transformer_code, namespace)

            if "DynamicCSTTransformer" not in namespace:
                return {
                    "success": False,
                    "error": "Class 'DynamicCSTTransformer' not found in synthesized code.",
                    "modified_code": target_code,
                    "modified": False,
                }

            import libcst as cst

            module = cst.parse_module(target_code)

            # Instantiate the dynamically generated transformer
            transformer_cls = namespace["DynamicCSTTransformer"]
            transformer_inst = transformer_cls()

            modified_module = module.visit(transformer_inst)
            is_modified = getattr(transformer_inst, "modified", False)

            return {
                "success": True,
                "modified_code": modified_module.code,
                "modified": is_modified,
                "error": None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"{e}\n{traceback.format_exc()}",
                "modified_code": target_code,
                "modified": False,
            }

    def evolve_and_remediate(
        self,
        target_file_path: str,
        instruction: str,
        max_healing_attempts: int = 3,
    ) -> bool:
        """End-to-End Meta-Remediation: Synthesize, Execute, and Self-Heal until success."""
        if not os.path.exists(target_file_path):
            console.print(
                f"❌ [red]Target file not found: {target_file_path}[/red]"
            )
            return False

        with open(
            target_file_path, "r", encoding="utf-8", errors="replace"
        ) as f:
            original_code = f.read()

        console.print(
            f"🧬 [cyan]Synthesizing LibCST Transformer for: '{instruction}'...[/cyan]"
        )
        current_transformer = self.synthesize_transformer_code(instruction)

        attempt = 0
        while attempt < max_healing_attempts:
            console.print(
                f"⚙️ [yellow]Executing and Validating Transformer (Attempt {attempt + 1}/{max_healing_attempts})...[/yellow]"
            )
            result = self.execute_transformer_safely(
                original_code, current_transformer
            )

            if result["success"]:
                if result["modified"]:
                    with open(target_file_path, "w", encoding="utf-8") as f:
                        f.write(result["modified_code"])
                    console.print(
                        "✨ [green]Meta-Remediation SUCCESS! File updated surgically.[/green]"
                    )
                    return True
                else:
                    console.print(
                        "⚠️ [yellow]Transformer executed but made ZERO modifications. Check your instruction context.[/yellow]"
                    )
                    return False
            else:
                error_tb = result["error"]
                console.print(
                    f"⚠️ [red]Transformation Error Encountered:[/red]\n{error_tb}"
                )
                attempt += 1
                if attempt < max_healing_attempts:
                    console.print(
                        "🩹 [cyan]Invoking Gemini Reflection to Self-Heal Transformer code...[/cyan]"
                    )
                    current_transformer = self.repair_transformer_code(
                        current_transformer, error_tb, instruction
                    )
                else:
                    console.print(
                        f"❌ [red]Meta-Remediation failed after {max_healing_attempts} self-healing attempts.[/red]"
                    )
                    return False
        return False
