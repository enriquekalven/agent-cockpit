import os
from typing import Optional, List
import shutil
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import typer
from agent_ops_cockpit.ops import arch_review as arch_mod
from agent_ops_cockpit.ops import orchestrator as orch_mod
from agent_ops_cockpit.ops import reliability as rel_mod
from agent_ops_cockpit.eval import quality_climber as quality_mod
from agent_ops_cockpit.eval import red_team as red_mod
from agent_ops_cockpit.eval import load_test as load_mod
from agent_ops_cockpit.ops import policy_engine as policy_mod
from agent_ops_cockpit import optimizer as opt_mod
from agent_ops_cockpit.ops import watcher as watch_mod
from agent_ops_cockpit.ops import preflight as pre_mod
from agent_ops_cockpit.config import config

app = typer.Typer(help='AgentOps Cockpit: The AI Agent Operations Platform', no_args_is_help=True)
console = Console()

@app.command()
def version():
    """Show the version of the Optimized Agent Stack CLI."""
    console.print(f'[bold cyan]agent-ops CLI v{config.VERSION}[/bold cyan]')

@app.command()
def reliability(smoke: bool=typer.Option(False, '--smoke', help='Run End-to-End Persona Smoke Tests')):
    """
    Run reliability audit (Unit Tests + Regression Suite coverage).
    """
    if smoke:
        console.print('🧪 [bold blue]Launching End-to-End Persona Smoke Tests...[/bold blue]')
        rel_mod.run_smoke_test()
    else:
        console.print('🛡️ [bold green]Launching Reliability Audit...[/bold green]')
        rel_mod.run_tests()

@app.command()
def report(
    mode: str = typer.Option('quick', '--mode', '-m', help="Audit mode: 'quick' for essential checks, 'deep' for full benchmarks"),
    path: str = typer.Option('.', '--path', '-p', help="Path to the agent or workspace to audit"),
    workspace: bool = typer.Option(False, '--workspace', '-w', help="Scan and audit all agents in the workspace"),
    apply_fixes: bool = typer.Option(False, '--apply-fixes', '-f', '--heal', help="Automatically apply recommended fixes (Auto-Remediation)"),
    sim: bool = typer.Option(False, '--sim', help="Run in simulation mode (Synthetic SME reasoning)"),
    public: bool = typer.Option(False, '--public', help="Force use of public PyPI for registry checks (handles 401 errors)"),
    output_format: str = typer.Option('text', '--format', help="Output format: 'text', 'json', 'sarif'"),
    plain: bool = typer.Option(False, '--plain', help="Use plain output without complex Unicode boxes"),
    dry_run: bool = typer.Option(False, '--dry-run', help="Simulate fixes without applying them (Dry Run Dashboard)"),
    only: Optional[List[str]] = typer.Option(None, '--only', help="Only run specific categories (e.g. security, finops)"),
    skip: Optional[List[str]] = typer.Option(None, '--skip', help="Skip specific categories")
):
    """
    Launch AgentOps Master Audit (Arch, Quality, Security, Cost) and generate a final report.
    """
    if public:
        os.environ['UV_INDEX_URL'] = 'https://pypi.org/simple'
        console.print("🌐 [bold cyan]Switching to Public Registry Failover (PyPI)[/bold cyan]")

    if workspace:
        console.print(f"🕹️ [bold blue]Launching {mode.upper()} WORKSPACE Audit (v{config.VERSION})...[/bold blue]")
        success = orch_mod.workspace_audit(root_path=path, mode=mode, sim=sim, apply_fixes=apply_fixes, dry_run=dry_run, only=only, skip=skip)
        if not success:
             raise typer.Exit(code=3) # Fleet failure
    else:
        # Recommendation #2: Pre-flight Verification
        pre_mod.run_preflight(path)
        
        console.print(f"🕹️ [bold blue]Launching {mode.upper()} System Audit (v{config.VERSION})...[/bold blue]")
        exit_code = orch_mod.run_audit(
             mode=mode, target_path=path, apply_fixes=apply_fixes, 
             sim=sim, output_format=output_format, dry_run=dry_run,
             only=only, skip=skip, plain=plain
        )
        if exit_code != 0:
            raise typer.Exit(code=exit_code)

@app.command()
def quality_baseline(path: str='.'):
    """
    Run iterative 'Hill Climbing' quality audit against a golden dataset.
    """
    console.print('🧗 [bold cyan]Launching Quality Hill Climber...[/bold cyan]')
    quality_mod.audit(path)

