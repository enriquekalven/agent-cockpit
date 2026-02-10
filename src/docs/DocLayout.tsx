import React, { useState, useEffect } from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  Menu, X, ChevronRight, BookOpen, Terminal, Rocket, 
  Cpu, Layout, Activity, ShieldCheck, Search, Github,
  Command, ExternalLink, Slack, Twitter, Zap, Lock, Shield
} from 'lucide-react';

import { ThemeToggle } from '../components/ThemeToggle';

const PILLAR_NAV = [
  {
    title: '🚀 Mission Control & SME Matrix',
    items: [
      { id: 'introduction', label: 'Operational Introduction', path: '/docs/introduction', icon: <BookOpen size={18} /> },
      { id: 'story', label: 'The Agentic Story', path: '/docs/story', icon: <BookOpen size={18} /> },
      { id: 'getting-started', label: 'Quickstart Guide', path: '/docs/getting-started', icon: <Rocket size={18} /> },
      { id: 'gemini', label: 'Gemini Context', path: '/docs/gemini', icon: <Cpu size={18} /> },
      { id: 'arch-review', label: 'Architect: Arch Review', path: '/docs/arch-review', icon: <ShieldCheck size={18} /> },
      { id: 'quality-guide', label: 'Quality Lead: Optimization', path: '/docs/quality-guide', icon: <Activity size={18} /> },
      { id: 'redteam-guide', label: 'Security: Red Team', path: '/docs/redteam-guide', icon: <Shield size={18} /> },
      { id: 'finops-guide', label: 'FinOps: Cost Optimization', path: '/docs/finops-guide', icon: <Zap size={18} /> },
      { id: 'ux-guide', label: 'UX/Face: A2UI Guide', path: '/docs/ux-guide', icon: <Layout size={18} /> },
      { id: 'infra-guide', label: 'SRE/Eng: Infra & Growth', path: '/docs/infra-guide', icon: <Cpu size={18} /> },
      { id: 'a2a-guide', label: 'Automations: A2A Standards', path: '/docs/a2a-guide', icon: <Command size={18} /> },
    ]
  },
  {
    title: '⌨️ The Command Center',
    items: [
      { id: 'cockpit-guide', label: 'The Cockpit UI Guide', path: '/docs/cockpit-guide', icon: <Layout size={18} /> },
      { id: 'audit-guide', label: 'Audit Suite Guide', path: '/docs/audit-guide', icon: <ShieldCheck size={18} /> },
      { id: 'commands-master', label: 'Master Command Reference', path: '/docs/commands-master', icon: <Terminal size={18} /> },
      { id: 'uvx-master', label: 'UVX & Portable Ops', path: '/docs/uvx-master', icon: <Command size={18} /> },
    ]
  },
  {
    title: '☁️ Production & Scaling',
    items: [
      { id: 'deployment', label: 'Deployment Masterclass', path: '/docs/deployment', icon: <Rocket size={18} /> },
      { id: 'production-checklist', label: 'Launch Checklist', path: '/docs/production-checklist', icon: <ShieldCheck size={18} /> },
      { id: 'google-architecture', label: 'Google Well-Architected', path: '/docs/google-architecture', icon: <ShieldCheck size={18} /> },
      { id: 'audit-scenarios', label: 'Audit Scenarios', path: '/docs/audit-scenarios', icon: <BookOpen size={18} /> },
    ]
  },
  {
    title: '🗺️ Project Governance',
    items: [
      { id: 'prd', label: 'The PRD', path: '/docs/prd', icon: <BookOpen size={18} /> },
      { id: 'roadmap', label: 'v1.3 Roadmap', path: '/docs/roadmap', icon: <Activity size={18} /> },
    ]
  }
];

const STACK_OPTIONS = [
  { id: 'standalone', label: 'Standalone Python', icon: '🐍' },
  { id: 'langgraph', label: 'LangGraph', icon: '🦜' },
  { id: 'crewai', label: 'CrewAI / Swarm', icon: '🐝' },
  { id: 'autogen', label: 'Microsoft AutoGen', icon: '🤖' },
];

