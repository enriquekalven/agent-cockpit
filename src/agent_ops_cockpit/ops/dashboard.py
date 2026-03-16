try:
    from google.adk.agents.context_cache_config import ContextCacheConfig
except (ImportError, AttributeError, ModuleNotFoundError):
    ContextCacheConfig = None

import hashlib
import os

from rich.console import Console
from tenacity import retry, stop_after_attempt, wait_exponential

console = Console()

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def generate_fleet_dashboard(results: dict):
    """Generates a Google Cloud grade fleet dashboard."""
    total = len(results) or 1
    passed_count = sum((1 for r in results.values() if r == 0))
    compliance_score = (passed_count / total * 100)
    
    suspicious_agents = total - passed_count
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AgentOps Cockpit | Fleet Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            :root {{
                --cockpit-emerald: #10b981; --cockpit-slate: #334155; --cockpit-red: #ef4444;
                --bg-color: #f8fafc; --sidebar-color: #ffffff; --text-primary: #1e293b;
                --text-secondary: #64748b; --border-color: #e2e8f0;
            }}
            body {{ font-family: 'Inter', sans-serif; background-color: var(--bg-color); color: var(--text-primary); margin: 0; display: flex; height: 100vh; overflow: hidden; }}
            #sidebar {{ width: 256px; background-color: var(--sidebar-color); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; }}
            #main-content {{ flex-grow: 1; display: flex; flex-direction: column; overflow: hidden; }}
            header {{ background-color: #ffffff; height: 48px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; padding: 0 16px; justify-content: space-between; }}
            .sub-header {{ background: #ffffff; padding: 12px 24px; border-bottom: 1px solid var(--border-color); }}
            .metrics-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding: 24px; }}
            .metric-card {{ background: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
            .content-area {{ padding: 24px; overflow-y: auto; flex-grow: 1; }}
            .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
            .agent-card {{ background: #ffffff; padding: 16px; border-radius: 8px; border: 1px solid var(--border-color); transition: transform 0.2s; }}
            .agent-card:hover {{ transform: translateY(-2px); border-color: var(--cockpit-emerald); }}
            .status-badge {{ padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; }}
            .status-pass {{ background: #ecfdf5; color: #059669; }}
            .status-fail {{ background: #fef2f2; color: #dc2626; }}
            .btn-emerald {{ background: var(--cockpit-emerald); color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; transition: opacity 0.2s; }}
            .btn-emerald:hover {{ opacity: 0.9; }}
        </style>
    </head>
    <body>
        <div id="sidebar">
            <div style="padding:16px; font-weight:700; font-size:18px; color:var(--cockpit-emerald); border-bottom:1px solid var(--border-color); display:flex; align-items:center; gap:8px;">
                🕹️ Cockpit
            </div>
            <div style="padding:8px 0;">
                <div style="padding:8px 24px; font-size:14px; background:#f0fdf4; color:var(--cockpit-emerald); font-weight:600; border-right:3px solid var(--cockpit-emerald);">Fleet Dashboard</div>
                <div style="padding:8px 24px; font-size:14px; color:var(--text-secondary); cursor:pointer;">Audit Sessions</div>
                <div style="padding:8px 24px; font-size:14px; color:var(--text-secondary); cursor:pointer;">Remediation Lake</div>
            </div>
        </div>
        <div id="main-content">
            <header>
                <div style="font-size:13px; background:var(--bg-color); color:var(--text-secondary); padding:4px 12px; border-radius:6px; font-weight:500; border:1px solid var(--border-color);">🚀 COCKPIT_FLEET_01</div>
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:28px; height:28px; background:var(--cockpit-emerald); border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:12px; font-weight:700;">A</div>
                </div>
            </header>
            <div class="sub-header">
                <div style="font-size:12px; color:var(--cockpit-emerald); font-weight:600; letter-spacing:0.05em; text-transform:uppercase;">Agent Management</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h1 style="margin:0; font-size:24px; font-weight:600; color:var(--cockpit-slate);">Mission Control</h1>
                    <button class="btn-emerald" onclick="location.reload()">SYNC FLEET</button>
                </div>
            </div>
            <div class="metrics-row">
                <div class="metric-card">
                    <div style="font-size:13px; color:var(--text-secondary); font-weight:500; margin-bottom:8px;">Compliance Score</div>
                    <div style="font-size:32px; font-weight:700; color:var(--cockpit-slate);">{compliance_score:.1f}%</div>
                </div>
                <div class="metric-card">
                    <div style="font-size:13px; color:var(--text-secondary); font-weight:500; margin-bottom:8px;">Anomalous Agents</div>
                    <div style="font-size:32px; font-weight:700; color:var(--cockpit-red);">{suspicious_agents}</div>
                </div>
                <div class="metric-card">
                    <div style="font-size:13px; color:var(--text-secondary); font-weight:500; margin-bottom:8px;">Cockpit Health</div>
                    <div style="font-size:32px; font-weight:700; color:var(--cockpit-emerald);">OPTIMAL</div>
                </div>
            </div>
            <div class="content-area">
                <h2 style="font-size:16px; font-weight:600; margin-bottom:16px; color:var(--cockpit-slate);">Agent Fleet Inventory</h2>
                <div class="agent-grid">
    """
    
    for agent, success in results.items():
        name = os.path.basename(agent)
        status_text = "Healthy" if success == 0 else "Anomalous"
        status_class = "status-pass" if success == 0 else "status-fail"
        agent_hash = hashlib.md5(os.path.abspath(agent).encode()).hexdigest()
        report_url = f"evidence_lake/{agent_hash}/report.html"
        
        html += f"""
                    <div class="agent-card">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div style="font-weight:600; font-size:15px; color:var(--cockpit-slate);">{name}</div>
                            <span class="status-badge {status_class}">{status_text}</span>
                        </div>
                        <div style="font-size:12px; color:var(--text-secondary); margin-top:4px; font-family:monospace; background:#f1f5f9; padding:2px 4px; border-radius:2px;">{agent}</div>
                        <div style="margin-top:20px;">
                            <a href="{report_url}" style="color:var(--cockpit-emerald); text-decoration:none; font-size:13px; font-weight:600;">ACCESS AUDIT →</a>
                        </div>
                    </div>
        """
        
    html += """
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    dashboard_path = os.path.join(os.getcwd(), '.cockpit', 'fleet_dashboard.html')
    output_dir = os.path.dirname(dashboard_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    with open(dashboard_path, 'w') as f:
        f.write(html)
    console.print(f'📄 [bold blue]Premium Fleet Dashboard generated at {dashboard_path}[/bold blue]')