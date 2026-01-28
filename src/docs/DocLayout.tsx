import React, { useState, useEffect } from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  Menu, X, ChevronRight, BookOpen, Terminal, Rocket,
  Cpu, Layout, Activity, ShieldCheck, Search, Github,
  Command, ExternalLink, Slack, Twitter
} from 'lucide-react';

import { ThemeToggle } from '../components/ThemeToggle';

const PILLAR_NAV = [
  {
    title: 'Introduction',
    items: [
      { id: 'story', label: 'The Trinity Vision', path: '/docs/story', icon: <BookOpen size={18} /> },
      { id: 'google-architecture', label: 'Google Well-Architected', path: '/docs/google-architecture', icon: <ShieldCheck size={18} /> },
      { id: 'getting-started', label: 'Quickstart Guide', path: '/docs/getting-started', icon: <Rocket size={18} /> },
    ]
  },
  {
    title: 'The Engine',
    items: [
      { id: 'be-integration', label: 'Backend Setup', path: '/docs/be-integration', icon: <Cpu size={18} /> },
      { id: 'optimization', label: 'Token Optimization', path: '/docs/cli-commands', icon: <Terminal size={18} /> },
    ]
  },
  {
    title: 'The Face',
    items: [
      { id: 'development', label: 'UI Components', path: '/docs/development', icon: <Layout size={18} /> },
      { id: 'a2a', label: 'A2UI Protocol', path: '/docs/a2a', icon: <Command size={18} /> },
    ]
  },
  {
    title: 'Operations',
    items: [
      { id: 'ops', label: 'The Cockpit Dashboard', path: '/ops', icon: <Activity size={18} /> },
      { id: 'security', label: 'Red Team Audits', path: '/docs/cli-commands', icon: <ShieldCheck size={18} /> },
      { id: 'deployment', label: 'Cloud Deployment', path: '/docs/deployment', icon: <Rocket size={18} /> },
    ]
  }
];

export const DocLayout: React.FC = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [searchFocused, setSearchFocused] = useState(false);
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
              <span>Docs</span>
              <ChevronRight size={14} />
              <span className="current">{location.pathname.split('/').pop()?.replace('-', ' ')}</span>
            </header>

            <div className="markdown-container">
              <Outlet />
            </div>

            <footer className="content-footer">
              <div className="footer-meta">
                <span>Last updated: 2026-01-27</span>
                <a href="#">Edit this page on GitHub</a>
              </div>
              <div className="footer-social">
                <Slack size={18} />
                <Twitter size={18} />
              </div>
            </footer>
          </div>

          {/* Table of Contents - Hidden on small screens */}
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
