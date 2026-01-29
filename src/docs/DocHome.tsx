import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Shield, Zap, Activity, Users,
  Terminal, Cpu, Layout, Rocket,
  Search, ShieldCheck, Lock, Command, BookOpen
} from 'lucide-react';

const FEATURE_TILES = [
  {
    title: 'Executive Summary',
    desc: 'The high-level "Why" and "How" for leadership and customers. Perfect for Presales and architectural alignment.',
    icon: <BookOpen size={24} />,
    color: '#94a3b8',
    path: '/docs/story'
  },
  {
    title: 'Adversarial Red-Team',
    desc: 'Simulate prompt injections and PII leaks across multiple languages (Cantonese, Spanish, English).',
    icon: <Shield size={24} />,
    color: '#ef4444',
    path: '/docs/security'
  },
  {
    title: 'FinOps Optimizer',
    desc: 'Identify token waste and apply automated fixes like Context Caching to reduce costs by up to 90%.',
    icon: <Zap size={24} />,
    color: '#f59e0b',
    path: '/docs/optimization'
  },
  {
    title: 'Semantic Hive-Mind',
    desc: 'Implement highly-performant semantic caching to avoid redundant LLM calls and latency.',
    icon: <Activity size={24} />,
    color: '#10b981',
    path: '/docs/cockpit'
  },
  {
    title: 'Multi-Agent Swarm',
    desc: 'Standardized A2A (Agent-to-Agent) coordination with built-in Evidence Packet verified traces.',
    icon: <Users size={24} />,
    color: '#3b82f6',
    path: '/docs/story'
  },
  {
    title: 'MCP Protocol Hub',
    desc: 'Natively connect and govern any Model Context Protocol tool server through the unified Cockpit hub.',
    icon: <Cpu size={24} />,
    color: '#8b5cf6',
    path: '/docs/be-integration'
  },
  {
    title: 'A2UI Visual Face',
    desc: 'Audit and implement the Generation UI standard for adaptive agentic surfaces.',
    icon: <Layout size={24} />,
    color: '#ec4899',
    path: '/docs/development'
  },
  {
    title: 'Evidence Bridge',
    desc: 'Verify design decisions with real-time citations from official Cloud Architecture Frameworks.',
    icon: <ShieldCheck size={24} />,
    color: '#0ea5e9',
    path: '/samples'
  }
];

export const DocHome: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="doc-home-v2">
      <header className="doc-home-hero">
        <div className="accent-pill">Documentation Hub</div>
        <h1>Welcome to the <span className="gradient-text">Cockpit</span></h1>
        <p>Your guide to building, governing, and scaling production AI agents on Google Cloud.</p>

        <div className="quick-actions">
          <button onClick={() => navigate('/docs/getting-started')} className="primary-doc-btn">
            <Rocket size={18} />
            Start Building
          </button>
          <button onClick={() => navigate('/docs/cli-commands')} className="secondary-doc-btn">
            <Terminal size={18} />
            View CLI Docs
          </button>
        </div>
      </header>

      <section className="feature-tiles-grid">
        {FEATURE_TILES.map((tile) => (
          <div
            key={tile.title}
            className="feature-tile"
            onClick={() => navigate(tile.path)}
            style={{ '--tile-color': tile.color } as any}
          >
            <div className="tile-icon-box">
              {tile.icon}
            </div>
            <h3>{tile.title}</h3>
            <p>{tile.desc}</p>
            <div className="tile-footer">
              <span>Learn more</span>
              <ChevronRight size={14} />
            </div>
          </div>
        ))}
      </section>

      <style>{`
        .doc-home-v2 {
          padding-top: 2rem;
        }
        .doc-home-hero {
          margin-bottom: 5rem;
          text-align: left;
        }
        .accent-pill {
          display: inline-block;
          background: rgba(var(--primary-color-rgb), 0.1);
          color: var(--primary-color);
          padding: 0.25rem 0.75rem;
          border-radius: 99px;
          font-size: 0.75rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          margin-bottom: 1.5rem;
        }
        .doc-home-hero h1 {
          font-size: 3.5rem;
          font-weight: 900;
          letter-spacing: -0.04em;
          margin-bottom: 1.5rem;
        }
        .doc-home-hero p {
          font-size: 1.25rem;
          color: var(--text-secondary);
          max-width: 600px;
          line-height: 1.6;
          margin-bottom: 3rem;
        }
        .quick-actions {
          display: flex;
          gap: 1rem;
        }
        .primary-doc-btn, .secondary-doc-btn {
          padding: 0.75rem 1.5rem;
          border-radius: 10px;
          font-weight: 700;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .primary-doc-btn {
          background: var(--primary-color);
          color: white;
          border: none;
          box-shadow: 0 4px 12px rgba(var(--primary-color-rgb), 0.2);
        }
        .secondary-doc-btn {
          background: transparent;
          border: 1px solid var(--border-color);
          color: var(--text-primary);
        }
        .primary-doc-btn:hover { transform: translateY(-2px); }
        .secondary-doc-btn:hover { background: rgba(var(--text-primary-rgb), 0.05); }

        .feature-tiles-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
          gap: 1.5rem;
          margin-bottom: 4rem;
        }
        .feature-tile {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 16px;
          padding: 2rem;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
          display: flex;
          flex-direction: column;
        }
        .feature-tile:hover {
          transform: translateY(-5px);
          border-color: var(--tile-color);
          box-shadow: 0 15px 30px rgba(0,0,0,0.05);
        }
        .feature-tile::before {
          content: '';
          position: absolute;
          top: -20%;
          right: -20%;
          width: 50%;
          height: 50%;
          background: radial-gradient(circle, var(--tile-color), transparent 70%);
          opacity: 0.05;
          transition: opacity 0.3s;
        }
        .feature-tile:hover::before { opacity: 0.15; }
        
        .tile-icon-box {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          background: rgba(var(--text-primary-rgb), 0.05);
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 1.5rem;
          color: var(--tile-color);
          border: 1px solid transparent;
          transition: all 0.3s;
        }
        .feature-tile:hover .tile-icon-box {
          background: var(--tile-color);
          color: white;
        }
        .feature-tile h3 {
          font-size: 1.15rem;
          font-weight: 800;
          margin-bottom: 1rem;
        }
        .feature-tile p {
          font-size: 0.9rem;
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 2rem;
          flex: 1;
        }
        .tile-footer {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          font-weight: 800;
          color: var(--tile-color);
          opacity: 0;
          transform: translateX(-10px);
          transition: all 0.3s;
        }
        .feature-tile:hover .tile-footer {
          opacity: 1;
          transform: translateX(0);
        }
      `}</style>
    </div>
  );
};

// Internal icon dependency fix
const ChevronRight = ({ size }: { size: number }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6" /></svg>
);
