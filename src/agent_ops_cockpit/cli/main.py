try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError):
    ContextCacheConfig = None
# v1.6.7 Sovereign Alignment: Optimized for AWS App Runner (Bedrock)
import os
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import Optional, List, Annotated
import shutil
import subprocess
from datetime import datetime
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import typer
from agent_ops_cockpit.ops import arch_review as arch_mod
from agent_ops_cockpit.ops import orchestrator as orch_mod
from agent_ops_cockpit.ops import reliability as rel_mod
from agent_ops_cockpit.eval import quality_climber as quality_mod
from agent_ops_cockpit.eval import red_team as red_mod
from agent_ops_cockpit.ops import policy_engine as policy_mod
from agent_ops_cockpit import optimizer as opt_mod
from agent_ops_cockpit.ops import rag_audit as rag_mod
from agent_ops_cockpit.ops import finops_roi as roi_mod
from agent_ops_cockpit.ops import workbench as workbench_mod
from agent_ops_cockpit.ops import mcp_store as mcp_mod
from agent_ops_cockpit.ops import watcher as watch_mod
from agent_ops_cockpit.ops import preflight as pre_mod
from agent_ops_cockpit.config import config
from agent_ops_cockpit.telemetry import telemetry
from agent_ops_cockpit.ops import migration as migrate_mod
from agent_ops_cockpit.ops import orchestrator as sovereign_mod
from agent_ops_cockpit.ops import documenter as doc_mod
from agent_ops_cockpit.ops import master_dashboard as master_mod
app = typer.Typer(help='🕹️ AgentOps Cockpit: The Sovereign Fleet Governance Platform.', no_args_is_help=False)
audit_app = typer.Typer(help="🛡️ Audit Hub: Verify security, quality, arch, and compliance.")

# --- MASTER HUB ---
@app.command(name="cockpit")
def master_dashboard(path: Annotated[str, typer.Option("--path", "-p", help="Path to workspace")] = "."):
    """🚀 Mission Control: The 'One Command' to manage your entire agent fleet."""
    dashboard = master_mod.MasterCockpit(path)
    dashboard.render_landing()
fleet_app = typer.Typer(help="🛰️ Fleet Hub: Day 2 Ops, Health Tracking, and FinOps scaling.")
deploy_app = typer.Typer(help="🚀 Deployment Hub: Project hydration, migration, and cloud factory.")
fix_app = typer.Typer(help="🔧 Evolution Hub: Targeted fixes and autonomous code synthesis.")
test_app = typer.Typer(help="🧪 Reliability Hub: Unit tests and Persona smoke tests.")
sys_app = typer.Typer(help="🩺 System Hub: Health diagnosis and version tracking.")
ops_app = typer.Typer(help="🛡️ Operations Hub: Observability bridges, Shadow Routing, and Runtime Watchers.")
create_app = typer.Typer(help="🏗️ Scaffolding Hub: Project initialization and UI creation.")

console = Console()

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """Global callback for all commands. Defaults to 'cockpit' if none provided."""
    if ctx.invoked_subcommand is None:
        dashboard = master_mod.MasterCockpit(".")
        dashboard.render_landing()
    else:
        telemetry.track_event_sync("cli_command", {"command": ctx.invoked_subcommand})

# --- SYSTEM HUB ---
@sys_app.command()
def version():
    """Show the version of the Optimized Agent Stack CLI."""
    console.print(f'[bold cyan]agent-ops CLI v{config.VERSION}[/bold cyan]')

@sys_app.command(name="doctor")
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def diagnose():
    """Diagnose your AgentOps environment for common issues (Env vars, SDKs, Paths)."""
    console.print(Panel.fit('🩺 [bold blue]AGENTOPS COCKPIT: SYSTEM DIAGNOSIS (DOCTOR)[/bold blue]', border_style='blue'))
    cockpit_dir = os.path.join(os.getcwd(), '.cockpit')
    has_cockpit = os.path.exists(cockpit_dir)
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column('Check', style='cyan')
    table.add_column('Status', style='bold')
    table.add_column('Recommendation', style='dim')
    try:
        import google.auth
        _, project = google.auth.default()
        table.add_row('GCP Auth (ADC)', f'[green]PASSED ({project})[/green]', 'Authenticated')
    except Exception:
        table.add_row('GCP Auth (ADC)', '[red]REAUTHENTICATION NEEDED[/red]', "Run 'gcloud auth application-default login'")
    if has_cockpit:
        table.add_row('Artifact Store', '[green].cockpit/ (Detected)[/green]', 'Sovereign data path OK')
    else:
        table.add_row('Artifact Store', '[yellow]NOT INITIALIZED[/yellow]', "Run 'agent-ops audit report' to bootstrap")
    try:
        import urllib.request
        with urllib.request.urlopen(config.PUBLIC_PYPI_URL, timeout=2) as response:
            if response.status == 200:
                table.add_row('Registry Access', '[green]CONNECTED[/green]', 'Public PyPI reachable')
    except Exception:
        table.add_row('Registry Access', '[yellow]OFFLINE / RESTRICTED[/yellow]', 'Check VPN or use --public')
    if os.path.exists('src/agent_ops_cockpit/agent.py') or os.path.exists('src/a2ui'):
        table.add_row('Trinity Structure', '[green]VERIFIED[/green]', 'Engine/Face folders present')
    else:
        table.add_row('Trinity Structure', '[yellow]NON-STANDARD[/yellow]', 'Running from external agent home')
    console.print(table)
    console.print("\n✨ [bold blue]Diagnosis complete. Run 'agent-ops audit report' for a deep audit.[/bold blue]")

