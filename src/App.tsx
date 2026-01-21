import React, { useState } from 'react';
import { A2UISurfaceRenderer } from './a2ui/A2UIRenderer';
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
          props: { text: 'No recent agent actions detected. Try prompting your agent to generate a new surface.', variant: 'body' },
        },
      ],
    },
  ],
};

function App() {
  const [surface] = useState(SAMPLE_A2UI_SURFACE);

  return (
    <div className="App">
      <header style={{ padding: '2rem', textAlign: 'center' }}>
        <div className="agent-status" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
          <span className="agent-pulse"></span>
          <span style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Agent Online</span>
        </div>
      </header>
      <main>
        <A2UISurfaceRenderer surface={surface} />
      </main>
    </div>
  );
}

export default App;
