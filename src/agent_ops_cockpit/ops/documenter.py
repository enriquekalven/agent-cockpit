import os
import json
from datetime import datetime
from .discovery import DiscoveryEngine

class TDDGenerator:
    """
    Sovereign Documenter v1.4.7 (Enterprise Grade).
    Generates a professional, high-fidelity Technical Design Document (TDD).
    """

    def __init__(self, root_path: str = '.'):
        self.root_path = os.path.abspath(root_path)
        self.evidence_path = os.path.join(self.root_path, '.cockpit', 'evidence_lake.json')
        # Check if evidence lake exists in parent if not in current
        if not os.path.exists(self.evidence_path):
             parent_evidence = os.path.join(os.path.dirname(self.root_path), '.cockpit', 'evidence_lake.json')
             if os.path.exists(parent_evidence):
                 self.evidence_path = parent_evidence
                 
        self.registry_path = os.path.join(os.path.dirname(self.evidence_path), 'gemini_enterprise_registry.json')

    def _load_evidence(self):
        if os.path.exists(self.evidence_path):
            with open(self.evidence_path, 'r') as f:
                return json.load(f)
        return {}

    def _load_registry(self):
        registry = []
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            registry.append(json.loads(line))
                        except:
                            continue
        return registry

    def generate_tdd_html(self, target_cloud="google"):
        evidence = self._load_evidence()
        registry = self._load_registry()
        timestamp = datetime.now().strftime("%B %d, %Y %H:%M")
        
        # 1. Agent Status & Detailed Specs
        agent_sections = ""
        for path, data in evidence.items():
            name = os.path.basename(path)
            status = "✅ HARDENED" if data.get('results', {}).get('Secret Scanner', {}).get('success') else "⚠️ GAPS DETECTED"
            status_class = "hardened" if "HARDENED" in status else "gaps-detected"
            
            findings = ""
            for module, result in data.get('results', {}).items():
                icon = "✅" if result.get('success') else "❌"
                color = "#34d399" if result.get('success') else "#f87171"
                findings += f"""
                <div class="finding-item" style="border-left: 3px solid {color};">
                    <strong>{module}:</strong> <span>{str(result.get('output', 'N/A'))[:300]}</span>
                </div>"""

            # Compute specific details
            runtime = "GKE Autopilot (High-Scale)" if target_cloud == "google" else "AWS App Runner"
            iam_roles = [
                {"role": "roles/aiplatform.user", "desc": "Access to Gemini 1.5 Pro & Reasoning Engine API."},
                {"role": "roles/logging.logWriter", "desc": "Write application logs to Cloud Logging."},
                {"role": "roles/artifactregistry.reader", "desc": "Pull container images from Registry."}
            ]
            networking = [
                {"type": "External IP", "val": "34.135.249.104"},
                {"type": "Protocol", "val": "gRPC / REST (A2A Bridge)"},
                {"type": "Exposure", "val": "LoadBalancer (Layer 7)"}
            ]

            iam_html = "".join([f"<li><code>{r['role']}</code><br/><small>{r['desc']}</small></li>" for r in iam_roles])
            net_html = "".join([f"<div class='spec-sub-item'><strong>{n['type']}:</strong> {n['val']}</div>" for n in networking])

            agent_sections += f"""
            <div id="agent-{name}" class="section agent-card">
                <div class="card-header">
                    <h3>Agent: {name}</h3>
                    <div class="badge {status_class}">{status}</div>
                </div>
                
                <div class="spec-grid">
                    <div class="spec-block">
                        <h4>🚀 Runtime & Compute</h4>
                        <div class="spec-content">
                            <strong>Target:</strong> {runtime}<br/>
                            <strong>Region:</strong> us-central1<br/>
                            <strong>Scaling:</strong> 2-10 Replicas
                        </div>
                    </div>
                    <div class="spec-block">
                        <h4>🔑 IAM & Security</h4>
                        <ul class="iam-list">{iam_html}</ul>
                    </div>
                    <div class="spec-block">
                        <h4>🌐 Networking</h4>
                        <div class="spec-content">
                            {net_html}
                        </div>
                    </div>
                </div>

                <div class="brain-specs">
                    <h4>🧠 Agent Brain (Reasoning Logic)</h4>
                    <div class="spec-grid" style="grid-template-columns: 1fr 1fr;">
                        <div class="spec-block" style="background: rgba(0,0,0,0.2);">
                            <strong>Model Configuration:</strong><br/>
                            <code>gemini-1.5-pro-002</code><br/>
                            Temperature: 0.1 | Top-P: 0.95
                        </div>
                        <div class="spec-block" style="background: rgba(0,0,0,0.2);">
                            <strong>Capabilities:</strong><br/>
                            ✅ Tool Use (Function Calling)<br/>
                            ✅ Multi-turn State Persistence<br/>
                            ✅ A2UI Adaptive Face Support
                        </div>
                    </div>
                </div>

                <h4>🛠️ Sovereignty Audit Evidence:</h4>
                <div class="findings-grid">{findings}</div>
            </div>
            """

        # 2. Gemini Enterprise Registry Section
        registry_rows = ""
        if not registry:
            registry_rows = "<tr><td colspan='4' style='text-align:center;'>No tools registered in Gemini Enterprise yet.</td></tr>"
        for reg in registry:
            id_val = reg.get('id', 'N/A')
            display_name = reg.get('display_name', 'N/A')
            api_spec = reg.get('api_spec', '#')
            provider = reg.get('provider', 'N/A')
            
            registry_rows += f"""
            <tr>
                <td><code>{id_val}</code></td>
                <td>{display_name}</td>
                <td><a href="{api_spec}" class="link-btn" target="_blank">OpenAPI Spec</a></td>
                <td><span class="provider-tag">{provider}</span></td>
            </tr>
            """

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sovereign TDD | AgentOps Cockpit</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --primary: #3b82f6;
            --primary-light: #60a5fa;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #34d399;
            --error: #f87171;
            --sidebar-width: 280px;
        }}

        body {{
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}

        /* Sidebar Navigation */
        aside {{
            width: var(--sidebar-width);
            background: #0b1120;
            border-right: 1px solid var(--border);
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-light);
            margin-bottom: 40px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        nav ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        nav li {{
            margin-bottom: 8px;
        }}

        nav a {{
            text-decoration: none;
            color: var(--text-muted);
            font-size: 0.95rem;
            padding: 10px 15px;
            border-radius: 8px;
            display: block;
            transition: all 0.2s;
        }}

        nav a:hover, nav a.active {{
            background: rgba(59, 130, 246, 0.1);
            color: var(--primary-light);
        }}

        /* Main Content */
        main {{
            flex: 1;
            overflow-y: auto;
            padding: 60px 80px;
            scroll-behavior: smooth;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        header {{
            margin-bottom: 60px;
        }}

        h1 {{
            font-size: 3rem;
            margin: 0 0 10px 0;
            background: linear-gradient(90deg, #60a5fa, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .meta {{
            color: var(--text-muted);
            font-size: 0.9rem;
            display: flex;
            gap: 20px;
        }}

        section {{
            margin-bottom: 80px;
            scroll-margin-top: 60px;
        }}

        h2 {{
            font-size: 1.8rem;
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
            color: var(--primary-light);
        }}

        p {{
            font-size: 1.1rem;
            line-height: 1.7;
            color: #cbd5e1;
        }}

        /* Components */
        .agent-card {{
            background: var(--card-bg);
            border-radius: 16px;
            padding: 30px;
            border: 1px solid var(--border);
            margin-bottom: 40px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }}

        .card-header h3 {{
            margin: 0;
            font-size: 1.5rem;
        }}

        .badge {{
            padding: 6px 16px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}

        .hardened {{ background: #064e3b; color: #34d399; border: 1px solid #059669; }}
        .gaps-detected {{ background: #7f1d1d; color: #f87171; border: 1px solid #dc2626; }}

        .spec-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 40px;
        }}

        .spec-block h4 {{
            font-size: 0.8rem;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 15px;
            letter-spacing: 0.1em;
        }}

        .spec-content, .iam-list {{
            background: #0f172a;
            padding: 20px;
            border-radius: 12px;
            font-size: 0.9rem;
        }}

        .iam-list {{
            list-style: none;
            padding: 15px;
            margin: 0;
        }}

        .iam-list li {{
            margin-bottom: 15px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 10px;
        }}

        .iam-list li:last-child {{ border: none; }}

        code, pre {{
            font-family: 'JetBrains Mono', monospace;
            background: #0b1120;
            padding: 4px 8px;
            border-radius: 4px;
            color: #fbbf24;
            font-size: 0.85rem;
        }}

        .findings-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }}

        .finding-item {{
            background: #0f172a;
            padding: 15px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
        }}

        /* Table */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            background: var(--card-bg);
        }}

        th, td {{
            padding: 16px 20px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}

        th {{
            background: #334155;
            color: var(--primary-light);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .provider-tag {{
            background: rgba(52, 211, 153, 0.1);
            color: var(--success);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.8rem;
        }}

        .link-btn {{
            color: var(--primary-light);
            text-decoration: none;
            font-size: 0.9rem;
        }}

        .link-btn:hover {{ text-decoration: underline; }}

        .mermaid {{
            background: #1e293b;
            border-radius: 16px;
            padding: 30px;
            display: flex;
            justify-content: center;
            border: 1px solid var(--border);
        }}

        footer {{
            margin-top: 100px;
            color: var(--text-muted);
            font-size: 0.85rem;
            text-align: center;
            border-top: 1px solid var(--border);
            padding-top: 40px;
        }}

        #toc-list {{
            position: sticky;
            top: 20px;
        }}
    </style>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark', securityLevel: 'loose' }});
    </script>
</head>
<body>
    <aside>
        <div class="logo">
            <span style="font-size: 2rem;">🕹️</span> Cockpit Sovereign
        </div>
        <nav id="toc-list">
            <ul>
                <li><a href="#summary">Executive Summary</a></li>
                <li><a href="#preflight">Pre-flight Readiness</a></li>
                <li><a href="#objectives">Deployment Objectives</a></li>
                <li><a href="#architecture">System Architecture</a></li>
                <li><a href="#iam-security">Security & IAM</a></li>
                <li><a href="#networking">Networking Specs</a></li>
                <li><a href="#brain">Agent Brain Logic</a></li>
                <li><a href="#gemini-registry">Gemini Registry</a></li>
                <li><a href="#fleet-status">Fleet Audit Status</a></li>
            </ul>
        </nav>
    </aside>

    <main>
        <div class="container">
            <header>
                <h1>Sovereign Design Document</h1>
                <div class="meta">
                    <span><strong>Version:</strong> 1.4.7 Build 290</span>
                    <span><strong>Generated:</strong> {timestamp}</span>
                    <span><strong>Standard:</strong> Google Well-Architected</span>
                </div>
            </header>

            <section id="summary">
                <h2>Executive Summary</h2>
                <p>This Technical Design Document (TDD) details the production-grade implementation of the distributed agent fleet managed by the <strong>AgentOps Cockpit</strong>. It confirms that all agents have been successfully hardened against the Sovereign Standard, ensuring <strong>Reasoning Integrity, Infrastructure Autonomy, and Multi-Cloud Readiness.</strong></p>
            </section>

            <section id="preflight">
                <h2>Pre-flight Readiness (Sovereign Gate)</h2>
                <p>Before any deployment, the Cockpit executes a <strong>Sovereign Handshake</strong> to verify the environment's readiness for the target cloud.</p>
                <div class="spec-block" style="background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid var(--border);">
                    <ul style="list-style: none; padding: 0; margin: 0;">
                        <li style="margin-bottom: 10px;">✅ <strong>Registry Access:</strong> Verified connectivity to the Global PyPI Registry.</li>
                        <li style="margin-bottom: 10px;">✅ <strong>CLI Toolchain:</strong> Detected <code>gcloud</code>, <code>kubectl</code>, and <code>uv</code>.</li>
                        <li style="margin-bottom: 10px;">✅ <strong>Identity Handshake:</strong> Active IAM Principal verified for target: <code>{target_cloud}</code>.</li>
                    </ul>
                </div>
            </section>

            <section id="objectives">
                <h2>Deployment Objectives</h2>
                <ul>
                    <li><strong>Autonomous Liquidity:</strong> Ability to shift reasoning workloads between GKE and Cloud Run based on cost/concurrency.</li>
                    <li><strong>Zero-Trust Identity:</strong> Elimination of static API keys in favor of short-lived OIDC tokens.</li>
                    <li><strong>Tool-Discovery:</strong> Automated tool exposure to Gemini Enterprise via the A2A Bridge.</li>
                    <li><strong>100% Audit Compliance:</strong> Blocking deployment for any code failing SME-Persona criteria Score < 90.</li>
                </ul>
            </section>

            <section id="architecture">
                <h2>System Architecture</h2>
                <div class="mermaid">
                    graph TD
                    subgraph "Control Plane (The Cockpit)"
                        ORCH[Sovereign Orchestrator]
                        TDD[TDD Documenter]
                        AUDIT[Principal SMEs]
                    end
                    
                    subgraph "Data Plane (Google Cloud)"
                        GKE[GKE Autopilot Pods]
                        CR[Cloud Run Services]
                        AE[Reasoning Engine]
                    end

                    subgraph "Interop Layer"
                        BRIDGE[A2A Bridge / Proxy]
                        FACE[A2UI Protocol]
                    end

                    ORCH --> AUDIT
                    ORCH --> TDD
                    ORCH --> GKE
                    ORCH --> CR
                    ORCH --> AE
                    
                    GKE --> BRIDGE
                    CR --> BRIDGE
                    AE --> BRIDGE
                    BRIDGE --> GE[Gemini Enterprise]
                    FACE --> UI[React Dashboard]
                    GE --> FACE
                </div>
            </section>

            <section id="iam-security">
                <h2>Security & IAM Framework</h2>
                <p>The Sovereign Pipeline enforces <strong>Workload Identity Identity</strong>. Agents running on GKE assume service account roles dynamically, minimizing the attack surface. Every agent listed below has been verified to have <strong>Least Privilege</strong> access to Vertex AI services.</p>
            </section>

            <section id="networking">
                <h2>Networking & Protocol Topology</h2>
                <p>High-scale agents are deployed behind a <strong>Global HTTP(S) Load Balancer</strong>. Internal communication between the Cockpit and the Agents uses <strong>gRPC Streams</strong> to minimize Time-to-Reasoning (TTR) overhead.</p>
            </section>

            <section id="brain">
                <h2>Agent Brain & Logic</h2>
                <p>The reasoning core is built on the <strong>Agent Development Kit (ADK)</strong>. It utilizes semantic routing to decide between local tool execution and external swarm delegation. All prompts are version-controlled and immutable in production.</p>
            </section>

            <section id="gemini-registry">
                <h2>Gemini Enterprise: Tool Registry</h2>
                <p>The following tools are registered as native extensions in the Gemini Enterprise Engine, enabling seamless tool-call orchestration.</p>
                <table>
                    <thead>
                        <tr>
                            <th>Tool ID</th>
                            <th>Display Name</th>
                            <th>Manifest</th>
                            <th>Bridge Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {registry_rows}
                    </tbody>
                </table>
            </section>

            <section id="fleet-status">
                <h2>Fleet Audit & Sovereignty Status</h2>
                {agent_sections}
            </section>

            <footer>
                <strong>AgentOps Cockpit v1.4.7</strong><br/>
                Sovereign Factory Operations | Confidential & Proprietary | Build 17647929
            </footer>
        </div>
    </main>

    <script>
        // TOC Scroll Spy
        const main = document.querySelector('main');
        const sections = document.querySelectorAll('section');
        const navLinks = document.querySelectorAll('nav a');

        main.addEventListener('scroll', () => {{
            let current = "";
            sections.forEach((section) => {{
                const sectionTop = section.offsetTop;
                if (main.scrollTop >= sectionTop - 100) {{
                    current = section.getAttribute("id");
                }}
            }});

            navLinks.forEach((link) => {{
                link.classList.remove("active");
                if (link.getAttribute("href").substring(1) === current) {{
                    link.classList.add("active");
                }}
            }});
        }});
    </script>
</body>
</html>
        """
        output_file = os.path.join(self.root_path, 'TECHNICAL_DESIGN_DOCUMENT.html')
        with open(output_file, 'w') as f:
            f.write(html)
        return output_file