export const DocLayout: React.FC = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [searchFocused, setSearchFocused] = useState(false);
  const [activeStack, setActiveStack] = useState(STACK_OPTIONS[0]);
  const [isStackDropdownOpen, setStackDropdownOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        document.querySelector<HTMLInputElement>('.search-wrapper input')?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  useEffect(() => {
    // Scroll to top on route change
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <div className="crew-docs-layout">
      {/* Search Header - Fixed */}
      <nav className="crew-top-nav">
        <div className="nav-left">
          <button
            className="mobile-toggle"
            onClick={() => setSidebarOpen(!isSidebarOpen)}
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <Link to="/" className="nav-logo">
            <div className="logo-icon">🕹️</div>
            <span>AgentOps <span className="text-secondary opacity-50">Cockpit</span></span>
          </Link>
        </div>

        <div className="nav-center">
          <div className={`search-wrapper ${searchFocused ? 'focused' : ''}`}>
            <Search size={18} className="search-icon" />
            <input
              type="text" 
              placeholder="Search documentation... (⌘K)"
              onFocus={() => setSearchFocused(true)}
              onBlur={() => setSearchFocused(false)}
            />
          </div>
        </div>

        <div className="nav-right">
          <a href="https://github.com/enriquekalven/agent-cockpit" target="_blank" rel="noopener noreferrer" className="nav-icon-btn">
            <Github size={20} />
          </a>
          <ThemeToggle />
          <Link to="/docs/getting-started" className="nav-button-primary">
            Quickstart
          </Link>
        </div>
      </nav>

      <div className="crew-main-container">
        {/* Sidebar */}
        <aside className={`crew-sidebar ${isSidebarOpen ? 'open' : ''}`}>
          <div className="sidebar-scroll">

            {/* Stack Selector */}
            <div className="stack-selector-container">
              <span className="sidebar-label">Active Stack Target</span>
              <div 
                className={`stack-dropdown ${isStackDropdownOpen ? 'active' : ''}`}
                onClick={() => setStackDropdownOpen(!isStackDropdownOpen)}
              >
                <div className="active-stack">
                  <span className="stack-icon">{activeStack.icon}</span>
                  <span className="stack-label">{activeStack.label}</span>
                  <ChevronRight size={16} className={`dropdown-arrow ${isStackDropdownOpen ? 'open' : ''}`} />
                </div>

                {isStackDropdownOpen && (
                  <div className="stack-options-menu">
                    {STACK_OPTIONS.map(opt => (
                      <div 
                        key={opt.id}
                        className={`stack-opt-item ${opt.id === activeStack.id ? 'current' : ''}`}
                        onClick={(e) => {
                          e.stopPropagation();
                          setActiveStack(opt);
                          setStackDropdownOpen(false);
                        }}
                      >
                        <span className="stack-icon">{opt.icon}</span>
                        <span className="stack-label">{opt.label}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {PILLAR_NAV.map((group) => (
              <div key={group.title} className="nav-section">
                <h3 className="section-title">{group.title}</h3>
                <div className="section-items">
                  {group.items.map((item) => {
                    const isActive = location.pathname === item.path;
                    return (
                      <Link
                        key={item.id}
                        to={item.path}
                        className={`sidebar-item ${isActive ? 'active' : ''}`}
                      >
                        {item.icon}
                        <span>{item.label}</span>
                        {isActive && <div className="active-glow" />}
                      </Link>
                    );
                  })}
                </div>
              </div>
            ))}

            <div className="sidebar-footer-links">
              <a href="#" className="footer-link">
                <Slack size={16} />
                <span>Join Slack Community</span>
              </a>
              <a href="#" className="footer-link">
                <Twitter size={16} />
                <span>Follow Updates</span>
              </a>
              <div style={{ marginTop: '1rem', opacity: 0.4, fontSize: '0.7rem' }}>
                v0.9.9 • Production Stack
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="crew-content">
          <div className="content-inner">
            <div className="content-breadcrumb">
              <Link to="/docs">Docs</Link>
              <ChevronRight size={14} />
              <span className="current">
                {location.pathname.split('/').pop()?.replace(/-/g, ' ')}
              </span>
            </div>

            <div className="markdown-container">
              <Outlet />
            </div>

            <footer className="content-footer">
              <div className="footer-meta">
                <span>Last updated: February 2026</span>
                <span>Caught a bug? <a href="#">Edit this page on GitHub</a></span>
                <span className="legal-links">
                  <Link to="/docs/legal">Legal Disclaimer</Link>
                  <span className="divider">•</span>
                  <Link to="/docs/privacy">Privacy Policy</Link>
                </span>
              </div>
              <div className="footer-social">
                <Github size={20} />
                <Slack size={20} />
                <Twitter size={20} />
              </div>
            </footer>
          </div>

          {/* Table of Contents - Sticky Right */}
          <aside className="crew-toc">
            <h4 className="toc-title">On this page</h4>
            <div className="toc-links">
              <a href="#overview" className="toc-link active">Overview</a>
              <a href="#installation" className="toc-link">Installation</a>
              <a href="#configuration" className="toc-link">Configuration</a>
              <a href="#usage" className="toc-link">Usage Examples</a>
              <a href="#best-practices" className="toc-link">Best Practices</a>
            </div>
          </aside>
        </main>
      </div>

      <style>{`
        .crew-docs-layout {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          background: var(--bg-color);
          color: var(--text-primary);
        }

        /* Top Nav */
        .crew-top-nav {
          height: 64px;
          border-bottom: 1px solid var(--border-color);
          padding: 0 1.5rem;
          display: flex;
          align-items: center;
          justify-content: space-between;
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          background: rgba(var(--bg-color-rgb), 0.8);
          backdrop-filter: blur(12px);
        }

        .nav-left {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .mobile-toggle {
          display: none;
          background: none;
          border: none;
          color: var(--text-primary);
          cursor: pointer;
        }

        .nav-logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          font-size: 1.1rem;
          text-decoration: none;
          color: var(--text-primary);
          letter-spacing: -0.02em;
        }
        .logo-icon { font-size: 1.25rem; }

        .nav-center {
          flex: 0 1 500px;
          margin: 0 2rem;
        }

        .search-wrapper {
          background: rgba(var(--text-primary-rgb), 0.05);
          border: 1px solid var(--border-color);
          border-radius: 8px;
          padding: 0.5rem 1rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          transition: all 0.2s;
        }
        .search-wrapper.focused {
          background: var(--bg-secondary);
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.1);
        }
        .search-wrapper input {
          background: none;
          border: none;
          color: var(--text-primary);
          width: 100%;
          font-size: 0.9rem;
          outline: none;
        }
        .search-icon { color: var(--text-secondary); opacity: 0.5; }

        .nav-right {
          display: flex;
          align-items: center;
          gap: 1.25rem;
        }

        .nav-icon-btn {
          color: var(--text-secondary);
          transition: color 0.2s;
          display: flex;
          align-items: center;
        }
        .nav-icon-btn:hover { color: var(--text-primary); }

        .nav-button-primary {
          background: var(--accent-color);
          color: var(--bg-color);
          padding: 0.5rem 1rem;
          border-radius: 6px;
          font-size: 0.85rem;
          font-weight: 700;
          text-decoration: none;
          transition: transform 0.2s;
        }
        .nav-button-primary:hover { transform: translateY(-1px); }

        .crew-main-container {
          display: flex;
          flex: 1;
          margin-top: 64px;
        }

        /* Stack Selector Style */
        .stack-selector-container {
          margin-bottom: 2rem;
          padding: 0 0.5rem;
        }
        .sidebar-label {
          font-size: 0.7rem;
          text-transform: uppercase;
          color: var(--text-secondary);
          opacity: 0.6;
          margin-bottom: 0.5rem;
          display: block;
          font-weight: 800;
        }
        .stack-dropdown {
          background: rgba(var(--text-primary-rgb), 0.05);
          border: 1px solid var(--border-color);
          border-radius: 8px;
          padding: 0.6rem 0.75rem;
          cursor: pointer;
          transition: all 0.2s;
          position: relative;
        }
        .stack-dropdown:hover {
          background: rgba(var(--text-primary-rgb), 0.08);
          border-color: var(--primary-color);
        }
        .stack-dropdown.active {
          border-color: var(--primary-color);
          background: var(--bg-secondary);
          box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .active-stack {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        .stack-icon { font-size: 1.1rem; }
        .stack-label {
          font-size: 0.85rem;
          font-weight: 700;
          flex: 1;
        }
        .dropdown-arrow { 
          transition: transform 0.2s; 
          opacity: 0.4;
        }
        .dropdown-arrow.open {
          transform: rotate(90deg);
          opacity: 1;
          color: var(--primary-color);
        }

        .stack-options-menu {
          position: absolute;
          top: calc(100% + 8px);
          left: 0;
          right: 0;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 12px;
          padding: 0.5rem;
          z-index: 1000;
          box-shadow: 0 10px 30px rgba(0,0,0,0.2);
          animation: slideUp 0.2s ease-out;
        }

        @keyframes slideUp {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .stack-opt-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.6rem 0.75rem;
          border-radius: 6px;
          transition: all 0.2s;
        }
        .stack-opt-item:hover {
          background: rgba(var(--text-primary-rgb), 0.05);
        }
        .stack-opt-item.current {
          background: rgba(var(--primary-color-rgb), 0.1);
          color: var(--primary-color);
        }

        /* Sidebar Styling */
        .crew-sidebar {
          width: 280px;
          border-right: 1px solid var(--border-color);
          position: fixed;
          top: 64px;
          bottom: 0;
          left: 0;
          z-index: 900;
          background: var(--bg-color);
          overflow: hidden;
        }

        .sidebar-scroll {
          height: 100%;
          overflow-y: auto;
          padding: 2rem 1.5rem;
        }

        .nav-section { margin-bottom: 2.5rem; }
        .section-title {
          font-size: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: var(--text-secondary);
          margin-bottom: 1rem;
          font-weight: 800;
        }

        .sidebar-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.6rem 0.8rem;
          border-radius: 6px;
          color: var(--text-secondary);
          text-decoration: none;
          font-size: 0.9rem;
          font-weight: 600;
          margin-bottom: 0.25rem;
          transition: all 0.2s;
          position: relative;
        }

        .sidebar-item:hover {
          color: var(--text-primary);
          background: rgba(var(--text-primary-rgb), 0.03);
        }

        .sidebar-item.active {
          color: var(--primary-color);
          background: rgba(var(--primary-color-rgb), 0.05);
        }

        .active-glow {
          position: absolute;
          left: -1.5rem;
          width: 4px;
          height: 16px;
          background: var(--primary-color);
          border-radius: 0 4px 4px 0;
          box-shadow: 0 0 10px var(--primary-color);
        }

        .sidebar-footer-links {
          margin-top: 4rem;
          padding-top: 2rem;
          border-top: 1px solid var(--border-color);
        }

        .footer-link {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: var(--text-secondary);
          font-size: 0.8rem;
          text-decoration: none;
          margin-bottom: 0.75rem;
        }

        /* Content Area */
        .crew-content {
          flex: 1;
          margin-left: 280px;
          display: flex;
          justify-content: space-between;
          padding: 3rem 4rem;
          position: relative;
        }

        .content-inner {
          max-width: 800px;
          width: 100%;
        }

        .content-breadcrumb {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          color: var(--text-secondary);
          margin-bottom: 2rem;
        }
        .content-breadcrumb .current {
          color: var(--primary-color);
          font-weight: 800;
          text-transform: capitalize;
        }

        .markdown-container {
          min-height: 60vh;
        }

        /* TOC Styling */
        .crew-toc {
          width: 240px;
          position: sticky;
          top: 100px;
          height: fit-content;
          margin-left: 4rem;
          display: none; /* Hidden by default, shown on XL screens */
        }

        @media (min-width: 1280px) {
          .crew-toc { display: block; }
        }

        .toc-title {
          font-size: 0.9rem;
          font-weight: 800;
          margin-bottom: 1.25rem;
          color: var(--text-primary);
        }

        .toc-links {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          border-left: 1px solid var(--border-color);
        }

        .toc-link {
          font-size: 0.85rem;
          color: var(--text-secondary);
          text-decoration: none;
          padding-left: 1rem;
          border-left: 2px solid transparent;
          margin-left: -1.5px;
          transition: all 0.2s;
        }

        .toc-link:hover { color: var(--text-primary); }
        .toc-link.active {
          color: var(--primary-color);
          border-left-color: var(--primary-color);
          font-weight: 700;
        }

        .content-footer {
          margin-top: 6rem;
          padding-top: 2rem;
          border-top: 1px solid var(--border-color);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .footer-meta {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          font-size: 0.85rem;
          color: var(--text-secondary);
        }
        .footer-meta a {
          color: var(--primary-color);
          text-decoration: none;
        }
        .legal-links {
          margin-top: 0.5rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 500;
        }
        .divider {
          opacity: 0.3;
        }

        .footer-social {
          display: flex;
          gap: 1.5rem;
          color: var(--text-secondary);
        }

        @media (max-width: 768px) {
          .mobile-toggle { display: block; }
          .nav-center { display: none; }
          .nav-logo span { font-size: 0.9rem; }
          .nav-logo span .text-secondary { display: none; }
          .nav-right .nav-button-primary { padding: 0.4rem 0.75rem; font-size: 0.75rem; }
          .nav-right .nav-icon-btn { display: none; }
          
          .crew-sidebar { 
            transform: translateX(-100%); 
            width: 280px; 
            box-shadow: 20px 0 50px rgba(0,0,0,0.3);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          }
          .crew-sidebar.open { transform: translateX(0); }
          .crew-content { margin-left: 0; padding: 2rem 1.5rem; }
          .search-bar-container { display: none; }
          
          .content-footer {
            flex-direction: column;
            gap: 2rem;
            align-items: flex-start;
          }
        }
      `}</style>
    </div>
  );
};
