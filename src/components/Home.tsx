import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Rocket, Shield, Activity, Cpu, Command,
  Terminal, ChevronRight, Github, ExternalLink,
  Layers, Zap, Search, Globe, Lock, Server, CheckCircle
} from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';

// SVG Logos for Ecosystem Bar
const GoogleCloudLogo = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="logo-svg">
    <path d="M12.48 10.92v3.28h7.84c-.24 1.84-.92 3.32-2.12 4.52-1.36 1.36-3.44 2.84-7.56 2.84-6.72 0-11.92-5.44-11.92-12.16S3.88 0 10.6 0c3.64 0 6.28 1.44 8.28 3.32l2.32-2.32C18.96 1.12 15.68 0 10.6 0 4.8 0 0 4.8 0 10.6s4.8 10.6 10.6 10.6c3.12 0 5.48-1.04 7.44-3.08 1.92-1.92 2.52-4.64 2.52-6.88 0-.68-.04-1.36-.16-2.04h-9.8z" />
  </svg>
);

const azureLogo = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="logo-svg">
    <path d="M5.483 21.3h15.115l-6.198-8.914-4.814 2.684L5.483 21.3zm13.111-13.844L8.761 18.067l4.633-2.583 5.2-10.3zm5.406 13.844L14.714 3.012l-3.322 3.355 7.108 11.577 5.501 3.355h.001zM0 21.3h5.483l3.279-3.233L2.203 9.412 0 21.3z" />
  </svg>
);

const openAILogo = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="logo-svg">
    <path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5153-4.9022 6.0462 6.0462 0 0 0-4.3412-2.7355 5.9803 5.9803 0 0 0-5.1328 1.3427 5.9928 5.9928 0 0 0-4.4365-2.0076 6.0521 6.0521 0 0 0-5.2277 3.0336 5.973 5.973 0 0 0-1.0545 5.5003 5.985 5.985 0 0 0 .5153 4.9022 6.053 6.053 0 0 0 4.3412 2.7355 5.981 5.981 0 0 0 5.1328-1.3427 5.992 5.992 0 0 0 4.4365 2.0076 6.0461 6.0461 0 0 0 5.2277-3.0336 5.973 5.973 0 0 0 1.0545-5.5003zm-9.3153 9.136a4.4828 4.4828 0 0 1-2.9034-1.0768l.1569-.0901 4.5452-2.6176a.443.443 0 0 0 .2215-.3836V8.6279l1.6214.936a.042.042 0 0 1 .0207.0315v5.3934a4.5028 4.5028 0 0 1-3.6623 4.3683zm-7.6534-1.928a4.4756 4.4756 0 0 1-.9013-3.1151l.1569.0901 4.5452 2.6176a.4434.4434 0 0 0 .4382-.0045l6.1664-3.5552-1.6214-.936a.0416.0416 0 0 1-.0259-.0281l-4.668-2.6953a4.5056 4.5056 0 0 1-4.0901-3.9735zM4.686 6.3194a4.4796 4.4796 0 0 1 2.0021-2.4285l-.014.1037-1.1214 6.4716a.4434.4434 0 0 0 .2166.4282l6.1664 3.5552-.003-1.872a.0416.0416 0 0 1 .012-.034l4.671-2.6934a4.5126 4.5126 0 0 1 .4278-5.3417zM11.0335 5.043a4.4827 4.4827 0 0 1 2.9034 1.0768l-.1569.0901-4.5452 2.6176a.443.443 0 0 0-.2215.3836V15.372l-1.6214-.936a.0416.0416 0 0 1-.0207-.0315V9.0111a4.5027 4.5027 0 0 1 3.6623-4.3683zm7.6534 1.928a4.4756 4.4756 0 0 1 .9013 3.115l-.1569-.0901-4.5452-2.6176a.4432.4432 0 0 0-.4382.0045l-6.1664 3.5552 1.6214.936a.042.042 0 0 1 .0259.0281l4.668 2.6953a4.5056 4.5056 0 0 1 4.0901 3.9735zm1.5312 10.1502a4.4795 4.4795 0 0 1-2.0021 2.4285l.014-.1037 1.1214-6.4716a.443.443 0 0 0-.2166-.4282l-6.1664-3.5552.003 1.872a.0416.0416 0 0 1-.012.034l-4.671 2.6934a4.5126 4.5126 0 0 1-.4278 5.3417zM12 10.7431L14.1818 12 12 13.2569 9.8182 12 12 10.7431z" />
  </svg>
);

