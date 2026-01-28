import React from 'react';
import { Link } from 'react-router-dom';
import { ThemeToggle } from './ThemeToggle';

export function Home() {
  return (
    <div className="home-container">
      <header className="home-header">
        <div className="logo-section">
          <span className="agent-pulse"></span>
          <span className="logo-text">Optimized Agent Stack</span>
        </div>
        <nav className="home-nav">
          <Link to="/docs" className="nav-item">How it Works</Link>
          <Link to="/docs/getting-started" className="nav-item">Documentation</Link>

          <ThemeToggle />
          <Link to="/docs/getting-started" className="nav-cta">Get Started</Link>
        </nav>
      </header>

      <main className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <span className="badge-dot"></span>
            v1.0.0 Now Available
          </div>
          <h1 className="hero-title">
            The <span className="highlight-text">Optimized</span> Agent Stack.
          </h1>
          <p className="hero-subtitle">
            Google Cloud gives you the infrastructure. We give you the <strong>Intelligence</strong>. The professional distribution for App Developers building on Gemini.
          </p>
          <div className="cta-group">
            <Link to="/docs/getting-started" className="cta-button primary">
              Start Building
            </Link>

          </div>
          <div className="hero-meta">
            <p>Powering the next generation of <strong>Agentic Apps</strong>.</p>
            <div className="hero-logos">
              <span className="logo-pill">Open Source</span>
              <span className="logo-pill">Type Safe</span>
              <span className="logo-pill">GenUI Ready</span>
            </div>
          </div>
        </div>

        <div className="hero-visual-container">
          <div className="hero-visual-glow"></div>
          <div className="hero-card main-card">
            <div className="card-browser-bar">
              <div className="browser-dot"></div>
              <div className="browser-dot"></div>
              <div className="browser-dot"></div>
            </div>
            <div className="card-code-content">
              <pre>
                <code>{`{
  "surfaceId": "agent-response",
  "content": [
    {
      "type": "Card",
      "props": { "title": "AI Action" },
      "children": [
        { "type": "Text", "props": { "text": "Deploying..." } }
      ]
    }
  ]
}`}</code>
              </pre>
            </div>
          </div>
          <div className="hero-card overlay-card">
            <div className="stat-label">Response Time</div>
            <div className="stat-value">14ms</div>
            <div className="stat-progress">
              <div className="progress-fill"></div>
            </div>
          </div>
        </div>
      </main>

      <section className="ecosystem-section">
        <div className="section-header">
          <h2 className="section-title">The <span className="gradient-text">Agentic Stack</span></h2>
          <p className="section-subtitle">A2UI is the critical missing layer between LLM reasoning and structured human interaction.</p>
        </div>

        <div className="ecosystem-grid">
          <div className="ecosystem-card full-width">
            <div className="glass-content story-mode">
              <div className="text-side">
                <div className="accent-label">The Strategy</div>
                <h3>Infrastructure vs. Intelligence</h3>
                <p>Google Cloud Official Pack gives you the pipes. We give you the High-Speed state sync and Cost Control your application needs.</p>

                <div className="comparison-table-mini">
                  <div className="table-row table-header-row">
                    <span className="col-1">Feature</span>
                    <span className="col-2">GCP Official</span>
                    <span className="col-3 highlight">Optimized Stack</span>
                  </div>
                  <div className="table-row">
                    <span className="col-1">Frontend Layer</span>
                    <span className="col-2">Generic / None</span>
                    <span className="col-3 highlight">A2UI + State Sync</span>
                  </div>
                  <div className="table-row">
                    <span className="col-1">Cost Control</span>
                    <span className="col-2">"Dumb Pipes"</span>
                    <span className="col-3 highlight">Semantic Cache</span>
                  </div>
                  <div className="table-row">
                    <span className="col-1">Security Audit</span>
                    <span className="col-2">IAM/VPCs</span>
                    <span className="col-3 highlight">Red Team CI/CD</span>
                  </div>
                  <div className="table-row">
                    <span className="col-1">Optimization</span>
                    <span className="col-2">Manual</span>
                    <span className="col-3 highlight">Interactive Linter</span>
                  </div>
                </div>
              </div>

              <div className="visual-side trinity-diagram-container">
                <div className="trinity-visual">
                  <div className="trinity-center-logo">
                    <span className="agent-pulse large"></span>
                  </div>
                  <div className="trinity-node core">
                    <div className="node-icon">⚙️</div>
                    <span>Intelligence</span>
                  </div>
                  <div className="trinity-node ui">
                    <div className="node-icon">🎭</div>
                    <span>Presentation</span>
                  </div>
                  <div className="trinity-node ops active-node">
                    <div className="node-icon">🕹️</div>
                    <span>Operations</span>
                  </div>

                  <svg className="trinity-lines" viewBox="0 0 300 300">
                    <line x1="150" y1="60" x2="60" y2="220" stroke="var(--border-color)" strokeWidth="2" strokeDasharray="4 4" />
                    <line x1="60" y1="220" x2="240" y2="220" stroke="var(--border-color)" strokeWidth="2" strokeDasharray="4 4" />
                    <line x1="240" y1="220" x2="150" y2="60" stroke="var(--primary-color)" strokeWidth="3" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

          <div className="ecosystem-card reverse full-width">
            <div className="glass-content">
              <div className="visual-side">
                <img src="/diagrams/value-proposition.png" alt="A2UI Value Proposition" className="ecosystem-img" />
              </div>
              <div className="text-side">
                <div className="accent-label">Value Proposition</div>
                <h3>From Text to Interface</h3>
                <p>Stop forcing your users to read walls of text. Move from chat-only outputs to full-fledged application surfaces that change based on what the agent is doing.</p>
                <div className="value-stats">
                  <div className="value-stat">
                    <h4>85%</h4>
                    <p>Faster Time-to-UI</p>
                  </div>
                  <div className="value-stat">
                    <h4>100%</h4>
                    <p>Standardized Schema</p>
                  </div>
                  <div className="value-stat">
                    <h4>v1.0</h4>
                    <p>Google Open Standard</p>
                  </div>
                </div>
              </div>
            </div>
        </div>
      </section>

      <section className="comparison-section">
        <div className="section-header">
          <h2 className="section-title">The <span className="gradient-text">Agentic Ecosystem</span></h2>
          <p className="section-subtitle">Clarifying the roles of modern AI interface standards and frameworks.</p>
        </div>

        <div className="comparison-grid">
          <div className="comparison-card">
            <div className="card-tag purple">FRAMEWORK</div>
            <h3>CopilotKit</h3>
            <p><strong>The Foundation.</strong> The open-source core for building AI copilots. It handles the backend logic, LLM streaming, and core state synchronization.</p>
            <div className="card-value">Role: <strong>Infrastructure</strong></div>
          </div>

          <div className="comparison-card">
            <div className="card-tag blue">SPECIFICATION</div>
            <h3>A2UI</h3>
            <p><strong>The Blueprint.</strong> A Google-originated declarative JSON schema. It defines UI components so agents can describe interfaces without writing code.</p>
            <div className="card-value">Role: <strong>Schema</strong></div>
          </div>

          <div className="comparison-card">
            <div className="card-tag teal">PROTOCOL</div>
            <h3>AG-UI</h3>
            <p><strong>The Protocol.</strong> The communication standard for Agent-User Interaction. It ensures agents and UIs speak the same language for human-in-the-loop flows.</p>
            <div className="card-value">Role: <strong>Communication</strong></div>
          </div>

          <div className="comparison-card highlight">
            <div className="card-tag black">YOU ARE HERE</div>
            <h3>AgentOps Starter Pack</h3>
            <p><strong>The Cockpit.</strong> The 1-click deployment for Day 2 Operations. It manages Shadow Mode traffic, Hive Mind Caching, and Security Audits for your agents.</p>
            <div className="card-value">Role: <strong>Control & Governance</strong></div>
          </div>
        </div>

        <div className="value-prop-banner">
          <div className="banner-content">
            <h3>Unified Value Proposition</h3>
            <div className="banner-grid">
              <div className="banner-item">
                <span className="item-number">01</span>
                <h4>Zero-Code UI</h4>
                <p>Agents generate full interfaces instantly via JSON, bypassing traditional frontend development cycles.</p>
              </div>
              <div className="banner-item">
                <span className="item-number">02</span>
                <h4>Cross-Platform</h4>
                <p>One schema works everywhere. Native support for React, with standard bridges for Mobile and Web Components.</p>
              </div>
              <div className="banner-item">
                <span className="item-number">03</span>
                <h4>Agent Logic First</h4>
                <p>Focus on your agent's reasoning. Let the A2UI renderer handle the complex visual manifestation.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="features-section">
        <div className="section-header">
          <h2 className="section-title">Built for <span className="gradient-text">Production Agent Ops</span></h2>
          <p className="section-subtitle">A2UI provides the infrastructure for high-scale, cost-effective agent deployments.</p>
        </div>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon-wrapper blue">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
            </div>
            <h3>Cost Guardrails</h3>
            <p>Built-in budget monitoring and smart token auditing to prevent expensive LLM runaways.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper purple">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
            </div>
            <h3>The Optimizer</h3>
            <p>Automatically compress prompts and identify Context Caching opportunities in your CI/CD pipeline.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper teal">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" /></svg>
            </div>
            <h3>Cloud Run Native</h3>
            <p>Vercel-style deployment for GCP. Serverless architecture that scales to zero when not in use.</p>
          </div>
        </div>
      </section>

      <footer className="home-footer">
        <div className="footer-content">
          <div className="footer-logo">
            <span className="agent-pulse"></span>
            <span>Optimized Agent Stack</span>
          </div>
          <p>© 2026 Agentic Systems Inc. All rights reserved.</p>
        </div>
      </footer>

      <style>{`
        /* Story Mode & Pillar Timeline */
        .glass-content.story-mode {
          display: flex;
          gap: 3rem;
          padding: 4rem;
        }
        .pillar-timeline {
          margin-top: 2rem;
          display: flex;
          flex-direction: column;
          gap: 2rem;
          position: relative;
        }
        .pillar-timeline::before {
          content: '';
          position: absolute;
          left: 7px;
          top: 10px;
          bottom: 10px;
          width: 2px;
          background: var(--border-color);
        }
        .pillar {
          display: flex;
          gap: 1.5rem;
          position: relative;
        }
        .pillar-dot {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: var(--surface-color);
          border: 2px solid var(--border-color);
          z-index: 2;
          margin-top: 4px;
        }
        .pillar-dot.highlighted {
          border-color: var(--primary-color);
          background: var(--primary-color);
          box-shadow: 0 0 15px var(--primary-color);
        }
        .pillar-info strong {
          display: block;
          font-size: 1rem;
          margin-bottom: 0.25rem;
        }
        .pillar-info span {
          font-size: 0.75rem;
          color: var(--primary-color);
          font-weight: 700;
          text-transform: uppercase;
        }
        .pillar-info p {
          font-size: 0.85rem;
          opacity: 0.7;
          margin-top: 0.5rem;
        }
        .pillar.active .pillar-info strong {
          color: var(--primary-color);
        }

        .platform-tag {
          font-size: 0.6rem;
          background: var(--border-color);
          padding: 0.2rem 0.5rem;
          border-radius: 4px;
          font-weight: 800;
          opacity: 0.6;
        }
        .platform-tag.active {
          background: rgba(var(--primary-color-rgb), 0.1);
          color: var(--primary-color);
          opacity: 1;
        }

        /* Trinity Visual */
        .visual-side.trinity-diagram-container {
          display: flex;
          align-items: center;
          justify-content: center;
          perspective: 1000px;
        }
        .trinity-visual {
          position: relative;
          width: 300px;
          height: 300px;
        }
        .trinity-center-logo {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          z-index: 1;
        }
        .agent-pulse.large {
          width: 50px;
          height: 50px;
          background: var(--primary-color);
        }
        .trinity-node {
          position: absolute;
          padding: 0.75rem 1rem;
          background: var(--surface-color);
          border: 1px solid var(--border-color);
          border-radius: 1rem;
          font-weight: 800;
          font-size: 0.8rem;
          z-index: 3;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.5rem;
          box-shadow: 0 10px 20px rgba(0,0,0,0.05);
          transition: all 0.3s ease;
        }
        .node-icon { font-size: 1.25rem; }
        .trinity-node.core { top: 0; left: 50%; transform: translateX(-50%); }
        .trinity-node.ui { bottom: 0; left: 0; }
        .trinity-node.ops { bottom: 0; right: 0; }
        .trinity-node.active-node {
          border-color: var(--primary-color);
          background: var(--bg-color);
          box-shadow: 0 15px 35px rgba(var(--primary-color-rgb), 0.2);
          transform: scale(1.1) translateY(-10px);
        }
        .trinity-node.ops.active-node {
           bottom: 10px;
           right: -10px;
        }

        .trinity-lines {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 2;
        }

        /* Existing Styles */
        .trinity-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1.5rem;
          margin-top: 2.5rem;
        }
        .trinity-item {
          background: rgba(var(--bg-color-rgb), 0.3);
          border: 1px solid var(--border-color);
          padding: 1.5rem;
          border-radius: 1rem;
          transition: all 0.3s ease;
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
        }
        .trinity-item.active {
          border-color: var(--primary-color);
          background: rgba(var(--primary-color-rgb), 0.05);
          box-shadow: 0 10px 30px rgba(var(--primary-color-rgb), 0.1);
        }
        .trinity-icon {
          font-size: 2rem;
          margin-bottom: 1rem;
          width: 60px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--surface-color);
          border-radius: 1rem;
          border: 1px solid var(--border-color);
        }
        .trinity-item h4 {
          font-size: 1rem;
          font-weight: 800;
          margin: 0;
          line-height: 1.2;
        }
        .trinity-sub {
          font-size: 0.7rem;
          font-weight: 700;
          color: var(--primary-color);
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin-bottom: 0.75rem;
          display: block;
        }
        .trinity-item p {
          font-size: 0.8rem;
          color: var(--text-secondary);
          line-height: 1.4;
          margin: 0;
        }
        .trinity-item:hover {
          transform: translateY(-5px);
          border-color: var(--primary-color);
        }

        /* Comparison Table Styles */
        .comparison-table-mini {
          margin-top: 2rem;
          background: rgba(var(--bg-color-rgb), 0.2);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          overflow: hidden;
        }
        .table-row {
          display: grid;
          grid-template-columns: 1.2fr 1fr 1fr;
          padding: 0.75rem 1.25rem;
          border-bottom: 1px solid var(--border-color);
          font-size: 0.85rem;
          align-items: center;
        }
        .table-row:last-child { border-bottom: none; }
        .table-header-row {
          background: rgba(0,0,0,0.02);
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          font-size: 0.7rem;
        }
        .col-3.highlight {
          color: var(--primary-color);
          font-weight: 700;
        }

        .home-container {
          min-height: 100vh;
        }

        .home-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem 2.5rem;
          background: var(--surface-color);
          backdrop-filter: blur(20px);
          -webkit-backdrop-filter: blur(20px);
          position: sticky;
          top: 0;
          z-index: 100;
          border-bottom: 1px solid var(--border-color);
        }

        .logo-section {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          font-size: 1.1rem;
          letter-spacing: -0.02em;
        }

        .home-nav {
          display: flex;
          align-items: center;
          gap: 1.5rem;
        }

        .home-nav .nav-item {
          text-decoration: none;
          color: var(--text-secondary);
          font-weight: 600;
          font-size: 0.9rem;
          transition: color 0.2s;
        }

        .home-nav .nav-item:hover {
          color: var(--text-primary);
        }

        .nav-cta {
          padding: 0.5rem 1.25rem;
          background: var(--accent-color);
          color: var(--bg-color);
          border-radius: var(--radius-pill);
          text-decoration: none;
          font-size: 0.85rem;
          font-weight: 700;
          transition: transform 0.2s;
        }

        .nav-cta:hover {
          transform: scale(1.05);
        }

        .hero-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 4rem;
          padding: 8rem 4rem;
          max-width: 1400px;
          margin: 0 auto;
          align-items: center;
        }

        .hero-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.4rem 1rem;
          background: rgba(0, 0, 0, 0.05);
          border-radius: var(--radius-pill);
          font-size: 0.8rem;
          font-weight: 700;
          margin-bottom: 2rem;
          color: var(--text-secondary);
        }

        .badge-dot {
          width: 6px;
          height: 6px;
          background: #3b82f6;
          border-radius: 50%;
        }

        .hero-title {
          font-size: 4.5rem;
          font-weight: 800;
          line-height: 1.05;
          letter-spacing: -0.05em;
          margin-bottom: 1.5rem;
        }

        .highlight-text {
          background: linear-gradient(to right, #3b82f6, #8b5cf6, #10b981);
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
          font-size: 1.25rem;
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 3rem;
          max-width: 550px;
        }

        .cta-group {
          display: flex;
          gap: 1rem;
          margin-bottom: 4rem;
        }

        .cta-button {
          padding: 1rem 2rem;
          border-radius: var(--radius-pill);
          font-weight: 700;
          text-decoration: none;
          transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
          font-size: 1rem;
        }

        .cta-button.primary {
          background: var(--accent-color);
          color: var(--bg-color);
          box-shadow: 0 10px 30px var(--accent-glow);
        }

        .cta-button.primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 15px 40px var(--accent-glow);
        }

        .cta-button.secondary {
          background: var(--bg-secondary);
          color: var(--text-primary);
          border: 1px solid var(--border-color);
        }

        .cta-button.secondary:hover {
          background: var(--bg-color);
          transform: translateY(-2px);
        }

        .hero-meta {
          font-size: 0.85rem;
          color: var(--text-secondary);
          font-weight: 500;
        }

        .hero-logos {
          display: flex;
          gap: 1rem;
          margin-top: 1.5rem;
        }

        .logo-pill {
          padding: 0.3rem 0.75rem;
          background: rgba(0,0,0,0.03);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-pill);
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          font-weight: 800;
          color: var(--text-secondary);
        }

        .hero-visual-container {
          position: relative;
        }

        .hero-visual-glow {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          width: 500px;
          height: 500px;
          background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
          z-index: -1;
        }

        .hero-card {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-xl);
          box-shadow: 0 30px 60px rgba(0,0,0,0.1);
          overflow: hidden;
        }

        .main-card {
          width: 100%;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card-browser-bar {
          padding: 0.75rem 1.25rem;
          background: rgba(0,0,0,0.03);
          border-bottom: 1px solid var(--border-color);
          display: flex;
          gap: 6px;
        }

        .browser-dot {
          width: 10px;
          height: 10px;
          border-radius: 50%;
          background: var(--border-color);
        }

        .card-code-content {
          padding: 2rem;
          font-family: var(--font-mono);
          font-size: 0.85rem;
          color: #3b82f6;
          line-height: 1.5;
        }

        .overlay-card {
          position: absolute;
          bottom: -2rem;
          right: -1rem;
          width: 220px;
          padding: 1.5rem;
          background: var(--bg-secondary);
          z-index: 2;
          animation: float 6s infinite ease-in-out;
        }

        .stat-label { font-size: 0.75rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 0.5rem; }
        .stat-value { font-size: 1.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 1rem; }
        .stat-progress { height: 6px; background: rgba(0,0,0,0.05); border-radius: 3px; overflow: hidden; }
        .progress-fill { width: 70%; height: 100%; background: #10b981; }

        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-15px) translateX(-5px); }
        }

        .features-section {
          padding: 8rem 4rem;
          background: rgba(0,0,0,0.02);
          border-top: 1px solid var(--border-color);
        }

        .section-header {
          text-align: center;
          margin-bottom: 5rem;
        }

        .section-title {
          font-size: 3.5rem;
          font-weight: 800;
          letter-spacing: -0.04em;
          margin-bottom: 1rem;
        }

        .gradient-text {
          background: linear-gradient(to right, #3b82f6, #10b981);
          -webkit-background-clip: text;
          background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .section-subtitle {
          font-size: 1.25rem;
          color: var(--text-secondary);
          max-width: 700px;
          margin: 0 auto;
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 2.5rem;
          max-width: 1400px;
          margin: 0 auto;
        }

        .feature-card {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          padding: 3rem;
          border-radius: var(--radius-xl);
          transition: all 0.3s ease;
        }

        .feature-card:hover {
          transform: translateY(-10px);
          border-color: var(--text-primary);
        }

        .feature-icon-wrapper {
          width: 50px;
          height: 50px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 2rem;
        }

        .feature-icon-wrapper.blue { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
        .feature-icon-wrapper.purple { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
        .feature-icon-wrapper.teal { background: rgba(16, 185, 129, 0.1); color: #10b981; }

        .feature-card h3 {
          font-size: 1.5rem;
          font-weight: 800;
          margin-bottom: 1rem;
          letter-spacing: -0.02em;
        }

        .feature-card p {
          color: var(--text-secondary);
          line-height: 1.6;
        }

        .home-footer {
          padding: 4rem;
          border-top: 1px solid var(--border-color);
        }

        .footer-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          max-width: 1400px;
          margin: 0 auto;
        }

        .footer-logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          color: var(--text-primary);
        }

        .footer-content p {
          color: var(--text-secondary);
          font-size: 0.9rem;
        }

        .comparison-section {
          padding: 8rem 4rem;
          max-width: 1400px;
          margin: 0 auto;
        }

        .comparison-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 2rem;
          margin-top: 4rem;
        }

        .comparison-card {
          padding: 3rem;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-xl);
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
          transition: all 0.3s ease;
        }

        .comparison-card:hover {
          transform: translateY(-5px);
          border-color: var(--text-primary);
        }

        .comparison-card.highlight {
          background: var(--text-primary);
          color: var(--bg-color);
          border-color: var(--text-primary);
        }

        .comparison-card.highlight h3, 
        .comparison-card.highlight p,
        .comparison-card.highlight .card-value {
          color: #FAFAFA;
        }

        .card-tag {
          font-family: var(--font-mono);
          font-size: 10px;
          font-weight: 800;
          letter-spacing: 0.1em;
          padding: 0.25rem 0.75rem;
          border-radius: var(--radius-pill);
          display: inline-block;
          width: fit-content;
        }

        .card-tag.purple { background: rgba(139, 92, 246, 0.1); color: #8b5cf6; }
        .card-tag.blue { background: rgba(59, 130, 246, 0.1); color: #3b82f6; }
        .card-tag.teal { background: rgba(16, 185, 129, 0.1); color: #10b981; }
        .card-tag.black { background: rgba(255, 255, 255, 0.2); color: white; }

        .comparison-card h3 {
          font-size: 1.75rem;
          font-weight: 800;
          margin: 0;
        }

        .comparison-card p {
          font-size: 1rem;
          line-height: 1.6;
          color: var(--text-secondary);
          margin: 0;
        }

        .comparison-card strong {
          color: var(--text-primary);
        }

        .comparison-card.highlight strong {
          color: #FFFFFF;
        }

        .card-value {
          margin-top: auto;
          font-size: 0.85rem;
          font-weight: 600;
          color: var(--text-primary);
        }

        .value-prop-banner {
          margin-top: 6rem;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: var(--radius-xl);
          padding: 6rem 4rem;
          position: relative;
          overflow: hidden;
        }

        .value-prop-banner::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: linear-gradient(to right, #3b82f6, #8b5cf6, #10b981);
        }

        .banner-content h3 {
          font-size: 2.5rem;
          font-weight: 800;
          text-align: center;
          margin-bottom: 4rem;
          letter-spacing: -0.04em;
        }

        .banner-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 4rem;
        }

        .banner-item {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .item-number {
          font-family: var(--font-mono);
          font-size: 0.85rem;
          font-weight: 800;
          color: #3b82f6;
          opacity: 0.5;
        }

        .banner-item h4 {
          font-size: 1.5rem;
          font-weight: 800;
          margin: 0;
        }

        .banner-item p {
          font-size: 1rem;
          line-height: 1.6;
          color: var(--text-secondary);
          margin: 0;
        }

        @media (max-width: 1024px) {
          .banner-grid { grid-template-columns: 1fr; gap: 3rem; }
          .value-prop-banner { padding: 4rem 2rem; }
          .banner-content h3 { font-size: 2rem; }
          .hero-section { grid-template-columns: 1fr; text-align: center; }
          .hero-subtitle { margin: 0 auto 3rem; }
          .cta-group { justify-content: center; }
          .hero-visual-container { display: none; }
          .features-grid { grid-template-columns: 1fr; }
          .comparison-grid { grid-template-columns: 1fr; }
          .hero-title { font-size: 3.5rem; }
        }

        [data-theme="dark"] .hero-badge { background: rgba(255, 255, 255, 0.05); }
        [data-theme="dark"] .logo-pill { background: rgba(255, 255, 255, 0.03); }
        [data-theme="dark"] .hero-visual-glow { 
          background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%); 
        }
        [data-theme="dark"] .comparison-card.highlight h3, 
        [data-theme="dark"] .comparison-card.highlight p,
        [data-theme="dark"] .comparison-card.highlight .card-value {
          color: #0A0A0A;
        }
        [data-theme="dark"] .comparison-card.highlight strong {
          color: #000000;
        }
      `}</style>
    </div>
  );
}
