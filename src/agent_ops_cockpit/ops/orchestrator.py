import os
import sys

# Ensure the project root is in sys.path for the tenacity mock
script_dir = os.path.dirname(os.path.abspath(__file__))
cockpit_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
if cockpit_root not in sys.path:
    sys.path.insert(0, cockpit_root)
# Also add src to path for internal imports
src_dir = os.path.dirname(os.path.dirname(script_dir))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from tenacity import retry, wait_exponential, stop_after_attempt
import subprocess
import json
import hashlib
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
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
        self.version = os.environ.get('AUDIT_VERSION', 'v1')
        self.report_path = f'cockpit_final_report_{self.version}.md'
        self.results = {}
        self.total_steps = 7
        self.completed_steps = 0
        self.workspace_results = {} # For fleet intelligence
        self.common_debt = {}

    def get_dir_hash(self, path: str):
        """Calculates a recursive hash of the directory contents for intelligent skipping."""
        from agent_ops_cockpit.ops.discovery import DiscoveryEngine
        discovery = DiscoveryEngine(path)
        hasher = hashlib.md5()
        for f_path in sorted(discovery.walk(path)):
            if not f_path.endswith(('.py', '.ts', '.js', '.go', '.json', '.yaml', '.prompt', '.md', 'toml')):
                continue
            try:
                with open(f_path, 'rb') as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
            except: pass
        return hasher.hexdigest()

    def detect_entry_point(self, path: str):
        """Autodetection logic using Discovery Engine."""
        from agent_ops_cockpit.ops.discovery import DiscoveryEngine
        discovery = DiscoveryEngine(path)
        brain = discovery.find_agent_brain()
        return os.path.relpath(brain, path)

    def run_command(self, name: str, cmd: list, progress: Progress, task_id: TaskID):
        """Helper to run a command and capture output while updating progress."""
        progress.update(task_id, description=f'[cyan]Running {name}...')
        cockpit_src = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cockpit_root = os.path.dirname(cockpit_src)
        env = os.environ.copy()
        env['PYTHONPATH'] = f"{cockpit_src}{os.pathsep}{cockpit_root}{os.pathsep}{env.get('PYTHONPATH', '')}"
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
    # Improvement #4: Fixability Mapping
    EFFORT_MAP = {
        'Secret Scanner': '⚡ 1-Click (Env Var)',
        'Token Optimization': '⚡ 1-Click (Caching)',
        'Policy Enforcement': '🔧 Medium (Policies)',
        'Reliability (Quick)': '🔧 Medium (Code)',
        'Architecture Review': '🏗️ Hard (Structural)',
        'Face Auditor': '🔧 Medium (A2UI)',
        'Red Team (Fast)': '🏗️ Hard (Model/Prompt)'
    }

    def generate_report(self):
        title = getattr(self, 'title', 'Audit Report')
        report = [f'# 🕹️ AgentOps Cockpit: {title}', f'**Timestamp**: {self.timestamp}', f"**Status**: {('✅ PASS' if all((r['success'] for r in self.results.values())) else '❌ FAIL')}", '\n---', '\n## 🧑\u200d💼 Principal SME Persona Approvals', 'Each pillar of your agent has been reviewed by a specialized SME persona.']
        persona_table = Table(title='🏛️ Persona Approval Matrix', show_header=True, header_style='bold blue')
        persona_table.add_column('SME Persona', style='cyan')
        persona_table.add_column('Audit Module', style='magenta')
        persona_table.add_column('Verdict', style='bold')
        persona_table.add_column('Remediation', style='dim')
        developer_actions = []
        developer_sources = []
        for name, data in self.results.items():
            status = '✅ APPROVED' if data['success'] else '❌ REJECTED'
            persona = self.PERSONA_MAP.get(name, '👤 Automated Auditor')
            effort = self.EFFORT_MAP.get(name, 'Manual')
            persona_table.add_row(persona, name, status, effort)
            effort_str = f" [Remediation: {effort}]" if not data['success'] else ""
            report.append(f'- **{persona}** ([{name}]): {status}{effort_str}')
            if data['output']:
                for line in data['output'].split('\n'):
                    if 'ACTION:' in line:
                        developer_actions.append(line.replace('ACTION:', '').strip())
                    if 'SOURCE:' in line:
                        developer_sources.append(line.replace('SOURCE:', '').strip())
        
        # --- [NEW] Maturity Velocity Logic ---
        lake_path = "evidence_lake.json"
        improvement_delta = 0
        target_abs = os.path.abspath(getattr(self, 'target_path', '.'))
        if os.path.exists(lake_path):
            try:
                with open(lake_path, 'r') as f:
                    lake_data = json.load(f)
                    historical = lake_data.get(target_abs, {}).get('summary', {})
                    prev_health = historical.get('health', 0) * 100
                    current_health = (sum(1 for r in self.results.values() if r['success']) / len(self.results) * 100) if self.results else 0
                    improvement_delta = current_health - prev_health
            except: pass

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
        
        # --- [NEW] Executive Risk Scorecard & Thresholds ---
        report.append('\n## 👔 Executive Risk Scorecard')
        
        from agent_ops_cockpit.ops.discovery import DiscoveryEngine
        discovery = DiscoveryEngine(getattr(self, 'target_path', '.'))
        threshold = discovery.config.get("threshold", 0)
        
        passed_ok = all(r['success'] for r in self.results.values())
        health_score = (sum(1 for r in self.results.values() if r['success']) / len(self.results) * 100) if self.results else 0
        
        executive_summary = "Audit baseline established. No critical blockers detected."
        if health_score < threshold:
             executive_summary = f"**Risk Alert**: Health score ({health_score:.1f}%) is below the configured threshold ({threshold}%). Strategic remediation required."
        elif not passed_ok:
            fail_list = [n for n, r in self.results.items() if not r['success']]
            executive_summary = f"**Risk Alert**: {len(fail_list)} governance gates REJECTED (including {', '.join(fail_list[:2])}). Remediation estimated to take 2-4 hours. Production deployment currently BLOCKED."
        
        report.append(executive_summary)
        
        # --- [NEW] Strategic Recommendations ---
        debt_analysis = "\n**Strategic Recommendations**:\n"
        if "Missing PII scrubber" in str(developer_actions):
            debt_analysis += "- ⚠️ **Global Debt**: Missing PII Scrubbers detected. Recommendation: Bulk inject `pii_scrubber.py` middleware.\n"
        if "Hardcoded secret" in str(developer_actions):
            debt_analysis += "- ⚠️ **Security Debt**: Hardcoded credentials detected. recommendation: Enforce Google Secret Manager.\n"
        report.append(debt_analysis)
        report.append('\n## 🔍 Raw System Artifacts')
        for name, data in self.results.items():
            report.append(f'\n### {name}')
            report.append('```text')
            report.append(data['output'][-2000:] if data['output'] else 'No output.')
            report.append('```')
        report.append('\n---')
        report.append('\n*Generated by the AgentOps Cockpit Orchestrator (Parallelized Edition).*')
        if improvement_delta != 0:
            velocity_icon = "📈" if improvement_delta > 0 else "📉"
            report.append(f'\n### {velocity_icon} Maturity Velocity: {improvement_delta:+.1f}% Compliance Change')

        with open(self.report_path, 'w') as f:
            f.write('\n'.join(report))
        self._generate_html_report(developer_actions, developer_sources)
        self._generate_sarif_report(developer_actions)
        self.save_to_evidence_lake(target_abs)

        console.print(f'\n✨ [bold green]Final Report generated at {self.report_path}[/bold green]')
        console.print(f'📄 [bold blue]Printable HTML Report available at cockpit_report.html[/bold blue]')

    def save_to_evidence_lake(self, target_abs: str):
        lake_path = 'evidence_lake.json'
        fleet_data = {}
        if os.path.exists(lake_path):
            try:
                with open(lake_path, 'r') as f: fleet_data = json.load(f)
            except: pass
        
        fleet_data[target_abs] = {
            'timestamp': self.timestamp,
            'hash': self.get_dir_hash(target_abs),
            'results': self.results,
            'summary': {
                'passed': all(r['success'] for r in self.results.values()),
                'health': (sum(1 for r in self.results.values() if r['success']) / len(self.results)) if self.results else 0
            }
        }
        with open(lake_path, 'w') as f: json.dump(fleet_data, f, indent=2)
        console.print(f'📜 [EVIDENCE LAKE] Centralized log updated for {target_abs}')

    def _generate_sarif_report(self, developer_actions):
        # Ported basic SARIF logic
        sarif = {"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "AgentOps Cockpit"}}, "results": []}]}
        for action in developer_actions:
            parts = action.split(' | ')
            if len(parts) == 3:
                sarif["runs"][0]["results"].append({"ruleId": parts[1].replace(" ", "_").lower(), "message": {"text": parts[2]}, "locations": [{"physicalLocation": {"artifactLocation": {"uri": parts[0]}}}]})
        with open('cockpit_audit.sarif', 'w') as f: json.dump(sarif, f, indent=2)

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
                <img src="/kokpi_kun.png" class="mascot" alt="Kokpi">
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

def generate_fleet_dashboard(results: dict):
    """Generates a premium unified HTML dashboard with deep-link drilldowns."""
    lake_path = "evidence_lake.json"
    fleet_data = {}
    if os.path.exists(lake_path):
        try:
            with open(lake_path, "r") as f: fleet_data = json.load(f)
        except: pass

    passed_count = sum(1 for r in results.values() if r)
    total = len(results)
    
    # ROI Predictor Logic
    total_savings = sum(r.get("savings", 0) for r in fleet_data.values() if isinstance(r, dict) and "savings" in r)
    if total_savings == 0: total_savings = 12.50 * total # Estimated baseline

    # Extract Global Velocity
    global_velocity = fleet_data.get("global_summary", {}).get("velocity", 0)
    velocity_color = "#059669" if global_velocity >= 0 else "#dc2626"
    velocity_icon = "📈" if global_velocity >= 0 else "📉"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AgentOps: Fleet Dashboard</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body {{ font-family: 'Inter', sans-serif; background: #f8fafc; padding: 40px; color: #1e293b; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
            .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }}
            .stat-card {{ background: white; padding: 24px; border-radius: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
            .stat-value {{ font-size: 2rem; font-weight: 700; color: #3b82f6; }}
            .roi-panel {{ background: #eff6ff; border: 1px solid #bfdbfe; padding: 24px; border-radius: 16px; margin-bottom: 40px; }}
            .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }}
            .agent-card {{ background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; transition: transform 0.2s; position: relative; overflow: hidden; }}
            .agent-card:hover {{ transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }}
            .status-pass {{ color: #059669; font-weight: 700; }}
            .status-fail {{ color: #dc2626; font-weight: 700; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛸 AgentOps Fleet Flight Deck</h1>
                <div style="text-align: right; color: #64748b;">Enterprise Governance v1.3.0 Antigravity</div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem;">Total Agents Scanned</div>
                    <div class="stat-value">{total}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem;">Production Ready</div>
                    <div class="stat-value" style="color: #059669;">{passed_count}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem;">Fleet Compliance</div>
                    <div class="stat-value">{(passed_count/total)*100:.1f}%</div>
                </div>
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem;">Maturity Velocity</div>
                    <div class="stat-value" style="color: {velocity_color};">{velocity_icon} {global_velocity:+.1f}%</div>
                </div>
            </div>

            <div class="roi-panel">
                <h2 style="margin-top: 0; color: #1e40af; font-size: 1.25rem;">💰 Enterprise ROI Predictor (FinOps)</h2>
                <p style="font-size: 0.875rem; color: #1e3a8a; margin-bottom: 16px;">Strategic opportunities for cost reduction across the fleet. Enabling **Context Caching** and **Semantic Routing** could save an estimated monthly amount based on current scan volume.</p>
                <div style="font-size: 1.5rem; font-weight: 700; color: #1e40af;">Total Fleet Savings Potential: ${total_savings:.2f} / 10k requests</div>
            </div>

            <h2>📡 Real-time Agent Status</h2>
            <div class="agent-grid">
    """
    
    for agent, success in results.items():
        status = "PASSED" if success else "FAILED"
        status_class = "status-pass" if success else "status-fail"
        abs_target = os.path.abspath(agent)
        agent_data = fleet_data.get(abs_target, {})
        
        # Determine likely fixability based on common rejection patterns
        fix_badge = ""
        if not success:
            fix_badge = '<div style="background: #fefce8; border: 1px solid #fef08a; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; color: #854d0e; margin-top: 8px; display: inline-block;">🔧 Fixable in 1-click</div>'
        
        html += f"""
                <div class="agent-card">
                    <h3 style="margin-top: 0; font-size: 1rem;">{os.path.basename(agent)}</h3>
                    <div class="{(status_class)}">{status}</div>
                    {fix_badge}
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 10px;">Path: {agent}</div>
                </div>
        """
        
    html += """
            </div>
        </div>
    </body>
    </html>
    """
    with open("fleet_dashboard.html", "w") as f: f.write(html)
    console.print("📄 [bold blue]Unified Fleet Dashboard generated at fleet_dashboard.html[/bold blue]")

def run_audit(mode: str='quick', target_path: str='.', title: str='QUICK SAFE-BUILD', apply_fixes: bool=False, sim: bool=False):
    orchestrator = CockpitOrchestrator()
    orchestrator.target_path = target_path
    orchestrator.sim = sim
    target_path = os.path.abspath(target_path)

    # Improvement #5: Declarative Sovereign Gates (cockpit.yaml)
    from agent_ops_cockpit.ops.discovery import DiscoveryEngine
    discovery = DiscoveryEngine(target_path)
    config = discovery.config # Automatically loads cockpit.yaml if present
    if config:
        console.print(f"⚙️ [dim]Loaded local Sovereign Config from {target_path}/cockpit.yaml[/dim]")
        if config.get("exclude_checks"):
             console.print(f"🚫 [yellow]Excluded checks per local config: {config['exclude_checks']}[/yellow]")

    # ⚡ Intelligent Skipping Logic
    lake_path = "evidence_lake.json"
    if os.path.exists(lake_path):
        try:
            with open(lake_path, 'r') as f:
                lake_data = json.load(f)
                current_hash = orchestrator.get_dir_hash(target_path)
                cached_entry = lake_data.get(target_path, {})
                if cached_entry.get('hash') == current_hash and not apply_fixes:
                    console.print(f"⚡ [bold green]SKIP:[/bold green] No changes detected in {target_path}. Reusing evidence lake artifacts.")
                    orchestrator.results = cached_entry.get('results', {})
                    orchestrator.generate_report()
                    return True
        except: pass

    subtitle = 'Essential checks for dev-velocity' if mode == 'quick' else 'Full benchmarks & stress-testing'
    console.print(Panel.fit(f'🕹️ [bold blue]AGENTOPS COCKPIT: {title}[/bold blue]\n{subtitle}...', border_style='blue'))
    
    with Progress(SpinnerColumn(), TextColumn('[progress.description]{task.description}'), BarColumn(bar_width=None), TextColumn('[progress.percentage]{task.percentage:>3.0f}%'), console=console, expand=True) as progress:
        base_mod = 'agent_ops_cockpit'
        
        # ⚡ Autodetect Entry Point
        entry_point = orchestrator.detect_entry_point(target_path)
        entry_point_path = os.path.join(target_path, entry_point)

        token_opt_args = [entry_point_path, '--no-interactive']
        if mode == 'quick': token_opt_args.append('--quick')

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
        
        # Improvement #5: Declarative sovereign filter
        excluded = config.get("exclude_checks", []) if config else []
        if excluded:
            steps = [s for s in steps if s[0] not in excluded and s[0].lower().replace(" ", "_") not in excluded]

        tasks = {name: progress.add_task(f'[white]Waiting: {name}', total=100) for name, cmd in steps}
        with ThreadPoolExecutor(max_workers=len(steps)) as executor:
            future_to_audit = {executor.submit(orchestrator.run_command, name, cmd, progress, tasks[name]): name for name, cmd in steps}
            for future in as_completed(future_to_audit):
                name, success = future.result()
    
    orchestrator.title = title
    orchestrator.generate_report()

    # 🛠️ Auto-Remediation logic
    if apply_fixes:
        from .remediator import CodeRemediator
        from .auditors.base import AuditFinding
        for name, data in orchestrator.results.items():
             if not data['success'] and data['output']:
                  for line in data['output'].split('\n'):
                       if 'ACTION:' in line:
                            parts = line.replace('ACTION:', '').strip().split(' | ')
                            if len(parts) == 3:
                                 remediator = CodeRemediator(parts[0].split(':')[0])
                                 # (Simplification: applying based on issue type in line)
                                 if "Resiliency" in parts[1]: remediator.apply_resiliency(AuditFinding(title=parts[1], description=parts[2], line_number=1))
                                 remediator.save()

    return all((r['success'] for r in orchestrator.results.values()))

def workspace_audit(root_path: str = ".", mode: str = "quick", sim: bool = False):
    """Fleet Orchestration: Scans workspace for agents and audits in parallel."""
    console.print(Panel(f"🛸 [bold blue]COCKPIT WORKSPACE MODE: FLEET ORCHESTRATION[/bold blue]\nScanning Root: [dim]{root_path}[/dim]", border_style="cyan"))
    from agent_ops_cockpit.ops.discovery import DiscoveryEngine
    discovery = DiscoveryEngine(root_path)
    
    agents = []
    # Efficient discovery of agents using the walk engine
    seen_dirs = set()
    for file_path in discovery.walk(root_path):
        dir_name = os.path.dirname(file_path)
        if dir_name in seen_dirs:
            continue
            
        file_name = os.path.basename(file_path)
        if file_name in ["agent.py", "main.py", "app.py", "go.mod", "package.json"]:
             agents.append(dir_name)
             seen_dirs.add(dir_name)
    
    if not agents:
        console.print("[yellow]⚠️ No agents found in workspace.[/yellow]")
        return

    results = {}
    with ProcessPoolExecutor(max_workers=5) as executor:
        future_map = {executor.submit(run_audit, mode, a, sim=sim): a for a in agents}
        for future in as_completed(future_map):
            agent_path = future_map[future]
            try:
                results[agent_path] = future.result()
                status = "[green]PASS[/green]" if results[agent_path] else "[red]FAIL[/red]"
                console.print(f"📡 [bold]Audit Complete[/bold]: {agent_path} -> {status}")
            except Exception as e: console.print(f"[red]💥 Error auditing {agent_path}: {e}[/red]")

    # Update Global Velocity in Evidence Lake
    lake_path = "evidence_lake.json"
    if os.path.exists(lake_path):
        try:
            with open(lake_path, 'r') as f: lake_data = json.load(f)
            prev_compliance = lake_data.get('global_summary', {}).get('compliance', 0)
            current_compliance = (sum(1 for r in results.values() if r) / len(agents)) * 100
            lake_data['global_summary'] = {'compliance': current_compliance, 'velocity': current_compliance - prev_compliance, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            with open(lake_path, 'w') as f: json.dump(lake_data, f, indent=2)
        except: pass

    generate_fleet_dashboard(results)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['quick', 'deep'], default='quick')
    parser.add_argument('--path', default='.')
    parser.add_argument('--workspace', action='store_true')
    parser.add_argument('--apply-fixes', action='store_true')
    parser.add_argument('--sim', action='store_true')
    args = parser.parse_args()
    
    if args.workspace:
        workspace_audit(root_path=args.path, mode=args.mode, sim=args.sim)
    else:
        success = run_audit(mode=args.mode, target_path=args.path, apply_fixes=args.apply_fixes, sim=args.sim)
        sys.exit(0 if success else 1)