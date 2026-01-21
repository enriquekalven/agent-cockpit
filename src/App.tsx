import React, { useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { A2UISurfaceRenderer } from './a2ui/A2UIRenderer';
import { DocLayout } from './docs/DocLayout';
import { DocPage } from './docs/DocPage';
import './index.css';

const SAMPLE_A2UI_SURFACE = {
  surfaceId: 'welcome-surface',
  content: [
    {
      type: 'Text',
      props: { text: 'Agent UI Starter Pack', variant: 'h1' },
    },
    {
      type: 'Card',
      props: { title: 'System Status' },
      children: [
        {
          type: 'Text',
          props: { text: 'Your agent is active and ready to generate interfaces. This dashboard is rendered using the A2UI protocol standard.', variant: 'body' },
        },
        {
          type: 'Button',
          props: { label: 'Explore Features', variant: 'primary' },
        },
      ],
    },
    {
      type: 'Card',
      props: { title: 'Recent Activity' },
      children: [
        {
          type: 'Text',
          props: { text: 'No recent agent activity detected.', variant: 'body' },
        },
      ],
    },
  ],
};

function Playground() {
  const [surface] = useState(SAMPLE_A2UI_SURFACE);

  return (
    <div className="App">
      <header className="app-header">
        <div className="agent-status">
          <span className="agent-pulse"></span>
          <span className="status-text">Agent Online</span>
        </div>
        <nav className="header-nav">
          <Link to="/docs/readme" className="nav-link">Documentation</Link>
          <a href="https://github.com/enriquekalven/agent-ui-starter-pack" target="_blank" rel="noopener noreferrer" className="nav-link">GitHub</a>
        </nav>
      </header>
      <main>
        <A2UISurfaceRenderer surface={surface} />
      </main>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Playground />} />
      <Route path="/docs" element={<DocLayout><DocPage /></DocLayout>}>
        <Route path=":docId" element={<DocPage />} />
      </Route>
      {/* Fallback */}
      <Route path="*" element={<Link to="/">Go Home</Link>} />
    </Routes>
  );
}

export default App;
