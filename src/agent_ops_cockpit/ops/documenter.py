import json
import os
from datetime import datetime


class TDDGenerator:
    """
    Cockpit Documenter v2.0.7 (Enterprise Grade).
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
                data = json.load(f)
                if isinstance(data, list):
                    evidence = {}
                    for item in data:
                        if isinstance(item, dict):
                            # The evidence lake can contain both agent data and metadata
                            # Agent data follows the pattern: { "/abs/path": { ... } }
                            for k, v in item.items():
                                if isinstance(v, dict) and ('results' in v or 'target_path' in v):
                                    evidence[k] = v
                    return evidence
                return data
        return {}

    def _load_registry(self):
        registry = []
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            registry.append(json.loads(line))
                        except Exception:
                            continue
        return registry

    def generate_tdd_html(self, target_cloud="google"):
        evidence = self._load_evidence()
        registry = self._load_registry()
        timestamp = datetime.now().strftime("%B %d, %Y %H:%M")
        
        # Gathering dynamic metadata
        github_url = "https://github.com/enriquekalven/agent-ops-cockpit"
        pypi_url = "https://pypi.org/project/agentops-cockpit/"
        firebase_url = "https://agent-cockpit.web.app"
        
        # 1. Agent Status & Detailed Specs
        agent_sections = ""
        for path, data in evidence.items():
            name = os.path.basename(path)
            health = data.get('summary', {}).get('health', 1.0) * 100
            status_text = "PASSED" if health >= 90 else "GAPS DETECTED"
            status_class = "status-pass" if health >= 90 else "status-fail"
            
            findings = ""
            for module, result in data.get('results', {}).items():
                status_icon = "●" if result.get('success') else "■"
                status_color = "#10b981" if result.get('success') else "#ef4444"
                
                findings += f"""
                <div class="finding-row">
                    <div class="finding-status" style="color: {status_color};">{status_icon}</div>
                    <div class="finding-module">{module}</div>
                    <div class="finding-detail">{str(result.get('output', 'N/A'))[:200]}...</div>
                </div>"""

            runtime = "Cockpit Cockpit Runtime (Enterprise Mesh)"
            iam_roles = [
                {"role": "cockpit.agent.executor", "desc": "Access to local reasoning engine and cockpit tools."},
                {"role": "cockpit.telemetry.writer", "desc": "Write application logs to Cockpit Evidence Lake."},
                {"role": "cockpit.registry.reader", "desc": "Pull container images from local cockpit registry."}
            ]
            networking = [
                {"type": "Internal IP", "val": "10.0.0.1"},
                {"type": "Protocol", "val": "gRPC / REST (Cockpit Bridge)"},
                {"type": "Exposure", "val": "Cockpit Mesh (Layer 7 mTLS)"}
            ]

            iam_list_html = "".join([f"<li><strong>{r['role']}</strong><br/><small>{r['desc']}</small></li>" for r in iam_roles])
            net_html = "".join([f"<div class='spec-item'><span>{n['type']}</span><strong>{n['val']}</strong></div>" for n in networking])

            agent_sections += f"""
            <div id="agent-{name}" class="agent-card">
                <div class="card-header">
                    <div class="card-title-group">
                        <h3>Agent: {name}</h3>
                        <div class="health-meta">Cockpit Score: {health:.1f}%</div>
                    </div>
                    <div class="badge {status_class}">{status_text}</div>
                </div>
                
                <div class="spec-grid">
                    <div class="spec-column">
                        <div class="spec-header">🚀 RUNTIME & COMPUTE</div>
                        <div class="spec-content">
                            <div class="spec-item"><span>Target</span><strong>{runtime}</strong></div>
                            <div class="spec-item"><span>Environment</span><strong>Production (Cockpit)</strong></div>
                            <div class="spec-item"><span>Scaling</span><strong>Elastic Auto-Scale</strong></div>
                        </div>
                    </div>
                    <div class="spec-column">
                        <div class="spec-header">🔑 IDENTITY & ACCESS</div>
                        <ul class="iam-list">{iam_list_html}</ul>
                    </div>
                    <div class="spec-column">
                        <div class="spec-header">🌐 NETWORK TOPOLOGY</div>
                        <div class="spec-content">{net_html}</div>
                    </div>
                </div>

                <div class="audit-section">
                    <div class="spec-header">🛡️ COCKPIT AUDIT FINDINGS</div>
                    <div class="findings-list">{findings}</div>
                </div>
            </div>
            """

        # 2. Tools Registry
        registry_rows = ""
        if not registry:
            registry_rows = "<tr><td colspan='4' style='text-align:center; padding: 40px;'>No tools registered in Gemini Enterprise registry yet.</td></tr>"
        for reg in registry:
            registry_rows += f"""
            <tr>
                <td><code>{reg.get('id', 'N/A')}</code></td>
                <td>{reg.get('display_name', 'N/A')}</td>
                <td><a href="{reg.get('api_spec', '#')}" class="text-link">OpenAPI Spec ↗</a></td>
                <td><span class="pill">{reg.get('provider', 'N/A')}</span></td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cockpit TDD | AgentOps Cockpit</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --emerald: #10b981; --emerald-dark: #059669; --emerald-light: #ecfdf5;
            --slate: #0f172a; --slate-light: #1e293b; --slate-lighter: #334155;
            --text-main: #f8fafc; --text-muted: #94a3b8; --text-dark: #cbd5e1;
            --border: #334155; --error: #ef4444; --warning: #f59e0b;
        }}
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Outfit', sans-serif; background: var(--slate); color: var(--text-main); margin: 0; display: flex; height: 100vh; overflow: hidden; }}
        
        /* Sidebar */
        aside {{ width: 300px; background: #0b1120; border-right: 1px solid var(--border); display: flex; flex-direction: column; }}
        .sidebar-brand {{ padding: 32px 24px; border-bottom: 1px solid var(--border); }}
        .brand-title {{ font-size: 22px; font-weight: 700; color: var(--emerald); display: flex; align-items: center; gap: 10px; letter-spacing: -0.02em; }}
        .nav-list {{ padding: 24px 16px; flex: 1; overflow-y: auto; }}
        .nav-item {{ display: block; padding: 12px 16px; color: var(--text-muted); text-decoration: none; font-weight: 500; font-size: 15px; border-radius: 8px; margin-bottom: 4px; transition: all 0.2s; }}
        .nav-item:hover, .nav-item.active {{ background: rgba(16, 185, 129, 0.1); color: var(--emerald); }}
        
        /* Main */
        main {{ flex: 1; overflow-y: auto; scroll-behavior: smooth; background: #0f172a; }}
        .content-container {{ max-width: 1100px; margin: 0 auto; padding: 60px 80px; }}
        
        header {{ margin-bottom: 80px; }}
        .doc-meta {{ display: flex; gap: 24px; font-size: 13px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 16px; }}
        h1 {{ font-size: 48px; font-weight: 700; margin: 0; background: linear-gradient(135deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.01em; }}
        .subtitle {{ font-size: 18px; color: var(--text-dark); margin-top: 12px; font-weight: 400; }}

        .external-links {{ display: flex; gap: 16px; margin-top: 32px; }}
        .btn-link {{ background: var(--slate-light); color: var(--text-main); text-decoration: none; padding: 10px 20px; border-radius: 12px; border: 1px solid var(--border); font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }}
        .btn-link:hover {{ border-color: var(--emerald); background: rgba(16, 185, 129, 0.05); }}

        section {{ margin-bottom: 100px; scroll-margin-top: 40px; }}
        h2 {{ font-size: 24px; font-weight: 700; color: var(--emerald); margin-bottom: 32px; display: flex; align-items: center; gap: 12px; }}
        
        /* Rationale Grid */
        .rationale-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
        .rationale-card {{ background: var(--slate-light); border: 1px solid var(--border); padding: 24px; border-radius: 20px; }}
        .rationale-card h4 {{ margin: 0 0 12px 0; font-size: 16px; color: var(--text-main); display: flex; align-items: center; gap: 8px; }}
        .rationale-card p {{ margin: 0; font-size: 14px; color: var(--text-muted); line-height: 1.6; }}

        /* Agent Card */
        .agent-card {{ background: var(--slate-light); border: 1px solid var(--border); border-radius: 24px; padding: 32px; margin-bottom: 40px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }}
        .card-title-group h3 {{ margin: 0; font-size: 22px; font-weight: 700; }}
        .health-meta {{ font-size: 13px; color: var(--emerald); font-weight: 600; margin-top: 4px; }}
        .badge {{ padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }}
        .status-pass {{ background: rgba(16, 185, 129, 0.1); color: var(--emerald); border: 1px solid var(--emerald); }}
        .status-fail {{ background: rgba(239, 68, 68, 0.1); color: var(--error); border: 1px solid var(--error); }}

        .spec-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 40px; }}
        .spec-header {{ font-size: 11px; font-weight: 700; color: var(--text-muted); letter-spacing: 0.1em; margin-bottom: 16px; }}
        .spec-content {{ background: #0b1120; padding: 20px; border-radius: 16px; border: 1px solid var(--border); }}
        .spec-item {{ display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px; font-size: 13px; }}
        .spec-item:last-child {{ margin-bottom: 0; }}
        .spec-item span {{ color: var(--text-muted); }}
        .spec-item strong {{ color: var(--text-main); }}

        .iam-list {{ background: #0b1120; list-style: none; padding: 20px; margin: 0; border-radius: 16px; border: 1px solid var(--border); }}
        .iam-list li {{ margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--slate-lighter); }}
        .iam-list li:last-child {{ border: none; padding-bottom: 0; margin-bottom: 0; }}
        .iam-list li strong {{ font-size: 12px; font-family: 'JetBrains Mono', monospace; color: var(--emerald); }}
        .iam-list li small {{ color: var(--text-muted); font-size: 11px; display: block; margin-top: 4px; }}

        .audit-section {{ border-top: 1px solid var(--border); padding-top: 32px; }}
        .findings-list {{ display: flex; flex-direction: column; gap: 8px; }}
        .finding-row {{ background: #0b1120; padding: 12px 20px; border-radius: 12px; display: flex; gap: 16px; align-items: center; border: 1px solid transparent; transition: all 0.2s; }}
        .finding-row:hover {{ border-color: var(--border); background: var(--slate-light); }}
        .finding-status {{ font-size: 10px; }}
        .finding-module {{ font-weight: 700; font-size: 13px; font-family: 'JetBrains Mono', monospace; width: 180px; color: var(--text-dark); }}
        .finding-detail {{ font-size: 13px; color: var(--text-muted); flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

        /* Table */
        .table-container {{ background: var(--slate-light); border-radius: 20px; border: 1px solid var(--border); overflow: hidden; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{ background: #0b1120; padding: 16px 24px; font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }}
        td {{ padding: 16px 24px; border-bottom: 1px solid var(--border); font-size: 14px; color: var(--text-dark); }}
        tr:last-child td {{ border-bottom: none; }}
        code {{ font-family: 'JetBrains Mono', monospace; color: var(--emerald); background: rgba(16, 185, 129, 0.05); padding: 4px 8px; border-radius: 4px; font-size: 13px; }}
        .pill {{ background: rgba(16, 185, 129, 0.1); color: var(--emerald); padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; }}
        .text-link {{ color: var(--emerald); text-decoration: none; font-weight: 600; font-size: 13px; }}

        .mermaid-card {{ background: var(--slate-light); padding: 40px; border-radius: 24px; border: 1px solid var(--border); display: flex; justify-content: center; }}

        footer {{ margin-top: 120px; padding: 60px 0; border-top: 1px solid var(--border); text-align: center; color: var(--text-muted); font-size: 13px; line-height: 2; }}

        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: var(--slate-lighter); border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--text-muted); }}

        @media print {{ aside {{ display: none; }} main {{ background: white; color: black; }} .content-container {{ padding: 40px; }} .btn-link {{ display: none; }} }}
    </style>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark', securityLevel: 'loose' }});
    </script>
</head>
<body>
    <aside>
        <div class="sidebar-brand"><div class="brand-title">🕹️ Cockpit Cockpit</div></div>
        <div class="nav-list">
            <a href="#summary" class="nav-item active">Executive Summary</a>
            <a href="#rationale" class="nav-item">Technology Rationale</a>
            <a href="#architecture" class="nav-item">System Architecture</a>
            <a href="#connections" class="nav-item">Platform Connections</a>
            <a href="#registry" class="nav-item">Tool Registry</a>
            <a href="#fleet" class="nav-item">Fleet Audit Status</a>
        </div>
        <div style="padding: 24px; font-size: 11px; color: var(--text-muted); border-top: 1px solid var(--border);">
            Build: v2.0.7-premium<br>
            Standard: A2A Cockpit Factory
        </div>
    </aside>

    <main>
        <div class="content-container">
            <header>
                <div class="doc-meta">
                    <span>Artifact ID: TDD-AO-2026-001</span>
                    <span>Status: Highly Hardened</span>
                </div>
                <h1>Technical Design Document</h1>
                <div class="subtitle">Architectural Blueprint for Cockpit Agent Operations.</div>
                
                <div class="external-links">
                    <a href="{github_url}" class="btn-link" target="_blank">View on GitHub</a>
                    <a href="{pypi_url}" class="btn-link" target="_blank">PyPI Registry</a>
                    <a href="{firebase_url}" class="btn-link" target="_blank">Live Face Dashboard</a>
                </div>
            </header>

            <section id="summary">
                <h2><span style="color:var(--text-muted); font-weight:400;">01.</span> Executive Summary</h2>
                <p>This design document details the multi-cloud, cockpit implementation of <strong>AgentOps Cockpit</strong>. Our architecture is designed to bridge the gap between "scripts" and "systems" by providing framework-agnostic governance for distributed AI fleets. The core objective is <strong>Autonomous Cockpitty</strong>—ensuring that your agents operate with hardened reasoning logic, secure tool schemas, and high-fidelity operational transparency.</p>
            </section>

            <section id="rationale">
                <h2><span style="color:var(--text-muted); font-weight:400;">02.</span> Technology Rationale</h2>
                <div class="rationale-grid">
                    <div class="rationale-card">
                        <h4>⚙️ The Agentic Trinity</h4>
                        <p>Decouples Reasoning (Engine), Interface (Face), and Operations (Cockpit). This ensures that architectural debt in one pillar does not compromise the security or performance of the others.</p>
                    </div>
                    <div class="rationale-card">
                        <h4>🧠 Cockpit Reasoning (ADK)</h4>
                        <p>Leveraging the Google ADK for robust function calling and multi-turn state persistence. We chose ADK for its "Shared State" and "Delegation" patterns which provide superior orchestration over vanilla RAG.</p>
                    </div>
                    <div class="rationale-card">
                        <h4>🛡️ Poka-Yoke Hardening</h4>
                        <p>Automated tool-schema reconciliation using AST-aware auditing. This "error-proofing" ensures that LLMs never attempt to call non-existent or dangerous tool variants.</p>
                    </div>
                    <div class="rationale-card">
                        <h4>🌉 The Cockpit Bridge</h4>
                        <p>A multi-cloud deployment engine (GCP / AWS / Azure). We chose this to prevent infrastructure lock-in, allowing reasoning workloads to shift based on latency and token-economics.</p>
                    </div>
                </div>
            </section>

            <section id="architecture">
                <h2><span style="color:var(--text-muted); font-weight:400;">03.</span> System Architecture</h2>
                <div class="mermaid-card">
                    <div class="mermaid">
                        graph TD
                        subgraph "Governance Plane (The Cockpit)"
                            ORCH[Cockpit Orchestrator]
                            AUDIT[SME Auditor Board]
                            HIVE[Semantic Hive Mind]
                        end
                        
                        subgraph "Execution Plane (Cockpit Infrastructure)"
                            MESH[Elastic Service Mesh]
                            RUNTIME[Cockpit Runtime Nodes]
                            EDGE[Cockpit Edge Gateway]
                        end

                        subgraph "Platform Integration"
                            GE[Gemini Enterprise]
                            FB[Firebase Face Layer]
                            AE[Reasoning Engine]
                        end

                        ORCH --> AUDIT
                        ORCH --> HIVE
                        AUDIT --> EDGE
                        EDGE --> RUNTIME
                        RUNTIME --> MESH
                        MESH --> GE
                        GE --> AE
                        FB --> ORCH
                        AE --> FB
                    </div>
                </div>
            </section>

            <section id="connections">
                <h2><span style="color:var(--text-muted); font-weight:400;">04.</span> Platform Connections</h2>
                <p>AgentOps Cockpit is a distributed system with deep integrations into enterprise cloud providers. Below are the verified production end-points for the current fleet.</p>
                <div class="table-container">
                    <table>
                        <thead><tr><th>Platform</th><th>Target Service</th><th>Connection Strategy</th></tr></thead>
                        <tbody>
                            <tr><td><strong>Google Cloud</strong></td><td>Vertex AI / GKE</td><td>Workload Identity / OIDC</td></tr>
                            <tr><td><strong>Firebase</strong></td><td>Hosting / Functions</td><td>Cockpit Face Deployment</td></tr>
                            <tr><td><strong>GitHub</strong></td><td>Source Registry</td><td>SSH Agent / CI-CD Bridge</td></tr>
                            <tr><td><strong>PyPI</strong></td><td>Package Registry</td><td>Trusted Publisher (OpenID)</td></tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section id="registry">
                <h2><span style="color:var(--text-muted); font-weight:400;">05.</span> Gemini Enterprise Tool Registry</h2>
                <div class="table-container">
                    <table>
                        <thead><tr><th>Tool ID</th><th>Display Name</th><th>Manifest</th><th>Status</th></tr></thead>
                        <tbody>{registry_rows}</tbody>
                    </table>
                </div>
            </section>

            <section id="fleet">
                <h2><span style="color:var(--text-muted); font-weight:400;">06.</span> Fleet Audit Status</h2>
                {agent_sections}
            </section>

            <footer>
                <strong>AgentOps Cockpit v2.0.7 Premium Insights</strong><br/>
                Confidential Architectural Artifact. Cockpit Systems Division.<br>
                Generated: {timestamp} | Standard: AIA Cockpit Design v1.4
            </footer>
        </div>
    </main>

    <script>
        const main = document.querySelector('main');
        const sections = document.querySelectorAll('section');
        const navLinks = document.querySelectorAll('.nav-item');

        main.addEventListener('scroll', () => {{
            let current = "";
            sections.forEach((section) => {{
                if (main.scrollTop >= section.offsetTop - 100) {{ current = section.getAttribute("id"); }}
            }});
            navLinks.forEach((link) => {{
                link.classList.remove("active");
                if (link.getAttribute("href").substring(1) === current) {{ link.classList.add("active"); }}
            }});
        }});
    </script>
</body>
</html>"""
        output_file = os.path.join(self.root_path, 'TECHNICAL_DESIGN_DOCUMENT.html')
        with open(output_file, 'w') as f:
            f.write(html)
        return output_file

    def generate_tdd_markdown(self):
        """
        Generates a high-fidelity Markdown version of the TDD.
        Optimized for AI consumption and version control.
        """
        evidence = self._load_evidence()
        timestamp = datetime.now().strftime("%B %d, %Y %H:%M")
        
        md = [
            "# 🏛️ Cockpit Technical Design Document (TDD)",
            f"**Generated**: {timestamp}",
            "**Standard**: Google Well-Architected for Agents (v2.0.7)",
            "**GitHub**: [enriquekalven/agent-ops-cockpit](https://github.com/enriquekalven/agent-ops-cockpit)",
            "**PyPI**: [agentops-cockpit](https://pypi.org/project/agentops-cockpit/)",
            "**Face**: [agent-cockpit.web.app](https://agent-cockpit.web.app)",
            "\n---",
            "\n## 1. Executive Summary",
            "This document details the production-grade implementation of the distributed agent fleet. It confirms hardening against the Cockpit Standard.",
            "\n## 2. Technology Rationale",
            "### ⚙️ The Agentic Trinity",
            "Decouples Reasoning (Engine), Interface (Face), and Operations (Cockpit).",
            "### 🧠 Cockpit Reasoning (ADK)",
            "Leveraging Google ADK for robust function calling and multi-turn state persistence.",
            "### 🛡️ Poka-Yoke Hardening",
            "Automated tool-schema reconciliation using AST-aware auditing.",
            "\n## 3. System Architecture",
            "The system follows the **Agentic Trinity** framework: Engine (Reasoning), Face (UX), and Cockpit (Operations).",
            "\n## 4. Fleet Audit Evidence",
        ]

        for path, data in evidence.items():
            name = os.path.basename(path)
            health = data.get('summary', {}).get('health', 0) * 100
            status = "✅ HARDENED" if health >= 90 else "⚠️ GAPS DETECTED"
            
            md.append(f"\n### Agent: {name}")
            md.append(f"- **Cockpit Score**: {health:.1f}%")
            md.append(f"- **Status**: {status}")
            md.append("\n#### 🛠️ SME Findings:")
            
            for module, result in data.get('results', {}).items():
                icon = "✅" if result.get('success') else "❌"
                md.append(f"- {icon} **{module}**: {str(result.get('output', 'N/A'))[:200]}...")

        md.append("\n---")
        md.append("\n*Generated by the AgentOps Cockpit Documenter v2.0.7.*")
        
        output_file = os.path.join(self.root_path, 'TECHNICAL_DESIGN_DOCUMENT.md')
        with open(output_file, 'w') as f:
            f.write("\n".join(md))
        return output_file

    def generate_codebase_bundle(self):
        """
        [Gittodoc Style] - Consolidates the entire codebase into a single AI-indexable file.
        Useful for long-context LLMs and rapid onboarding.
        """
        from agent_ops_cockpit.ops.discovery import DiscoveryEngine
        discovery = DiscoveryEngine(self.root_path)
        
        bundle = [
            "# 🛰️ COCKPIT CODEBASE BUNDLE",
            f"**Generated**: {datetime.now().isoformat()}",
            "**Purpose**: High-fidelity AI context for Cockpit Fleet Operations.",
            "\n---\n"
        ]
        
        # Add File Tree
        bundle.append("## 📂 Repository Structure\n```text")
        # Simplified tree
        for root, dirs, files in os.walk(self.root_path):
            # Ignore hidden dirs and some common weights/venv
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'dist', 'build', '__pycache__']]
            level = root.replace(self.root_path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            bundle.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if not f.startswith('.'):
                    bundle.append(f"{subindent}{f}")
        bundle.append("```\n\n---\n")

        # Consolidate Files (Gittodoc Pattern)
        bundle.append("## 📄 Source Code Consolidation\n")
        
        for file_path in discovery.walk(self.root_path):
            # Filter for meaningful source files
            if not file_path.endswith(('.py', '.ts', '.js', '.yaml', '.prompt', '.md', 'toml', 'Makefile')):
                continue
            if 'node_modules' in file_path or 'dist' in file_path or '.cockpit' in file_path:
                continue
                
            rel_path = os.path.relpath(file_path, self.root_path)
            bundle.append(f"\n### FILE: `{rel_path}`")
            bundle.append("---")
            
            ext = rel_path.split('.')[-1]
            lang = 'python' if ext == 'py' else 'typescript' if ext == 'ts' else ext
            
            bundle.append(f"```{lang}")
            try:
                with open(file_path, 'r') as f:
                    bundle.append(f.read())
            except Exception as e:
                bundle.append(f"Error reading file: {e}")
            bundle.append("```\n")

        output_file = os.path.join(self.root_path, 'CODEBASE_BUNDLE.md')
        with open(output_file, 'w') as f:
            f.write("\n".join(bundle))
        return output_file
