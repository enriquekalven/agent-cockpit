import os
import sys
import json
import subprocess
import time
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
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.report_path = "cockpit_final_report.md"
        self.results = {}
        self.total_steps = 7
        self.completed_steps = 0

    def run_command(self, name: str, cmd: list, progress: Progress, task_id: TaskID):
        """Helper to run a command and capture output while updating progress."""
        progress.update(task_id, description=f"[cyan]Running {name}...")

        # Use absolute path for the cockpit source code
        cockpit_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{cockpit_root}{os.pathsep}{env.get('PYTHONPATH', '')}"

        try:
            start_time = time.time()
            # We use Popen to potentially stream output if we wanted,
            # but for now we'll just run it and capture.
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env
            )

            stdout, stderr = process.communicate()
            duration = time.time() - start_time
            success = process.returncode == 0

            output = stdout if success else f"{stdout}\n{stderr}"
            self.results[name] = {"success": success, "output": output, "duration": round(duration, 2)}

            if success:
                progress.update(task_id, description=f"[green]✅ {name} ({round(duration, 1)}s)", completed=100)
            else:
                progress.update(
                    task_id, description=f"[red]❌ {name} Failed", completed=100
                )

            return name, success
        except Exception as e:
            self.results[name] = {"success": False, "output": str(e)}
            progress.update(task_id, description=f"[red]💥 {name} Error", completed=100)
            return name, False

    def save_to_evidence_lake(self, target_path: str):
        """
        Centralizes audit results into a unified 'Evidence Lake' for enterprise tracking.
        """
        lake_path = "evidence_lake.json"
        entry_id = os.path.abspath(target_path)

        fleet_data = {}
        if os.path.exists(lake_path):
            try:
                with open(lake_path, "r") as f:
                    fleet_data = json.load(f)
            except Exception:
                pass

        # Add historical delta tracking
        previous_score = fleet_data.get(entry_id, {}).get("summary", {}).get("score", 0)

        fleet_data[entry_id] = {
            "timestamp": self.timestamp,
            "results": self.results,
            "summary": {
                "passed": all(r["success"] for r in self.results.values()),
                "total_duration": sum(r.get("duration", 0) for r in self.results.values()),
                "health": sum(1 for r in self.results.values() if r["success"])
                / len(self.results)
                if self.results
                else 0,
                "improvement_delta": previous_score,  # Placeholder for more complex delta logic
            },
        }

        with open(lake_path, "w") as f:
            json.dump(fleet_data, f, indent=2)
        print(f"📜 [EVIDENCE LAKE] Centralized log updated for {target_path}")

    PERSONA_MAP = {
        "Architecture Review": "🏛️ Principal Platform Engineer",
        "Policy Enforcement": "⚖️ Governance & Compliance SME",
        "Secret Scanner": "🔐 SecOps Principal",
        "Token Optimization": "💰 FinOps Principal Architect",
        "Reliability (Quick)": "🛡️ QA & Reliability Principal",
        "Quality Hill Climbing": "🧗 AI Quality SME",
        "Red Team Security (Full)": "🚩 Red Team Principal (White-Hat)",
        "Red Team (Fast)": "🚩 Security Architect",
        "Load Test (Baseline)": "🚀 SRE & Performance Principal",
        "Evidence Packing Audit": "📜 Legal & Transparency SME",
        "Face Auditor": "🎭 UX/UI Principal Designer",
    }

    def generate_report(self):
        title = getattr(self, "title", "Audit Report")
        total_duration = sum(r.get("duration", 0) for r in self.results.values())
        report = [
            f"# 🕹️ AgentOps Cockpit: {title}",
            f"**Timestamp**: {self.timestamp}",
            f"**Total Duration**: {total_duration:.2f}s",
            f"**Status**: {'✅ PASS' if all(r['success'] for r in self.results.values()) else '❌ FAIL'}",
            "\n---",
            "\n## 🧑‍💼 Principal SME Persona Approvals",
            "Each pillar of your agent has been reviewed by a specialized SME persona.",
        ]

        persona_table = Table(
            title="🏛️ Persona Approval Matrix",
            show_header=True,
            header_style="bold blue",
        )
        persona_table.add_column("SME Persona", style="cyan")
        persona_table.add_column("Audit Module", style="magenta")
        persona_table.add_column("Verdict", style="bold")

        # Collect developer actions and sources
        developer_actions = []
        developer_sources = []

        # Maturity Delta Logic
        lake_path = "evidence_lake.json"
        improvement_delta = 0
        fleet_data = {}
        target_abs = os.path.abspath(getattr(self, "target_path", "."))

        if os.path.exists(lake_path):
            try:
                with open(lake_path, "r") as f:
                    fleet_data = json.load(f)
                    historical = fleet_data.get(target_abs, {}).get("summary", {})
                    prev_health = historical.get("health", 0) * 100
                    current_health = (
                        sum(1 for r in self.results.values() if r["success"])
                        / len(self.results)
                        * 100
                        if self.results
                        else 0
                    )
                    improvement_delta = current_health - prev_health
            except Exception:
                pass

        for name, data in self.results.items():
            duration = data.get("duration", 0)
            status = f"✅ APPROVED ({duration}s)" if data["success"] else f"❌ REJECTED ({duration}s)"
            persona = self.PERSONA_MAP.get(name, "💼 SME")
            persona_table.add_row(persona, name, status)
            report.append(f"- **{persona}** ([{name}]): {status}")

            # Parse outputs
            if data["output"]:
                for line in data["output"].split("\n"):
                    if "ACTION:" in line:
                        developer_actions.append(line.replace("ACTION:", "").strip())
                    if "SOURCE:" in line:
                        developer_sources.append(line.replace("SOURCE:", "").strip())

        console.print("\n", persona_table)

        if developer_actions:
            report.append("\n## 🛠️ Developer Action Plan")
            report.append(
                "The following specific fixes are required to achieve a passing 'Well-Architected' score."
            )
            report.append("| File:Line | Issue | Recommended Fix |")
            report.append("| :--- | :--- | :--- |")
            for action in developer_actions:
                parts = action.split(" | ")
                if len(parts) == 3:
                    report.append(f"| `{parts[0]}` | {parts[1]} | {parts[2]} |")

        if developer_sources:
            report.append("\n## 📜 Evidence Bridge: Research & Citations")
            report.append(
                "Cross-verified architectural patterns and SDK best-practices mapped to official cloud standards."
            )
            report.append(
                "| Knowledge Pillar | SDK/Pattern Citation | Evidence & Best Practice |"
            )
            report.append("| :--- | :--- | :--- |")
            for source in developer_sources:
                parts = source.split(" | ")
                if len(parts) == 3:
                    report.append(
                        f"| {parts[0]} | [Source Citation]({parts[1]}) | {parts[2]} |"
                    )

        report.append("\n## 🔍 Raw System Artifacts")
        for name, data in self.results.items():
            report.append(f"\n### {name}")
            report.append("```text")
            report.append(data["output"][-2000:] if data["output"] else "No output.")
            report.append("```")

        report.append("\n---")
        report.append(
            "\n*Generated by the AgentOps Cockpit Orchestrator (Parallelized Edition).*"
        )

        with open(self.report_path, "w") as f:
            f.write("\n".join(report))

        # Also generate a professional HTML report
        self._generate_html_report(developer_actions, developer_sources)
        if improvement_delta > 0:
            console.print(
                f"📈 [bold green]Maturity Velocity:[/bold green] +{improvement_delta:.1f}% improvement since last audit!"
            )
            report.append(
                f"### 📈 Maturity Velocity: +{improvement_delta:.1f}% Improvement"
            )
        elif improvement_delta < 0:
            console.print(
                f"📉 [bold red]Maturity Delta:[/bold red] {improvement_delta:.1f}% reduction in compliance."
            )
            report.append(f"### 📉 Maturity Delta: {improvement_delta:.1f}% Reduction")

        console.print("\n")
        console.print(
            Panel(
                f"📄 [bold blue]Final Report generated at {self.report_path}[/bold blue]\n"
                f"📄 [bold blue]Printable HTML Report available at cockpit_report.html[/bold blue]",
                border_style="green",
            )
        )

    def _generate_html_report(self, developer_actions, developer_sources):
        """Generates a premium HTML version of the report with Kokpi mascot."""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>AgentOps Audit: {getattr(self, "title", "Report")}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
                body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: #1e293b; max-width: 1000px; margin: 0 auto; padding: 60px 40px; background: #f1f5f9; }}
                .report-card {{ background: white; padding: 40px; border-radius: 24px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04); border: 1px solid #e2e8f0; }}
                header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 40px; border-bottom: 2px solid #f1f5f9; padding-bottom: 30px; }}
                .mascot-container {{ text-align: center; background: #fff; border: 1px solid #e2e8f0; padding: 10px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
                .mascot {{ width: 80px; height: 80px; border-radius: 12px; object-fit: contain; }}
                .mascot-name {{ font-size: 0.6rem; font-weight: 800; color: #3b82f6; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.1em; }}
                h1 {{ color: #0f172a; margin: 0; font-size: 2.25rem; letter-spacing: -0.025em; font-weight: 900; }}
                h2 {{ color: #0f172a; margin-top: 48px; font-size: 1.25rem; display: flex; align-items: center; gap: 12px; font-weight: 800; border-left: 4px solid #3b82f6; padding-left: 15px; text-transform: uppercase; letter-spacing: 0.05em; }}
                .status-badge {{ display: inline-block; padding: 6px 16px; border-radius: 999px; font-weight: 700; text-transform: uppercase; font-size: 0.75rem; margin-top: 10px; }}
                .pass {{ background: #dcfce7; color: #166534; }}
                .fail {{ background: #fee2e2; color: #991b1b; }}
                table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 24px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }}
                th, td {{ text-align: left; padding: 16px; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: #f8fafc; font-weight: 700; color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
                .action-table th {{ background: #eff6ff; color: #1e40af; }}
                .source-table th {{ background: #f0f9ff; color: #0369a1; }}
                code {{ font-family: 'JetBrains Mono', monospace; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
                pre {{ background: #0f172a; color: #e2e8f0; padding: 24px; border-radius: 16px; overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-top: 16px; border: 1px solid #1e293b; }}
                .source-link {{ color: #3b82f6; text-decoration: none; font-weight: 600; border-bottom: 1px solid transparent; }}
                .source-link:hover {{ border-bottom-color: #3b82f6; }}
                .footer {{ margin-top: 40px; text-align: center; color: #94a3b8; font-size: 0.8rem; border-top: 1px solid #e2e8f0; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="report-card">
                <header>
                    <div>
                        <h1>🕹️ AgentOps Cockpit</h1>
                        <p style="color: #64748b; margin: 8px 0 0 0; font-weight: 500;">Report: {getattr(self, "title", "Build Audit")}</p>
                        <span class="status-badge {"pass" if all(r["success"] for r in self.results.values()) else "fail"}">
                            {"PASSED" if all(r["success"] for r in self.results.values()) else "FAILED"}
                        </span>
                    </div>
                    <div class="mascot-container">
                        <img src="public/kokpi_branded.jpg" class="mascot" alt="Kokpi">
                        <div class="mascot-name">KOKPI APPROVED</div>
                    </div>
                </header>

                <p style="font-size: 0.875rem; color: #64748b;">
                    <strong>Timestamp</strong>: {self.timestamp}<br>
                    <strong>Total Duration</strong>: {sum(r.get("duration", 0) for r in self.results.values()):.2f}s
                </p>

                <h2>🧑‍💼 SME Persona Approvals</h2>
                <table>
                    <thead>
                        <tr>
                            <th>SME Persona</th>
                            <th>Module</th>
                            <th>Verdict</th>
                            <th>Duration</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for name, data in self.results.items():
            persona = self.PERSONA_MAP.get(name, "Automated Auditor")
            status = "APPROVED" if data["success"] else "REJECTED"
            html_content += f"""
                <tr>
                    <td>{persona}</td>
                    <td>{name}</td>
                    <td><span class="status-badge {"pass" if data["success"] else "fail"}">{status}</span></td>
                    <td><code>{data.get("duration", 0)}s</code></td>
                </tr>
            """

        html_content += """
                    </tbody>
                </table>
        """

        if developer_actions:
            html_content += """
                <h2>🛠️ Developer Action Plan</h2>
                <table class="action-table">
                    <thead>
                        <tr>
                            <th>Location (File:Line)</th>
                            <th>Issue Detected</th>
                            <th>Recommended Implementation</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for action in developer_actions:
                parts = action.split(" | ")
                if len(parts) == 3:
                    html_content += f"""
                        <tr>
                            <td><code>{parts[0]}</code></td>
                            <td>{parts[1]}</td>
                            <td style="color: #059669; font-weight: 600;">{parts[2]}</td>
                        </tr>
                    """
            html_content += "</tbody></table>"

        if developer_sources:
            html_content += """
                <h2>📜 Evidence Bridge: Research & Citations</h2>
                <table class="source-table">
                    <thead>
                        <tr>
                            <th>Knowledge Pillar</th>
                            <th>SDK/Pattern Citation</th>
                            <th>Evidence & Best Practice</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for source in developer_sources:
                parts = source.split(" | ")
                if len(parts) == 3:
                    html_content += f"""
                        <tr>
                            <td style="font-weight: 700;">{parts[0]}</td>
                            <td><a href="{parts[1]}" class="source-link" target="_blank">View Citation &rarr;</a></td>
                            <td style="font-size: 0.85rem; color: #475569;">{parts[2]}</td>
                        </tr>
                    """
            html_content += "</tbody></table>"

        html_content += """
                <h2>🔍 Audit Evidence</h2>
        """

        for name, data in self.results.items():
            html_content += f"<h3>{name}</h3><pre>{data['output']}</pre>"

        html_content += """
                <div class="footer">
                    Generated by AgentOps Cockpit Orchestrator v0.9.8. 
                    <br>Ensuring safe-build standards for multi-cloud agentic ecosystems.
                </div>
            </div>
        </body>
        </html>
        """

        with open("cockpit_report.html", "w") as f:
            f.write(html_content)

    def send_email_report(
        self, recipient: str, smtp_server: str = "smtp.gmail.com", port: int = 587
    ):
        """Sends the markdown report via email."""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = os.environ.get("AGENT_OPS_SENDER_EMAIL")
        sender_password = os.environ.get(
            "AGENT_OPS_SME_TOKEN"
        )  # Custom auth token for the cockpit

        if not sender_email or not sender_password:
            console.print(
                "[red]❌ Email failed: AGENT_OPS_SENDER_EMAIL or AGENT_OPS_SME_TOKEN not set.[/red]"
            )
            return False

        try:
            msg = MIMEMultipart()
            msg["From"] = f"AgentOps Cockpit Audit <{sender_email}>"
            msg["To"] = recipient
            msg["Subject"] = (
                f"🏁 Audit Report: {getattr(self, 'title', 'Agent Result')}"
            )

            # Use the markdown as content
            with open(self.report_path, "r") as f:
                content = f.read()

            msg.attach(MIMEText(content, "plain"))

            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            console.print(
                f"📧 [bold green]Report emailed successfully to {recipient}![/bold green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]❌ Email failed: {e}[/red]")
            return False


def run_audit(
    mode: str = "quick", target_path: str = ".", title: str = "QUICK SAFE-BUILD"
):
    orchestrator = CockpitOrchestrator()
    orchestrator.target_path = target_path

    subtitle = (
        "Essential checks for dev-velocity"
        if mode == "quick"
        else "Deep production-readiness audit"
    )

    console.print(
        Panel.fit(
            f"🕹️ [bold blue]AGENTOPS COCKPIT: {title}[/bold blue]\n{subtitle}...",
            border_style="blue",
        )
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        expand=True,
    ) as progress:
        # Use the consolidated package
        base_mod = "agent_ops_cockpit"

        # 1. Essential "Safe-Build" Steps (Fast)
        token_opt_cmd = [
            sys.executable,
            "-m",
            f"{base_mod}.optimizer",
            target_path,
            "--no-interactive",
        ]
        if mode == "quick":
            token_opt_cmd.append("--quick")

        steps = [
            (
                "Architecture Review",
                [
                    sys.executable,
                    "-m",
                    f"{base_mod}.ops.arch_review",
                    "--path",
                    target_path,
                ],
            ),
            (
                "Policy Enforcement",
                [sys.executable, "-m", f"{base_mod}.ops.policy_engine"],
            ),  # Policy is global to cockpit
            (
                "Secret Scanner",
                [sys.executable, "-m", f"{base_mod}.ops.secret_scanner", target_path],
            ),
            ("Token Optimization", token_opt_cmd),
            (
                "Reliability (Quick)",
                [
                    sys.executable,
                    "-m",
                    f"{base_mod}.ops.reliability",
                    "--quick",
                    "--path",
                    target_path,
                ],
            ),
            (
                "Face Auditor",
                [
                    sys.executable,
                    "-m",
                    f"{base_mod}.ops.ui_auditor",
                    "--path",
                    target_path,
                ],
            ),
        ]

        # 2. Add "Deep" steps if requested
        if mode == "deep":
            steps.extend(
                [
                    (
                        "Quality Hill Climbing",
                        [
                            sys.executable,
                            "-m",
                            f"{base_mod}.eval.quality_climber",
                            "--steps",
                            "10",
                        ],
                    ),
                    (
                        "Red Team Security (Full)",
                        [
                            sys.executable,
                            "-m",
                            f"{base_mod}.eval.red_team",
                            target_path,
                        ],
                    ),
                    (
                        "Load Test (Baseline)",
                        [
                            sys.executable,
                            "-m",
                            f"{base_mod}.eval.load_test",
                            "--requests",
                            "50",
                            "--concurrency",
                            "5",
                        ],
                    ),
                    (
                        "Evidence Packing Audit",
                        [
                            sys.executable,
                            "-m",
                            f"{base_mod}.ops.arch_review",
                            "--path",
                            target_path,
                        ],
                    ),
                ]
            )
        else:
            # Quick mode still needs a fast security check
            steps.append(
                (
                    "Red Team (Fast)",
                    [sys.executable, "-m", f"{base_mod}.eval.red_team", target_path],
                )
            )

        # Add tasks to progress bar
        tasks = {
            name: progress.add_task(f"[white]Waiting: {name}", total=100)
            for name, cmd in steps
        }

        # Execute in parallel
        with ThreadPoolExecutor(max_workers=len(steps)) as executor:
            future_to_audit = {
                executor.submit(
                    orchestrator.run_command, name, cmd, progress, tasks[name]
                ): name
                for name, cmd in steps
            }

            for future in as_completed(future_to_audit):
                name, success = future.result()

    orchestrator.title = title
    orchestrator.generate_report()
    orchestrator.save_to_evidence_lake(target_path)

    # Return True if all steps passed
    return all(r["success"] for r in orchestrator.results.values())


def workspace_audit(root_path: str = ".", mode: str = "quick"):
    """
    Fleet Orchestration: Scans a workspace for agents and audits them in parallel.
    """
    console.print(
        Panel(
            f"🛸 [bold blue]COCKPIT WORKSPACE MODE: FLEET ORCHESTRATION[/bold blue]\n"
            f"Scanning Root: [dim]{root_path}[/dim]",
            border_style="cyan",
        )
    )

    agents = []
    for entry in os.listdir(root_path):
        full_path = os.path.join(root_path, entry)
        if os.path.isdir(full_path) and not entry.startswith("."):
            # Heuristic: must contain agentic patterns
            if any(
                os.path.exists(os.path.join(full_path, f))
                for f in ["agent.py", "README.md", "pyproject.toml"]
            ):
                agents.append(full_path)

    if not agents:
        console.print("[yellow]⚠️ No agents found in workspace.[/yellow]")
        return

    console.print(
        f"🔍 Identified [bold]{len(agents)} agents[/bold]. Initializing parallel fleet audit...\n"
    )

    results = {}
    # Increased max_workers for fleet throughput
    with ThreadPoolExecutor(max_workers=min(10, len(agents))) as executor:
        future_map = {
            executor.submit(run_audit, mode, agent): agent for agent in agents
        }

        for future in as_completed(future_map):
            agent_path = future_map[future]
            try:
                success = future.result()
                results[agent_path] = success
                status = "[green]PASS[/green]" if success else "[red]FAIL[/red]"
                console.print(
                    f"📡 [bold]Audit Complete[/bold]: {agent_path} -> {status}"
                )
            except Exception as e:
                console.print(f"[red]💥 Error auditing {agent_path}: {e}[/red]")

    # Global Fleet Report Summary
    passed_count = sum(1 for r in results.values() if r)
    fleet_table = Table(title="🏢 ENTERPRISE FLEET COMPLIANCE STATUS")
    fleet_table.add_column("Agent Workspace", style="cyan")
    fleet_table.add_column("Verdict", style="bold")

    for agent, success in results.items():
        fleet_table.add_row(
            agent, "[green]APPROVED[/green]" if success else "[red]REJECTED[/red]"
        )

    console.print("\n")
    console.print(fleet_table)
    console.print(
        f"\n🚀 [bold]Fleet Score: {passed_count}/{len(agents)} Agents Production Ready.[/bold]\n"
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["quick", "deep"], default="quick")
    parser.add_argument("--path", default=".")
    parser.add_argument(
        "--workspace", action="store_true", help="Run audit on all agents in the path"
    )
    args = parser.parse_args()

    if args.workspace:
        workspace_audit(root_path=args.path, mode=args.mode)
    else:
        success = run_audit(mode=args.mode, target_path=args.path)
        sys.exit(0 if success else 1)
