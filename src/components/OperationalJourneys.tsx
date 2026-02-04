import React, { useState } from 'react';
import {
  Terminal, Code, Shield, Briefcase,
  Settings, ChevronRight, Layout, Cpu,
  ExternalLink, FileText, CheckCircle
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
      { name: 'Local Mocking / CLI', path: '/docs/commands-master' },
      { name: 'Reference: Agent Starter Pack', path: 'https://github.com/GoogleCloudPlatform/agent-starter-pack/' }
    ],
    reports: [
      { name: 'A2UI Contract Audit', path: '/master-audit-report.html' },
      { name: 'Unit Test Evidence', path: '/compliance-evidence.md' }
    ],
    command: 'uvx agent-starter-pack create my-agent',
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
    description: 'Design resilient, multi-cloud agentic systems aligned with Well-Architected patterns.',
    docs: [
      { name: 'Google Architecture', path: '/docs/google-architecture' },
      { name: 'Deployment Strategy', path: '/docs/deployment' },
      { name: 'Production Checklist', path: '/docs/production-checklist' }
    ],
    reports: [
      { name: 'Architecture Review (ADR)', path: '/arch-review-report.html' },
      { name: 'Design Consensus Report', path: '/master-audit-report.html' }
    ],
    command: 'make apply-architecture',
    output: `🏗️ Applying Well-Architected Patterns...
🔍 Analyzing /src/backend for policy alignment
✅ Engine: Redundant Cloud Run deployment confirmed.
✅ Face: Multi-cloud CDN caching via Firebase enabled.
✅ Cockpit: Shadow Router active on Vertex AI.
🔒 Security: PII Scrubber injected into middleware.
Infrastructure aligned with Google Well-Architected Framework.`
  },
  {
    id: 'security',
    name: 'The Guardian',
    persona: 'Security Specialist',
    icon: <Shield size={24} />,
    color: '#ef4444',
    description: 'Hardening agents against adversarial attacks, prompt injections, and data privacy leaks.',
    docs: [
      { name: 'Security Protocol', path: '/docs/redteam-guide' },
      { name: 'Red Team Audits', path: '/docs/redteam-guide' },
      { name: 'Privacy & Policies', path: '/docs/audit-guide' }
    ],
    reports: [
      { name: 'Red Team Pentest Report', path: '/master-audit-report.html' },
      { name: 'Policy Violation Log', path: '/compliance-evidence.md' }
    ],
    command: 'make red-team --target=agent-x',
    output: `🛡️ Starting Adversarial Audit...
🕵️ Testing Prompt Injection: [Attempt 01..15]
✅ Result: Sanitized (Blocked via Policy Engine)
🕵️ Checking PII Leakage: [No sensitive data found]
⚠️ Warning: Identity verified via Evidence Bridge.
✅ Reliability: 99.9% Success rate across 100 simulations.
Status: SECURE (Compliant with Enterprise Standard)`
  },
  {
    id: 'governance',
    name: 'The Controller',
    persona: 'Admin / Governance',
    icon: <Settings size={24} />,
    color: '#8b5cf6',
    description: 'Gain full visibility into agent estates with centralized compliance and evidence collection.',
    docs: [
      { name: 'Governance Guide', path: '/docs/audit-guide' },
      { name: 'Evidence & Compliance', path: '/docs/audit-guide' },
      { name: 'Cockpit Ops', path: '/docs/cockpit-guide' }
    ],
    reports: [
      { name: 'Global Compliance Audit', path: '/master-audit-report.html' },
      { name: 'Evidence Lake Export', path: '/compliance-evidence.md' }
    ],
    command: 'make audit-all',
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
      { name: 'FinOps ROI Analysis', path: '/master-audit-report.html' },
      { name: 'UX Readiness Scorecard', path: '/arch-review-report.html' }
    ],
    command: 'agent-ops --analyze-roi',
    output: `📊 Analyzing Agent Performance & ROI...
💰 Token usage: 48.2K saved (Semantic Cache hit rate: 64%)
⏱️ Latency: 2.1s avg reduction per turn.
🎨 GenUI Coverage: 100% (A2UI compliant)
📈 Estimated Monthly Savings: $2,400.
Conclusion: Positive ROI confirmed for Q1.
✨ Deployment status: ACTIVE`
  }
];

export function OperationalJourneys() {
  const [activeTab, setActiveTab] = useState(JOURNEYS[0].id);
  const activeJourney = JOURNEYS.find(j => j.id === activeTab) || JOURNEYS[0];

  return (
    <section className="journeys-section">
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
                <div className="tab-icon">{journey.icon}</div>
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
          gap: 0.75rem;
        }

        .persona-tab {
          display: flex;
          align-items: center;
          gap: 1.25rem;
          padding: 1.25rem;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 16px;
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

        .tab-icon {
          width: 44px;
          height: 44px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(0,0,0,0.03);
          color: var(--text-secondary);
          transition: all 0.3s;
        }

        .persona-tab.active .tab-icon {
          background: var(--active-color);
          color: white;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
      `}</style>
    </section>
  );
}