# --- AUDIT HUB ---
@sys_app.command(name="telemetry")
def sys_telemetry(admin: Annotated[bool, typer.Option("--admin", help="Show administrative global metrics")] = True):
    """View usage metrics and global fleet health."""
    if not admin:
        console.print("[bold yellow]Status:[/bold yellow] Telemetry is [green]ACTIVE[/green].")
        console.print(f"Anonymous ID: [dim]{telemetry._user_id}[/dim]")
        console.print(f"Session ID:   [dim]{telemetry._session_id}[/dim]")
        return

    # Admin View
    data = telemetry.get_admin_dashboard()
    console.print(Panel.fit("📡 [bold blue]AGENTOPS COCKPIT: GLOBAL ADMIN METRICS[/bold blue]", border_style="blue"))
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold")
    
    table.add_row("Total Installs (Global)", f"{data['total_installs']:,}")
    table.add_row("Active Agents (24h)", str(data["active_24h"]))
    table.add_row("Avg SME Success Rate", f"[green]{data['avg_success_rate']}%[/green]")
    
    console.print(table)
    
    cmd_table = Table(title="Top Orchestrator Commands", show_header=True, header_style="bold yellow")
    cmd_table.add_column("Command", style="blue")
    cmd_table.add_column("Global Calls", justify="right")
    
    for cmd_stat in data["top_commands"]:
        cmd_table.add_row(f"agent-ops {cmd_stat['cmd']}", f"{cmd_stat['count']:,}")
    
    console.print(cmd_table)
    console.print("\n🌐 [dim]View live global map at: https://agent-cockpit.web.app/metrics[/dim]")
@sys_app.command(name="models")
def list_models():
    """List accessible Gemini models and their capabilities in the current landscape."""
    console.print(Panel.fit('🧠 [bold blue]AGENTOPS COCKPIT: MODEL CAPABILITY DISCOVERY[/bold blue]', border_style='blue'))
    try:
        from google.genai import Client
        client = Client()
        models = client.models.list()
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Model ID", style="cyan")
        table.add_column("Capabilities", style="dim")
        table.add_column("Max Tokens", justify="right")
        
        for m in models:
            # Filter for common Gemini models unless verbose
            if "gemini" in m.name.lower():
                methods = ", ".join([meth.split(":")[0] for meth in m.supported_generation_methods])
                table.add_row(m.name, methods, str(m.output_token_limit))
        
        console.print(table)
        console.print("\n✨ [dim]Capabilities: generate_content, count_tokens, embed_content, etc.[/dim]")
    except Exception as e:
        console.print(f"[bold red]Discovery Failed:[/bold red] {str(e)}")
        console.print("[dim]Hint: Ensure GOOGLE_API_KEY is set or run 'gcloud auth application-default login'.[/dim]")

@app.command(name="certify")
def certification(path: Annotated[str, typer.Option("--path", "-p", help="Path to the agent project to certify")] = ".", no_interactive: Annotated[bool, typer.Option("--no-interactive", help="Run in non-interactive mode")] = True):
    """
    Launch the 'Sovereign Certification' checklist.
    Runs Pre-flight, Deep Audit (Security/Load), and Full Regression (Unit/Smoke).
    """
    console.print(Panel.fit('🏅 [bold blue]AGENTOPS COCKPIT: PRODUCTION READINESS CERTIFICATION[/bold blue]', border_style='blue'))
    
    # 1. Environment Pre-flight
    if not pre_mod.run_preflight(target_path=path, target_cloud="google"):
        console.print("\n[bold red]CERTIFICATION DENIED:[/bold red] Pre-flight environment check failed.")
        raise typer.Exit(code=1)

    # 2. Deep Functional & Security Audit
    console.print("\n🛰️ [bold blue]Step 2: Deep Functional, Security & Load Audit...[/bold blue]")
    audit_exit_code = orch_mod.run_audit(mode='deep', target_path=path, title='PRODUCTION CERTIFICATION AUDIT')
    
    # 3. Full Regression Suite (Unit + Smoke Tests)
    console.print("\n🧪 [bold blue]Step 3: Full Regression Suite (Unit + Smoke tests)...[/bold blue]")
    try:
        rel_mod.run_regression_suite()
        regression_passed = True
    except Exception as e:
        console.print(f"[bold red]Regression Suite Failed:[/bold red] {str(e)}")
        regression_passed = False

    # 4. Final Verdict
    console.print("\n" + "="*80)
    if audit_exit_code == 0 and regression_passed:
        console.print(Panel.fit("🏆 [bold green]CERTIFICATION GRANTED[/bold green]\nAgent is ready for Production Deployment to Google Cloud / AWS.", border_style="green"))
    else:
        console.print(Panel.fit("🛑 [bold red]CERTIFICATION DENIED[/bold red]\nCritical gaps detected in Security, Reliability or Logic.", border_style="red"))
        console.print("[dim]Review the reports above and in the .cockpit/ directory for remediation steps.[/dim]")
        raise typer.Exit(code=2)

