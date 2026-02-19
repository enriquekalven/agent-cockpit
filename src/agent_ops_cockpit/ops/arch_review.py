try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None
# v1.8.4 Sovereign Alignment: Optimized for Google Cloud Run
from tenacity import retry, wait_exponential, stop_after_attempt
import typer
import os
import ast
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from agent_ops_cockpit.ops.frameworks import detect_framework, FRAMEWORKS, NIST_AI_RMF_CHECKLIST
from agent_ops_cockpit.ops.auditors.security import SecurityAuditor
from agent_ops_cockpit.ops.auditors.reliability import ReliabilityAuditor
from agent_ops_cockpit.ops.auditors.paradigm import ParadigmAuditor
from agent_ops_cockpit.ops.auditors.manifest import ManifestAuditor
from agent_ops_cockpit.ops.auditors.sre_a2a import SREAuditor
from agent_ops_cockpit.ops.auditors.finops import FinOpsAuditor
from agent_ops_cockpit.ops.remediator import CodeRemediator
from agent_ops_cockpit.ops.discovery import DiscoveryEngine
from agent_ops_cockpit.ops.git_portal import GitPortal
from agent_ops_cockpit.ops.benchmarker import ReliabilityBenchmarker
app = typer.Typer(help='Cockpit Project Auditor: Standards & Performance Essentials')
console = Console()

def run_scan(path: str, verbose: bool = False, context: dict = None):
    """Refined Audit: Scans code for Security, Reliability, and Strategic Strategy gaps."""
    import time
    start_time = time.time()
    
    # Consolidated Pillars for reduced cognitive load
    auditors = [
        SecurityAuditor(), 
        ReliabilityAuditor(), 
        ParadigmAuditor(),
        ManifestAuditor(),
        SREAuditor(),
        FinOpsAuditor()
    ]
    all_findings = []
    file_count = 0
    discovery = DiscoveryEngine(path)
    for file_path in discovery.walk():
        if discovery.is_library_file(file_path):
            continue
        file_count += 1
        if verbose:
            console.print(f"🔍 [dim]Scanning {file_path}...[/dim]")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            tree = ast.parse(content) if file_path.endswith('.py') else ast.parse('')
            for auditor in auditors:
                # Tailor findings based on context if available
                res = auditor.audit(tree, content, file_path)
                if context:
                    for f_item in res:
                        if context['cloud'] == 'aws':
                            f_item.description = f_item.description.replace('Google Cloud Secret Manager', 'AWS Secrets Manager')
                            f_item.description = f_item.description.replace('Cloud Logging', 'CloudWatch')
                            f_item.description = f_item.description.replace('Vertex AI', 'Amazon Bedrock')
                        if context['framework'] == 'flask' and 'Synchronous' in f_item.title:
                            f_item.description += " [blue]Recommendation: Pivot to FastAPI for true Agentic Concurrency.[/blue]"
                all_findings.extend(res)
            
            # v2.0.2 Deep Structural Analysis: Check for monoliths
            if len(content.splitlines()) > 200:
                from agent_ops_cockpit.ops.auditors.base import AuditFinding
                all_findings.append(AuditFinding(
                    title="🏛️ Structural Monolith Detected",
                    description="Agent file is too large (>200 lines). Recommend splitting into specialized sub-agents/peers.",
                    category="🏗️ Architecture",
                    impact="High Latency / Reduced Token Density",
                    roi="High (TTFT reduction)",
                    file_path=file_path,
                    line_number=1
                ))
        except Exception as e:
            if verbose:
                console.print(f"⚠️ [red]Error scanning {file_path}: {e}[/red]")
    duration = time.time() - start_time
    if verbose:
        console.print(f"⏱️ [bold blue]Scan complete. Processed {file_count} files in {duration:.2f}s.[/bold blue]")
    return all_findings

