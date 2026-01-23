import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import { Menu, X, ChevronRight, BookOpen, Terminal, Rocket, Cpu, Layout, Activity, ShieldCheck } from 'lucide-react';

import { ThemeToggle } from '../components/ThemeToggle';

interface DocLayoutProps {
  children?: React.ReactNode;
}

const DOC_NAV = [
  { id: 'getting-started', label: 'Getting Started', path: '/docs/getting-started', icon: <Rocket size={18} /> },
  { id: 'development', label: 'Development', path: '/docs/development', icon: <Cpu size={18} /> },
  { id: 'deployment', label: 'Deployment', path: '/docs/deployment', icon: <BookOpen size={18} /> },
  { id: 'cli-commands', label: 'CLI Reference', path: '/docs/cli-commands', icon: <Terminal size={18} /> },
  { id: 'readme', label: 'Architecture Overview', path: '/docs/readme', icon: <Layout size={18} /> },
];

const ECOSYSTEM_NAV = [
  { id: 'a2a', label: 'A2A Protocol Guide', path: '/docs/a2a', icon: <Cpu size={18} /> },
  { id: 'be-integration', label: 'Backend Integration', path: '/docs/be-integration', icon: <Terminal size={18} /> },
];

const EXTERNAL_LINKS = [
  { label: 'AG UI (A2UI Official)', url: 'https://github.com/google/A2UI', icon: <Layout size={18} /> },
  { label: 'CopilotKit (AG UI High-End)', url: 'https://github.com/CopilotKit/CopilotKit', icon: <Rocket size={18} /> },
  { label: 'GenUI Flutter SDK', url: 'https://github.com/a2aproject/adk', icon: <Cpu size={18} /> },
  { label: 'Lit Web Components', url: 'https://lit.dev/', icon: <Layout size={18} /> },
];

export const DocLayout: React.FC<DocLayoutProps> = ({ children }) => {
  const [isSidebarOpen, setSidebarOpen] = React.useState(true);
  const location = useLocation();

  return (
    <div className="doc-layout">
      {/* Sidebar */}
      <aside className={`doc-sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
        <div className="doc-sidebar-header">
          <Link to="/" className="doc-logo">
            <span className="agent-pulse mini"></span>
            Agent Ops Starter Pack
          </Link>
          <button className="mobile-toggle" onClick={() => setSidebarOpen(!isSidebarOpen)}>
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        
        <nav className="doc-nav">
          <div className="nav-group">
            <div className="nav-group-title">Core Documentation</div>
            {DOC_NAV.map((item) => (
              <Link
                key={item.id}
                to={item.path}
                className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              >
                {item.icon}
                <span>{item.label}</span>
                <ChevronRight size={14} className="chevron" />
              </Link>
            ))}
          </div>

          <div className="nav-group">
            <div className="nav-group-title">Guides & Protocol</div>
            {ECOSYSTEM_NAV.map((item) => (
              <Link
                key={item.id}
                to={item.path}
                className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              >
                {item.icon}
                <span>{item.label}</span>
                <ChevronRight size={14} className="chevron" />
              </Link>
            ))}
          </div>

          <div className="nav-group">
            <div className="nav-group-title">Standards & Ecosystem</div>
            {EXTERNAL_LINKS.map((item) => (
              <a
                key={item.label}
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="nav-item"
              >
                {item.icon}
                <span>{item.label}</span>
                <Rocket size={14} className="chevron external" />
              </a>
            ))}
          </div>

          <div className="nav-group">
            <div className="nav-group-title">Interactive</div>
            <Link to="/playground" className="nav-item">
              <Layout size={18} />
              <span>A2UI Playground</span>
            </Link>
          </div>
          
          <div className="nav-group">
            <div className="nav-group-title">Agent Ops (Day 2)</div>
            <Link to="/ops" className="nav-item">
              <Activity size={18} />
              <span>Ops Dashboard</span>
            </Link>
            <div className="nav-item disabled" style={{ opacity: 0.5 }}>
              <ShieldCheck size={18} />
              <span>Red Team Audit</span>
            </div>
          </div>

          <div className="nav-group">
            <div className="nav-group-title">Resources</div>
            <a href="https://a2ui.org" target="_blank" rel="noopener noreferrer" className="nav-item">
              <BookOpen size={18} />
              <span>Official A2UI.org</span>
            </a>
          </div>
        </nav>
      </aside>


      {/* Main Content */}
      <main className="doc-main">
        <header className="doc-header">
          <div className="breadcrumb">
            <Link to="/">Home</Link>
            <ChevronRight size={14} />
            <Link to="/docs/getting-started">Docs</Link>
            <ChevronRight size={14} />
            <span>{location.pathname.split('/').pop()}</span>
          </div>
          <div style={{ marginLeft: 'auto' }}>
            <ThemeToggle />
          </div>
        </header>
        <div className="doc-content-wrapper">
          {children || <Outlet />}
        </div>
      </main>
    </div>
  );
};