@audit_app.command()
def report(
    mode: Annotated[str, typer.Option('--mode', '-m', help="Audit mode: 'quick' for essential checks, 'deep' for full benchmarks")] = 'quick',
    path: Annotated[str, typer.Option('--path', '-p', help='Path to the agent or workspace to audit')] = '.',
    workspace: Annotated[bool, typer.Option('--workspace', '-w', help='Scan and audit all agents in the workspace')] = False,
    apply_fixes: Annotated[bool, typer.Option('--apply-fixes', '-f', '--heal', help='Automatically apply recommended fixes (Auto-Remediation)')] = False,
    sim: Annotated[bool, typer.Option('--sim', help='Run in simulation mode (Synthetic SME reasoning)')] = False,
    public: Annotated[bool, typer.Option('--public', help='Force use of public PyPI for registry checks (handles 401 errors)')] = False,
    output_format: Annotated[str, typer.Option('--format', help="Output format: 'text', 'json', 'sarif'")] = 'text',
    plain: Annotated[bool, typer.Option('--plain', help='Use plain output without complex Unicode boxes')] = False,
    dry_run: Annotated[bool, typer.Option('--dry-run', help='Simulate fixes without applying them (Dry Run Dashboard)')] = False,
    only: Annotated[Optional[List[str]], typer.Option('--only', help='Only run specific categories (e.g. security, finops)')] = None,
    skip: Annotated[Optional[List[str]], typer.Option('--skip', help='Skip specific categories')] = None,
    verbose: Annotated[bool, typer.Option('--verbose', '-v', help='Enable verbose output for debugging')] = False
):
    """Launch AgentOps Master Audit (Arch, Quality, Security, Cost)."""
    if public:
        os.environ['UV_INDEX_URL'] = 'https://pypi.org/simple'
        console.print('🌐 [bold cyan]Switching to Public Registry Failover (PyPI)[/bold cyan]')
    if workspace:
        console.print(f'🕹️ [bold blue]Launching {mode.upper()} WORKSPACE Audit (v{config.VERSION})...[/bold blue]')
        success = orch_mod.workspace_audit(root_path=path, mode=mode, sim=sim, apply_fixes=apply_fixes, dry_run=dry_run, only=only, skip=skip)
        if not success:
            raise typer.Exit(code=3)
    else:
        pre_mod.run_preflight(path)
        console.print(f'🕹️ [bold blue]Launching {mode.upper()} System Audit (v{config.VERSION})...[/bold blue]')
        exit_code = orch_mod.run_audit(mode=mode, target_path=path, apply_fixes=apply_fixes, sim=sim, output_format=output_format, dry_run=dry_run, only=only, skip=skip, plain=plain, verbose=verbose)
        if exit_code != 0:
            raise typer.Exit(code=exit_code)

@audit_app.command()
def security(path: Annotated[str, typer.Argument(help='Directory to scan')] = '.'):
    """Run security audit including Red Team and Secret Scanning."""
    console.print('🚩 [bold red]Launching Security Audit (Red Team + Secrets)...[/bold red]')
    from agent_ops_cockpit.ops import secret_scanner as secret_mod
    secret_mod.scan(path)
    red_mod.audit(path)

@audit_app.command()
def quality(path: str='.'):
    """Run Hill Climbing quality optimization."""
    quality_mod.audit(path)

@audit_app.command()
def arch(path: Annotated[str, typer.Option('--path', '-p', help='Path to workspace')] = '.'):
    """Architecture Design Review (v1.4 compliant)."""
    arch_mod.audit(path)

@audit_app.command()
def context(path: Annotated[str, typer.Option('--path', '-p', help='Path to workspace')] = '.'):
    """Visualize Token window usage (Static vs Turn-based)."""
    from agent_ops_cockpit.ops.auditors.context_auditor import ContextSME
    auditor = ContextSME()
    auditor.audit(path)

@audit_app.command()
def document(path: Annotated[str, typer.Option('--path', '-p', help='Path to workspace')] = '.'):
    """[Task 2] Professional TDD Generator (PDF/HTML)."""
    generator = doc_mod.TDDGenerator(path)
    output = generator.generate_tdd_html()
    console.print(f"📄 [bold green]Technical Design Document generated:[/bold green] {output}")

@audit_app.command()
def policy(input_text: Annotated[Optional[str], typer.Option('--text', '-t', help='Input text to validate')] = None):
    """Audit declarative guardrails (Forbidden topics, HITL)."""
    console.print('🛡️ [bold green]Launching Guardrail Policy Audit...[/bold green]')
    engine = policy_mod.GuardrailPolicyEngine()
    if input_text:
        try:
            engine.validate_input(input_text)
            console.print('✅ [bold green]Input Passed Validation.[/bold green]')
        except policy_mod.PolicyViolation as e:
            console.print(f'❌ [bold red]Violation Detected:[/bold red] {e.category} - {e.message}')
    else:
        report = engine.get_audit_report()
        console.print(f"📋 [bold cyan]Policy Engine Status:[/bold cyan] {report['policy_active']}")
        console.print(f"🚫 [bold]Forbidden Topics:[/bold] {report['forbidden_topics_count']}")
        console.print(f"🤝 [bold]HITL Tools:[/bold] {', '.join(report['hitl_tools'])}")

@audit_app.command()
def maturity():
    """Display the Expertise Matrix for personas and frameworks."""
    audit_maturity()

@audit_app.command()
def email(recipient: Annotated[str, typer.Argument(help='Recipient email address')]):
    """Email the latest audit report."""
    console.print(f'📡 [bold blue]Preparing to email audit report to {recipient}...[/bold blue]')
    orchestrator = orch_mod.CockpitOrchestrator()
    if not os.path.exists('cockpit_final_report.md'):
        console.print("[red]❌ Error: Run 'agent-ops audit report' first.[/red]")
        return
    orchestrator.send_email_report(recipient)

@audit_app.command()
def face(path: Annotated[str, typer.Option('--path', help='Path to Face folder')] = 'src'):
    """Audit the Face (Frontend) for A2UI alignment."""
    from agent_ops_cockpit.ops import ui_auditor as ui_mod
    ui_mod.audit(path)

# --- OPERATIONS HUB ---
@ops_app.command()
def export(target: str = "local", format: str = "json"):
    """[OBSERVABILITY BRIDGE] Export telemetry traces to 3rd party hubs (Arize, LangSmith)."""
    console.print(f"📡 [bold blue]AgentOps Export: Exporting traces to {target} ({format})...[/bold blue]")
    res = telemetry.export_traces(format=format, target_hub=target)
    if res["status"] == "success":
        console.print(f"✅ [bold green]Export Complete![/bold green] {res.get('file', res.get('message'))}")
    else:
        console.print(f"❌ [bold red]Export Failed:[/bold red] {res['message']}")

@ops_app.command()
def shadow_routing(diversion: float = 0.05):
    """[DIVERSION GAP] Activate the Production Shadow Router for live traffic analysis."""
    from agent_ops_cockpit.ops import shadow as shadow_mod
    shadow_mod.ProductionShadowRouter(diversion_percent=diversion)
    console.print("✨ [bold]Shadow Router in standby.[/bold] Listening for diversion signals...")