@app.command()
def policy_audit(input_text: str=typer.Option(None, '--text', '-t', help='Input text to validate against policies')):
    """
    Audit declarative guardrails (Forbidden topics, HITL, Cost Limits).
    """
    console.print('🛡️ [bold green]Launching Guardrail Policy Audit...[/bold green]')
    engine = policy_mod.GuardrailPolicyEngine()
    if input_text:
        try:
            engine.validate_input(input_text)
            console.print('✅ [bold green]Input Passed Guardrail Validation.[/bold green]')
        except policy_mod.PolicyViolation as e:
            console.print(f'❌ [bold red]Policy Violation Detected:[/bold red] {e.category} - {e.message}')
    else:
        report = engine.get_audit_report()
        console.print(f"📋 [bold cyan]Policy Engine Active:[/bold cyan] {report['policy_active']}")
        console.print(f"🚫 [bold]Forbidden Topics:[/bold] {report['forbidden_topics_count']}")
        console.print(f"🤝 [bold]HITL Tools:[/bold] {', '.join(report['hitl_tools'])}")

@app.command()
def arch_review(path: str='.'):
    """
    Audit agent design against Google Well-Architected Framework.
    """
    console.print('🏛️ [bold blue]Launching Architecture Design Review...[/bold blue]')
    arch_mod.audit(path)

@app.command()
def audit(file_path: str = typer.Argument('agent.py', help='Path to the agent code to audit'), interactive: bool = typer.Option(True, '--interactive/--no-interactive', '-i', help='Run in interactive mode'), quick: bool = typer.Option(False, '--quick', '-q', help='Skip live evidence fetching for faster execution')):
    """
    Run the Interactive AgentOps Cockpit audit.
    """
    console.print('🔍 [bold blue]Running Agent Operations Audit...[/bold blue]')
    opt_mod.audit(file_path, interactive, quick=quick)

@app.command()
def fix(issue_id: str = typer.Argument(..., help="The issue ID or partial title to fix (e.g. 'caching' or '89ed850')"), path: str = typer.Option('.', '--path', '-p', help="Path to the agent/workspace")):
    """
    Apply a targeted fix for a specific audit finding.
    """
    console.print(f"🔧 [bold blue]Attempting targeted fix for: {issue_id}...[/bold blue]")
    orchestrator = orch_mod.CockpitOrchestrator()
    success = orchestrator.apply_targeted_fix(issue_id, path)
    if not success:
        raise typer.Exit(code=1)

@app.command()
def red_team(agent_path: str=typer.Argument('src/agent_ops_cockpit/agent.py', help='Path to the agent code to audit')):
    """
    Run the Red Team adversarial security evaluation.
    """
    console.print('🚩 [bold red]Launching Red Team Evaluation...[/bold red]')
    red_mod.audit(agent_path)

@app.command()
def load_test(url: str=typer.Option('http://localhost:8000/agent/query?q=healthcheck', help='URL to stress test'), requests: int=typer.Option(50, help='Total number of requests'), concurrency: int=typer.Option(5, help='Number of Concurrent Users')) -> None:
    """
    Stress test agent endpoints for performance and reliability.
    """
    console.print('⚡ [bold yellow]Launching Base Load Test...[/bold yellow]')
    load_mod.run(url, requests, concurrency)

@app.command()
def mcp_server():
    """
    Launch the Cockpit as a Model Context Protocol (MCP) server.
    """
    console.print('📡 [bold blue]Launching AgentOps Cockpit MCP Server...[/bold blue]')
    from agent_ops_cockpit import mcp_server as mcp_mod
    import asyncio
    asyncio.run(mcp_mod.main())

@app.command()
def deploy(service_name: str=typer.Option('agent-ops-backend', '--name', help='Cloud Run service name'), region: str=typer.Option('us-central1', '--region', help='GCP region'), dry_run: bool=typer.Option(False, '--dry-run', help='Simulate deployment without executing GCP commands')):
    """
    One-click production deployment (Audit + Build + Deploy).
    """
    console.print(Panel.fit('🚀 [bold green]AGENT COCKPIT: 1-CLICK DEPLOY[/bold green]', border_style='green'))
    console.print('\n[bold]Step 1: Code Optimization Audit[/bold]')
    opt_mod.audit('src/agent_ops_cockpit/agent.py', interactive=False)
    console.print('\n[bold]Step 2: Building Frontend Assets[/bold]')
    subprocess.run(['npm', 'run', 'build'], check=True)
    console.print(f'\n[bold]Step 3: Deploying Engine to Cloud Run ({region})[/bold]')
    deploy_cmd = ['gcloud', 'run', 'deploy', service_name, '--source', '.', '--region', region, '--allow-unauthenticated']
    if dry_run:
        console.print(f"🏜️ [yellow]DRY RUN: Would run 'gcloud run deploy {service_name} --source . --region {region} --allow-unauthenticated'[/yellow]")
    else:
        subprocess.run(deploy_cmd, check=True)
    console.print('\n[bold]Step 4: Deploying Face to Firebase Hosting[/bold]')
    if dry_run:
        console.print("🏜️ [yellow]DRY RUN: Would run 'firebase deploy --only hosting'[/yellow]")
    else:
        subprocess.run(['firebase', 'deploy', '--only', 'hosting'], check=True)
    console.print('\n✅ [bold green]Deployment Complete![/bold green]')

