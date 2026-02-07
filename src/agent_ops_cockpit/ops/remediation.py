
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
    if not os.path.exists(target_path) or os.path.isdir(target_path):
        # Use heuristic to find entry point
        priorities = ["agent.py", "main.py", "app.py", "index.ts", "index.js", "main.ts", "main.js"]
        found = False
        search_dir = target_path if os.path.isdir(target_path) else "."
        for p in priorities:
            if os.path.exists(os.path.join(search_dir, p)):
                target_path = os.path.join(search_dir, p)
                found = True
                break
        
        if not found and os.path.isdir(target_path):
            # Fallback: find any source file
            for f in os.listdir(target_path):
                if f.endswith((".py", ".ts", ".js")):
                    target_path = os.path.join(target_path, f)
                    found = True
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
    if not VERTEX_AVAILABLE:
        console.print("❌ [red]Remediation failed: Vertex AI not installed.[/red]")
        return False

    try:
        vertexai.init()
        model = GenerativeModel("gemini-1.5-flash")
        
        lang = "python" if target_path.endswith(".py") else "javascript" if target_path.endswith((".js", ".ts")) else "text"
        
        prompt = f"""
        As an Agentic DevRel Engineer, apply the following fix to the provided code.
        
        ISSUE: {issue}
        RECOMMENDED FIX: {fix}
        
        Original Code ({lang}):
        ```{lang}
        {original_code}
        ```
        
        Return ONLY the updated code block. No explanations. Ensure all required imports are added.
        """
        
        response = model.generate_content(prompt)
        new_code = response.text.strip().replace("```python", "").replace("```javascript", "").replace("```typescript", "").replace("```", "")
        
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
