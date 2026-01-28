import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import { Menu, X, ChevronRight, BookOpen, Terminal, Rocket, Cpu, Layout, Activity, ShieldCheck } from 'lucide-react';

import { ThemeToggle } from '../components/ThemeToggle';

interface DocLayoutProps {
  children?: React.ReactNode;
}

const PILLAR_NAV = [
  {
    title: 'The Engine (Day 0)',
    items: [
      { id: 'story', label: 'The Trinity Vision', path: '/docs/story', icon: <BookOpen size={18} /> },
      { id: 'getting-started', label: 'Backend Setup', path: '/docs/getting-started', icon: <Cpu size={18} /> },
      { id: 'be-integration', label: 'ADK Integration', path: '/docs/be-integration', icon: <Terminal size={18} /> },
    ]
  },
  {
    title: 'The Face (Day 1)',
    items: [
      { id: 'development', label: 'UI Development', path: '/docs/development', icon: <Layout size={18} /> },
      { id: 'a2a', label: 'A2UI Protocol', path: '/docs/a2a', icon: <BookOpen size={18} /> },
    ]
  },
  {
    title: 'The Cockpit (Day 2)',
    items: [
      { id: 'ops', label: 'The Cockpit', path: '/ops', icon: <Activity size={18} /> },
      { id: 'cli-commands', label: 'Optimizer CLI', path: '/docs/cli-commands', icon: <Terminal size={18} /> },
      { id: 'deployment', label: 'Cloud Deployment', path: '/docs/deployment', icon: <Rocket size={18} /> },
    ]
  }
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
            Optimized Agent Stack
          </Link>
          <button className="mobile-toggle" onClick={() => setSidebarOpen(!isSidebarOpen)}>
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        
        <nav className="doc-nav">
          {PILLAR_NAV.map((group) => (
            <div className="nav-group" key={group.title}>
              <div className="nav-group-title">{group.title}</div>
              {group.items.map((item) => (
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
          ))}



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