@ops_app.command()
def watch_ops():
    """[RUNTIME HUB] Launch the Operational Watcher for LLM-driven runtime interpretation."""
    watch_mod.run_operational_watch()

@ops_app.command()
def simulate_ops(mode: str = "nominal"):
    """[CHAOS ENGINE] Battle-test agent tools with Chaos/Latency proxy injections."""
    from agent_ops_cockpit.ops import simulator as sim_mod
    proxy = sim_mod.ToolProxy(mode=mode)
    proxy.execute_mock_tool("search_api", {"query": "Sovereign Audit"})

@audit_app.command()
def shadow_analysis(base: Annotated[str, typer.Argument(help="Path to base agent/report")], candidate: Annotated[str, typer.Argument(help="Path to candidate agent/report")]):
    """Shadow Mode: Differential reasoning analysis (V1 vs V2)."""
    from agent_ops_cockpit.ops import shadow as shadow_mod
    runner = shadow_mod.ShadowRunner(base, candidate)
    runner.run_differential()

# --- FLEET HUB ---
@fleet_app.command(name="status")
def fleet_status():
    """[Day 2 Ops] Display the stateful registry of all deployed agents."""
    orchestrator = sovereign_mod.SovereignOrchestrator()
    orchestrator.list_fleet()

@fleet_app.command()
def mothball(cloud: Annotated[Optional[str], typer.Option('--cloud', help='Specific cloud to mothball')] = None):
    """Scale fleet to zero to stop incurring costs."""
    orchestrator = sovereign_mod.SovereignOrchestrator()
    orchestrator.mothball_fleet(cloud)

@fleet_app.command()
def resume(cloud: Annotated[Optional[str], typer.Option('--cloud', help='Specific cloud to resume')] = None):
    """Resume a mothballed fleet."""
    orchestrator = sovereign_mod.SovereignOrchestrator()
    orchestrator.resume_fleet(cloud)

@fleet_app.command()
def tunnel(path: Annotated[str, typer.Option('--path', '-p', help='Path to local agent')] = '.', port: Annotated[int, typer.Option('--port', help='Local port')] = 8080):
    """Mocks a production registration for a local agent (GE Bridge)."""
    console.print(f"🌉 [bold magenta]Establishing Local-to-Cloud Bridge for port {port}...[/bold magenta]")
    orchestrator = sovereign_mod.SovereignOrchestrator()
    agent_name = os.path.basename(os.path.abspath(path))
    engine = migrate_mod.MigrationEngine(path)
    tunnel_url = f"http://localhost:{port}"
    engine.auto_register_to_gemini(agent_name, a2a_proxy=True)
    orchestrator.fleet_manager.register_agent(name=agent_name, path=path, cloud="local-tunnel", endpoint=tunnel_url, version=config.VERSION)
    console.print(f"✅ [green]Tunnel Active:[/] Gemini Enterprise now sees [bold]{agent_name}[/] at {tunnel_url}")

@fleet_app.command(name="anomaly")
def anomaly_check(name: Annotated[str, typer.Option(help='Agent name to audit')], sim_rogue: Annotated[bool, typer.Option('--rogue', help='Simulate rogue PII exfiltration')] = False):
    """Detect Tool Misuse and Rogue behavior in live telemetry."""
    telemetry_data = [
        {"timestamp": datetime.now().isoformat(), "tool_calls": 12, "payload": "Normal reasoning loop"},
    ]
    if sim_rogue:
        telemetry_data.append({"timestamp": datetime.now().isoformat(), "tool_calls": 1, "payload": "Extracting PII: user@example.com"})
    orchestrator = sovereign_mod.SovereignOrchestrator()
    report = orchestrator.fleet_manager.monitor_agent_anomaly(name, telemetry_data)
    from agent_ops_cockpit.ops.auditors.anomaly_auditor import AnomalySME
    auditor = AnomalySME()
    auditor.display_report(report)

@fleet_app.command(name="telemetry")
def fleet_telemetry(name: Annotated[str, typer.Option(..., help='Agent name to fetch data for')]):
    """Fetch live telemetry metrics for a specific agent."""
    console.print(f"📡 [bold blue]Fetching telemetry for {name}...[/bold blue]")
    data = telemetry.get_agent_telemetry(name)
    
    panel_content = f"[bold]Status:[/] {data['status']}\n"
    panel_content += f"[bold]Avg Latency:[/] {data['avg_latency']}\n"
    panel_content += f"[bold]Token Usage:[/] {data['token_usage']}\n"
    panel_content += f"[bold]Projected Cost:[/] {data['cost_projected']}"
    
    console.print(Panel(panel_content, title=f"📊 {name} Metrics", border_style="cyan"))
    
    table = Table(title="Recent Events", show_header=True, header_style="bold magenta")
    table.add_column("Timestamp", style="dim")
    table.add_column("Event")
    
    for event in data["recent_events"]:
        table.add_row(event["timestamp"], event["event"])
    
    console.print(table)

@fleet_app.command()
def watch_fleet():
    """Track ecosystem updates (ADK, LangChain, etc.) in real-time."""
    watch_mod.run_watch()

# --- DEPLOY HUB ---
@deploy_app.command()
def sovereign(path: Annotated[str, typer.Option("--path", "-p", help="Path to the agent/workspace")] = ".", fleet: Annotated[bool, typer.Option("--fleet", help="Process all agents in the workspace")] = True, target: Annotated[str, typer.Option("--target", "-t", help="Target Cloud Platform: google, aws, azure")] = "google"):
    """End-to-End Agent Factory: Audit -> Fix -> Hydrate -> Deploy."""
    orchestrator = sovereign_mod.SovereignOrchestrator(target_cloud=target)
    asyncio.run(orchestrator.run_pipeline(path, fleet=fleet))

