from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
from tenacity import retry, wait_exponential, stop_after_attempt
import os
import sys
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
console = Console()

class CockpitOrchestrator:
    """
    Main orchestrator for AgentOps audits.
    Optimized for concurrency and real-time progress visibility.
    """

    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.report_path = 'cockpit_final_report.md'
        self.results = {}
        self.total_steps = 7
        self.completed_steps = 0

    def run_command(self, name: str, cmd: list, progress: Progress, task_id: TaskID):
        """Helper to run a command and capture output while updating progress."""
        progress.update(task_id, description=f'[cyan]Running {name}...')
        cockpit_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{cockpit_root}{os.pathsep}{env.get('PYTHONPATH', '')}"
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
            stdout, stderr = process.communicate()
            success = process.returncode == 0
            output = stdout if success else f'{stdout}\n{stderr}'
            self.results[name] = {'success': success, 'output': output}
            if success:
                progress.update(task_id, description=f'[green]✅ {name}', completed=100)
            else:
                progress.update(task_id, description=f'[red]❌ {name} Failed', completed=100)
            return (name, success)
        except Exception as e:
            self.results[name] = {'success': False, 'output': str(e)}
            progress.update(task_id, description=f'[red]💥 {name} Error', completed=100)
            return (name, False)
    PERSONA_MAP = {'Architecture Review': '🏛️ Principal Platform Engineer', 'Policy Enforcement': '⚖️ Governance & Compliance SME', 'Secret Scanner': '🔐 SecOps Principal', 'Token Optimization': '💰 FinOps Principal Architect', 'Reliability (Quick)': '🛡️ QA & Reliability Principal', 'Quality Hill Climbing': '🧗 AI Quality SME', 'Red Team Security (Full)': '🚩 Red Team Principal (White-Hat)', 'Red Team (Fast)': '🚩 Security Architect', 'Load Test (Baseline)': '🚀 SRE & Performance Principal', 'Evidence Packing Audit': '📜 Legal & Transparency SME', 'Face Auditor': '🎭 UX/UI Principal Designer'}
    PRIMARY_RISK_MAP = {
        'Secret Scanner': 'Credential Leakage & Unauthorized Access',
        'Architecture Review': 'Systemic Rigidity & Technical Debt',
        'Policy Enforcement': 'Prompt Injection & Reg Breach',
        'Token Optimization': 'FinOps Efficiency & Margin Erosion',
        'Reliability (Quick)': 'Failure Under Stress & Latency spikes',
        'Red Team (Fast)': 'Adversarial Jailbreaking',
        'Face Auditor': 'A2UI Protocol Drift'
    }

    def generate_report(self):
        title = getattr(self, 'title', 'Audit Report')
        report = [f'# 🕹️ AgentOps Cockpit: {title}', f'**Timestamp**: {self.timestamp}', f"**Status**: {('✅ PASS' if all((r['success'] for r in self.results.values())) else '❌ FAIL')}", '\n---', '\n## 🧑\u200d💼 Principal SME Persona Approvals', 'Each pillar of your agent has been reviewed by a specialized SME persona.']
        persona_table = Table(title='🏛️ Persona Approval Matrix', show_header=True, header_style='bold blue')
        persona_table.add_column('SME Persona', style='cyan')
        persona_table.add_column('Audit Module', style='magenta')
        persona_table.add_column('Verdict', style='bold')
        developer_actions = []
        developer_sources = []
        for name, data in self.results.items():
            status = '✅ APPROVED' if data['success'] else '❌ REJECTED'
            persona = self.PERSONA_MAP.get(name, '👤 Automated Auditor')
            persona_table.add_row(persona, name, status)
            report.append(f'- **{persona}** ([{name}]): {status}')
            if data['output']:
                for line in data['output'].split('\n'):
                    if 'ACTION:' in line:
                        developer_actions.append(line.replace('ACTION:', '').strip())
                    if 'SOURCE:' in line:
                        developer_sources.append(line.replace('SOURCE:', '').strip())
        console.print('\n', persona_table)
        if developer_actions:
            report.append('\n## 🛠️ Developer Action Plan')
            report.append("The following specific fixes are required to achieve a passing 'Well-Architected' score.")
            report.append('| File:Line | Issue | Recommended Fix |')
            report.append('| :--- | :--- | :--- |')
            for action in developer_actions:
                parts = action.split(' | ')
                if len(parts) == 3:
                    report.append(f'| `{parts[0]}` | {parts[1]} | {parts[2]} |')
        if developer_sources:
            report.append('\n## 📜 Evidence Bridge: Research & Citations')
            report.append('Cross-verified architectural patterns and SDK best-practices mapped to official cloud standards.')
            report.append('| Knowledge Pillar | SDK/Pattern Citation | Evidence & Best Practice |')
            report.append('| :--- | :--- | :--- |')
            for source in developer_sources:
                parts = source.split(' | ')
                if len(parts) == 3:
                    report.append(f'| {parts[0]} | [Source Citation]({parts[1]}) | {parts[2]} |')
        report.append('\n## 🔍 Raw System Artifacts')
        for name, data in self.results.items():
            report.append(f'\n### {name}')
            report.append('```text')
            report.append(data['output'][-2000:] if data['output'] else 'No output.')
            report.append('```')
        report.append('\n---')
        report.append('\n*Generated by the AgentOps Cockpit Orchestrator (Parallelized Edition).*')
        with open(self.report_path, 'w') as f:
            f.write('\n'.join(report))
        self._generate_html_report(developer_actions, developer_sources)
        console.print(f'\n✨ [bold green]Final Report generated at {self.report_path}[/bold green]')
        console.print(f'📄 [bold blue]Printable HTML Report available at cockpit_report.html[/bold blue]')

    def _generate_html_report(self, developer_actions, developer_sources):
        """Generates a v1.2 Principal SME Grade HTML report with Professional Mode toggle."""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Principal SME Audit: {getattr(self, 'title', 'Build Report')}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono&display=swap');
                body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: #1e293b; max-width: 1100px; margin: 0 auto; padding: 40px; background: #f1f5f9; }}
                .report-card {{ background: white; padding: 50px; border-radius: 32px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; position: relative; }}
                
                /* Professional Mode Toggle */
                .mode-toggle {{ position: absolute; top: 20px; right: 20px; display: flex; align-items: center; gap: 8px; font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; }}
                #prof-mode-checkbox {{ cursor: pointer; }}
                body.prof-mode .mascot-container {{ display: none; }}
                body.prof-mode .report-card {{ border-top: 8px solid #1e3a8a; border-radius: 8px; }}
                body.prof-mode h1 {{ font-family: 'Georgia', serif; letter-spacing: 0; }}

                header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; }}
                .mascot-container {{ text-align: center; background: #fff; border: 1px solid #e2e8f0; padding: 12px; border-radius: 20px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }}
                .mascot {{ width: 100px; height: 100px; border-radius: 12px; object-fit: contain; }}
                .mascot-name {{ font-size: 0.65rem; font-weight: 800; color: #3b82f6; text-transform: uppercase; margin-top: 8px; letter-spacing: 0.1em; }}
                
                h1 {{ color: #0f172a; margin: 0; font-size: 2.75rem; letter-spacing: -0.05em; font-weight: 900; }}
                h2 {{ color: #0f172a; margin-top: 50px; font-size: 1.4rem; display: flex; align-items: center; gap: 12px; font-weight: 800; border-left: 5px solid #3b82f6; padding-left: 20px; text-transform: uppercase; letter-spacing: 0.05em; }}
                
                .status-badge {{ display: inline-block; padding: 6px 16px; border-radius: 999px; font-weight: 700; text-transform: uppercase; font-size: 0.7rem; margin-top: 10px; }}
                .pass {{ background: #dcfce7; color: #166534; }}
                .fail {{ background: #fee2e2; color: #991b1b; }}
                .warning {{ background: #fef9c3; color: #854d0e; }}

                table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 24px; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; font-size: 0.9rem; }}
                th, td {{ text-align: left; padding: 18px; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: #f8fafc; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.75rem; }}
                
                .persona-table th {{ background: #f0f9ff; color: #0369a1; }}
                .risk-text {{ font-size: 0.8rem; color: #64748b; font-style: italic; }}

                code {{ font-family: 'JetBrains Mono', monospace; background: #f1f5f9; padding: 3px 8px; border-radius: 6px; font-size: 0.85em; color: #ef4444; }}
                pre {{ background: #0f172a; color: #e2e8f0; padding: 24px; border-radius: 20px; overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-top: 16px; border: 1px solid #1e293b; }}
                
                .footer {{ margin-top: 60px; text-align: center; color: #94a3b8; font-size: 0.85rem; border-top: 1px solid #e2e8f0; padding-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="report-card">
                <div class="mode-toggle">
                    <label for="prof-mode-checkbox">Professional Mode</label>
                    <input type="checkbox" id="prof-mode-checkbox" onchange="document.body.classList.toggle('prof-mode')">
                </div>

                <header>
                    <div>
                        <h1>🏛️ SME Executive Review</h1>
                        <p style="color: #64748b; margin: 10px 0 0 0; font-weight: 600; font-size: 1.1rem;">Protocol: {getattr(self, 'title', 'Principal Build')}</p>
                        <span class="status-badge {('pass' if all((r['success'] for r in self.results.values())) else 'fail')}">
                            Consensus: {('APPROVED' if all((r['success'] for r in self.results.values())) else 'REJECTED')}
                        </span>
                    </div>
                    <div class="mascot-container">
                        <img src="https://raw.githubusercontent.com/GoogleCloudPlatform/agent-starter-pack/main/docs/assets/kokpi.png" class="mascot" alt="Kokpi">
                        <div class="mascot-name">KOKPI CERTIFIED</div>
                    </div>
                </header>

                <div style="background: #f8fafc; padding: 25px; border-radius: 16px; margin-bottom: 40px; border: 1px solid #e2e8f0;">
                    <h3 style="margin-top:0; font-weight:800; text-transform:uppercase; font-size:0.85rem; color:#64748b;">Board-Level Executive Summary</h3>
                    <p style="margin-bottom:0; font-size:1.05rem;">The following audit was performed by a parallelized array of <strong>Principal SME Personas</strong>. This "Safe-Build" standard ensures that the {getattr(self, 'title', 'Agent')} meets the <strong>Google Well-Architected Framework</strong> requirements for security, reliability, and cost-efficiency.</p>
                </div>

                <h2>🧑‍💼 Principal SME Persona Approval Matrix</h2>
                <table class="persona-table">
                    <thead>
                        <tr>
                            <th>SME Persona</th>
                            <th>Primary Business Risk</th>
                            <th>Module</th>
                            <th>Verdict</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for name, data in self.results.items():
            persona = self.PERSONA_MAP.get(name, 'Automated Auditor')
            risk = self.PRIMARY_RISK_MAP.get(name, 'Architectural Neutrality')
            status = 'APPROVED' if data['success'] else 'REJECTED'
            html_content += f"""
                <tr>
                    <td style="font-weight:700; color:#0f172a;">{persona}</td>
                    <td class="risk-text">{risk}</td>
                    <td>{name}</td>
                    <td><span class="status-badge {('pass' if data['success'] else 'fail')}">{status}</span></td>
                </tr>
            """
        html_content += '</tbody></table>'
        if developer_actions:
            html_content += '\n                <h2>🛠️ Developer Action Plan</h2>\n                <table class="action-table">\n                    <thead>\n                        <tr>\n                            <th>Location (File:Line)</th>\n                            <th>Issue Detected</th>\n                            <th>Recommended Implementation</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n            '
            for action in developer_actions:
                parts = action.split(' | ')
                if len(parts) == 3:
                    html_content += f'\n                        <tr>\n                            <td><code>{parts[0]}</code></td>\n                            <td>{parts[1]}</td>\n                            <td style="color: #059669; font-weight: 600;">{parts[2]}</td>\n                        </tr>\n                    '
            html_content += '</tbody></table>'
        if developer_sources:
            html_content += '\n                <h2>📜 Evidence Bridge: Research & Citations</h2>\n                <table class="source-table">\n                    <thead>\n                        <tr>\n                            <th>Knowledge Pillar</th>\n                            <th>SDK/Pattern Citation</th>\n                            <th>Evidence & Best Practice</th>\n                        </tr>\n                    </thead>\n                    <tbody>\n            '
            for source in developer_sources:
                parts = source.split(' | ')
                if len(parts) == 3:
                    html_content += f'\n                        <tr>\n                            <td style="font-weight: 700;">{parts[0]}</td>\n                            <td><a href="{parts[1]}" class="source-link" target="_blank">View Citation &rarr;</a></td>\n                            <td style="font-size: 0.85rem; color: #475569;">{parts[2]}</td>\n                        </tr>\n                    '
            html_content += '</tbody></table>'
        html_content += '\n                <h2>🔍 Audit Evidence</h2>\n        '
        for name, data in self.results.items():
            html_content += f"<h3>{name}</h3><pre>{data['output']}</pre>"
        html_content += '\n                <div class="footer">\n                    Generated by AgentOps Cockpit Orchestrator v0.9.0. \n                    <br>Ensuring safe-build standards for multi-cloud agentic ecosystems.\n                </div>\n            </div>\n        </body>\n        </html>\n        '
        with open('cockpit_report.html', 'w') as f:
            f.write(html_content)

    def send_email_report(self, recipient: str, smtp_server: str='smtp.gmail.com', port: int=587):
        """Sends the markdown report via email."""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        sender_email = os.environ.get('AGENT_OPS_SENDER_EMAIL')
        sender_password = os.environ.get('AGENT_OPS_SME_TOKEN')
        if not sender_email or not sender_password:
            console.print('[red]❌ Email failed: AGENT_OPS_SENDER_EMAIL or AGENT_OPS_SME_TOKEN not set.[/red]')
            return False
        try:
            msg = MIMEMultipart()
            msg['From'] = f'AgentOps Cockpit Audit <{sender_email}>'
            msg['To'] = recipient
            msg['Subject'] = f"🏁 Audit Report: {getattr(self, 'title', 'Agent Result')}"
            with open(self.report_path, 'r') as f:
                content = f.read()
            msg.attach(MIMEText(content, 'plain'))
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            console.print(f'📧 [bold green]Report emailed successfully to {recipient}![/bold green]')
            return True
        except Exception as e:
            console.print(f'[red]❌ Email failed: {e}[/red]')
            return False

def run_audit(mode: str='quick', target_path: str='.'):
    orchestrator = CockpitOrchestrator()
    target_path = os.path.abspath(target_path)
    title = 'QUICK SAFE-BUILD' if mode == 'quick' else 'DEEP SYSTEM AUDIT'
    subtitle = 'Essential checks for dev-velocity' if mode == 'quick' else 'Full benchmarks & stress-testing'
    console.print(Panel.fit(f'🕹️ [bold blue]AGENTOPS COCKPIT: {title}[/bold blue]\n{subtitle}...', border_style='blue'))
    with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), BarColumn(bar_width=None), TextColumn('[progress.percentage]{task.percentage:>3.0f}%'), console=console, expand=True) as progress:
        base_mod = 'agent_ops_cockpit'
        token_opt_args = [target_path, '--no-interactive']
        if mode == 'quick':
            token_opt_args.append('--quick')

        steps = [
            ('Architecture Review', [sys.executable, '-m', f'{base_mod}.ops.arch_review', 'audit', '--path', target_path]),
            ('Policy Enforcement', [sys.executable, '-m', f'{base_mod}.ops.policy_engine']),
            ('Secret Scanner', [sys.executable, '-m', f'{base_mod}.ops.secret_scanner', 'scan', target_path]),
            ('Token Optimization', [sys.executable, '-m', f'{base_mod}.optimizer', 'audit'] + token_opt_args),
            ('Reliability (Quick)', [sys.executable, '-m', f'{base_mod}.ops.reliability', 'audit', '--quick', '--path', target_path]),
            ('Face Auditor', [sys.executable, '-m', f'{base_mod}.ops.ui_auditor', 'audit', target_path])
        ]
        if mode == 'deep':
            steps.extend([
                ('Quality Hill Climbing', [sys.executable, '-m', f'{base_mod}.eval.quality_climber', 'climb', '--steps', '10']),
                ('Red Team Security (Full)', [sys.executable, '-m', f'{base_mod}.eval.red_team', 'audit', target_path]),
                ('Load Test (Baseline)', [sys.executable, '-m', f'{base_mod}.eval.load_test', 'run', '--requests', '50', '--concurrency', '5']),
                ('Evidence Packing Audit', [sys.executable, '-m', f'{base_mod}.ops.arch_review', 'audit', '--path', target_path])
            ])
        else:
            steps.append(('Red Team (Fast)', [sys.executable, '-m', f'{base_mod}.eval.red_team', 'audit', target_path]))
        tasks = {name: progress.add_task(f'[white]Waiting: {name}', total=100) for name, cmd in steps}
        with ThreadPoolExecutor(max_workers=len(steps)) as executor:
            future_to_audit = {executor.submit(orchestrator.run_command, name, cmd, progress, tasks[name]): name for name, cmd in steps}
            for future in as_completed(future_to_audit):
                name, success = future.result()
    orchestrator.title = title
    orchestrator.generate_report()
    return all((r['success'] for r in orchestrator.results.values()))
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['quick', 'deep'], default='quick')
    parser.add_argument('--path', default='.')
    args = parser.parse_args()
    success = run_audit(mode=args.mode, target_path=args.path)
    sys.exit(0 if success else 1)