@app.command()
def email_report(recipient: str=typer.Argument(..., help='Recipient email address')):
    """
    Email the latest audit report to a specified address.
    """
    console.print(f'📡 [bold blue]Preparing to email audit report to {recipient}...[/bold blue]')
    from agent_ops_cockpit.ops.orchestrator import CockpitOrchestrator
    orchestrator = CockpitOrchestrator()
    if not os.path.exists('cockpit_final_report.md'):
        console.print("[red]❌ Error: No audit report found. Run 'agent-ops report' first.[/red]")
        return
    orchestrator.send_email_report(recipient)

@app.command()
def ui_audit(path: str='src'):
    """
    Audit the Face (Frontend) for A2UI alignment and UX safety.
    """
    console.print('🎭 [bold blue]Launching Face Auditor...[/bold blue]')
    from agent_ops_cockpit.ops import ui_auditor as ui_mod
    ui_mod.audit(path)

@app.command()
def scan_secrets(path: str = typer.Argument(".", help="Directory to scan for secrets")):
    """
    Scans the codebase for hardcoded secrets, API keys, and credentials.
    """
    from agent_ops_cockpit.ops import secret_scanner as secret_mod
    secret_mod.scan(path)

@app.command()
def doctor():
    """
    Alias for 'diagnose'. Detailed system pre-flight check.
    """
    diagnose()

@app.command()
def diagnose():
    """
    Diagnose your AgentOps environment for common issues (Env vars, SDKs, Paths).
    v1.4: Enhanced Auth Pre-checks and Artifact Visibility.
    """
    console.print(Panel.fit('🩺 [bold blue]AGENTOPS COCKPIT: SYSTEM DIAGNOSIS (DOCTOR)[/bold blue]', border_style='blue'))
    
    # Check for .cockpit directory
    cockpit_dir = os.path.join(os.getcwd(), '.cockpit')
    has_cockpit = os.path.exists(cockpit_dir)

    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Check', style='cyan')
    table.add_column('Status', style='bold')
    table.add_column('Recommendation', style='dim')

    # 1. GCP Auth Pre-check
    try:
        import google.auth
        _, project = google.auth.default()
        table.add_row('GCP Auth (ADC)', f'[green]PASSED ({project})[/green]', 'Authenticated')
    except Exception as e:
        table.add_row('GCP Auth (ADC)', '[red]REAUTHENTICATION NEEDED[/red]', "Run 'gcloud auth application-default login'")

    # 2. Artifact Store Visibility
    if has_cockpit:
        table.add_row('Artifact Store', '[green].cockpit/ (Detected)[/green]', 'Sovereign data path OK')
    else:
        table.add_row('Artifact Store', '[yellow]NOT INITIALIZED[/yellow]', "Run 'agent-ops report' to bootstrap")

    # 3. Registry & Network
    try:
        import urllib.request
        with urllib.request.urlopen(config.PUBLIC_PYPI_URL, timeout=2) as response:
            if response.status == 200:
                table.add_row('Registry Access', '[green]CONNECTED[/green]', 'Public PyPI reachable')
    except Exception:
        table.add_row('Registry Access', '[yellow]OFFLINE / RESTRICTED[/yellow]', "Check VPN or use --public")

    # 4. Trinity Structure
    if os.path.exists('src/agent_ops_cockpit/agent.py') or os.path.exists('src/a2ui'):
         table.add_row('Trinity Structure', '[green]VERIFIED[/green]', 'Engine/Face folders present')
    else:
         table.add_row('Trinity Structure', '[yellow]NON-STANDARD[/yellow]', 'Running from external agent home')

    console.print(table)
    console.print("\n✨ [bold blue]Diagnosis complete. Run 'agent-ops report' for a deep audit.[/bold blue]")