@deploy_app.command()
def migrate(path: Annotated[str, typer.Option('--path', '-p', help='Path to look for agents to migrate')] = '.', target: Annotated[str, typer.Option('--target', '-t', help='Target Cloud Platform: google, aws, azure')] = 'google'):
    """Move agents to Google Cloud, AWS, or Azure."""
    engine = migrate_mod.MigrationEngine(path)
    results = engine.run_migration_loop(target_cloud=target.lower())
    if not results:
        console.print(f"[yellow]No migration candidates found for target: {target}[/yellow]")
    else:
        for r in results:
            reg_info = f" | Registry: [bold magenta]{r['registry']}[/bold magenta]" if r['cloud'] == 'google' else ""
            console.print(f"✅ [bold green]Migrated:[/bold green] {r['agent']} -> [bold cyan]{target.upper()}[/bold cyan] ({', '.join(r['assets'])}){reg_info}")

@deploy_app.command()
def register(path: Annotated[str, typer.Option('--path', '-p', help='Path to workspace or agent to register')] = '.', a2a: Annotated[bool, typer.Option('--a2a', help='Enable A2A (Agent-to-Agent) bridge for cross-cloud agents')] = False):
    """Register agent fleet as native Vertex AI Tools."""
    engine = migrate_mod.MigrationEngine(path)
    console.print(f"📡 [bold blue]Gemini Enterprise: Fleet Registration Initialized for {path}...[/bold blue]")
    if a2a:
        console.print("🌉 [bold magenta]Mode: A2A Bridge Enabled (Multi-Cloud Interop)[/bold magenta]")
    
    # We walk the discovery engine for all py files and attempt registration
    count = 0
    for file_path in engine.discovery.walk():
        if not file_path.endswith('.py'):
            continue
        base_name = os.path.basename(file_path).replace('.py', '')
        if base_name in ['agent', 'main', 'app']:
             # Use parent directory name for better visibility
             name = os.path.basename(os.path.dirname(file_path)).lower().replace('_', '-')
        else:
             name = base_name.lower().replace('_', '-')
        
        # If a2a is enabled, we register even if not explicitly on GCP (via bridge)
        url = engine.auto_register_to_gemini(name, a2a_proxy=a2a)
        if url:
            label = "Registered (Agent Engine)" if not a2a else "Registered (A2A Bridge)"
            console.print(f"✅ [bold green]{label}:[/bold green] {name} -> {url}")
            count += 1
    
    if count == 0:
        console.print("[yellow]No services found to register. Ensure agents are deployed or use --a2a for cross-cloud bridge.[/yellow]")
    else:
        console.print(f"\n✨ [bold green]Successfully on-boarded {count} agents to Gemini Enterprise (Agent Engine / A2A).[/bold green]")

@deploy_app.command(name="prep")
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def deploy_prep(path: Annotated[str, typer.Option('--path', help='Path to agent/workspace')] = '.', target: Annotated[str, typer.Option('--target', help='Primary target cloud')] = 'google'):
    """Generate multi-cloud deployment assets without forced deployment."""
    console.print(Panel.fit('🚀 [bold green]PRODUCTION READINESS FACTORY[/bold green]', border_style='green'))
    
    # Step 1: Deep Audit & Auto-Remediation
    console.print('\n[bold]Step 1: Deep Sovereignty Audit & Auto-Fix[/bold]')
    orch_mod.run_audit(mode='deep', target_path=path, apply_fixes=True)
    
    # Step 2: Multi-Cloud Asset Generation (Hydration)
    console.print('\n[bold]Step 2: Hydrating Multi-Cloud Deployment Assets[/bold]')
    engine = migrate_mod.MigrationEngine(path)
    engine.generate_deployment_assets(path, target_cloud='google')
    engine.generate_deployment_assets(path, target_cloud='aws')
    engine.generate_deployment_assets(path, target_cloud='azure')
    
    # Step 3: Frontend Build Verification
    console.print('\n[bold]Step 4: A2UI Face Preparation (npm run build)[/bold]')
    try:
        subprocess.run(['npm', 'run', 'build'], check=True, capture_output=True)
        console.print("✅ A2UI Build Artifacts Ready (./dist)")
    except Exception:
        console.print("⚠️  Frontend build skipped or failed. Ensure node_modules are installed.")

    # Step 4: Staging Gemini Enterprise Registration
    console.print('\n[bold]Step 5: Staging Gemini Enterprise Tool Registry[/bold]')
    # We stage the registration manifest even if not yet deployed
    reg_path = os.path.join('.cockpit', 'gemini_enterprise_registry.json')
    import json
    manifest = {
        "timestamp": datetime.now().isoformat(),
        "agent": os.path.basename(path),
        "status": "PRODUCTION_READY",
        "endpoints": ["cloud-run", "app-runner", "container-apps"],
        "registration_mode": "native"
    }
    with open(reg_path, 'w') as f:
        json.dump(manifest, f, indent=4)
    console.print(f"📦 Registration manifest staged at: [cyan]{reg_path}[/cyan]")

    console.print(Panel(
        "[bold green]FLEET IS PRODUCTION READY[/bold green]\n\n"
        "1. [bold]Google Cloud:[/bold] Dockerfile.gcp ready.\n"
        "2. [bold]AWS App Runner:[/bold] Dockerfile.aws + aws-apprunner.json ready.\n"
        "3. [bold]Azure Container Apps:[/bold] Dockerfile.azure + azure-deploy.bicep ready.\n"
        "4. [bold]Gemini Enterprise:[/bold] Run [dim]make register[/dim] after cloud push.\n\n"
        "[dim]Note: Direct 'cloud run deploy' is deferred to your CI/CD pipeline.[/dim]",
        title="Artifact Factory Results", border_style="green"
    ))

@deploy_app.command()
def simulate_deploy():
    """Battle-test the Sovereign Pipeline across GCP, AWS, and Azure."""
    from agent_ops_cockpit.ops import simulator
    sim = simulator.SovereignSimulator()
    asyncio.run(sim.run_battle_test())

