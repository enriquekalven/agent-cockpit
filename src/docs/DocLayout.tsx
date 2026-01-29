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
    title: 'Introductions',
    items: [
      { id: 'docs-home', label: 'Documentation Home', path: '/docs', icon: <Activity size={18} /> },
      { id: 'story', label: 'The Trinity Vision', path: '/docs/story', icon: <BookOpen size={18} /> },
    ]
  },
  {
    title: 'The Mission (Architecture)',
    items: [
      { id: 'google-architecture', label: 'Google Well-Architected', path: '/docs/google-architecture', icon: <ShieldCheck size={18} /> },
      { id: 'a2a', label: 'A2A Standard', path: '/docs/a2a', icon: <Command size={18} /> },
    ]
  },
  {
    title: 'Getting Started',
    items: [
      { id: 'getting-started', label: 'Installation', path: '/docs/getting-started', icon: <Rocket size={18} /> },
      { id: 'cli-commands', label: 'CLI Reference', path: '/docs/cli-commands', icon: <Terminal size={18} /> },
    ]
  },
  {
    title: 'Operations (The Cockpit)',
    items: [
      { id: 'optimization', label: 'FinOps & Optimization', path: '/docs/optimization', icon: <Zap size={18} /> },
      { id: 'cockpit', label: 'Semantic Caching', path: '/docs/cockpit', icon: <Activity size={18} /> },
      { id: 'governance', label: 'Governance & Privacy', path: '/docs/governance', icon: <Lock size={18} /> },
    ]
  },
  {
    title: 'Security (Red Team)',
    items: [
      { id: 'security', label: 'Adversarial Audits', path: '/docs/security', icon: <Shield size={18} /> },
      { id: 'production-checklist', label: 'Launch Readiness', path: '/docs/production-checklist', icon: <ShieldCheck size={18} /> },
    ]
  },
  {
    title: 'Engineering',
    items: [
      { id: 'be-integration', label: 'Engine (Backend)', path: '/docs/be-integration', icon: <Cpu size={18} /> },
      { id: 'development', label: 'Face (UI/A2UI)', path: '/docs/development', icon: <Layout size={18} /> },
      { id: 'deployment', label: 'Cloud Deployment', path: '/docs/deployment', icon: <Rocket size={18} /> },
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
        <div className="top-nav-left">
          <Link to="/" className="crew-logo">
            <span className="agent-pulse mini"></span>
            <span>AgentOps Cockpit</span>
          </Link>
          <div className="search-bar-container">
            <div className={`search-wrapper ${searchFocused ? 'focused' : ''}`}>
              <Search size={16} className="search-icon" />
              <input
                type="text"
                placeholder="Search documentation..."
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
              />
              <kbd className="search-kbd">⌘K</kbd>
            </div>
          </div>
        </div>
        
        <div className="top-nav-right">
          <a href="https://github.com/enriquekalven/agent-cockpit" target="_blank" className="icon-link">
            <Github size={20} />
          </a>
          <ThemeToggle />
          <Link to="/ops" className="nav-button-primary">The Cockpit</Link>
        </div>
      </nav>

      <div className="crew-main-container">
        {/* Sidebar */}
        <aside className={`crew-sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
          <div className="sidebar-scroll">
            {/* Stack Selector - Following CopilotKit pattern */}
            <div className="stack-selector-container">
              <label className="sidebar-label">Active Integration</label>
              <div
                className={`stack-dropdown ${isStackDropdownOpen ? 'active' : ''}`}
                onClick={() => setStackDropdownOpen(!isStackDropdownOpen)}
              >
                <div className="active-stack">
                  <span className="stack-icon">{activeStack.icon}</span>
                  <span className="stack-label">{activeStack.label}</span>
                  <ChevronRight size={14} className={`dropdown-arrow ${isStackDropdownOpen ? 'open' : ''}`} />
                </div>

                {isStackDropdownOpen && (
                  <div className="stack-options-menu">
                    {STACK_OPTIONS.map(opt => (
                      <div
                        key={opt.id}
                        className={`stack-opt-item ${activeStack.id === opt.id ? 'current' : ''}`}
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

            <nav className="sidebar-nav">
              {PILLAR_NAV.map((group) => (
                <div className="nav-section" key={group.title}>
                  <h4 className="section-title">{group.title}</h4>
                  <div className="section-items">
                    {group.items.map((item) => (
                      <Link
                        key={item.id}
                        to={item.path}
                        className={`sidebar-item ${location.pathname === item.path ? 'active' : ''}`}
                      >
                        <span className="item-icon">{item.icon}</span>
                        <span className="item-label">{item.label}</span>
                        {location.pathname === item.path && <div className="active-glow" />}
                      </Link>
                    ))}
                  </div>
                </div>
              ))}

              <div className="sidebar-footer-links">
                <a href="https://a2ui.org" target="_blank" className="footer-link">
                  <ExternalLink size={14} />
                  Official A2UI Spec
                </a>
              </div>
            </nav>
          </div>
        </aside>

        {/* Content */}
        <main className="crew-content">
          <div className="content-inner">
            <header className="content-breadcrumb">
              <Link to="/docs" style={{ color: 'inherit', textDecoration: 'none' }}>Docs</Link>
              {location.pathname !== '/docs' && (
                <>
                  <ChevronRight size={14} />
                  <span className="current">{location.pathname.split('/').pop()?.replace('-', ' ')}</span>
                </>
              )}
            </header>

            <div className="markdown-container">
              <Outlet />
            </div>

            <footer className="content-footer">
              <div className="footer-meta">
                <span>Last updated: 2026-01-27</span>
                <a href="https://github.com/enriquekalven/agent-cockpit" target="_blank">Edit on GitHub</a>
              </div>
              <div className="footer-social">
                <Slack size={18} />
                <Twitter size={18} />
              </div>
            </footer>
          </div>

          {/* Table of Contents - Hidden on index page */}
          {location.pathname !== '/docs' && (
            <aside className="crew-toc">
              <div className="toc-inner">
                <h4 className="toc-title">On this page</h4>
                <nav className="toc-links">
                  <a href="#overview" className="toc-link active">Overview</a>
                  <a href="#setup" className="toc-link">Setup</a>
                  <a href="#usage" className="toc-link">Usage Examples</a>
                  <a href="#best-practices" className="toc-link">Best Practices</a>
                </nav>
              </div>
            </aside>
          )}
        </main>
      </div>

      <style>{`
        .crew-docs-layout {
          min-height: 100vh;
          background-color: var(--bg-color);
          color: var(--text-primary);
          display: flex;
          flex-direction: column;
        }

        .crew-top-nav {
          height: 64px;
          border-bottom: 1px solid var(--border-color);
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 1.5rem;
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          background: rgba(var(--bg-color-rgb), 0.8);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
        }

        .top-nav-left {
          display: flex;
          align-items: center;
          gap: 2rem;
          flex: 1;
        }

        .crew-logo {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          font-weight: 800;
          font-size: 1.1rem;
          color: var(--text-primary);
          text-decoration: none;
          min-width: fit-content;
        }

        .search-bar-container {
          max-width: 400px;
          width: 100%;
        }

        .search-wrapper {
          display: flex;
          align-items: center;
          background: rgba(var(--text-primary-rgb), 0.05);
          border: 1px solid var(--border-color);
          border-radius: 8px;
          padding: 0.5rem 0.75rem;
          gap: 0.5rem;
          transition: all 0.2s;
        }

        .search-wrapper.focused {
          background: var(--bg-secondary);
          border-color: var(--primary-color);
          box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.1);
        }

        .search-wrapper input {
          background: transparent;
          border: none;
          outline: none;
          color: var(--text-primary);
          width: 100%;
          font-size: 0.9rem;
        }

        .search-icon { color: var(--text-secondary); }
        .search-kbd {
          font-size: 0.7rem;
          background: rgba(var(--text-primary-rgb), 0.1);
          padding: 0.1rem 0.4rem;
          border-radius: 4px;
          color: var(--text-secondary);
        }

        .top-nav-right {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .icon-link {
          color: var(--text-secondary);
          transition: color 0.2s;
        }
        .icon-link:hover { color: var(--text-primary); }

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

        .footer-social {
          display: flex;
          gap: 1.5rem;
          color: var(--text-secondary);
        }

        @media (max-width: 1024px) {
          .crew-sidebar { width: 240px; }
          .crew-content { margin-left: 240px; padding: 3rem 2rem; }
        }

        @media (max-width: 768px) {
          .crew-sidebar { transform: translateX(-100%); width: 100%; }
          .crew-sidebar.open { transform: translateX(0); }
          .crew-content { margin-left: 0; padding: 2rem 1.5rem; }
          .search-bar-container { display: none; }
        }
      `}</style>
    </div>
  );
};
