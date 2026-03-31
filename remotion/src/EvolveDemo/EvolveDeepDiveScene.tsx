import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const EvolveDeepDiveScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEnter = spring({ frame: frame - 15, fps, config: { damping: 12 } });
  const subtitleEnter = spring({ frame: frame - 25, fps, config: { damping: 12 } });
  
  // Pillars
  const pillars = [
    { 
      title: '🏗️ Architectural Refactoring',
      desc: 'Injects modular routers to split "Spaghetti Agents" and refactors passive retrieval into managed RAG "decider logic".'
    },
    { 
      title: '📈 Reliability Enhancements',
      desc: 'Scaffolds retry loops, exponential backoff, telemetry (logger.ts, trace.ts), and Poka-Yoke tool guardrails.'
    },
    { 
      title: '💰 FinOps Upgrades',
      desc: 'Injects Gemini Context-Caching optimizations directly into payloads to drastically lower token costs and boost speed.'
    },
    { 
      title: '🛡️ Security & Compliance',
      desc: 'Autonomously scaffolds declarative guardrail engines and tool_privilege_check gates to prevent lateral movement.'
    }
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
        marginBottom: 20,
        textAlign: 'center',
        background: 'linear-gradient(to right, #3b82f6, #10b981)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent'
      }}>
        The Closer Engine: Beyond Security
      </div>
      
      <div style={{
        opacity: subtitleEnter,
        transform: `translateY(${interpolate(subtitleEnter, [0, 1], [30, 0])}px)`,
        color: '#9ca3af',
        fontSize: 28,
        fontWeight: '500',
        marginBottom: 80,
        textAlign: 'center',
        maxWidth: 1200,
        lineHeight: 1.5
      }}>
        Command an Autonomous Evolution that injects enterprise-grade boilerplate<br/>to transform prototypes into production-ready deployments.
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, width: '100%', maxWidth: 1400 }}>
        {pillars.map((p, i) => {
          const pEnter = spring({ frame: frame - 45 - (i * 10), fps, config: { damping: 14 } });
          return (
            <div key={i} style={{
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: 24,
              padding: 40,
              opacity: pEnter,
              transform: `translateY(${interpolate(pEnter, [0, 1], [50, 0])}px)`,
              boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center'
            }}>
              <h3 style={{ color: 'white', fontSize: 28, marginBottom: 16 }}>{p.title}</h3>
              <p style={{ color: '#9ca3af', fontSize: 20, lineHeight: 1.6, margin: 0 }}>{p.desc}</p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
