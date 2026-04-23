import os
import sys
import json
import subprocess
from rich.console import Console
from rich.table import Table
import typer

app = typer.Typer(help="Run Promptfoo evaluations for all ingested skills")
console = Console()

@app.command()
def run(
    target_path: str = typer.Argument(".", help="Path to the agent project")
):
    console.print("🚀 [bold blue]SKILL-BASED RED TEAMING INITIALIZED[/bold blue]")
    
    skills_dir = os.path.join(os.path.abspath(target_path), ".cockpit", "promptfoo_skills")
    if not os.path.exists(skills_dir):
        console.print(f"ℹ️ No skill-based Promptfoo configs found at {skills_dir}")
        return
        
    configs = [f for f in os.listdir(skills_dir) if f.endswith('.json')]
    if not configs:
        console.print(f"ℹ️ No skill-based Promptfoo configs found in {skills_dir}")
        return
        
    console.print(f"Found {len(configs)} skill configs to evaluate.")
    
    total_passed = 0
    total_tests = 0
    
    summary_table = Table(title="🛡️ SKILL DEFENSIBILITY REPORT")
    summary_table.add_column("Skill", style="bold")
    summary_table.add_column("Passed", justify="center")
    summary_table.add_column("Total", justify="center")
    summary_table.add_column("Score", justify="center")
    
    for config_file in configs:
        skill_name = config_file.replace('.json', '')
        config_path = os.path.join(skills_dir, config_file)
        
        console.print(f"\nEvaluating Skill: [bold cyan]{skill_name}[/bold cyan]")
        
        results_path = os.path.join(skills_dir, f"{skill_name}_results.json")
        
        # Set env var for provider
        env = os.environ.copy()
        env["COCKPIT_AGENT_PATH"] = target_path # Or detect entry point
        
        try:
            cmd = ["npx", "promptfoo@latest", "eval", "-c", config_path, "--output", results_path]
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                console.print(f"❌ [red]Promptfoo failed for {skill_name}:[/red] {result.stderr}")
                continue
                
            with open(results_path, 'r') as f:
                data = json.load(f)
                
            summary = data.get('summary', {})
            passed = summary.get('numPassed', 0)
            total = summary.get('numTests', 0)
            
            total_passed += passed
            total_tests += total
            
            score = int((passed / total) * 100) if total > 0 else 0
            score_str = f"[bold {('green' if score > 80 else 'yellow' if score > 50 else 'red')}]{score}%[/]"
            
            summary_table.add_row(skill_name, str(passed), str(total), score_str)
            
            # Print failures
            for res in data.get('results', []):
                if not res.get('success'):
                    test_vars = res.get('vars', {})
                    prompt = test_vars.get('prompt', 'Unknown Prompt')
                    console.print(f"  - [yellow]FAIL:[/] {prompt}")
                    # Generate ACTION line for Cockpit report
                    print(f"ACTION: {target_path} | Skill Breach: {skill_name} | Agent failed skill check for prompt: {prompt}")
                    
        except Exception as e:
            console.print(f"❌ Error evaluating {skill_name}: {str(e)}")
            
    console.print("\n", summary_table)
    
    overall_score = int((total_passed / total_tests) * 100) if total_tests > 0 else 0
    console.print(f"\n📊 [bold]Overall Skill Defensibility Score: {overall_score}%[/bold]")
    
    if overall_score < 100:
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