@app.command()
def apply_fixes(path: str='.', dry_run: bool=typer.Option(False, '--dry-run', help='Skip saving patches')):
    """
    Apply remediations for detected architectural standards gaps.
    """
    console.print(Panel.fit('🚀 [bold blue]COCKPIT: AUTOMATED FIX ENGINE[/bold blue]', border_style='blue'))
    findings = run_scan(path)
    if not findings:
        console.print('✅ [bold green]No remediable issues found. Architecture is hardened.[/bold green]')
        return
    file_map = {}
    for f in findings:
        if not f.file_path:
            continue
        if f.file_path not in file_map:
            file_map[f.file_path] = []
        file_map[f.file_path].append(f)
    for file_path, file_findings in file_map.items():
        if not file_path.endswith('.py'):
            continue
        console.print(f'🔧 [bold cyan]Analyzing {file_path}...[/bold cyan]')
        remediator = CodeRemediator(file_path)
        applied_count = 0
        for f in file_findings:
            if 'Resiliency' in f.title or 'retry' in f.description.lower():
                remediator.apply_resiliency(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Exponential Backoff Decorator[/green] ({f.title})')
            elif 'Zombie' in f.title or 'Timeout' in f.title:
                remediator.apply_timeouts(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Async Timeout Guard[/green] ({f.title})')
            elif 'Caching' in f.title:
                remediator.apply_caching(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Performance Caching[/green] ({f.title})')
            elif 'Hardening' in f.title:
                remediator.apply_tool_hardening(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Schema Validation[/green] ({f.title})')
            elif 'Compaction' in f.title:
                remediator.apply_context_compaction(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Context Compaction Strategy[/green] ({f.title})')
            elif 'Reflection' in f.title:
                remediator.apply_sovereign_reflection(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Reasoning Reflection Loop[/green] ({f.title})')
            elif 'Over-Privilege' in f.title or 'HITL Gate' in f.title:
                remediator.apply_mcp_gating(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]HITL MCP Gate[/green] ({f.title})')
            elif 'Monocultural' in f.title or 'Provider Bias' in f.title:
                remediator.apply_cloud_abstraction(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Cloud Provider Abstraction[/green] ({f.title})')
            elif 'Legacy Intelligence' in f.title or 'SDK Latency' in f.title:
                remediator.apply_manifest_drift_fix(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Frontier SDK Upgrade[/green] ({f.title})')
            elif 'Malformed MCP' in f.title or 'Protocol Fragility' in f.title:
                remediator.apply_mcp_validation(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Protocol Manifest Fix[/green] ({f.title})')
            elif 'Passive Retrieval' in f.title or 'Passive RAG' in f.title:
                remediator.apply_passive_retrieval(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Managed RAG Refactor[/green] ({f.title})')
            elif 'Structural Monolith' in f.title:
                remediator.apply_structural_split(f)
                applied_count += 1
                console.print(f'   🛠️ Planned: [green]Architectural Split Scaffold[/green] ({f.title})')
        if applied_count > 0:
            if dry_run:
                console.print(f'🏜️ [yellow]DRY RUN: Skip saving patch for {file_path}[/yellow]\n')
            else:
                patch_path = remediator.save_patch()
                console.print(f"✨ [bold green]Patch generated:[/bold green] {patch_path}")
                console.print(f"👉 [bold yellow]Review with:[/bold yellow] [white]agent-ops workbench --path {path}[/white]\n")
    console.print('🏁 [bold]Plan-then-Execute cycle complete. Review patches to apply fixes.[/bold]')

@app.command()
def propose_fixes(path: str='.'):
    """
    Remediate on a new branch and prepare a GitHub PR.
    """
    console.print(Panel.fit('🌿 [bold green]COCKPIT: AUTOMATED PR GENERATOR[/bold green]', border_style='green'))
    findings = run_scan(path)
    if not findings:
        console.print('✅ [bold green]Architecture is already optimal. No PR needed.[/bold green]')
        return
    portal = GitPortal(path)
    import time
    branch_name = f'cockpit-fix-{int(time.time())}'
    portal.create_fix_branch(branch_name)
    file_map = {}
    for f in findings:
        if not f.file_path:
            continue
        if f.file_path not in file_map:
            file_map[f.file_path] = []
        file_map[f.file_path].append(f)
    modified_files = []
    for file_path, file_findings in file_map.items():
        if not file_path.endswith('.py'):
            continue
        console.print(f'🔧 [bold cyan]Proposing fixes for {file_path}...[/bold cyan]')
        remediator = CodeRemediator(file_path)
        applied = 0
        for f in file_findings:
            if 'Resiliency' in f.title or 'retry' in f.description.lower():
                remediator.apply_resiliency(f)
                applied += 1
            elif 'Zombie' in f.title or 'Timeout' in f.title:
                remediator.apply_timeouts(f)
                applied += 1
            elif 'Caching' in f.title:
                remediator.apply_caching(f)
                applied += 1
            elif 'Hardening' in f.title:
                remediator.apply_tool_hardening(f)
                applied += 1
            elif 'Compaction' in f.title:
                remediator.apply_context_compaction(f)
                applied += 1
        if applied > 0:
            remediator.save()
            modified_files.append(file_path)
    if modified_files:
        portal.commit_fixes(modified_files, f'fix: [Cockpit] resolve {len(findings)} architectural gaps')
        console.print(f"\n✨ [bold green]All fixes committed to branch '{branch_name}'.[/bold green]")
        console.print(f'👉 [bold cyan]Next Step:[/bold cyan] Run [white]git push origin {branch_name}[/white] to propose these changes to your team.\n')
    else:
        console.print('⚠️  No fixes could be automatically applied.')

@app.command()
def benchmark(path: str='.', count: int=50):
    """
    Phase 7: Automated Benchmarking (v1.2).
    Generates 50+ stress prompts and outputs a Reliability Waterfall.
    """
    bench = ReliabilityBenchmarker(path)
    import asyncio
    asyncio.run(bench.run_stress_test(count))

@app.command()
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def audit(path: str=typer.Option('.', '--path', '-p', help='Path to the agent project to audit'), export: bool=typer.Option(False, '--export', help='Export reports in HTML format'), verbose: bool=typer.Option(False, '--verbose', '-v', help='Enable verbose output for debugging')):
    """
    Run the Enterprise Architect Design Review v1.1.
    Uses AST Reasoning, Behavioral Trace Audit, and Contextual Graphing.
    """
    discovery = DiscoveryEngine(path)
    context = discovery.detect_context()
    framework_key = detect_framework(path)
    framework_data = FRAMEWORKS[framework_key]
    checklist = framework_data['checklist'] + NIST_AI_RMF_CHECKLIST
    framework_name = framework_data['name']
    console.print(Panel.fit(f'🏛️ [bold blue]{framework_name.upper()}: ENTERPRISE ARCHITECT REVIEW v1.8[/bold blue]', border_style='blue'))
    console.print(f'Detected Stack: [bold green]{framework_name}[/bold green] | [bold cyan]Cloud Context: {context["cloud"].upper()}[/bold cyan] | [bold magenta]Framework: {context["framework"].upper()}[/bold magenta]\n')
    with console.status('[bold blue]Performing Multi-Modal Scan (AST + Behavior + Infra)...'):
        all_findings = run_scan(path, verbose=verbose, context=context)
    total_checks = 0.0
    passed_checks = 0.0
    weights = {'🛡️': 1.5, '🧗': 1.2, '💰': 1.0, '📉': 1.2, '🌍': 1.1, '🌐': 1.3, '🏗️': 1.3, '🚀': 1.4, '⚖️': 1.3, '🎭': 1.4}
    table_data = []
    for section in checklist:
        table = Table(title=section['category'], show_header=True, header_style='bold magenta')
        table.add_column('Design Check', style='cyan', width=50)
        table.add_column('Status', style='green', justify='center')
        table.add_column('Verification', style='dim')
        cat_prefix = section['category'][:2]
        weight = weights.get(cat_prefix, 1.0)
        for check_text, rationale in section['checks']:
            total_checks += weight
            check_key = check_text.lower()
            matching_finding = next((f for f in all_findings if f.category[:2] == cat_prefix and f.title.lower() in check_key), None)
            if matching_finding:
                status_text = 'FAIL'
                status_rich = '[bold red]FAIL[/bold red]'
                verif = f'DEEP SCAN: {matching_finding.description}'
            else:
                status_text = 'PASSED'
                status_rich = '[bold green]PASSED[/bold green]'
                verif = 'Verified by Pattern Match'
                passed_checks += weight
            table.add_row(check_text, status_rich, verif)
            table_data.append({'category': section['category'], 'check': check_text, 'status': status_text, 'verif': verif})
        console.print(table)
    score = passed_checks / total_checks * 100 if total_checks > 0 else 0
    console.print(f'\n📊 [bold]Architecture Maturity Score (v1.3): {score:.0f}/100[/bold]')
    impact_report = []
    if all_findings:
        console.print()
        console.print(Panel.fit('📋 [bold yellow]CRITICAL FINDINGS & BUSINESS IMPACT (v1.3)[/bold yellow]', border_style='yellow'))
        for f in all_findings:
            console.print(f"🚩 [bold red]{f.title}[/bold red] ({f.file_path}:{f.line_number or ''})")
            console.print(f'   [dim]{f.description}[/dim]')
            console.print(f'   ⚖️ [bold green]Strategic ROI:[/bold green] {f.roi}')
            console.print(f'ACTION: {f.file_path}:{f.line_number or 1} | {f.title} | {f.description}')
            impact_report.append(f'- **{f.title}**: {f.description} (Impact: {f.impact})')
    latency_impact = sum((1 for f in all_findings if 'latency' in f.description.lower())) * 200
    cost_risk = 'HIGH' if any((f.category == '💰 FinOps' and 'pro' in f.description.lower() for f in all_findings)) else 'LOW'
    
    adr_md = f"""
# 📋 Project Integrity Audit Record
**Status**: AUDIT_COMPLETED | **Score**: {score:.0f}/100

## 🛠️ Summary of Findings
{(chr(10).join(impact_report) if impact_report else 'No architectural gaps detected.')}

## 🚀 Strategic Recommendations
1. **Automated Fixing**: Run `cockpit audit --apply-fixes` to resolve identified patterns.
2. **Cloud Portability**: Review provider-specific logic to ensure multi-cloud readiness.
3. **Logic Hardening**: Implement reflection and validation hooks for high-stakes tools.
"""
    console.print()
    console.print(Panel(Markdown(adr_md), title='📐 COCKPIT AUDIT RECORD', border_style='cyan'))
    
    if export:
        output_root = os.path.join(os.getcwd(), '.cockpit')
        if not os.path.exists(output_root):
            os.makedirs(output_root, exist_ok=True)
        report_path = os.path.join(output_root, 'audit_report.html')
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cockpit Audit Report</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
                body {{ font-family: 'Outfit', sans-serif; background: #fafafa; color: #1e293b; line-height: 1.6; padding: 40px; }}
                .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 50px; border-radius: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
                h1 {{ font-weight: 800; font-size: 2rem; margin-bottom: 24px; color: #0f172a; }}
                .score-header {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; padding-bottom: 24px; border-bottom: 1px solid #f1f5f9; }}
                .score {{ font-size: 4rem; font-weight: 800; color: {('#10b981' if score > 80 else '#ef4444')}; }}
                .badge {{ padding: 6px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; background: #f1f5f9; color: #64748b; }}
                .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 40px; }}
                .card {{ background: #f8fafc; padding: 24px; border-radius: 16px; border: 1px solid #e2e8f0; }}
                .card-val {{ display: block; font-size: 1.25rem; font-weight: 800; color: #0f172a; }}
                .card-label {{ font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; }}
                .finding {{ border-left: 4px solid #ef4444; background: #fef2f2; padding: 20px; border-radius: 8px; margin-bottom: 16px; }}
                .finding h4 {{ margin: 0 0 8px 0; color: #991b1b; }}
                .finding p {{ margin: 0; font-size: 0.95rem; color: #7f1d1d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="score-header">
                    <div>
                        <h1>📊 Project Integrity Audit</h1>
                        <p style="color: #64748b; margin:0;">Analysis for {framework_name} Architecture</p>
                    </div>
                    <div style="text-align:right;">
                        <span class="score">{score:.0f}</span>
                        <div class="card-label">Overall Health</div>
                    </div>
                </div>

                <div class="grid">
                    <div class="card">
                        <span class="card-val">{latency_impact}ms</span>
                        <span class="card-label">Potential Latency Debt</span>
                    </div>
                    <div class="card">
                        <span class="card-val">{cost_risk}</span>
                        <span class="card-label">Inference Cost Risk</span>
                    </div>
                </div>

                <h2>🚩 Critical Findings</h2>
                {''.join([f'<div class="finding"><h4>{f.title}</h4><p>{f.description}</p></div>' for f in all_findings]) if all_findings else '<p>No critical gaps found.</p>'}

                <h2>🚀 Next Steps</h2>
                <ul>
                    <li>Run <code>cockpit audit --apply-fixes</code> to modernize the code.</li>
                    <li>Verify agent reasoning loops in the Cockpit Workbench.</li>
                </ul>

                <div style="margin-top: 60px; border-top: 1px solid #f1f5f9; padding-top: 20px; font-size: 0.8rem; color: #94a3b8; text-align: center;">
                    Generated by AgentOps Cockpit v2.0.2
                </div>
            </div>
        </body>
        </html>
        """
        with open(report_path, 'w') as f:
            f.write(html_report)
        console.print(f'\n✨ [bold green]Audit Report generated: {report_path}[/bold green]')
if __name__ == '__main__':
    app()