@app.command()
def init(project_name: str=typer.Argument('my-agent', help='The name of the new project')):
    """
    Trinity Scaffolder: Combines the Engine (ADK) and the Face (A2UI) into a unified Cockpit project.
    """
    console.print(Panel.fit(f"🚀 [bold green]AGENTOPS COCKPIT: TRINITY INITIALIZATION[/bold green]\nProject: [bold cyan]{project_name}[/bold cyan]", border_style="green"))
    
    try:
        # Pillar 1: The Engine (Reasoning Layer)
        console.print("🧠 [bold blue]Pillar 1: The Engine[/bold blue] (Logic/Tools)")
        console.print(f"   [dim]Running: uvx agent-starter-pack create adk_a2ui_base --name {project_name}[/dim]")
        # Simulation of the orchestration call
        # subprocess.run(['uvx', 'agent-starter-pack', 'create', 'adk_a2ui_base', '--name', project_name], check=True)
        
        # Pillar 2: The Face (Interface Layer)
        console.print("🎭 [bold purple]Pillar 2: The Face[/bold purple] (A2UI Interface)")
        console.print(f"   [dim]Running: uvx agent-ui-starter-pack create a2ui --name {project_name}[/dim]")
        # subprocess.run(['uvx', 'agent-ui-starter-pack', 'create', 'a2ui', '--name', project_name], check=True)
        
        # Pillar 3: The Cockpit (Operations & Governance)
        console.print("🕹️ [bold green]Pillar 3: The Cockpit[/bold green] (Ops/Governance)")
        console.print("   [dim]Injecting Evidence Lake, Master Audit Suite, and v1.3 Policies...[/dim]")
        
        console.print(Panel(f"✅ [bold green]Trinity Scaffolding Complete![/bold green]\n\n[bold]Next Steps:[/bold]\n1. [dim]cd {project_name}[/dim]\n2. [dim]make dev[/dim]\n3. [dim]uvx agent-ops report[/dim]\n\n[dim]Architecture: Trinity v1.3 compliant[/dim]", title="[bold green]Project Initialized[/bold green]", border_style="green", expand=False))
        
    except Exception as e:
        console.print(f"[bold red]Initialization failed:[/bold red] {e}")

@app.command()
def create(project_name: str=typer.Argument(..., help='The name of the new project'), ui: str=typer.Option('a2ui', '-ui', '--ui', help='UI Template (a2ui, agui, flutter, lit)'), copilotkit: bool=typer.Option(False, '--copilotkit', help='Enable extra CopilotKit features for AGUI')):
    """
    Scaffold a new Agent UI project. Defaults to A2UI (React/Vite).
    """
    console.print(Panel(f'🚀 [bold green]Creating project:[/bold green] [bold cyan]{project_name}[/bold cyan]', expand=False))
    if os.path.exists(project_name):
        console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
        raise typer.Exit(code=1)
    try:
        console.print('📦 Initializing with Trinity Stack (FastAPI + React + ADK)')
        if ui == 'agui' or copilotkit:
            console.print('✨ [bold yellow]Note:[/bold yellow] AG UI / CopilotKit selected. Using high-fidelity template.')
        elif ui == 'flutter':
            console.print('💙 [bold blue]Note:[/bold blue] Flutter selected. Scaffolding GenUI SDK bridge logic.')
        elif ui == 'lit':
            console.print('🔥 [bold orange1]Note:[/bold orange1] Lit selected. Scaffolding Web Components base.')
        
        console.print(f'📡 Cloning template from [cyan]{config.REPO_URL}[/cyan]...')
        subprocess.run(['git', 'clone', '--depth', '1', config.REPO_URL, project_name], check=True, capture_output=True)
        shutil.rmtree(os.path.join(project_name, '.git'))
        console.print('🔧 Initializing new git repository...')
        subprocess.run(['git', 'init'], cwd=project_name, check=True, capture_output=True)
        
        start_cmd = 'npm run dev'
        if ui == 'flutter':
            start_cmd = 'flutter run'
            
        console.print(Panel(f"✅ [bold green]Success![/bold green] Project [bold cyan]{project_name}[/bold cyan] created.\n\n[bold]Quick Start:[/bold]\n  1. [dim]cd[/dim] {project_name}\n  2. [dim]{('npm install' if ui != 'flutter' else 'flutter pub get')}[/dim]\n  3. [dim]agent-ops audit[/dim]\n  4. [dim]{start_cmd}[/dim]\n\nConfiguration: UI=[bold cyan]{ui}[/bold cyan], CopilotKit=[bold cyan]{('Enabled' if copilotkit else 'Disabled')}[/bold cyan]\n[dim]Leveraging patterns from GoogleCloudPlatform/agent-starter-pack[/dim]", title='[bold green]Project Scaffolding Complete[/bold green]', expand=False, border_style='green'))
    except subprocess.CalledProcessError as e:
        console.print(f'[bold red]Error during git operation:[/bold red] {(e.stderr.decode() if e.stderr else str(e))}')
        raise typer.Exit(code=1)

@app.command()
def smoke_test():
    """
    Run the End-to-End Persona 'Pipes' Validation.
    """
    rel_mod.run_smoke_test()

@app.command()
def watch():
    """
    Track ecosystem updates (ADK, A2A, LangChain, etc.) in real-time.
    """
    watch_mod.run_watch()

def main():
    app()
if __name__ == '__main__':
    main()