const awsLogo = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="logo-svg">
    <path d="M12.915 5.8s.09.435.09.83c0 .87-.51 1.695-1.5 2.13-1.005.42-2.31.54-3.375.54h-1.5c-1.125 0-2.4-.105-3.3-.855-.84-.705-1.11-1.74-1.11-2.91 0-1.89.78-3.03 2.19-3.795C5.835 1.095 8.01 1.02 10.035 1.02c1.92 0 4.14.21 5.385 1.86.63.84.81 1.845.81 2.895v2.85c0 1.275.075 2.505.48 3.42.345.81.99 1.485 1.815 1.755.765.24 1.545.24 2.325.21v.96c-1.17.165-2.295.075-3.39-.42-1.02-.45-1.635-1.29-1.92-2.34-.6 1.08-1.53 1.875-2.7 2.34-1.29.495-2.73.57-4.11.51-2.31-.105-4.44-.81-5.61-3.045-.525-.975-.54-2.145-.54-3.21 0-1.44.3-2.655 1.2-3.66C5.64.12 7.425 0 9.21 0c2.16 0 4.41.045 6.06 1.65.645.63.885 1.575.885 2.46V5.8h-3.24zm-1.875 3.3c-.945-.045-1.545-.465-1.545-1.5 0-.96.48-1.575 1.41-1.695.885-.12 1.785-.09 2.67-.09h.735v2.025s-.57.69-1.77.81c-.51.045-1.02.48-1.5.45zM12 18.06c-3.15 0-6.105.81-8.52 2.295-.345.21-.555.57-.45.96.105.39.465.585.81.42C6.18 20.37 9.045 19.65 12 19.65c2.955 0 5.82.72 8.16 2.085.345.195.705 0 .81-.39.105-.39-.105-.75-.45-.96-2.415-1.485-5.37-2.325-8.52-2.325zm9.33-1.14c-.18-.21-.495-.195-.72-.06-1.995 1.23-4.395 1.95-6.915 1.95-2.52 0-4.92-.72-6.915-1.95-.225-.135-.54-.15-.72.06-.18.21-.135.54.09.69 2.175 1.35 4.785 2.145 7.545 2.145 2.76 0 5.37-.795 7.545-2.145.225-.15.27-.48.09-.69z" />
  </svg>
);

const anthropicLogo = () => (
  <svg viewBox="0 0 24 24" fill="currentColor" className="logo-svg">
    <path d="M16.903 0H7.097L0 24h3.742l1.677-5.806h13.161L20.258 24H24L16.903 0zm-1.161 14.71H8.258l4.323-14.71L15.742 14.71z" />
  </svg>
);

