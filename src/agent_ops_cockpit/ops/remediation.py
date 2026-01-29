
import os
import sys
import json
from rich.console import Console

console = Console()

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False

def apply_remediation(target_path: str, issue: str, fix: str):
    """
    Uses an LLM to automatically apply a recommended fix to the codebase.
    This is the essence of 'Agentic Self-Healing'.
    """
    console.print(f"🛠️ [bold blue]Applying Auto-Remediation:[/bold blue] {issue}")
    
    # 1. Read the target file
    if not os.path.exists(target_path):
        # If the gap is at the codebase level, we target the main entry point
        if target_path == "codebase":
            for f in ["agent.py", "main.py", "app.py"]:
                if os.path.exists(f):
                    target_path = f
                    break
    
    if not os.path.exists(target_path) or os.path.isdir(target_path):
        console.print(f"⚠️ [yellow]Remediation skipped: Target {target_path} is complex or missing.[/yellow]")
        return False

    try:
        with open(target_path, "r") as f:
            original_code = f.read()
    except Exception as e:
        console.print(f"❌ [red]Fail to read {target_path}: {e}[/red]")
        return False

    # 2. Invoke LLM for the fix
    if not VERTEX_AVAILABLE or not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")):
        console.print("❌ [red]Remediation failed: Vertex AI not configured for Auto-Repair.[/red]")
        return False

    try:
        vertexai.init()
        model = GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
        As an Agentic DevRel Engineer, apply the following fix to the provided code.
        
        ISSUE: {issue}
        RECOMMENDED FIX: {fix}
        
        Original Code:
        ```python
        {original_code}
        ```
        
        Return ONLY the updated code block. No explanations. Ensure all required imports are added.
        """
        
        response = model.generate_content(prompt)
        new_code = response.text.strip().replace("```python", "").replace("```", "")
        
        # 3. Write back the fixed code
        with open(target_path, "w") as f:
            f.write(new_code)
            
        console.print(f"✅ [bold green]Fix Applied successfully to {target_path}[/bold green]")
        return True
    except Exception as e:
        console.print(f"❌ [red]Remediation Error: {e}[/red]")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    parser.add_argument("--issue", required=True)
    parser.add_argument("--fix", required=True)
    args = parser.parse_args()
    
    apply_remediation(args.path, args.issue, args.fix)
