import os
import json
import hashlib
from datetime import datetime
from rich.console import Console

console = Console()

def generate_fleet_dashboard(results: dict):
    """Generates a premium unified HTML dashboard with deep-link drilldowns and Maturity Radar Charts."""
    lake_path = os.path.join(os.getcwd(), '.cockpit', 'evidence_lake.json')
    fleet_data = {}
    if os.path.exists(lake_path):
        try:
            with open(lake_path, "r") as f:
                fleet_data = json.load(f)
        except Exception:
            pass

    total = len(results)
    
    # Extract Granular Compliance from Global Summary
    global_summary = fleet_data.get("global_summary", {})
    compliance_score = global_summary.get("compliance", 0)
    
    passed_count = sum(1 for r in results.values() if r == 0)
    # If no agent fully passes, we show the granular compliance score in the header
    display_compliance = compliance_score if passed_count == 0 else (passed_count/total)*100
    
    # ROI Predictor Logic
    total_savings = sum(r.get("savings", 0) for r in fleet_data.values() if isinstance(r, dict) and "savings" in r)
    if total_savings == 0:
        total_savings = 12.50 * total # Estimated baseline

    # Extract Global Velocity
    global_velocity = global_summary.get("velocity", 0)
    velocity_color = "#059669" if global_velocity >= 0 else "#dc2626"
    velocity_icon = "📈" if global_velocity >= 0 else "📉"

    # Maturity Radar Data (Averaged across fleet)
    radar_labels = ["Reliability", "Safety", "A2UI", "FinOps", "Grounding"]
    radar_values = [0, 0, 0, 0, 0]
    
    mapping = {
        "Reliability (Quick)": 0,
        "Red Team (Fast)": 1,
        "Red Team Security (Full)": 1,
        "Face Auditor": 2,
        "Token Optimization": 3,
        "RAG Fidelity Audit": 4
    }

    bucket_counts = [0] * 5
    for path, data in fleet_data.items():
        if path == "global_summary":
            continue
        agent_results = data.get("results", {})
        for audit_name, audit_res in agent_results.items():
            idx = mapping.get(audit_name)
            if idx is not None:
                radar_values[idx] += 100 if audit_res.get("success") else 30
                bucket_counts[idx] += 1

    final_values = []
    for i in range(5):
        val = radar_values[i] / max(1, bucket_counts[i]) if bucket_counts[i] > 0 else 20
        final_values.append(round(val, 1))

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AgentOps: Fleet Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
            body {{ font-family: 'Inter', sans-serif; background: #f8fafc; padding: 40px; color: #1e293b; line-height: 1.5; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
            .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }}
            .stat-card {{ background: white; padding: 24px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }}
            .stat-value {{ font-size: 2.25rem; font-weight: 800; color: #3b82f6; letter-spacing: -0.025em; }}
            .dashboard-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin-bottom: 40px; }}
            .roi-panel {{ background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; padding: 30px; border-radius: 24px; }}
            .radar-panel {{ background: white; padding: 30px; border-radius: 24px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px; }}
            .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 24px; }}
            .agent-card {{ background: white; padding: 24px; border-radius: 20px; border: 1px solid #e2e8f0; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; }}
            .agent-card:hover {{ transform: translateY(-8px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04); border-color: #3b82f6; }}
            .status-pass {{ color: #059669; font-weight: 700; background: #ecfdf5; padding: 4px 12px; border-radius: 999px; font-size: 0.875rem; display: inline-block; }}
            .status-fail {{ color: #dc2626; font-weight: 700; background: #fef2f2; padding: 4px 12px; border-radius: 999px; font-size: 0.875rem; display: inline-block; }}
            h1, h2, h3 {{ font-weight: 800; letter-spacing: -0.025em; }}
            .badge {{ background: #3b82f6; color: white; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; margin-bottom: 8px; display: inline-block; text-transform: uppercase; }}
            #radarContainer {{ width: 100%; max-width: 400px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <span class="badge">Enterprise Governance v1.4.0</span>
                    <h1 style="margin: 0; font-size: 2.5rem;">🛸 AgentOps Cockpit</h1>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #64748b;">Fleet Flight Deck</div>
                    <div style="font-size: 0.875rem; color: #94a3b8;">System Time: {datetime.now().strftime("%H:%M:%S")}</div>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Total Agents</div>
                    <div class="stat-value">{total}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Maturity Score</div>
                    <div class="stat-value">{display_compliance:.1f}%</div>
                </div>
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Ready for Prod</div>
                    <div class="stat-value" style="color: #059669;">{passed_count}</div>
                </div>
                <div class="stat-card">
                    <div style="color: #64748b; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">Agility Velocity</div>
                    <div class="stat-value" style="color: {velocity_color};">{velocity_icon} {global_velocity:+.1f}%</div>
                </div>
            </div>

            <div class="dashboard-grid">
                <div class="roi-panel">
                    <h2 style="margin-top: 0; color: #1e40af; font-size: 1.5rem;">💰 Enterprise ROI Waterfall</h2>
                    <p style="font-size: 1rem; color: #1e3a8a; margin-bottom: 20px;">Strategic opportunities for cost reduction. Implementing <strong>Context Caching</strong> and <strong>Model PIVOT</strong> could save an estimated monthly amount based on fleet telemetry.</p>
                    <div style="font-size: 2rem; font-weight: 800; color: #1e40af;">Total Opportunity: ${total_savings:,.2f}</div>
                    <div style="margin-top: 15px; font-size: 0.875rem; color: #3b82f6; font-weight: 600;">&rarr; Run 'agent-ops roi' for breakdown</div>
                </div>
                
                <div class="radar-panel">
                    <h3 style="margin: 0 0 20px 0; font-size: 1.125rem; color: #64748b; text-transform: uppercase;">Maturity Radar</h3>
                    <div id="radarContainer">
                        <canvas id="radarChart"></canvas>
                    </div>
                </div>
            </div>

            <h2 style="margin-bottom: 24px;">📡 Real-time Fleet Status</h2>
            <div class="agent-grid">
    """
    
    for agent, success in results.items():
        status = "PASSED" if success == 0 else "FAILED"
        status_class = "status-pass" if success == 0 else "status-fail"
        abs_target = os.path.abspath(agent)
        agent_data = fleet_data.get(abs_target, {})
        
        fix_badge = ""
        if success != 0:
            fix_badge = '<div style="background: #fffbeb; border: 1px solid #fef3c7; padding: 6px 12px; border-radius: 8px; font-size: 0.75rem; color: #92400e; margin-top: 12px; display: inline-block; font-weight: 600;">⚡ AUTO-FIX AVAILABLE</div>'
        
        failing_modules = []
        if success != 0 and agent_data:
            agent_results = agent_data.get('results', {})
            failing_modules = [m for m, r in agent_results.items() if not r.get('success')]
        
        failure_summary = ""
        if failing_modules:
            failure_list = "".join([f'<li style="margin-bottom: 4px;">{m}</li>' for m in failing_modules[:3]])
            if len(failing_modules) > 3:
                failure_list += f'<li>+ {len(failing_modules)-3} more</li>'
            failure_summary = f'<div style="font-size: 0.75rem; color: #dc2626; margin-top: 12px;"><ul style="padding-left: 16px; margin: 0;">{failure_list}</ul></div>'

        agent_hash = hashlib.md5(abs_target.encode()).hexdigest()
        report_url = f"evidence_lake/{agent_hash}/report.html"
        report_link = f'<a href="{report_url}" style="font-size: 0.875rem; color: #3b82f6; text-decoration: none; display: block; margin-top: 16px; font-weight: 700;">View Full Audit &rarr;</a>'

        html += f"""
                <div class="agent-card">
                    <h3 style="margin: 0 0 8px 0; font-size: 1.125rem;">{os.path.basename(agent)}</h3>
                    <div class="{(status_class)}">{status}</div>
                    {failure_summary}
                    {fix_badge}
                    {report_link}
                    <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 16px; font-family: monospace; word-break: break-all;">{agent}</div>
                </div>
        """
        
    html += f"""
            </div>
            <div style="margin-top: 60px; border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center; color: #94a3b8; font-size: 0.875rem;">
                Generated by AgentOps Cockpit v1.4.0. Sovereign Intelligence Division.
            </div>
        </div>
        <script>
            const ctx = document.getElementById('radarChart').getContext('2d');
            new Chart(ctx, {{
                type: 'radar',
                data: {{
                    labels: {json.dumps(radar_labels)},
                    datasets: [{{
                        label: 'Fleet Maturity Avg',
                        data: {json.dumps(final_values)},
                        fill: true,
                        backgroundColor: 'rgba(59, 130, 246, 0.2)',
                        borderColor: 'rgb(59, 130, 246)',
                        pointBackgroundColor: 'rgb(59, 130, 246)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgb(59, 130, 246)'
                    }}]
                }},
                options: {{
                    elements: {{
                        line: {{
                            borderWidth: 3
                        }}
                    }},
                    scales: {{
                        r: {{
                            angleLines: {{
                                display: true
                            }},
                            suggestedMin: 0,
                            suggestedMax: 100
                        }}
                    }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    dashboard_path = os.path.join(os.getcwd(), '.cockpit', 'fleet_dashboard.html')
    output_dir = os.path.dirname(dashboard_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    with open(dashboard_path, "w") as f:
        f.write(html)
    console.print(f"📄 [bold blue]Premium Fleet Dashboard generated at {dashboard_path}[/bold blue]")