export function Home() {
  const [stars, setStars] = useState<number | null>(null);

  useEffect(() => {
    fetch('https://api.github.com/repos/enriquekalven/agent-cockpit')
      .then(res => res.json())
      .then(data => {
        if (data.stargazers_count) {
          setStars(data.stargazers_count);
        }
      })
      .catch(err => console.error('Error fetching stars:', err));
  }, []);

  return (
    <div className="crew-home">
      {/* Latest Release Banner */}
      <div className="release-banner">
        <div className="banner-content">
          <span className="banner-tag">NEW v0.8.0</span>
          <span className="banner-text">The Governance Update: Principal SME Persona Approvals, Legal/Marketing Audits, and PDF Reporting are now active.</span>
          <div className="flex gap-4">
            <Link to="/docs" className="banner-link">View Docs <ChevronRight size={14} /></Link>
            <div className="flex items-center gap-2">
              <Link to="/samples" className="banner-link">View Sample Reports <ChevronRight size={14} /></Link>
            </div>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <section className="crew-hero">
        <header className="crew-home-nav">
          <div className="nav-logo">
            <img src="/kokpi_branded.jpg" alt="Kokpi" className="nav-mascot" />
            <span>AgentOps Cockpit</span>
          </div>
          <nav className="nav-links">
            <Link to="/docs" className="nav-link">Documentation</Link>
            <Link to="/docs/google-architecture" className="nav-link">Framework</Link>
            <a href="https://github.com/enriquekalven/agent-cockpit/blob/main/CHANGELOG.md" className="nav-link">Changelog</a>
            <a href="https://github.com/enriquekalven/agent-cockpit" target="_blank" rel="noopener noreferrer" className="nav-icon-link">
              <Github size={20} />
              {stars !== null && (
                <span className="nav-star-count">{(stars / 1000).toFixed(1)}k</span>
              )}
            </a>
            <ThemeToggle />
          </nav>
        </header>

        <div className="hero-main">
          <div className="hero-content-v2">
            <div className="pill-badge">
              <span className="pulsing-dot"></span>
              Multi-Cloud Well-Architected Framework for Agents
            </div>
            <h1 className="hero-headline">
              <span className="hero-headline-text">The Professional Logic Layer for <span className="gradient-text">Agentic Apps</span></span>
            </h1>
            <p className="hero-description">
              Move beyond basic prompt engineering. The AgentOps Cockpit is a high-performance distribution for managing, optimizing, and securing AI agents across <strong>all major cloud providers and LLM ecosystems.</strong>
            </p>
            <div className="hero-actions flex-wrap">
              <Link to="/docs/getting-started" className="btn-primary">
                Get Started
                <ChevronRight size={18} />
              </Link>
              <Link to="/samples" className="btn-secondary">
                <Shield size={18} />
                View Sample Reports
              </Link>
            </div>

            <div className="hero-features-preview">
              <div className="preview-item">
                <Shield size={20} className="text-blue-500" />
                <span>Adversarial Audits</span>
              </div>
              <div className="preview-item">
                <Activity size={20} className="text-green-500" />
                <span>Cost Optimization</span>
              </div>
              <div className="preview-item">
                <Lock size={20} className="text-purple-500" />
                <span>PII Scrubbing</span>
              </div>
            </div>
          </div>

          <div className="hero-visual-v2">
            <div className="visual-container">
              <div className="visual-background-glow"></div>

              <div className="mock-cockpit-preview">
                <div className="cockpit-header">
                  <Activity size={16} className="text-green-400" />
                  <span>OP-CENTER CLUSTER: US-CENTRAL1</span>
                </div>
                <div className="cockpit-stats-grid">
                  <div className="c-stat">
                    <span className="c-label">COST SAVINGS</span>
                    <span className="c-value text-green-400">92%</span>
                  </div>
                  <div className="c-stat">
                    <span className="c-label">LATENCY</span>
                    <span className="c-value text-blue-400">42ms</span>
                  </div>
                </div>
                <div className="cockpit-graph">
                  <div className="bar" style={{ height: '40%' }}></div>
                  <div className="bar" style={{ height: '70%' }}></div>
                  <div className="bar active" style={{ height: '90%' }}></div>
                  <div className="bar" style={{ height: '60%' }}></div>
                </div>
              </div>

              <div className="mock-terminal">
                <div className="terminal-header">
                  <div className="dots"><span></span><span></span><span></span></div>
                  <div className="terminal-title">agent-ops --safe-build</div>
                </div>
                <div className="terminal-body">
                  <div className="line terminal-cmd">$ make audit</div>
                  <div className="line text-blue-400">🕹️ Running Persona-Based Audit...</div>
                  <div className="line text-green-400">🏛️ Platform SME: APPROVED</div>
                  <div className="line text-green-400">⚖️ Legal SME: APPROVED</div>
                  <div className="line text-green-400">💰 FinOps SME: APPROVED</div>
                  <div className="line text-green-400">🎭 UX SME: APPROVED</div>
                  <div className="line blink">_</div>
                </div>
              </div>

              <div className="floating-stat stat-1 green-vibrant">
                <Zap size={16} />
                <span>$420 Saved Today</span>
              </div>
              <div className="floating-stat stat-2 purple-vibrant">
                <Shield size={16} />
                <span>100% Red Team Pass</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Ecosystem Logos Bar */}
      <section className="ecosystem-logos-bar">
        <div className="container">
          <div className="ecosystem-logos-container">
            <div className="ecosystem-item-v2" title="Google Cloud">
              <img src="https://cdn.simpleicons.org/googlecloud" alt="Google Cloud" className="logo-img" />
              <span>Google Cloud</span>
            </div>
            <div className="ecosystem-item-v2" title="Azure">
              <img src="https://cdn.simpleicons.org/microsoftazure" alt="Azure" className="logo-img" />
              <span>Azure</span>
            </div>
            <div className="ecosystem-item-v2" title="OpenAI">
              <img src="https://cdn.simpleicons.org/openai" alt="OpenAI" className="logo-img" />
              <span>OpenAI</span>
            </div>
            <div className="ecosystem-item-v2" title="AWS">
              <img src="https://cdn.simpleicons.org/amazonwebservices" alt="AWS" className="logo-img" />
              <span>AWS</span>
            </div>
            <div className="ecosystem-item-v2" title="Anthropic">
              <img src="https://cdn.simpleicons.org/anthropic" alt="Anthropic" className="logo-img" />
              <span>Anthropic</span>
            </div>
            <div className="ecosystem-item-v2" title="CopilotKit">
              <img src="https://cdn.simpleicons.org/copilotkit" alt="CopilotKit" className="logo-img" />
              <span>CopilotKit</span>
            </div>
          </div>
        </div>
      </section>

      <section className="frameworks-bar">
        <div className="container">
          <div className="framework-section">
            <div className="frameworks-label">Orchestration Frameworks</div>
            <div className="frameworks-grid">
              <div className="framework-badge adk">Google ADK</div>
              <div className="framework-badge crew">CrewAI</div>
              <div className="framework-badge langgraph">LangGraph</div>
              <div className="framework-badge autogen">AutoGen</div>
              <div className="framework-badge openai">OpenAI Agentkit</div>
              <div className="framework-badge copilot">CopilotKit</div>
              <div className="framework-badge angular">Angular Face</div>
              <div className="framework-badge streamlit">Streamlit</div>
              <div className="framework-badge lit">Lit / Web Components</div>
            </div>
          </div>

          <div className="framework-section mt-12">
            <div className="frameworks-label">Programming Languages & Runtimes</div>
            <div className="frameworks-grid">
              <div className="framework-badge python">Python</div>
              <div className="framework-badge go">Golang</div>
              <div className="framework-badge nodejs">NodeJS</div>
              <div className="framework-badge typescript">TypeScript</div>
              <div className="framework-badge cloudrun">Cloud Run</div>
              <div className="framework-badge gke">GKE</div>
              <div className="framework-badge agentengine">Agent Engine</div>
            </div>
          </div>
        </div>
      </section>

      {/* Visual: Agentic Trinity */}
      <section className="ecosystem-section bg-trinity">
        <div className="ecosystem-card full-width glass-trinity">
          <div className="glass-content">
            <div className="text-side">
              <span className="accent-label">Core Architecture</span>
              <h3>The Agentic <span className="gradient-text">Trinity</span></h3>
              <p>We divide production complexity into three specialized layers. This isolation allows you to optimize reasoning, interface, and governance independently.</p>
              <ul className="accent-list">
                <li><strong>The Engine</strong>: Reasoning trajectories and tool orchestrations.</li>
                <li><strong>The Face</strong>: Reactive UX surfaces and A2UI protocols.</li>
                <li><strong>The Cockpit</strong>: Governance, cost control, and policy enforcement.</li>
              </ul>
            </div>
            <div className="visual-side">
              <img src="/assets/trinity.png" alt="Agentic Trinity" className="ecosystem-img shadow-vibrant" />
            </div>
          </div>
        </div>
      </section>


      {/* Philosophy Section */}
      <section className="crew-philosophy">
        <div className="container">
          <div className="philosophy-header">
            <h2>Framework <span className="text-primary">Agnostic Governance</span></h2>
            <p>Whether you use ADK, CrewAI, or OpenAI, we provide the architectural blueprints and executable safety audits to move your agents into production.</p>
          </div>

          <div className="trinity-grid-v2">
            <div className="trinity-card">
              <div className="card-icon blue"><Cpu /></div>
              <h3>The Engine</h3>
              <p>The reasoning core. Built with Vertex AI and Google's Agent Development Kit (ADK) for reliable tool orchestration.</p>
              <Link to="/docs/be-integration" className="card-link">Learn about Engine →</Link>
            </div>
            <div className="trinity-card active">
              <div className="card-icon green"><Activity /></div>
              <h3>The Cockpit</h3>
              <p>The operational brain. Real-time cost control, semantic caching, and security auditing for "Day 2" success.</p>
              <div className="flex flex-col gap-2">
                <Link to="/ops" className="card-link">Launch the Cockpit →</Link>
                <div className="flex gap-4">
                  <a href="/sample-report.html" target="_blank" className="card-link text-sm opacity-80" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    Audit (HTML) <ExternalLink size={14} />
                  </a>
                  <a href="/sample-report.md" target="_blank" className="card-link text-sm opacity-80" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    Audit (MD) <ExternalLink size={14} />
                  </a>
                </div>
              </div>
            </div>
            <div className="trinity-card">
              <div className="card-icon purple"><Layers /></div>
              <h3>The Face</h3>
              <p>The user experience. Adaptive surfaces and GenUI standards (A2UI) that transform text into interactive applications.</p>
              <Link to="/docs/development" className="card-link">Build the Face →</Link>
            </div>
          </div>
        </div>
      </section>

      {/* Visual: Ecosystem Integrations */}
      <section className="ecosystem-section">
        <div className="ecosystem-card full-width reverse">
          <div className="glass-content">
            <div className="visual-side">
              <img src="/assets/ecosystem.png" alt="Ecosystem Integration" className="ecosystem-img" />
            </div>
            <div className="text-side">
              <span className="accent-label">Enterprise Ready</span>
              <h3>Native <span className="text-primary">Ecosystem</span> Handshake</h3>
              <p>The Cockpit isn't a silo. It acts as the intelligent orchestration layer between your agents and the Google Cloud ecosystem.</p>
              <div className="value-stats">
                <div className="value-stat">
                  <h4>90%+</h4>
                  <p>Cost Reduction</p>
                </div>
                <div className="value-stat">
                  <h4>&lt;50ms</h4>
                  <p>Cache Latency</p>
                </div>
                <div className="value-stat">
                  <h4>100%</h4>
                  <p>Identity Sync</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="crew-features">
        <div className="container">
          <div className="features-header">
            <span className="accent-label">Capabilities</span>
            <h2>Hardened for <span className="gradient-text">Production</span></h2>
          </div>

          <div className="capabilities-grid">
            <div className="capability-item">
              <div className="item-icon"><Shield size={24} /></div>
              <div>
                <h4>Red Team Auditor</h4>
                <p>Automated adversarial auditing to prevent prompt injections and PII leaks before deployment.</p>
              </div>
            </div>
            <div className="capability-item">
              <div className="item-icon"><Zap size={24} /></div>
              <div>
                <h4>Hive Mind Cache</h4>
                <p>Semantic caching layer that reduces LLM billable tokens by serving similar queries in milliseconds.</p>
              </div>
            </div>
            <div className="capability-item">
              <div className="item-icon"><Globe size={24} /></div>
              <div>
                <h4>Shadow Routing</h4>
                <p>Compare new models and prompt versions against production traffic without user impact.</p>
              </div>
            </div>
            <div className="capability-item">
              <div className="item-icon"><Layers size={24} /></div>
              <div>
                <h4>Tiered Governance</h4>
                <p>Choose between a 15s "Safe-Build" for dev agility or a deep 5m audit for production-gate benchmarking.</p>
              </div>
            </div>
            <div className="capability-item glass-highlight border-blue-500/30">
              <div className="item-icon text-blue-500"><Command size={24} /></div>
              <div>
                <h4>Agentic Pair Programming</h4>
                <p>Pair with <strong>Antigravity</strong> or <strong>Claude Code</strong> to maximize findings and iteratively fix them upon your approval.</p>
              </div>
            </div>
            <div className="capability-item">
              <div className="item-icon text-orange-500"><Server size={24} /></div>
              <div>
                <h4>MCP Connectivity Hub</h4>
                <p>Native Model Context Protocol (MCP) server support. Connect your agent to any 1P/3P tool ecosystem with audited execution.</p>
              </div>
            </div>
            <div className="capability-item">
              <div className="item-icon text-green-500"><CheckCircle size={24} /></div>
              <div>
                <h4>CI/CD Build Gates</h4>
                <p>Automated GitHub Actions that block production deployments if security vulnerabilities or cost overruns are detected.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Visual: Operational Flow */}
      <section className="ecosystem-section bg-dark-flow">
        <div className="container">
          <div className="philosophy-header">
            <span className="accent-label">Execution Pipeline</span>
            <h2 className="text-white">The Operational <span className="gradient-text">Safe-Build</span></h2>
          </div>
          <div className="workflow-visual-container">
            <img src="/assets/workflow.png" alt="Operational Workflow" className="workflow-img" />
            <div className="workflow-overlay-text">
              Each cycle in the Cockpit goes through a multi-stage validation: Situational Audit → Conflict Guard → Quality Hill Climbing → Automated Red Teaming. <strong>Enforced via GitHub Actions on every PR.</strong>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="crew-cta-section">
        <div className="cta-box">
          <h2>Ready to build high-fidelity agents?</h2>
          <p>Join the next generation of teams building on the Optimized Agent Stack.</p>
          <div className="cta-btns">
            <Link to="/docs/getting-started" className="btn-primary">Get Started</Link>
            <a href="https://github.com/enriquekalven/agent-cockpit" className="btn-secondary">Star on GitHub</a>
          </div>
        </div>
      </section>

      {/* Community Section */}
      <section className="crew-community">
        <div className="container">
          <div className="community-card">
            <div className="community-left">
              <span className="accent-label">Community</span>
              <h2>Help us reach <span className="text-primary">10K Stars</span></h2>
              <p>The AgentOps Cockpit is an open-source movement to bring professional governance to the AI agent ecosystem. Star the repo to follow our roadmap and contribute to the Well-Architected standard.</p>
              <div className="community-actions">
                <a href="https://github.com/enriquekalven/agent-cockpit" target="_blank" className="btn-github">
                  <Github size={20} />
                  Star on GitHub
                </a>
                <div className="star-count-badge">
                  <span className="count">{stars ? `${(stars / 1000).toFixed(1)}K` : '9.8K'}</span>
                  <span>Stars reached</span>
                </div>
              </div>
            </div>
            <div className="community-right">
              <div className="contributor-grid">
                {[1, 2, 3, 4, 5, 6].map(i => (
                  <div key={i} className="contributor-avatar pulse-i"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="crew-footer">
        <div className="footer-content">
          <div className="nav-logo">
            <span className="agent-pulse mini"></span>
            <span>AgentOps Cockpit</span>
          </div>
          <div className="footer-links">
            <Link to="/docs">Documentation</Link>
            <Link to="/ops">Dashboard</Link>
            <a href="https://github.com/enriquekalven/agent-cockpit/blob/main/CHANGELOG.md">Changelog</a>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
          </div>
          <div className="footer-copyright">
            © 2026 Agentic Systems. Powered by Google Cloud & Gemini.
          </div>
        </div>
      </footer>

      <style>{`
        .crew-home {
          background-color: var(--bg-color);
          color: var(--text-primary);
          overflow-x: hidden;
          padding-top: 0;
        }

        .release-banner {
          background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 50%, #1e3a8a 100%);
          color: white;
          padding: 0.75rem 1rem;
          text-align: center;
          font-size: 0.85rem;
          font-weight: 600;
          position: relative;
          z-index: 200;
          border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .banner-content {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1rem;
          max-width: 1400px;
          margin: 0 auto;
        }

        .banner-tag {
          background: rgba(255, 255, 255, 0.2);
          padding: 0.2rem 0.6rem;
          border-radius: 999px;
          font-size: 0.7rem;
          font-weight: 800;
          letter-spacing: 0.05em;
        }

        .banner-link {
          color: white;
          text-decoration: underline;
          display: inline-flex;
          align-items: center;
          gap: 0.25rem;
          font-weight: 700;
          transition: opacity 0.2s;
        }

        .banner-link:hover { opacity: 0.8; }

        @media (max-width: 768px) {
          .banner-text { display: none; }
          .banner-content { gap: 0.5rem; }
        }

        /* Hero Styling */
        .crew-hero {
          position: relative;
          padding-top: 2rem;
          min-height: 90vh;
          display: flex;
          flex-direction: column;
        }

        .crew-home-nav {
          max-width: 1400px;
          margin: 0 auto;
          width: 100%;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 2rem;
          z-index: 100;
        }

        .nav-logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          font-size: 1.15rem;
          letter-spacing: -0.02em;
          color: var(--text-primary);
        }

        .nav-mascot {
          width: 32px;
          height: 32px;
          border-radius: 8px;
          object-fit: cover;
          border: 1px solid var(--border-color);
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .nav-links {
          display: flex;
          align-items: center;
          gap: 2rem;
        }

        .nav-link {
          text-decoration: none;
          color: var(--text-secondary);
          font-weight: 600;
          font-size: 0.95rem;
          transition: color 0.2s;
        }

        .nav-link:hover { color: var(--text-primary); }

        .nav-icon-link {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          text-decoration: none;
          color: var(--text-secondary);
          transition: color 0.2s;
        }

        .nav-icon-link:hover {
          color: var(--text-primary);
        }

        .nav-star-count {
          font-size: 0.75rem;
          font-weight: 700;
          background: rgba(var(--text-primary-rgb), 0.05);
          padding: 0.1rem 0.4rem;
          border-radius: 4px;
          border: 1px solid var(--border-color);
        }

        .nav-cta-btn {
          background: var(--text-primary);
          color: var(--bg-color);
          padding: 0.6rem 1.25rem;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 700;
          font-size: 0.9rem;
          transition: transform 0.2s;
        }

        .nav-cta-btn:hover { transform: translateY(-2px); }

        .hero-main {
          max-width: 1400px;
          margin: 0 auto;
          padding: 6rem 2rem;
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 4rem;
          align-items: center;
          flex: 1;
        }

        .pill-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.75rem;
          background: rgba(var(--primary-color-rgb), 0.1);
          color: var(--primary-color);
          padding: 0.5rem 1rem;
          border-radius: 999px;
          font-size: 0.8rem;
          font-weight: 800;
          margin-bottom: 2rem;
          border: 1px solid rgba(var(--primary-color-rgb), 0.2);
        }

        .pulsing-dot {
          width: 8px;
          height: 8px;
          background: var(--primary-color);
          border-radius: 50%;
          animation: pulse-ring-glow 2s infinite;
        }

        @keyframes pulse-ring-glow {
          0% { box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0.4); }
          70% { box-shadow: 0 0 0 10px rgba(var(--primary-color-rgb), 0); }
          100% { box-shadow: 0 0 0 0 rgba(var(--primary-color-rgb), 0); }
        }

        .hero-headline {
          font-size: clamp(2.5rem, 8vw, 4.5rem);
          line-height: 1;
          font-weight: 900;
          letter-spacing: -0.04em;
          margin-bottom: 2rem;
        }

        .gradient-text {
          background: linear-gradient(135deg, #3b82f6 0%, #10b981 100%);
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .hero-description {
          font-size: clamp(1rem, 2.5vw, 1.4rem);
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 3rem;
          max-width: 600px;
        }

        .hero-actions {
          display: flex;
          gap: 1.5rem;
          margin-bottom: 4rem;
        }

        .btn-primary {
          background: var(--primary-color);
          color: white;
          padding: 1rem 2rem;
          border-radius: 12px;
          text-decoration: none;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          box-shadow: 0 10px 20px rgba(var(--primary-color-rgb), 0.2);
          transition: all 0.2s;
        }

        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 15px 30px rgba(var(--primary-color-rgb), 0.3);
        }

        .btn-secondary {
          background: transparent;
          border: 1px solid var(--border-color);
          color: var(--text-primary);
          padding: 1rem 2rem;
          border-radius: 12px;
          text-decoration: none;
          font-weight: 700;
          transition: background 0.2s;
        }

        .btn-secondary:hover { background: rgba(var(--text-primary-rgb), 0.05); }

        .hero-features-preview {
          display: flex;
          gap: 2rem;
          font-size: 0.9rem;
          font-weight: 700;
          color: var(--text-secondary);
        }

        .preview-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        /* Hero Visual */
        .hero-visual-v2 {
          position: relative;
          z-index: 1;
          display: flex;
          justify-content: flex-end;
        }

        .visual-container {
          position: relative;
          perspective: 1000px;
          display: flex;
          justify-content: flex-end;
          min-height: 400px;
          width: 100%;
        }

        .visual-background-glow {
          position: absolute;
          top: 0;
          right: -10%;
          width: 120%;
          height: 120%;
          background: radial-gradient(circle, rgba(var(--primary-color-rgb), 0.1) 0%, transparent 70%);
          z-index: -1;
        }

        .mock-terminal {
          background: #0D0D0D;
          border-radius: 12px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          box-shadow: 0 30px 60px rgba(0,0,0,0.3);
          overflow: hidden;
          width: 100%;
          max-width: 500px;
          transform: rotateX(5deg) rotateY(-8deg); /* Slightly steeper for better perspective */
        }

        .terminal-header {
          background: #151515;
          padding: 0.75rem 1rem;
          display: flex;
          align-items: center;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .dots { display: flex; gap: 6px; }
        .dots span { width: 10px; height: 10px; border-radius: 50%; }
        .dots span:nth-child(1) { background: #ff5f56; }
        .dots span:nth-child(2) { background: #ffbd2e; }
        .dots span:nth-child(3) { background: #27c93f; }

        .terminal-title {
          flex: 1;
          text-align: center;
          font-size: 0.75rem;
          font-family: var(--font-mono);
          color: #71717A;
        }

        .terminal-body {
          padding: 1.5rem;
          font-family: var(--font-mono);
          font-size: 0.85rem;
          line-height: 1.6;
        }

        .terminal-cmd { color: #a5b4fc; }
        .blink { animation: blink 1s step-end infinite; }
        @keyframes blink { 50% { opacity: 0; } }

        .floating-stat {
          position: absolute;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          padding: 0.75rem 1.25rem;
          border-radius: 12px;
          box-shadow: 0 10px 20px rgba(0,0,0,0.1);
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          font-size: 0.85rem;
          z-index: 2;
        }

        .stat-1 { top: -20px; right: 20px; animation: float-v2 5s infinite ease-in-out; }
        .stat-2 { bottom: 20px; left: 10%; animation: float-v2 5s infinite ease-in-out 1s; } /* Moved left slightly */
        .green-vibrant { border-color: rgba(34, 197, 94, 0.4); color: #22c55e; box-shadow: 0 10px 30px rgba(34, 197, 94, 0.2); }
        .purple-vibrant { border-color: rgba(168, 85, 247, 0.4); color: #a855f7; box-shadow: 0 10px 30px rgba(168, 85, 247, 0.2); }

        .mock-cockpit-preview {
          background: rgba(13, 13, 13, 0.8);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 16px;
          padding: 1.5rem;
          width: 280px; 
          position: absolute;
          top: 220px; /* Moved lower to clear the prompt area */
          left: -120px; /* Shifted further left for balance */
          z-index: 10;
          backdrop-filter: blur(20px);
          transform: rotateX(10deg) rotateY(10deg);
          box-shadow: 0 40px 80px rgba(0,0,0,0.5);
        }

        .floating-stat.stat-2 {
          bottom: -20px;
          left: 15%;
          animation: float-v2 5s infinite ease-in-out 1s;
        }
        .cockpit-header { display: flex; align-items: center; gap: 0.75rem; font-size: 0.7rem; font-weight: 800; opacity: 0.6; margin-bottom: 1.5rem; letter-spacing: 0.1em; }
        .cockpit-stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }
        .c-stat { display: flex; flex-direction: column; gap: 0.25rem; }
        .c-label { font-size: 0.6rem; font-weight: 800; opacity: 0.4; text-transform: uppercase; }
        .c-value { font-size: 1.5rem; font-weight: 900; }
        .cockpit-graph { display: flex; align-items: flex-end; gap: 4px; height: 40px; }
        .bar { flex: 1; background: rgba(255, 255, 255, 0.1); border-radius: 2px; }
        .bar.active { background: var(--primary-color); box-shadow: 0 0 15px var(--primary-color); }

        @keyframes float-v2 {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-10px); }
        }

        /* Philosophy Section */
        .crew-philosophy {
          padding: 10rem 2rem;
          background: rgba(var(--primary-color-rgb), 0.02);
          border-top: 1px solid var(--border-color);
        }

        .container {
          max-width: 1200px;
          margin: 0 auto;
        }

        .philosophy-header {
          text-align: center;
          max-width: 700px;
          margin: 0 auto 5rem;
        }

        .philosophy-header h2 {
          font-size: 3rem;
          font-weight: 850;
          letter-spacing: -0.04em;
          margin-bottom: 1rem;
        }

        .text-primary { color: var(--primary-color); }

        .trinity-grid-v2 {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 2rem;
        }

        .trinity-card {
          background: var(--bg-color);
          border: 1px solid var(--border-color);
          padding: 3rem 2rem;
          border-radius: 20px;
          transition: all 0.3s;
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          text-align: left;
        }

        .trinity-card.active {
          border-color: var(--primary-color);
          background: rgba(var(--primary-color-rgb), 0.02);
          box-shadow: 0 20px 40px rgba(0,0,0,0.05);
          transform: translateY(-8px);
        }

        .card-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 2rem;
        }

        .card-icon.blue { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
        .card-icon.green { background: rgba(16, 185, 129, 0.1); color: #10b981; }
        .card-icon.purple { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }

        .trinity-card h3 {
          font-size: 1.5rem;
          font-weight: 800;
          margin-bottom: 1rem;
        }

        .trinity-card p {
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 2rem;
          flex: 1;
        }

        .card-link {
          font-weight: 800;
          text-decoration: none;
          color: var(--text-primary);
          font-size: 0.9rem;
          transition: color 0.2s;
        }
        .card-link:hover { color: var(--primary-color); }

        /* Features Section */
        .crew-features { padding: 10rem 2rem; }

        .features-header { margin-bottom: 5rem; }
        .accent-label {
          text-transform: uppercase;
          color: var(--primary-color);
          font-weight: 800;
          font-size: 0.75rem;
          letter-spacing: 0.15em;
          margin-bottom: 1rem;
          display: block;
        }

        .features-header h2 {
          font-size: 3.5rem;
          font-weight: 900;
          letter-spacing: -0.04em;
        }

        .capabilities-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 4rem;
        }

        .capability-item {
          display: flex;
          gap: 2rem;
          align-items: flex-start;
        }

        .item-icon {
          background: var(--bg-secondary);
          color: var(--text-primary);
          padding: 1rem;
          border-radius: 12px;
          border: 1px solid var(--border-color);
        }

        .capability-item h4 {
          font-size: 1.25rem;
          font-weight: 800;
          margin-bottom: 0.75rem;
        }

        .capability-item p {
          color: var(--text-secondary);
          line-height: 1.6;
        }

        /* CTA Box */
        .crew-cta-section { padding: 5rem 2rem 10rem; }
        .cta-box {
          background: #0D0D0D;
          border-radius: 32px;
          padding: 5rem;
          text-align: center;
          color: white;
          max-width: 1000px;
          margin: 0 auto;
          position: relative;
          overflow: hidden;
        }

        .cta-box h2 { font-size: 3rem; font-weight: 900; margin-bottom: 1.5rem; }
        .cta-box p { font-size: 1.25rem; opacity: 0.7; margin-bottom: 3rem; }
        .cta-btns { display: flex; gap: 1rem; justify-content: center; }

        /* Community Section */
        .crew-community { padding: 5rem 2rem; }
        .community-card {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 32px;
          padding: 4rem;
          display: grid;
          grid-template-columns: 1.2fr 0.8fr;
          gap: 4rem;
          align-items: center;
        }

        .community-left h2 { font-size: 3.5rem; font-weight: 900; margin-bottom: 1.5rem; letter-spacing: -0.04em; }
        .community-left p { font-size: 1.25rem; color: var(--text-secondary); line-height: 1.6; margin-bottom: 3rem; }

        .community-actions { display: flex; align-items: center; gap: 2rem; }
        
        .btn-github {
          background: #24292e;
          color: white;
          padding: 1rem 2rem;
          border-radius: 12px;
          text-decoration: none;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          transition: transform 0.2s;
        }
        .btn-github:hover { transform: translateY(-2px); }

        .star-count-badge {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
        }
        .star-count-badge .count { font-size: 1.5rem; font-weight: 900; color: var(--text-primary); }
        .star-count-badge span:last-child { font-size: 0.8rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase; }

        .contributor-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1.5rem;
        }
        .contributor-avatar {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background: var(--border-color);
          opacity: 0.3;
        }
        .pulse-i { animation: pulse-avatar 2s infinite ease-in-out; }
        @keyframes pulse-avatar { 0%, 100% { opacity: 0.2; } 50% { opacity: 0.4; transform: scale(1.05); } }

        @media (max-width: 1024px) {
          .community-card { grid-template-columns: 1fr; text-align: center; }
          .community-actions { justify-content: center; }
          .contributor-grid { justify-content: center; display: none; }
        }

        /* Footer */
        .crew-footer {
          padding: 5rem 2rem;
          border-top: 1px solid var(--border-color);
        }

        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 2rem;
        }

        .footer-links { display: flex; gap: 3rem; }
        .footer-links a {
          text-decoration: none;
          color: var(--text-secondary);
          font-weight: 600;
          font-size: 0.9rem;
        }

        .footer-copyright {
          font-size: 0.85rem;
          color: var(--text-secondary);
          font-weight: 500;
        }

        @media (max-width: 1024px) {
          .hero-main { grid-template-columns: 1fr; text-align: center; }
          .hero-actions, .hero-features-preview { justify-content: center; }
          .hero-visual-v2 { display: none; }
          .trinity-grid-v2 { grid-template-columns: 1fr; }
        }

        /* Frameworks Bar Styling */
        .frameworks-bar {
          padding: 4rem 1.5rem;
          border-bottom: 1px solid var(--border-color);
          background: rgba(var(--bg-secondary-rgb), 0.3);
          position: relative;
          z-index: 10;
        }
        .frameworks-label {
          text-align: center;
          font-size: 0.75rem;
          font-weight: 850;
          text-transform: uppercase;
          letter-spacing: 0.2em;
          color: var(--text-secondary);
          margin-bottom: 2.5rem;
          opacity: 0.7;
        }
        .frameworks-grid {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
          gap: 1.25rem;
          max-width: 1100px;
          margin: 0 auto;
          padding: 0 2rem;
        }
        .framework-badge {
          padding: 0.6rem 1.5rem;
          border-radius: 12px;
          font-size: 0.85rem;
          font-weight: 800;
          border: 1px solid var(--border-color);
          background: var(--bg-color);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          cursor: default;
          box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .framework-badge:hover {
          transform: translateY(-4px);
          border-color: var(--primary-color);
          box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .framework-badge.copilot { border-bottom: 3px solid #6366f1; }
        .framework-badge.crew { border-bottom: 3px solid #ff4b4b; }
        .framework-badge.langgraph { border-bottom: 3px solid #2c3e50; }
        .framework-badge.llamaindex { border-bottom: 3px solid #00d1b2; }
        .framework-badge.openai { border-bottom: 3px solid #412991; }
        .framework-badge.langchain { border-bottom: 3px solid #1C3C3C; }
         .framework-badge.autogen { border-bottom: 3px solid #0078d4; }
        .framework-badge.adk { border-bottom: 3px solid #4285F4; }
        .framework-badge.python { border-bottom: 3px solid #3776ab; }
        .framework-badge.go { border-bottom: 3px solid #00add8; }
        .framework-badge.nodejs { border-bottom: 3px solid #339933; }
        .framework-badge.typescript { border-bottom: 3px solid #3178c6; }
        .framework-badge.angular { border-bottom: 3px solid #dd0031; }
        .framework-badge.streamlit { border-bottom: 3px solid #ff4b4b; }
        .framework-badge.lit { border-bottom: 3px solid #324fff; }
        .framework-badge.cloudrun { border-bottom: 3px solid #4285f4; }
        .framework-badge.gke { border-bottom: 3px solid #326ce5; }
        .framework-badge.agentengine { border-bottom: 3px solid #34a853; }

        .framework-section { margin-bottom: 3rem; }
        .mt-12 { margin-top: 3rem; }

        /* Expanded Visual Styles */
        .glass-trinity {
          border: 1px solid rgba(var(--primary-color-rgb), 0.2);
          background: radial-gradient(circle at 100% 0%, rgba(var(--primary-color-rgb), 0.05) 0%, transparent 50%);
        }
        .bg-trinity { background: linear-gradient(to bottom, transparent, rgba(var(--primary-color-rgb), 0.02)); }
        .shadow-vibrant { box-shadow: 0 40px 80px rgba(var(--primary-color-rgb), 0.15); }
        
        .bg-dark-flow {
          background: #050505;
          padding: 10rem 2rem;
          border-radius: 40px;
          margin: 0 2rem;
          color: white;
        }
        .text-white { color: white !important; }
        .workflow-visual-container {
          margin-top: 4rem;
          position: relative;
          text-align: center;
        }
        .workflow-img {
          width: 100%;
          max-width: 1100px;
          border-radius: 20px;
        }
        .workflow-overlay-text {
          margin-top: 2rem;
          font-size: 1.1rem;
          color: #A1A1AA;
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
          line-height: 1.6;
        }

      `}</style>
    </div>
  );
}