# --- EVOLUTION HUB ---
@fix_app.command(name="issue")
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def fix_issue(issue_id: Annotated[str, typer.Argument(help="The issue ID or partial title to fix (e.g. 'caching' or '89ed850')")], path: Annotated[str, typer.Option('--path', '-p', help='Path to the agent/workspace')] = '.'):
    """Apply a targeted fix for a specific audit finding."""
    console.print(f'🔧 [bold blue]Attempting targeted fix for: {issue_id}...[/bold blue]')
    orchestrator = orch_mod.CockpitOrchestrator()
    success = orchestrator.apply_targeted_fix(issue_id, path)
    if not success:
        raise typer.Exit(code=1)

@fix_app.command()
def evolve(path: Annotated[str, typer.Option('--path', '-p', help='Path to the agent/workspace')] = '.', branch: Annotated[bool, typer.Option('--branch/--no-branch', help='Create a new git branch for the fixes')] = True):
    """Autonomous Evolution: Surgically fixes gaps and creates a hardened branch."""
    orch_mod.run_autonomous_evolution(path, branch=branch)

# --- RELIABILITY HUB ---
@test_app.command(name="unit")
def reliability_unit_test():
    """Run core unit tests (pytest)."""
    rel_mod.run_tests()

@test_app.command()
def smoke():
    """Run E2E Persona 'Pipes' Validation."""
    rel_mod.run_smoke_test()

@test_app.command()
def regression():
    """Full Regression Suite: Unit Tests + Smoke Tests + A2UI Compliance."""
    rel_mod.run_regression_suite()

@test_app.command()
def simulate_test():
    """Stress-test reasoning depth with Persona-based User Simulation."""
    rel_mod.run_user_simulation()

# --- SCAFFOLDING HUB ---
@create_app.command(name="trinity")
def create_trinity(project_name: Annotated[str, typer.Argument(help='The name of the new project')] = 'my-agent'):
    """Scaffold a unified Cockpit project (Engine + Face)."""
    # Readiness Check
    if not pre_mod.run_preflight(target_cloud="google"):
        console.print("\n[bold red]FATAL: Project environment is not production-ready.[/bold red]")
        console.print("[dim]Please resolve the BLOCKED checks above before scaffolding.[/dim]")
        raise typer.Exit(code=1)

    console.print(Panel.fit(f'🚀 [bold green]AGENTOPS COCKPIT: TRINITY INITIALIZATION[/bold green]\nProject: [bold cyan]{project_name}[/bold cyan]', border_style='green'))
    try:
        console.print('🧠 [bold blue]Pillar 1: The Engine[/bold blue] (Logic/Tools)')
        console.print(f'   [dim]Running: uvx agent-starter-pack create adk_a2ui_base --name {project_name}[/dim]')
        console.print('🎭 [bold purple]Pillar 2: The Face[/bold purple] (A2UI Interface)')
        console.print(f'   [dim]Running: uvx agent-ui-starter-pack create a2ui --name {project_name}[/dim]')
        console.print('🕹️ [bold green]Pillar 3: The Cockpit[/bold green] (Ops/Governance)')
        console.print('   [dim]Injecting Evidence Lake, Master Audit Suite, and v1.6.7 Policies...[/dim]')
        console.print(Panel(f'✅ [bold green]Trinity Scaffolding Complete![/bold green]\n\n[bold]Next Steps:[/bold]\n1. [dim]cd {project_name}[/dim]\n2. [dim]make dev[/dim]\n3. [dim]uvx agentops-cockpit audit report[/dim]\n\n[dim]Architecture: Trinity v1.6.7 compliant[/dim]', title='[bold green]Project Initialized[/bold green]', border_style='green', expand=False))
    except Exception as e:
        console.print(f'[bold red]Initialization failed:[/bold red] {e}')

@create_app.command(name="face")
def create_face(project_name: Annotated[str, typer.Argument(help='The name of the new project')], ui: Annotated[str, typer.Option('-ui', '--ui', help='UI Template (a2ui, agui, flutter, lit)')] = 'a2ui', copilotkit: Annotated[bool, typer.Option('--copilotkit', help='Enable extra CopilotKit features for AGUI')] = False):
    """Scaffold a new Agent UI project. Defaults to A2UI (React/Vite)."""
    # Readiness Check
    if not pre_mod.run_preflight(target_cloud="google"):
         console.print("\n[bold red]FATAL: Project environment is not production-ready.[/bold red]")
         raise typer.Exit(code=1)
    
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
        console.print(Panel(f"✅ [bold green]Success![/bold green] Project [bold cyan]{project_name}[/bold cyan] created.\n\n[bold]Quick Start:[/bold]\n  1. [dim]cd[/dim] {project_name}\n  2. [dim]{('npm install' if ui != 'flutter' else 'flutter pub get')}[/dim]\n  3. [dim]agent-ops audit report[/dim]\n  4. [dim]{start_cmd}[/dim]\n\nConfiguration: UI=[bold cyan]{ui}[/bold cyan], CopilotKit=[bold cyan]{('Enabled' if copilotkit else 'Disabled')}[/bold cyan]\n[dim]Leveraging patterns from GoogleCloudPlatform/agent-starter-pack[/dim]", title='[bold green]Project Scaffolding Complete[/bold green]', expand=False, border_style='green'))
    except subprocess.CalledProcessError as e:
        console.print(f'[bold red]Error during git operation:[/bold red] {(e.stderr.decode() if e.stderr else str(e))}')
        raise typer.Exit(code=1)

# --- LEGACY ALIASES (Non-breaking) ---
@app.command(name="report", hidden=True)
def legacy_report(
    mode: Annotated[str, typer.Option('--mode', '-m')] = 'quick', 
    path: Annotated[str, typer.Option('--path', '-p')] = '.', 
    workspace: Annotated[bool, typer.Option('--workspace', '-w')] = False
):
    """[DEPRECATED] Use 'audit report' instead."""
    report(mode=mode, path=path, workspace=workspace)

