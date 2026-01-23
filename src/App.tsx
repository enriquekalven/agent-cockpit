import React, { useState } from 'react';
import { Routes, Route, Link, Navigate, Outlet } from 'react-router-dom';
import { Activity } from 'lucide-react';
import { A2UISurfaceRenderer } from './a2ui/A2UIRenderer';
import { DocLayout } from './docs/DocLayout';
import { DocPage } from './docs/DocPage';
import { ThemeToggle } from './components/ThemeToggle';
import { Home } from './components/Home';
import { OpsDashboard } from './components/OpsDashboard';
import './index.css';

const SAMPLE_A2UI_SURFACE = {
  surfaceId: 'welcome-surface',
  content: [
    {
      type: 'Text',
      props: { text: 'Optimized Agent Stack', variant: 'h1' },
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

const RANDOM_TEMPLATES = [
  {
    name: 'Shopping Cart',
    json: {
      surfaceId: 'shopping-cart',
      content: [
        { type: 'Text', props: { text: '🛒 Your Shopping Cart', variant: 'h1' } },
        {
          type: 'Card',
          props: { title: 'Agent-Enhanced Checkout' },
          children: [
            { type: 'Image', props: { src: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&q=80&w=400', alt: 'Smart Watch', caption: '✨ Premium Smart Watch - $299.00' } },
            { type: 'List', props: { title: 'Order Summary', items: ['⌚ Smart Watch: $299.00', '🚚 Shipping: $0.00', '💸 Tax: $24.50'] } },
            { type: 'Button', props: { label: 'Confirm Order ($323.50) 💳', variant: 'primary' } }
          ]
        }
      ]
    }
  },
  {
    name: 'Weather Forecast',
    json: {
      surfaceId: 'weather-forecast',
      content: [
        { type: 'Text', props: { text: '🌉 San Francisco Weather', variant: 'h1' } },
        {
          type: 'Card',
          props: { title: 'Weekly Outlook' },
          children: [
            { type: 'Text', props: { text: 'Currently: 62°F | Partly Cloudy ⛅', variant: 'h2' } },
            { type: 'StatBar', props: { label: 'Humidity', value: 78, color: '#3b82f6' } },
            { type: 'StatBar', props: { label: 'UV Index', value: 45, color: '#f59e0b' } },
            { type: 'List', props: { items: ['Monday: ☀️ 72°F', 'Tuesday: 🌤️ 68°F', 'Wednesday: ☁️ 64°F', 'Thursday: 🌧️ 58°F', 'Friday: ⛅ 62°F'] } }
          ]
        }
      ]
    }
  },
  {
    name: 'Server Dashboard',
    json: {
      surfaceId: 'server-dashboard',
      content: [
        { type: 'Text', props: { text: '🖥️ Infrastructure Overview', variant: 'h1' } },
        {
          type: 'Card',
          props: { title: 'Global Traffic' },
          children: [
            { type: 'Image', props: { src: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=600', alt: 'World Map', caption: 'Live Global Data Mesh' } },
            { type: 'StatBar', props: { label: 'Traffic Load', value: 65, color: '#10b981' } },
            { type: 'StatBar', props: { label: 'Error Rate', value: 2, color: '#ef4444' } }
          ]
        }
      ]
    }
  }
];

function Playground() {
  const [jsonText, setJsonText] = useState(JSON.stringify(SAMPLE_A2UI_SURFACE, null, 2));
  const [surface, setSurface] = useState(SAMPLE_A2UI_SURFACE);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<'editor' | 'agent'>('editor');
  const [chatInput, setChatInput] = useState('');
  const [messages, setMessages] = useState<any[]>([]);

  const handleJsonChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value;
    setJsonText(newText);
    try {
      const parsed = JSON.parse(newText);
      setSurface(parsed);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const generateRandomJson = () => {
    const template = RANDOM_TEMPLATES[Math.floor(Math.random() * RANDOM_TEMPLATES.length)];
    setSurface(template.json as any);
    setJsonText(JSON.stringify(template.json, null, 2));
    setError(null);
  };

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;
    
    const newMsg = { role: 'user', text: chatInput };
    setMessages([...messages, newMsg]);
    setChatInput('');

    // Simulate agent response
    setTimeout(async () => {
      const lowerInput = chatInput.toLowerCase();
      let responseText = "I've updated your view based on your request.";
      let newSurface = { ...surface };

      if ((window as any).USE_REAL_BE) {
        try {
          const res = await fetch(`http://localhost:8000/agent/query?q=${encodeURIComponent(chatInput)}`);
          if (res.ok) {
            newSurface = await res.json();
            responseText = "Received live A2UI from your ADK agent.";
          }
        } catch (err) {
          responseText = "Error connecting to local backend at port 8000. Is the agent running?";
        }
      } else {
        if (lowerInput.includes('chart') || lowerInput.includes('stats') || lowerInput.includes('metrics')) {
          responseText = "📊 I've generated a real-time system health report with visual diagnostics.";
          newSurface = {
            surfaceId: 'system-report',
            content: [
              { type: 'Text', props: { text: '⚡ Infrastructure Health Metrics', variant: 'h1' } },
              { 
                type: 'Card', 
                props: { title: 'Live Performance 📈' }, 
                children: [
                  { type: 'StatBar', props: { label: 'Network Load', value: 45, color: '#3b82f6' } },
                  { type: 'StatBar', props: { label: 'CPU Usage', value: 12, color: '#10b981' } },
                  { type: 'StatBar', props: { label: 'Memory Reserved', value: 72, color: '#f59e0b' } },
                  { type: 'List', props: { items: ['Pod-A: ✅ Ready', 'Pod-B: ✅ Ready', 'Pod-C: 🔄 Scaling'] } }
                ]
              },
              {
                type: 'Card',
                props: { title: 'Node Status 🏢' },
                children: [
                  { type: 'Image', props: { src: 'https://images.unsplash.com/photo-1558494949-ef010cbdcc51?auto=format&fit=crop&q=80&w=400', alt: 'Server', caption: 'Primary Cluster Node' } },
                  { type: 'Text', props: { text: 'All systems operational in us-central1.', variant: 'body' } }
                ]
              }
            ]
          } as any;
        } else if (lowerInput.includes('dark') || lowerInput.includes('theme')) {
          responseText = "🌙 Switching to dark mode patterns.";
        } else {
          responseText = `🤖 I understand you want to: ${chatInput}. I've updated the canvas.`;
          newSurface = {
            ...surface,
            content: [
              ...surface.content,
              { type: 'Card', props: { title: 'Dynamic Response ✨' }, children: [{ type: 'Text', props: { text: `Simulated response for: ${chatInput}`, variant: 'body' }}]}
            ]
          };
        }
      }
      
      const agentMsg = { role: 'agent', text: responseText };
      setMessages(prev => [...prev, agentMsg]);
      setSurface(newSurface);
      setJsonText(JSON.stringify(newSurface, null, 2));
    }, 1000);
  };

  return (
    <div className="playground-container">
      <header className="app-header">
        <div className="agent-status">
          <span className="agent-pulse"></span>
          <span className="status-text">Optimized Agent Stack</span>
        </div>
        <div className="mode-toggle">
          <button className={mode === 'editor' ? 'active' : ''} onClick={() => setMode('editor')}>Editor</button>
          <button className={mode === 'agent' ? 'active' : ''} onClick={() => setMode('agent')}>Agent Mode</button>
        </div>
        <nav className="header-nav">
          <Link to="/docs" className="nav-link">← Back to Docs</Link>
          <Link to="/ops" className="nav-link special-alt" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Activity size={14} /> Agent Ops Dashboard
          </Link>
          <ThemeToggle />
          <a href="/docs/be-integration" className="nav-link special">Connect to Agent →</a>
        </nav>
      </header>
      
      <div className="playground-main">
        {mode === 'editor' ? (
          <div className="editor-pane">
            <div className="editor-header">
              <span className="editor-label">A2UI JSON Blueprint</span>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button className="feature-btn mini" onClick={generateRandomJson}>Random</button>
                {error && <span className="error-badge">Invalid</span>}
              </div>
            </div>
            <textarea
              className="json-textarea"
              value={jsonText}
              onChange={handleJsonChange}
              spellCheck={false}
            />
          </div>
        ) : (
          <div className="agent-pane">
              <div className="editor-header">
                <span className="editor-label">Agent Logic Console</span>
            </div>
            <div className="chat-history">
              {messages.length === 0 && <p className="empty-chat">Ask the agent to modify the UI (e.g., "Show me some stats")</p>}
              {messages.map((m, i) => (
                <div key={i} className={`chat-message ${m.role}`}>
                  <div className="msg-bubble">{m.text}</div>
                </div>
              ))}
            </div>
            <div className="chat-input-area">
              <input 
                type="text" 
                placeholder="Talk to the agent..." 
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              />
                <button onClick={handleSendMessage}>SEND</button>
            </div>
          </div>
        )}

        {/* Live Preview */}
        <div className="live-preview-pane">
          <div className="preview-header">
            <span className="editor-label">Adaptive Interface Preview</span>
            <div className="agent-status" style={{ border: 'none', padding: 0 }}>
              <span className="agent-pulse"></span>
              <span className="status-text" style={{ fontSize: '0.7rem' }}>Live</span>
            </div>
          </div>
          <div className="preview-canvas">
            {error ? (
              <div className="parse-error">
                <p>Error parsing A2UI JSON:</p>
                <code>{error}</code>
              </div>
            ) : (
              <A2UISurfaceRenderer surface={surface} />
            )}
          </div>
          <div className="backend-settings-overlay">
            <label>
              <input type="checkbox" onChange={(e) => (window as any).USE_REAL_BE = e.target.checked} />
              Connect to Local ADK Agent
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/docs" element={<DocLayout />}>
        <Route index element={<Navigate to="/docs/getting-started" replace />} />
        <Route path=":docId" element={<DocPage />} />
      </Route>

      <Route path="/playground" element={<Playground />} />
      <Route path="/ops" element={<OpsDashboard />} />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
