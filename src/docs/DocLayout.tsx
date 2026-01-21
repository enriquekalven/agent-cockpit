import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, ChevronRight, BookOpen, Terminal, Rocket, Cpu, Layout } from 'lucide-react';

interface DocLayoutProps {
  children: React.ReactNode;
}

const DOC_NAV = [
  { id: 'readme', label: 'Getting Started', path: '/', icon: <Rocket size={18} /> },
  { id: 'a2a', label: 'A2A Protocol', path: '/docs/a2a', icon: <Cpu size={18} /> },
  { id: 'deployment', label: 'Deployment', path: '/docs/deployment', icon: <Terminal size={18} /> },
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
            A2UI Docs
          </Link>
          <button className="mobile-toggle" onClick={() => setSidebarOpen(!isSidebarOpen)}>
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
        
        <nav className="doc-nav">
          <div className="nav-group">
            <div className="nav-group-title">Documentation</div>
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
            <div className="nav-group-title">Sandbox</div>
            <Link to="/playground" className="nav-item">
              <Layout size={18} />
              <span>A2UI Playground</span>
            </Link>
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
            <span>Docs</span>
          </div>
        </header>
        <div className="doc-content-wrapper">
          {children}
        </div>
      </main>
    </div>
  );
};