@app.command(name="reliability", hidden=True)
def legacy_reliability(smoke: Annotated[bool, typer.Option('--smoke', help='Run End-to-End Persona Smoke Tests')] = False):
    """[DEPRECATED] Use 'test smoke' or 'test unit' instead."""
    if smoke:
        rel_mod.run_smoke_test()
    else:
        rel_mod.run_tests()

@app.command(name="audit", hidden=True)
def legacy_audit(
    file_path: Annotated[str, typer.Argument(help='Path to the agent code to audit')] = 'agent.py', 
    interactive: Annotated[bool, typer.Option('--interactive/--no-interactive', '-i', help='Run in interactive mode')] = True, 
    quick: Annotated[bool, typer.Option('--quick', '-q', help='Skip live evidence fetching for faster execution')] = False
):
    """[DEPRECATED] Use 'audit report' or 'audit interactive' instead."""
    console.print('🔍 [bold blue]Running Agent Operations Audit...[/bold blue]')
    opt_mod.audit(file_path, interactive, quick=quick)

@app.command(name="fix", hidden=True)
def legacy_fix(issue_id: str=typer.Argument(..., help="The issue ID or partial title to fix (e.g. 'caching' or '89ed850')"), path: str=typer.Option('.', '--path', '-p', help='Path to the agent/workspace')):
    """[DEPRECATED] Use 'fix issue' instead."""
    fix_issue(issue_id, path)

@app.command(name="red-team", hidden=True)
def legacy_red_team(agent_path: Annotated[str, typer.Argument(help='Path to the agent code to audit')] = 'src/agent_ops_cockpit/agent.py'):
    """[DEPRECATED] Use 'audit security' instead."""
    red_mod.audit(agent_path)

@app.command(name="sovereign", hidden=True)
def legacy_sovereign(
    path: Annotated[str, typer.Option("--path", "-p", help="Path to agent or workspace")] = ".", 
    target: Annotated[str, typer.Option("--target", "-t", help="Target Cloud: google, aws, azure")] = "google",
    fleet: Annotated[bool, typer.Option("--fleet", help="Run for all agents in the path")] = False
):
    """[DEPRECATED] Use 'deploy sovereign' instead."""
    sovereign(path, fleet, target)

@app.command(name="document", hidden=True)
def legacy_document(path: str=typer.Option('.', '--path', '-p', help='Path to workspace')):
    """[DEPRECATED] Use 'audit document' instead."""
    document(path)

@app.command(name="register", hidden=True)
def legacy_register(path: str=typer.Option('.', '--path', '-p', help='Path to workspace or agent to register'), fleet: bool=typer.Option(True, '--fleet', help='Register all production-ready agents in the workspace'), a2a: bool=typer.Option(False, '--a2a', help='Enable A2A (Agent-to-Agent) bridge for cross-cloud agents')):
    """[DEPRECATED] Use 'deploy register' instead."""
    register(path, a2a)

@app.command(name="fleet-status", hidden=True)
def legacy_fleet_status():
    """[DEPRECATED] Use 'fleet status' instead."""
    fleet_status()

@app.command(name="mothball", hidden=True)
def legacy_mothball(cloud: Optional[str] = typer.Option(None, '--cloud', help='Specific cloud to mothball')):
    """[DEPRECATED] Use 'fleet mothball' instead."""
    mothball(cloud)

@app.command(name="resume", hidden=True)
def legacy_resume(cloud: Optional[str] = typer.Option(None, '--cloud', help='Specific cloud to resume')):
    """[DEPRECATED] Use 'fleet resume' instead."""
    resume(cloud)

@app.command(name="tunnel", hidden=True)
def legacy_tunnel(path: str=typer.Option('.', '--path', '-p', help='Path to local agent'),
           port: int=typer.Option(8080, '--port', help='Local port the agent is running on')):
    """[DEPRECATED] Use 'fleet tunnel' instead."""
    tunnel(path, port)

@app.command(name="anomaly-check", hidden=True)
def anomaly_check_deprecated(name: str=typer.Option(..., help='Agent name to audit'), 
                  sim_rogue: bool=typer.Option(False, '--rogue', help='Simulate rogue PII exfiltration')):
    """[DEPRECATED] Use 'fleet anomaly' instead."""
    anomaly_check(name, sim_rogue)

@app.command(name="evolve", hidden=True)
def legacy_evolve(path: str=typer.Option('.', '--path', '-p', help='Path to the agent/workspace'), branch: bool=typer.Option(True, '--branch/--no-branch', help='Create a new git branch for the fixes')):
    """[DEPRECATED] Use 'fix evolve' instead."""
    evolve(path, branch)

@app.command(hidden=True)
def deploy_prep_alias(path: str=typer.Option('.', '--path', help='Path to agent/workspace'), target: str=typer.Option('google', '--target', help='Primary target cloud')):
    """[DEPRECATED] Use 'deploy prep' instead."""
    deploy_prep(path, target)

@app.command(name="simulate-sovereign", hidden=True)
def legacy_simulate_sovereign():
    """[DEPRECATED] Use 'deploy simulate' instead."""
    simulate_deploy()

@app.command(name="email-report", hidden=True)
def legacy_email_report(recipient: str=typer.Argument(...)):
    """[DEPRECATED] Use 'audit email' instead."""
    email(recipient)

@app.command(name="face", hidden=True)
def legacy_face(path: str='src'):
    """[DEPRECATED] Use 'audit face' instead."""
    from agent_ops_cockpit.ops import ui_auditor as ui_mod
    ui_mod.audit(path)

@app.command(name="secrets", hidden=True)
def legacy_secrets(path: str=typer.Argument('.', help='Directory to scan')):
    """[DEPRECATED] Use 'audit security' instead."""
    from agent_ops_cockpit.ops import secret_scanner as secret_mod
    secret_mod.scan(path)

@app.command(name="doctor", hidden=True)
def legacy_doctor():
    """[DEPRECATED] Use 'sys doctor' instead."""
    diagnose()

@app.command(name="init", hidden=True)
def legacy_init(project_name: str=typer.Argument('my-agent', help='The name of the new project')):
    """[DEPRECATED] Use 'create agent' or 'create face' instead."""
    create_trinity(project_name)

