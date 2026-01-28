import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Rocket, Shield, Activity, Cpu, Command,
  Terminal, ChevronRight, Github, ExternalLink,
  Layers, Zap, Search, Globe, Lock
} from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';

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
      {/* Hero Section */}
      <section className="crew-hero">
        <header className="crew-home-nav">
          <div className="nav-logo">
            <span className="agent-pulse"></span>
            <span>AgentOps Cockpit</span>
          </div>
          <nav className="nav-links">
            <Link to="/docs" className="nav-link">Documentation</Link>
            <Link to="/docs/google-architecture" className="nav-link">Framework</Link>
            <a href="https://github.com/enriquekalven/agent-cockpit" className="nav-icon-link">
              <Github size={20} />
            </a>
            <ThemeToggle />
            <Link to="/ops" className="nav-cta-btn">Launch Dashboard</Link>
          </nav>
        </header>

        <div className="hero-main">
          <div className="hero-content-v2">
            <div className="pill-badge">
              <span className="pulsing-dot"></span>
              Google Well-Architected Framework for Agents
            </div>
            <h1 className="hero-headline">
              The Professional Logic Layer for <span className="gradient-text">Agentic Apps</span>
            </h1>
            <p className="hero-description">
              Move beyond basic prompt engineering. The AgentOps Cockpit is a high-performance distribution for managing, optimizing, and securing AI agents on Google Cloud.
            </p>
            <div className="hero-actions">
              <Link to="/docs/getting-started" className="btn-primary">
                Get Started Free
                <ChevronRight size={18} />
              </Link>
              <Link to="/docs/google-architecture" className="btn-secondary">
                Explore the Framework
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
              <div className="mock-terminal">
                <div className="terminal-header">
                  <div className="dots"><span></span><span></span><span></span></div>
                  <div className="terminal-title">agent-ops --audit</div>
                </div>
                <div className="terminal-body">
                  <div className="line terminal-cmd">$ uvx agent-ops-cockpit arch-review</div>
                  <div className="line text-blue-400">🏛️ Launching Architecture Design Review...</div>
                  <div className="line text-gray-500">[1/4] Checking Core Architecture... [OK]</div>
                  <div className="line text-gray-500">[2/4] Verifying Privacy Middleware... [PII_SCRUBBER_ACTIVE]</div>
                  <div className="line text-gray-500">[3/4] Auditing Token Optimization... [40%_SAVINGS_FOUND]</div>
                  <div className="line text-green-400">✅ Architecture aligned with Google Well-Architected Framework.</div>
                  <div className="line blink">_</div>
                </div>
              </div>
              <div className="floating-stat stat-1">
                <Zap size={16} />
                <span>40% Cost Savings</span>
              </div>
              <div className="floating-stat stat-2">
                <Shield size={16} />
                <span>100% Secure</span>
              </div>
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
              <Link to="/ops" className="card-link">Launch the Cockpit →</Link>
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
              <div className="item-icon"><Lock size={24} /></div>
              <div>
                <h4>Compliance-First</h4>
                <p>PII Scrubbing and Evidence Packing come standard to ensure enterprise-grade data handling.</p>
              </div>
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
          gap: 1rem;
          font-weight: 800;
          font-size: 1.25rem;
          letter-spacing: -0.02em;
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
          grid-template-columns: 1.2fr 0.8fr;
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
          font-size: 4.5rem;
          line-height: 1.1;
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
          font-size: 1.4rem;
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
        }

        .visual-container {
          position: relative;
          perspective: 1000px;
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
          width: 500px;
          transform: rotateX(5deg) rotateY(-5deg);
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
        .stat-2 { bottom: 20px; left: -20px; animation: float-v2 5s infinite ease-in-out 1s; }

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
          padding: 4rem 0;
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

      `}</style>
    </div>
  );
}
