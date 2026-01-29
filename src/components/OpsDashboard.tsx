import React from 'react';
import { FlightRecorder } from './FlightRecorder';
import { Activity, ShieldCheck, Zap, Database, Search, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

export const OpsDashboard: React.FC = () => {
  return (
    <div className="ops-dashboard">
      <header className="ops-header">
        <Link to="/" className="back-link">
          <ArrowLeft size={20} />
          <span>Back to Home</span>
        </Link>
        <div className="flex flex-col">
          <h1 className="text-2xl font-bold tracking-tight">Agent Ops Control Room</h1>
          <p className="opacity-50 text-sm">Real-time visibility into Day 2 Operations</p>
        </div>
        <div className="health-badge">
          <span className="pulse"></span>
          <span>System Stable</span>
        </div>
      </header>

      <div className="ops-grid">
        {/* Shadow Mode Stats */}
        <div className="ops-card glass-panel shadow-vibrant">
          <div className="card-header">
            <div className="icon-box green-glow">
              <ShieldCheck className="text-green-400" size={20} />
            </div>
            <h3>Shadow Mode (v1 vs v2)</h3>
          </div>
          <div className="card-body">
            <div className="comparison-stat">
              <div className="stat-row">
                <span>Production (v1)</span>
                <span className="font-mono text-green-400">98.2% Accuracy</span>
              </div>
              <div className="stat-row">
                <span>Shadow (v2)</span>
                <span className="font-mono text-blue-400">99.1% Confidence</span>
              </div>
            </div>
            <p className="text-xs opacity-50 mt-4">Evaluating Gemini 2.0 Pro with zero-impact.</p>
          </div>
        </div>

        {/* Semantic Cache Hit Rate */}
        <div className="ops-card glass-panel zap-vibrant">
          <div className="card-header">
            <div className="icon-box yellow-glow">
              <Zap className="text-yellow-400" size={20} />
            </div>
            <h3>Hive Mind Cache</h3>
          </div>
          <div className="card-body">
            <div className="big-stat">
              <span className="stat-value text-gradient-yellow">42%</span>
              <span className="stat-label">Hit Rate</span>
            </div>
            <div className="mt-4">
              <div className="flex justify-between text-xs mb-1">
                <span>Total Savings today</span>
                <span className="text-green-400">$24.50</span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill yellow-gradient" style={{ width: '42%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Security / Red Team */}
        <div className="ops-card glass-panel">
          <div className="card-header">
            <Activity className="text-red-400" size={24} />
            <h3>Red Team CI Audit</h3>
          </div>
          <div className="card-body">
            <div className="status-item">
              <ShieldCheck className="text-green-400" size={16} />
              <span>Last Audit: 12 minutes ago</span>
            </div>
            <div className="status-item">
              <ShieldCheck className="text-green-400" size={16} />
              <span>Vulnerabilities: 0 Found</span>
            </div>
            <button className="run-audit-btn">Run Adhoc Audit</button>
          </div>
        </div>

        {/* RAG Dropzone Status */}
        <div className="ops-card glass-panel secure-vibrant">
          <div className="card-header">
            <div className="icon-box purple-glow">
              <Database className="text-purple-400" size={20} />
            </div>
            <h3>RAG Dropzone</h3>
          </div>
          <div className="card-body">
            <div className="flex items-center gap-3">
              <div className="rag-file-icon">
                <Search size={20} />
              </div>
              <div>
                <p className="text-sm font-bold">14 Documents Indexed</p>
                <p className="text-xs opacity-50">Last sync: 1h ago</p>
              </div>
            </div>
            <div className="rag-tags mt-4">
              <span className="tag purple-tag">policies/</span>
              <span className="tag purple-tag">docs/</span>
            </div>
          </div>
        </div>

        {/* MCP Connectivity Hub */}
        <div className="ops-card glass-panel" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="card-header">
            <Search className="text-blue-400" size={24} />
            <h3>MCP Tool Hub</h3>
          </div>
          <div className="card-body">
            <div className="stat-row">
              <span>Connected Tools</span>
              <span className="font-mono">12/12</span>
            </div>
            <div className="stat-row">
              <span>Legacy APIs</span>
              <span className="font-mono text-red-400">1 Warning</span>
            </div>
            <p className="text-xs opacity-50 mt-4">Migrate 'Legacy CRM' to MCP to remove bottleneck.</p>
          </div>
        </div>
      </div>

      {/* Flight Recorder - Taking full width */}
      <div className="ops-bottom-section">
        <FlightRecorder />
      </div>

      <style>{`
        .ops-dashboard {
          padding: 2rem;
          background: var(--bg-color);
          min-height: 100vh;
          color: var(--text-color);
        }
        .ops-header {
          display: flex;
          align-items: center;
          gap: 2rem;
          margin-bottom: 3rem;
        }
        .back-link {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          color: var(--primary-color);
          text-decoration: none;
          font-weight: 600;
          font-size: 0.9rem;
          padding: 0.5rem 1rem;
          background: rgba(var(--primary-color-rgb), 0.1);
          border-radius: 0.75rem;
          transition: all 0.2s;
        }
        .back-link:hover {
          background: rgba(var(--primary-color-rgb), 0.2);
        }
        .health-badge {
          margin-left: auto;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(16, 185, 129, 0.1);
          color: #10b981;
          padding: 0.5rem 1rem;
          border-radius: 2rem;
          font-size: 0.8rem;
          font-weight: bold;
        }
        .pulse {
          width: 8px;
          height: 8px;
          background: #10b981;
          border-radius: 50%;
          animation: ops-pulse 2s infinite;
        }
        @keyframes ops-pulse {
          0% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.5); opacity: 0.4; }
          100% { transform: scale(1); opacity: 1; }
        }
        .ops-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }
        .ops-card {
          padding: 1.5rem;
          border-radius: 1.25rem;
          background: var(--surface-color);
          border: 1px solid var(--border-color);
          transition: transform 0.2s;
        }
        .ops-card:hover {
          transform: translateY(-4px);
        }
        .card-header {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1.5rem;
        }
        .card-header h3 {
          font-size: 0.9rem;
          font-weight: 700;
          opacity: 0.8;
        }
        .stat-row {
          display: flex;
          justify-content: space-between;
          font-size: 0.85rem;
          margin-bottom: 0.5rem;
        }
        .big-stat {
          display: flex;
          align-items: baseline;
          gap: 0.5rem;
        }
        .stat-value {
          font-size: 2.5rem;
          font-weight: 800;
          background: linear-gradient(135deg, var(--text-color), var(--primary-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .stat-label {
          font-size: 0.8rem;
          font-weight: 600;
          opacity: 0.5;
        }
        .progress-bar {
          height: 6px;
          background: var(--border-color);
          border-radius: 3px;
          overflow: hidden;
        }
        .progress-fill {
          height: 100%;
          background: var(--primary-color);
          border-radius: 3px;
        }
        .yellow-gradient {
          background: linear-gradient(90deg, #facc15, #eab308);
          box-shadow: 0 0 10px rgba(234, 179, 8, 0.4);
        }
        .icon-box {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 800;
        }
        .green-glow { background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); box-shadow: 0 8px 16px rgba(34, 197, 94, 0.1); }
        .yellow-glow { background: rgba(234, 179, 8, 0.1); border: 1px solid rgba(234, 179, 8, 0.2); box-shadow: 0 8px 16px rgba(234, 179, 8, 0.1); }
        .purple-glow { background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.2); box-shadow: 0 8px 16px rgba(168, 85, 247, 0.1); }
        .blue-glow { background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); box-shadow: 0 8px 16px rgba(59, 130, 246, 0.1); }
        .red-glow { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); box-shadow: 0 8px 16px rgba(239, 68, 68, 0.1); }

        .text-gradient-yellow {
          background: linear-gradient(135deg, #fef08a, #eab308);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .purple-tag { border-color: rgba(168, 85, 247, 0.4); color: #a855f7; }

        .shadow-vibrant { border-top: 3px solid #22c55e; position: relative; overflow: hidden; }
        .shadow-vibrant::after {
          content: ''; position: absolute; top: -20%; right: -20%; width: 50%; height: 50%;
          background: radial-gradient(circle, rgba(34, 197, 94, 0.08), transparent 70%);
          pointer-events: none;
        }
        .zap-vibrant { border-top: 3px solid #eab308; }
        .zap-vibrant::after {
          content: ''; position: absolute; top: -20%; right: -20%; width: 50%; height: 50%;
          background: radial-gradient(circle, rgba(234, 179, 8, 0.08), transparent 70%);
          pointer-events: none;
        }
        .secure-vibrant { border-top: 3px solid #a855f7; }
        .secure-vibrant::after {
          content: ''; position: absolute; top: -20%; right: -20%; width: 50%; height: 50%;
          background: radial-gradient(circle, rgba(168, 85, 247, 0.08), transparent 70%);
          pointer-events: none;
        }
        
        .ops-card {
          backdrop-filter: blur(24px);
          -webkit-backdrop-filter: blur(24px);
          background: rgba(var(--bg-secondary-rgb), 0.5);
          position: relative;
        }
        .status-item {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.8rem;
          margin-bottom: 0.75rem;
        }
        .run-audit-btn {
          width: 100%;
          margin-top: 0.5rem;
          padding: 0.6rem;
          background: var(--border-color);
          border: none;
          color: var(--text-color);
          border-radius: 0.75rem;
          font-size: 0.75rem;
          font-weight: bold;
          cursor: pointer;
          transition: all 0.2s;
        }
        .run-audit-btn:hover {
          background: var(--primary-color);
          color: white;
        }
        .rag-file-icon {
          width: 40px;
          height: 40px;
          background: rgba(139, 92, 246, 0.1);
          color: #8b5cf6;
          border-radius: 0.75rem;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .rag-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .tag {
          font-size: 0.65rem;
          background: var(--border-color);
          padding: 0.2rem 0.5rem;
          border-radius: 0.4rem;
          font-family: 'JetBrains Mono', monospace;
          opacity: 0.7;
        }
      `}</style>
    </div>
  );
};
