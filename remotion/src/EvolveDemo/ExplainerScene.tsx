import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const ExplainerScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEnter = spring({ frame: frame - 15, fps, config: { damping: 12 } });
  
  // Pillars
  const pillars = [
    { title: 'Governance as Code', desc: 'Surgically audit code for PII leaks, infinite loops, and API vulnerabilities before they ever hit production.', icon: '🛡️' },
    { title: 'Autonomous Remediation', desc: 'Securely isolate, branch, and rewrite entire repository architectures without human intervention.', icon: '⚡' },
    { title: 'Fleet Observability & FinOps', desc: 'Map agent topologies, intercept telemetry, and mathematically downgrade API costs via Shadow ROI.', icon: '🛰️' }
  ];

  return (
    <AbsoluteFill style={{ 
      justifyContent: 'center', 
      alignItems: 'center', 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #0a0a20, #000005 80%)',
      padding: 60
    }}>
      <div style={{
        opacity: titleEnter,
        transform: `translateY(${interpolate(titleEnter, [0, 1], [50, 0])}px)`,
        color: 'white',
        fontSize: 72,
        fontWeight: '900',
        marginBottom: 80,
        textAlign: 'center',
        background: 'linear-gradient(to right, #3b82f6, #a855f7)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent'
      }}>
        What is AgentOps Cockpit?
      </div>
      
      <div style={{ display: 'flex', gap: 40, width: '100%', maxWidth: 1400 }}>
        {pillars.map((p, i) => {
          const pEnter = spring({ frame: frame - 45 - (i * 15), fps, config: { damping: 14 } });
          return (
            <div key={i} style={{
              flex: 1,
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: 24,
              padding: 50,
              opacity: pEnter,
              transform: `translateY(${interpolate(pEnter, [0, 1], [50, 0])}px)`,
              boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: 84, marginBottom: 32 }}>{p.icon}</div>
              <h3 style={{ color: 'white', fontSize: 32, marginBottom: 20 }}>{p.title}</h3>
              <p style={{ color: '#9ca3af', fontSize: 22, lineHeight: 1.6 }}>{p.desc}</p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
