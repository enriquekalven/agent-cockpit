import React, { useState, useEffect } from 'react';
import { Play, Square, FastForward, Rewind, Activity, ShieldCheck, Zap } from 'lucide-react';

interface Trace {
  timestamp: string;
  query: string;
  steps: {
    name: string;
    input: string;
    output: string;
    latency: number;
    status: 'success' | 'error';
  }[];
}

export const FlightRecorder: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // Mock trace data
  const mockTrace: Trace = {
    timestamp: new Date().toISOString(),
    query: "Optimize my cloud storage costs",
    steps: [
      { name: "Semantic Cache Check", input: "Optimize cloud storage costs", output: "MISS", latency: 0.1, status: 'success' },
      { name: "Context Retrieval", input: "storage-policy-h1", output: "Found 2 related documents in RAG", latency: 0.4, status: 'success' },
      { name: "LLM Reasoning (Gemini Pro)", input: "Analyze storage policies...", output: "Suggesting lifecycle policy update.", latency: 1.2, status: 'success' },
      { name: "A2UI Generation", input: "Policy JSON", output: "Dashboard Blueprint Created", latency: 0.2, status: 'success' }
    ]
  };

  const steps = mockTrace.steps;

  return (
    <div className="flight-recorder glass-panel">
      <div className="recorder-header">
        <div className="flex items-center gap-2">
          <div className="pulse-dot"></div>
          <h3 className="text-sm font-bold uppercase tracking-widest text-primary-color">The Black Box Flight Recorder</h3>
        </div>
        <div className="trace-info flex gap-4 text-xs opacity-70">
          <span>Trace ID: TR-2947-AX</span>
          <span>Query: "{mockTrace.query}"</span>
        </div>
      </div>

      <div className="recorder-timeline">
        {steps.map((step, idx) => (
          <div 
            key={idx} 
            className={`timeline-node ${idx <= currentStep ? 'active' : ''} ${step.status}`}
            onClick={() => setCurrentStep(idx)}
          >
            <div className="node-icon">
              {idx === 0 ? <Zap size={14} /> : idx === 1 ? <Activity size={14} /> : <ShieldCheck size={14} />}
            </div>
            <div className="node-label">{step.name}</div>
          </div>
        ))}
      </div>

      <div className="recorder-viewport">
        <div className="viewport-aside">
          <div className="control-group">
            <button className="icon-btn" onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}>
              <Rewind size={18} />
            </button>
            <button className="icon-btn primary" onClick={() => setIsPlaying(!isPlaying)}>
              {isPlaying ? <Square size={18} /> : <Play size={18} />}
            </button>
            <button className="icon-btn" onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}>
              <FastForward size={18} />
            </button>
          </div>

          <div className="stats-group">
            <div className="stat">
              <span className="label">Step Latency</span>
              <span className="value">{steps[currentStep].latency}s</span>
            </div>
          </div>
        </div>

        <div className="viewport-main">
          <div className="io-panel">
            <div className="io-section">
              <span className="section-label">Input Payload</span>
              <pre className="code-block">{steps[currentStep].input}</pre>
            </div>
            <div className="io-section mt-4">
              <span className="section-label">Output / Result</span>
              <pre className="code-block highlight">{steps[currentStep].output}</pre>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .flight-recorder {
          margin-top: 2rem;
          background: var(--surface-color);
          border: 1px solid var(--border-color);
          border-radius: 1.5rem;
          overflow: hidden;
          padding: 1.5rem;
        }
        .recorder-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
        }
        .recorder-timeline {
          display: flex;
          justify-content: space-between;
          position: relative;
          margin-bottom: 2rem;
          padding: 0 2rem;
        }
        .recorder-timeline::before {
          content: '';
          position: absolute;
          top: 15px;
          left: 3rem;
          right: 3rem;
          height: 2px;
          background: var(--border-color);
          z-index: 0;
        }
        .timeline-node {
          position: relative;
          z-index: 1;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.5rem;
          cursor: pointer;
        }
        .node-icon {
          width: 32px;
          height: 32px;
          background: var(--bg-color);
          border: 2px solid var(--border-color);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
        }
        .timeline-node.active .node-icon {
          border-color: var(--primary-color);
          box-shadow: 0 0 15px var(--glow-color);
          background: var(--primary-color);
          color: white;
        }
        .node-label {
          font-size: 0.65rem;
          font-weight: 600;
          opacity: 0.5;
          text-transform: uppercase;
        }
        .timeline-node.active .node-label {
          opacity: 1;
          color: var(--primary-color);
        }
        .recorder-viewport {
          display: grid;
          grid-template-columns: 200px 1fr;
          gap: 1.5rem;
          background: rgba(0,0,0,0.05);
          border-radius: 1rem;
          padding: 1.5rem;
          border: 1px solid var(--border-color);
        }
        .control-group {
          display: flex;
          gap: 0.5rem;
          margin-bottom: 2rem;
        }
        .icon-btn {
          background: var(--surface-color);
          border: 1px solid var(--border-color);
          border-radius: 0.5rem;
          padding: 0.5rem;
          cursor: pointer;
          color: var(--text-color);
          transition: all 0.2s;
        }
        .icon-btn.primary {
          background: var(--primary-color);
          color: white;
          border: none;
        }
        .section-label {
          font-size: 0.6rem;
          font-weight: 800;
          text-transform: uppercase;
          opacity: 0.4;
          margin-bottom: 0.5rem;
          display: block;
        }
        .code-block {
          background: var(--bg-color);
          padding: 1rem;
          border-radius: 0.75rem;
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.75rem;
          border: 1px solid var(--border-color);
          white-space: pre-wrap;
          word-break: break-all;
        }
        .code-block.highlight {
          border-color: var(--primary-color);
          background: rgba(var(--primary-color-rgb), 0.05);
        }
        .pulse-dot {
          width: 8px;
          height: 8px;
          background: #ff4d4d;
          border-radius: 50%;
          animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.5); opacity: 0.5; }
          100% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
};