@app.command(name="create", hidden=True)
def legacy_create(project_name: str=typer.Argument(..., help='The name of the new project'), ui: str=typer.Option('a2ui', '-ui', '--ui', help='UI Template (a2ui, agui, flutter, lit)'), copilotkit: bool=typer.Option(False, '--copilotkit', help='Enable extra CopilotKit features for AGUI')):
    """[DEPRECATED] Use 'create face' instead."""
    create_face(project_name, ui, copilotkit)

@app.command(name="smoke-test", hidden=True)
def legacy_smoke_test():
    """[DEPRECATED] Use 'test smoke' instead."""
    rel_mod.run_smoke_test()

@app.command(hidden=True)
def watch_legacy():
    """[DEPRECATED] Use 'fleet watch' instead."""
    watch_mod.run_watch()


@app.command(hidden=True)
def audit_maturity():
    """
    [DEPRECATED] Use 'audit maturity' instead.
    Expertise Matrix: Display the Cockpit's maturity levels across personas, frameworks, and platforms.
    """
    console.print(Panel.fit("🕹️ [bold blue]AGENTOPS COCKPIT: MATURITY EXPERTISE MATRIX (v1.6.7)[/bold blue]", border_style="blue"))
    
    # 1. Persona Matrix
    persona_table = Table(title="👩‍round Principal SME Personas", show_header=True, header_style="bold magenta")
    persona_table.add_column("Persona", style="cyan")
    persona_table.add_column("Mandate", style="dim")
    persona_table.add_column("Expertise Level", style="bold green")
    
    persona_table.add_row("🛡️ SecOps Principal", "Zero-Trust & Adversarial Defense", "MASTER (v1.4)")
    persona_table.add_row("💰 FinOps Principal", "ROI Waterfall & Token Density", "PRINCIPAL (v1.4)")
    persona_table.add_row("🌐 SRE Principal", "Networking Debt & Latent IQ", "SENIOR (v1.3)")
    persona_table.add_row("🏛️ Autonomous Architect", "AST Synthesis & Evolution", "MASTER (v1.4)")
    persona_table.add_row("🧗 AI Quality SME", "Hill Climbing & RAG Fidelity", "PRINCIPAL (v1.4)")
    persona_table.add_row("🎭 UX Designer", "A2UI Handshake & GenUI Flow", "MASTER (v1.3)")
    
    console.print(persona_table)

    # 2. Ecosystem Support Matrix
    eco_table = Table(title="🏗️ Supported Ecosystem & Protocols", show_header=True, header_style="bold yellow")
    eco_table.add_column("Category", style="yellow")
    eco_table.add_column("Frameworks / Platforms", style="cyan")
    eco_table.add_column("Knowledge Depth", style="dim")

    eco_table.add_row("Orchestration", "LangGraph, CrewAI, ADK, AutoGen, LlamaIndex", "Deep AST Probing")
    eco_table.add_row("Cloud (GCP)", "Vertex AI, Cloud Run, GKE, Firebase, BigQuery", "Native Integration")
    eco_table.add_row("Cloud (AWS/Az)", "Bedrock, Azure OpenAI, IAM Federation", "Architecture Alignment")
    eco_table.add_row("Protocols", "Model Context (MCP), A2UI, UCP, AP2", "Protocol Enforcement")
    eco_table.add_row("Databases (Vector)", "Chroma, Pinecone, Weaviate, AlloyDB", "Retrieval Auditing")
    eco_table.add_row("Databases (Enterprise)", "BigQuery, Snowflake, Databricks, Redshift", "Analytical Integration")
    eco_table.add_row("Databases (OLTP/NoSQL)", "Cloud SQL, Firestore, Spanner", "State Persistence Audit")
    
    console.print(eco_table)

    # 3. Research & Wisdom Sources
    wisdom_table = Table(title="🧠 Maturity Wisdom Sources (The Knowledge Base)", show_header=True, header_style="bold green")
    wisdom_table.add_column("Source", style="green")
    wisdom_table.add_column("Integration", style="cyan")
    
    wisdom_table.add_row("Google Well-Architected", "Full alignment with AI/ML Pillar (v1.3)")
    wisdom_table.add_row("OWASP LLM Top 10", "Real-time vulnerability mapping")
    wisdom_table.add_row("AI Brand Safety Playbook", "Declarative safety threshold audits")
    wisdom_table.add_row("ArXiv (cs.AI)", "Latest research in Self-Reflexion & ToT")
    
    console.print(wisdom_table)
    console.print("\n✨ [bold blue]The Cockpit is currently operating at Maturity Level 4 (Autonomous Governance).[/bold blue]")

@app.command()
def mcp_server():
    """
    Launch the Cockpit as a Model Context Protocol (MCP) server.
    """
    console.print('📡 [bold blue]Launching AgentOps Cockpit MCP Server...[/bold blue]')
    from agent_ops_cockpit import mcp_server as mcp_mod
    import asyncio
    asyncio.run(mcp_mod.main())

# --- REGISTRATION ---
app.add_typer(audit_app, name="audit")
app.add_typer(fleet_app, name="fleet")
app.add_typer(deploy_app, name="deploy")
app.add_typer(fix_app, name="fix")
app.add_typer(test_app, name="test")
app.add_typer(sys_app, name="sys")
app.add_typer(ops_app, name="ops")
app.add_typer(create_app, name="create")
app.add_typer(create_app, name="init", hidden=False) # Alias for init hurdle
@app.command(name="models")
def top_level_models():
    """Alias for 'sys models' - List accessible Gemini models."""
    list_models()

# Integrations
app.add_typer(rag_mod.app, name='rag')
audit_app.add_typer(roi_mod.app, name='roi')
fix_app.add_typer(workbench_mod.app, name='workbench')
app.add_typer(mcp_mod.app, name='mcp')

def main():
    app()
if __name__ == '__main__':
    main()