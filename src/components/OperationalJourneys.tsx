import React, { useState } from 'react';
import {
  Terminal, Code, Shield, Settings,
  ChevronRight, Layout, Cpu, Activity,
  Zap, Command, ExternalLink, FileText,
  CheckCircle, Briefcase
} from 'lucide-react';
import { Link } from 'react-router-dom';

const JOURNEYS = [
  {
    id: 'developer',
    name: 'The Builder',
    persona: 'Developer / Engineer',
    icon: <Code size={24} />,
    color: '#3b82f6',
    description: 'Rapidly scaffold and debug production agents across any stack with professional-grade SDKs.',
    docs: [
      { name: 'Getting Started', path: '/docs/getting-started' },
      { name: 'UX & A2UI Guide', path: '/docs/ux-guide' },
      { name: 'Local Mocking / CLI', path: '/docs/commands-master' }
    ],
    reports: [
      { name: 'A2UI Contract Audit', path: '/master-audit-report.html' },
      { name: 'Unit Test Evidence', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit create trinity',
    diagram: '/assets/persona_builder_new.png',
    output: `🚀 Creating new agent: my-agent
📦 Initializing with Trinity Stack (FastAPI + React + ADK)
✅ Framework detected: Python 3.12, Node 20
✅ Multi-stack Support: TypeScript, Go, Java
✨ Agent logic scaffolded in /src/backend/agent.py
Ready to roll. Run 'make dev' to start.`
  },
  {
    id: 'architect',
    name: 'The Strategist',
    persona: 'Solution Architect',
    icon: <Layout size={24} />,
    color: '#10b981',
    description: 'Design resilient, multi-cloud agentic systems aligned with v1.6 Wisdom Store patterns.',
    docs: [
      { name: 'Google Architecture', path: '/docs/google-architecture' },
      { name: 'Deployment Strategy', path: '/docs/deployment' },
      { name: 'Maturity Wisdom Store', path: '/docs/arch-review' }
    ],
    reports: [
      { name: 'Architecture Review (ADR)', path: '/arch-review-report.html' },
      { name: 'Multi-Cloud Maturity Score', path: '/master-audit-report.html' }
    ],
    command: 'agentops-cockpit audit arch',
    diagram: '/assets/persona_strategist_new.png',
    output: `🏗️ Starting Architecture Review v1.6.7...
🔍 Scanning /src for Maturity Wisdom drift
✅ AWS Patterns: Bedrock Action Groups detected (Well-Architected)
✅ GCP Patterns: Vertex AI Context Caching enabled (+90% savings)
⚠️ Azure Patterns: Missing Managed Identity for Tool ingestion
📜 Generating ADR: Wisdom Store alignment at 92%`
  },
  {
    id: 'quality',
    name: 'The Optimizer',
    persona: 'Quality Lead',
    icon: <Activity size={24} />,
    color: '#06b6d4',
    description: 'v1.6: RAG Fidelity Auditing, Hill Climbing, and reasoning-based optimization.',
    docs: [
      { name: 'Quality & Eval Guide', path: '/docs/quality-guide' },
      { name: 'RAG Truth-Sayer SME', path: '/docs/quality-guide' }
    ],
    reports: [
      { name: 'Quality Scorecard', path: '/quality-audit-report.html' },
      { name: 'RAG Fidelity Trace', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit rag audit',
    diagram: '/assets/persona_optimizer.png',
    output: `🧗 RAG TRUTH-SAYER: FIDELITY AUDIT
🔍 Detecting Retrieval-Reasoning Drift...
✅ Grounding Logic: Verifiable citations found in prompt.
⚠️ Temperature Risk: Detected 0.7 in RAG path (Suggested <= 0.2)
✅ Stability: Tool trajectory matches golden dataset.
✨ Quality baseline: High (No hallucinations detected)`
  },
  {
    id: 'security',
    name: 'The Guardian',
    persona: 'Security Specialist',
    icon: <Shield size={24} />,
    color: '#ef4444',
    description: 'v1.6: Brand Safety Playbook hardening against advanced adversarial attacks.',
    docs: [
      { name: 'Brand Safety Playbook', path: '/docs/redteam-guide' },
      { name: 'Red Team Audits', path: '/docs/redteam-guide' }
    ],
    reports: [
      { name: 'Brand Safety scorecard', path: '/red-team-report.html' },
      { name: 'Vulnerability Regression', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit audit security',
    diagram: '/assets/persona_guardian.png',
    output: `🛡️ RED TEAM: BRAND SAFETY AUDIT v2.0
🕵️ Testing Payload Splitting: [Attempt 1/10] -> BLOCKED
🕵️ Checking Tone of Voice: [Adversarial probe: Neutral] -> PASS
🕵️ Domain Sensitivity: [Legal/Finance probes] -> SAFE
✅ Vulnerability Regression: Fixed 2 historical jailbreaks.
Status: SECURE (Compliant with Brand Safety Playbook)`
  },
  {
    id: 'finops',
    name: 'The Economist',
    persona: 'FinOps Specialist',
    icon: <Zap size={24} />,
    color: '#f59e0b',
    description: 'FinOps ROI Waterfall modeling and model-tier optimization pivots.',
    docs: [
      { name: 'FinOps ROI Guide', path: '/docs/finops-guide' },
      { name: 'Token Management', path: '/docs/finops-guide' }
    ],
    reports: [
      { name: 'ROI Waterfall Report', path: '/finops-roi-report.html' },
      { name: 'Optimization Model', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit audit roi',
    diagram: '/assets/persona_economist.png',
    output: `💰 FINOPS ROI WATERFALL: TCO MODELING
1. Gemini 1.5 Flash Pivot: -$3,200/mo savings
2. Context Caching (90%): -$1,850/mo savings
3. Semantic Cache: -$420/mo savings
🚀 Total Monthly Opportunity: $5,470 (88% reduction)
ROI Multiplier: 8.2x efficiency gain confirmed.`
  },
  {
    id: 'governance',
    name: 'The Controller',
    persona: 'Admin / Governance',
    icon: <Settings size={24} />,
    color: '#8b5cf6',
    description: 'Gain full visibility into agent estates with centralized compliance and evidence collection.',
    docs: [
      { name: 'Operational Introduction', path: '/docs/introduction' },
      { name: 'Governance Guide', path: '/docs/audit-guide' },
      { name: 'Evidence & Compliance', path: '/docs/audit-guide' },
      { name: 'Cockpit Ops', path: '/docs/cockpit-guide' }
    ],
    reports: [
      { name: 'Global Compliance Log', path: '/compliance-audit-report.html' },
      { name: 'Evidence Lake Export', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit audit report',
    diagram: '/assets/persona_controller.png',
    output: `🏛️ Global Agent Audit Initiated...
📂 Scanning Workspace: enriquekalven/agent-cockpit
   - sales-agent: PASS (92% Score)
   - ops-agent: PASS (100% Score)
   - legacy-agent: PASS (Bridge evidence confirmed)
📜 Generating Evidence Lake Report...
✅ Report saved to cockpit_report.html
Estate Health: 98% Compliant.`
  },
  {
    id: 'sre',
    name: 'The Reliability Lead',
    persona: 'SRE / DevOps',
    icon: <Settings size={24} />,
    color: '#6366f1',
    description: 'Hardening infrastructure, auto-remediation, and planetary-scale distribution.',
    docs: [
      { name: 'Infra & Growth Guide', path: '/docs/infra-guide' },
      { name: 'Deployment Masterclass', path: '/docs/deployment' }
    ],
    reports: [
      { name: 'Fleet Health Report', path: '/compliance-audit-report.html' },
      { name: 'Uptime Evidence', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit audit report',
    diagram: '/assets/persona_reliability.png',
    output: `🛰️ Global Fleet Audit Initiated...
📂 Scanning Estate: 12 Active Agents
   - sales-agent: PASS
   - ops-agent: PASS
   - audit-agent: PASS
📜 Generating Evidence Lake Report...
✅ Fleet Health: 100% Availability.`
  },
  {
    id: 'interop',
    name: 'The Orchestrator',
    persona: 'A2A / Interop Specialist',
    icon: <Command size={24} />,
    color: '#ec4899',
    description: 'Agent-to-Agent transmission standards and cross-framework connectivity.',
    docs: [
      { name: 'A2A Standards Guide', path: '/docs/a2a-guide' },
      { name: 'MCP Connectivity', path: '/docs/cockpit-guide' }
    ],
    reports: [
      { name: 'Transmission Audit', path: '/master-audit-report.html' },
      { name: 'Interop Consensus', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit mcp-server',
    diagram: '/assets/persona_orchestrator.png',
    output: `🔌 Initializing MCP Transmission Hub...
📡 Discovering Tools: [Search, SQL, Artifacts]
✅ Registered 12 tools to MCP Fleet.
🤝 Establishing Trust Bridge (Evidence-backed)
Protocol Standard: A2A v1.3 compliant.`
  },
  {
    id: 'product',
    name: 'The Visionary',
    persona: 'Product / Sales',
    icon: <Briefcase size={24} />,
    color: '#f59e0b',
    description: 'Maximize ROI and user experience with latency analysis and GenUI optimization.',
    docs: [
      { name: 'The Agent Ops Story', path: '/docs/story' },
      { name: 'Optimization ROI', path: '/docs/finops-guide' },
      { name: 'A2UI Visual Standards', path: '/docs/a2a-guide' }
    ],
    reports: [
      { name: 'FinOps ROI Matrix', path: '/finops-roi-report.html' },
      { name: 'UX Readiness Scorecard', path: '/arch-review-report.html' }
    ],
    command: 'agentops-cockpit audit roi',
    diagram: '/assets/persona_visionary.png',
    output: `📊 Analyzing Agent Performance & ROI...
💰 Token usage: 48.2K saved (Semantic Cache hit rate: 64%)
⏱️ Latency: 2.1s avg reduction per turn.
🎨 GenUI Coverage: 100% (A2UI compliant)
📈 Estimated Monthly Savings: $2,400.
Conclusion: Positive ROI confirmed for Q1.
✨ Deployment status: ACTIVE`
  },
  {
    id: 'automation',
    name: 'The Automator',
    persona: 'CI/CD & Automation Lead',
    icon: <Cpu size={24} />,
    color: '#6366f1',
    description: 'Zero-install portable governance for CI/CD pipelines and ephemeral agents.',
    docs: [
      { name: 'UVX Master Guide', path: '/docs/uvx-master' },
      { name: 'Pipeline Integration', path: '/docs/uvx-master' }
    ],
    reports: [
      { name: 'Ephemeral Audit Log', path: '/master-audit-report.html' },
      { name: 'CI/CD Pass/Fail Evidence', path: '/compliance-evidence.md' }
    ],
    command: 'uvx agentops-cockpit audit report',
    diagram: '/assets/persona_automator.png',
    output: `📦 Running Portable AgentOps via UVX...
🔍 Project: external-repo-auditor
✅ No local installation detected (Standalone Mode)
🔍 Scanning dependencies...
⚠️ Security: 2 vulnerable packages found.
✅ Compliance: Google Well-Architected standard met.
[CI/CD] Build Gate: PASSED.`
  },
  {
    id: 'compliance',
    name: 'The Compliance Officer',
    persona: 'Legal / Compliance SME',
    icon: <FileText size={24} />,
    color: '#a855f7',
    description: 'Audit for legal defensibility, PII masking, and ISO/SOC2 enterprise policy alignment.',
    docs: [
      { name: 'Governance & Policy', path: '/docs/audit-guide' },
      { name: 'PII Guardrails', path: '/docs/audit-guide' },
      { name: 'Evidence Packing', path: '/docs/audit-guide' }
    ],
    reports: [
      { name: 'Policy Compliance Log', path: '/compliance-audit-report.html' },
      { name: 'Evidence Lake Trace', path: '/compliance-evidence.md' }
    ],
    command: 'agentops-cockpit audit policy',
    diagram: '/assets/persona_controller.png',
    output: `🕵️ POLICY AUDIT: ENTERPRISE DATA DEFENSE
🔍 Scanning for Policy ID: ISO-27001-AI
✅ PII Scrubber: Active (Emails/SSNs masked)
✅ Evidence Packing: 100% Attribution found
⚠️ Data Residency: 1 tool path using EU-WEST1 (Policy mandates US)
⚖️ Compliance Status: 92% (Legal SME approval required)`
  },
  {
    id: 'operator',
    name: 'The SITL Pilot',
    persona: 'Human-in-the-Loop / Ops',
    icon: <Activity size={24} />,
    color: '#f43f5e',
    description: 'Monitor autonomous tool triggers and maintain manual oversight on high-stakes actions.',
    docs: [
      { name: 'HITL Workflows', path: '/docs/cockpit-guide' },
      { name: 'Tool Approvals', path: '/docs/cockpit-guide' },
      { name: 'Sentinel Oversight', path: '/docs/cockpit-guide' }
    ],
    reports: [
      { name: 'HITL Audit Trail', path: '/compliance-audit-report.html' },
      { name: 'Intervention Metrics', path: '/master-audit-report.html' }
    ],
    command: 'agentops-cockpit fleet watch',
    diagram: '/assets/persona_reliability.png',
    output: `🕹️ FLEET WATCH: ACTIVE MONITORING
🟢 sales-agent: IDLE
🟡 finance-agent: PENDING APPROVAL (Action: transfer_funds)
   - Reason: Amount > $1,000 threshold
   - Surface: A2UI Approval Node #412
🔘 Waiting for human intervention...
✅ User approved. Executing tool securely.`
  }
];

export function OperationalJourneys() {
  const [activeTab, setActiveTab] = useState(JOURNEYS[0].id);
  const activeJourney = JOURNEYS.find(j => j.id === activeTab) || JOURNEYS[0];

  // A2UI: surfaceId="operational-journeys"
  return (
    <section className="journeys-section" data-surface-id="operational-journeys">
      <div className="container">
        <div className="journeys-header">
          <span className="accent-label">Operational Paths</span>
          <h2>Mission Control: <span className="gradient-text">Tailored Journeys</span></h2>
          <p>Choose your professional lens to see how the Cockpit empowers your specific role across frameworks, clouds, and languages.</p>
        </div>

        <div className="journeys-grid">
          {/* Persona Tabs */}
          <div className="persona-tabs">
            {JOURNEYS.map((journey) => (
              <button
                key={journey.id}
                className={`persona-tab ${activeTab === journey.id ? 'active' : ''}`}
                onClick={() => setActiveTab(journey.id)}
                style={{ '--active-color': journey.color } as React.CSSProperties}
              >
                <div className="tab-avatar-container">
                  <img src={journey.diagram} alt={journey.name} className="tab-avatar" />
                  <div className="tab-avatar-overlay">
                    {journey.icon}
                  </div>
                </div>
                <div className="tab-info">
                  <span className="tab-name">{journey.name}</span>
                  <span className="tab-persona">{journey.persona}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Journey Content */}
          <div className="journey-card">
            <div className="journey-main">
              <div className="journey-details">
                <div className="journey-description-box">
                  <div className="journey-badge" style={{ backgroundColor: `${activeJourney.color}15`, color: activeJourney.color }}>
                    {activeJourney.name} Pathway
                  </div>
                  <h3>Mission: {activeJourney.description}</h3>
                  <div className="support-chips">
                    <span className="chip">Multi-Cloud</span>
                    <span className="chip">Multi-Framework</span>
                    <span className="chip">Any LLM</span>
                  </div>
                </div>

                <div className="journey-resources">
                  <h4>Critical Documentation</h4>
                  <div className="docs-list">
                    {activeJourney.docs.map((doc, i) => (
                      doc.path.startsWith('http') ? (
                        <a key={i} href={doc.path} target="_blank" rel="noopener noreferrer" className="doc-item">
                          <FileText size={18} />
                          <span>{doc.name}</span>
                          <ExternalLink size={14} className="chevron" />
                        </a>
                      ) : (
                        <Link key={i} to={doc.path} className="doc-item">
                          <FileText size={18} />
                          <span>{doc.name}</span>
                          <ChevronRight size={14} className="chevron" />
                        </Link>
                      )
                    ))}
                  </div>

                  <h4 style={{ marginTop: '2rem' }}>Sample Reports</h4>
                  <div className="docs-list">
                    {activeJourney.reports && activeJourney.reports.map((report, i) => (
                      <a key={i} href={report.path} target="_blank" rel="noopener noreferrer" className="doc-item report-accent">
                        <CheckCircle size={18} style={{ color: activeJourney.color }} />
                        <span>{report.name}</span>
                        <ExternalLink size={14} className="chevron" />
                      </a>
                    ))}
                  </div>
                </div>
              </div>

              <div className="journey-visual">
                <div className="persona-diagram-container">
                  <img src={(activeJourney as any).diagram} alt={activeJourney.name} className="persona-diagram-img" />
                </div>
                <div className="terminal-container">
                  <div className="terminal-header">
                    <div className="terminal-dots">
                      <span className="dot red"></span>
                      <span className="dot orange"></span>
                      <span className="dot green"></span>
                    </div>
                    <div className="terminal-title">bash — {activeJourney.command}</div>
                  </div>
                  <div className="terminal-body">
                    <div className="terminal-line cmd">
                      <span className="prompt">$</span> {activeJourney.command}
                    </div>
                    <pre className="terminal-output">{activeJourney.output}</pre>
                    <div className="terminal-line cursor">_</div>
                  </div>
                </div>
                <div className="visual-caption">
                  <CheckCircle size={14} />
                  Real-world CLI output sample
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .journeys-section {
          padding: 10rem 2rem;
          background: rgba(var(--primary-color-rgb), 0.02);
          border-top: 1px solid var(--border-color);
        }

        .journeys-header {
          text-align: center;
          margin-bottom: 5rem;
          max-width: 800px;
          margin-left: auto;
          margin-right: auto;
        }

        .journeys-header h2 {
          font-size: 3.5rem;
          font-weight: 900;
          letter-spacing: -0.04em;
          margin-bottom: 1.5rem;
        }

        .journeys-header p {
          font-size: 1.25rem;
          color: var(--text-secondary);
          line-height: 1.6;
        }

        .journeys-grid {
          display: grid;
          grid-template-columns: 320px 1fr;
          gap: 3rem;
          align-items: start;
        }

        .persona-tabs {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          max-height: 580px;
          overflow-y: auto;
          padding-right: 0.5rem;
        }

        /* Custom scrollbar for persona list */
        .persona-tabs::-webkit-scrollbar {
          width: 4px;
        }
        .persona-tabs::-webkit-scrollbar-track {
          background: transparent;
        }
        .persona-tabs::-webkit-scrollbar-thumb {
          background: var(--border-color);
          border-radius: 10px;
        }

        .persona-tab {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.75rem 1rem;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          text-align: left;
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          color: var(--text-primary);
        }

        .persona-tab:hover {
          transform: translateX(8px);
          border-color: var(--text-secondary);
        }

        .persona-tab.active {
          background: var(--bg-color);
          border-color: var(--active-color);
          box-shadow: 0 10px 20px rgba(0,0,0,0.05);
          transform: translateX(12px);
        }

        .tab-avatar-container {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          position: relative;
          overflow: hidden;
          border: 2px solid var(--border-color);
          flex-shrink: 0;
          transition: all 0.3s;
          background: var(--bg-color);
        }

        .persona-tab.active .tab-avatar-container {
          border-color: var(--active-color);
          box-shadow: 0 0 15px var(--active-color);
          transform: scale(1.1);
        }

        .tab-avatar {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.3s;
        }

        .persona-tab:hover .tab-avatar {
          transform: scale(1.1);
        }

        .tab-avatar-overlay {
          position: absolute;
          inset: 0;
          background: rgba(0,0,0,0.4);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          opacity: 0;
          transition: opacity 0.3s;
        }

        .tab-avatar-overlay svg {
          width: 20px;
          height: 20px;
        }

        .persona-tab.active .tab-avatar-overlay {
          opacity: 1;
        }

        .tab-info {
          display: flex;
          flex-direction: column;
        }

        .tab-name {
          font-weight: 800;
          font-size: 1.05rem;
          letter-spacing: -0.01em;
        }

        .tab-persona {
          font-size: 0.8rem;
          color: var(--text-secondary);
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .journey-card {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 32px;
          padding: 3.5rem;
          min-height: 580px;
          position: relative;
          overflow: hidden;
          box-shadow: 0 40px 80px rgba(0,0,0,0.05);
        }

        .journey-main {
          display: grid;
          grid-template-columns: 1fr 1.1fr;
          gap: 4rem;
          height: 100%;
        }

        .journey-description-box h3 {
          font-size: 2.25rem;
          font-weight: 850;
          line-height: 1.2;
          margin-bottom: 2rem;
          letter-spacing: -0.02em;
        }

        .journey-badge {
          display: inline-block;
          padding: 0.5rem 1rem;
          border-radius: 999px;
          font-size: 0.8rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          margin-bottom: 1.5rem;
        }

        .support-chips {
          display: flex;
          gap: 0.75rem;
          margin-bottom: 3rem;
        }

        .chip {
          padding: 0.4rem 0.8rem;
          background: rgba(var(--text-primary-rgb), 0.05);
          border: 1px solid var(--border-color);
          border-radius: 8px;
          font-size: 0.75rem;
          font-weight: 700;
          color: var(--text-secondary);
        }

        .journey-resources h4 {
          font-size: 0.9rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: var(--text-secondary);
          margin-bottom: 1.5rem;
        }

        .docs-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .doc-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem 1.25rem;
          background: var(--bg-color);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          text-decoration: none;
          color: var(--text-primary);
          font-weight: 700;
          font-size: 0.95rem;
          transition: all 0.2s;
        }

        .doc-item:hover {
          background: var(--bg-secondary);
          border-color: var(--text-primary);
          transform: translateY(-2px);
        }

        .doc-item .chevron {
          margin-left: auto;
          opacity: 0.3;
        }

        .doc-item:hover .chevron {
          opacity: 1;
          color: var(--text-primary);
        }
 
        .persona-diagram-container {
          margin-bottom: 2rem;
          border-radius: 20px;
          overflow: hidden;
          border: 1px solid var(--border-color);
          box-shadow: 0 10px 30px rgba(0,0,0,0.1);
          background: var(--bg-color);
        }
 
        .persona-diagram-img {
          width: 100%;
          height: auto;
          display: block;
        }
 
        .terminal-container {
          background: #0D0D0D;
          border-radius: 16px;
          border: 1px solid rgba(255,255,255,0.1);
          overflow: hidden;
          box-shadow: 0 20px 40px rgba(0,0,0,0.3);
          height: 100%;
          display: flex;
          flex-direction: column;
        }

        .terminal-header {
          background: #1A1A1A;
          padding: 0.75rem 1.25rem;
          display: flex;
          align-items: center;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .terminal-dots {
          display: flex;
          gap: 8px;
        }

        .dot {
          width: 10px;
          height: 10px;
          border-radius: 50%;
        }

        .dot.red { background: #ff5f56; }
        .dot.orange { background: #ffbd2e; }
        .dot.green { background: #27c93f; }

        .terminal-title {
          flex: 1;
          text-align: center;
          font-family: var(--font-mono);
          font-size: 0.75rem;
          color: #71717A;
          padding-right: 40px;
        }

        .terminal-body {
          padding: 1.5rem;
          font-family: var(--font-mono);
          font-size: 0.85rem;
          line-height: 1.6;
          color: #E2E8F0;
          flex: 1;
          overflow-y: auto;
        }

        .terminal-line.cmd {
          margin-bottom: 1rem;
          color: #A5B4FC;
          font-weight: 600;
        }

        .terminal-line .prompt {
          color: #22D3EE;
          margin-right: 0.5rem;
        }

        .terminal-output {
          margin: 0;
          white-space: pre-wrap;
          font-family: inherit;
          color: #D1D5DB;
        }

        .terminal-line.cursor {
          animation: blink 1s step-end infinite;
          color: #3b82f6;
          font-weight: bold;
        }

        .visual-caption {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          margin-top: 1.5rem;
          font-size: 0.8rem;
          font-weight: 700;
          color: var(--text-secondary);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        @keyframes blink {
          50% { opacity: 0; }
        }

        @media (max-width: 1100px) {
          .journey-main {
            grid-template-columns: 1fr;
          }
          .journeys-grid {
            grid-template-columns: 1fr;
          }
          .persona-tabs {
            flex-direction: row;
            overflow-x: auto;
            padding-bottom: 1rem;
          }
          .persona-tab {
            flex-shrink: 0;
            width: 200px;
          }
          .persona-tab.active {
            transform: translateY(-4px);
          }
        }

        @media (max-width: 768px) {
          .journeys-header h2 { font-size: 2rem; }
          .journeys-header p { font-size: 1rem; }
          .journeys-section { padding: 4rem 1rem; }
          .journey-card { padding: 1.5rem; }
          .journey-description-box h3 { font-size: 1.5rem; }
          .persona-tab { width: 160px; padding: 0.5rem; }
          .tab-avatar-container { width: 40px; height: 40px; }
          .tab-name { font-size: 0.9rem; }
          .tab-persona { font-size: 0.7rem; }
        }
      `}</style>
    </section>
  );
}
