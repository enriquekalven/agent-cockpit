import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
} from 'remotion';

export const TargetAudienceScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Smooth Animations
  const entrance = spring({ frame, fps, config: { damping: 12 } });
  const slideX = interpolate(entrance, [0, 1], [100, 0]);
  const opacity = interpolate(entrance, [0.2, 1], [0, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#0f172a',
      color: 'white',
      fontFamily: 'system-ui, sans-serif',
      overflow: 'hidden'
    }}>
      {/* Subtle Animated Gradient Background */}
      <div style={{
        position: 'absolute',
        inset: 0,
        background: 'radial-gradient(circle at 50% 30%, rgba(6,182,212,0.15), transparent 60%)',
        zIndex: 0
      }} />

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        padding: '80px 120px',
        height: '100%',
        zIndex: 1,
        transform: `translateY(${slideX}px)`,
        opacity,
      }}>
        {/* Header: Executive Statement */}
        <div style={{ marginBottom: '60px' }}>
          <h1 style={{
            fontSize: '72px',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            margin: 0,
            background: 'linear-gradient(to right, #fff, #94a3b8)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            🎯 Target Audience: Who Uses the Cockpit?
          </h1>
          <p style={{
            fontSize: '28px',
            color: '#cbd5e1',
            marginTop: '20px',
            lineHeight: '1.6',
            maxWidth: '1400px'
          }}>
            While tools like <strong>Claude Code</strong> and <strong>Cursor</strong> are excellent for 
            <span style={{ color: '#38bdf8' }}> Day-1 Prototyping</span>, the AgentOps Cockpit is explicitly built for 
            <span style={{ color: '#10b981' }}> Day-2 Enterprise Operations & Platform Governance</span>.
          </p>
        </div>

        {/* Three Pillars Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '40px',
          flex: 1,
          marginBottom: '40px'
        }}>
          {/* Pillar 1: SRE / Platform Engineers */}
          <div style={{
            background: 'rgba(30, 41, 59, 0.7)',
            backdropFilter: 'blur(16px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '24px',
            padding: '40px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🛡️</div>
              <h3 style={{ fontSize: '32px', margin: '0 0 16px 0', color: '#38bdf8' }}>
                SREs & Platform Engineers
              </h3>
              <div style={{ marginBottom: '24px', fontSize: '20px', color: '#94a3b8' }}>
                <strong>Problem:</strong> Fragile local prototypes break under multi-cloud scaling and concurrent load.
              </div>
            </div>
            <div style={{
              background: 'rgba(56, 189, 248, 0.1)',
              border: '1px solid rgba(56, 189, 248, 0.2)',
              padding: '20px',
              borderRadius: '16px',
              fontSize: '20px',
              color: '#e0f2fe'
            }}>
              <strong>Cockpit Solution:</strong> Autonomous Release Engine (Zero2Hero), Load Testing, and automated Multi-cloud assets.
            </div>
          </div>

          {/* Pillar 2: Red Teams & Security */}
          <div style={{
            background: 'rgba(30, 41, 59, 0.7)',
            backdropFilter: 'blur(16px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '24px',
            padding: '40px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🚨</div>
              <h3 style={{ fontSize: '32px', margin: '0 0 16px 0', color: '#f43f5e' }}>
                Red Teams & AI Auditors
              </h3>
              <div style={{ marginBottom: '24px', fontSize: '20px', color: '#94a3b8' }}>
                <strong>Problem:</strong> Unregulated AI skills miss ISO/Brand Safety compliance and prompt injection sweeps.
              </div>
            </div>
            <div style={{
              background: 'rgba(244, 63, 94, 0.1)',
              border: '1px solid rgba(244, 63, 94, 0.2)',
              padding: '20px',
              borderRadius: '16px',
              fontSize: '20px',
              color: '#ffe4e6'
            }}>
              <strong>Cockpit Solution:</strong> Brand Safety Playbooks via <code>audit security</code> before code hits merge phase.
            </div>
          </div>

          {/* Pillar 3: FinOps & Strategy */}
          <div style={{
            background: 'rgba(30, 41, 59, 0.7)',
            backdropFilter: 'blur(16px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '24px',
            padding: '40px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>💰</div>
              <h3 style={{ fontSize: '32px', margin: '0 0 16px 0', color: '#10b981' }}>
                FinOps Leads & Strategists
              </h3>
              <div style={{ marginBottom: '24px', fontSize: '20px', color: '#94a3b8' }}>
                <strong>Problem:</strong> Local token usage creates heavy OpEx liabilities when scaled to enterprise volumes.
              </div>
            </div>
            <div style={{
              background: 'rgba(16, 185, 129, 0.1)',
              border: '1px solid rgba(16, 185, 129, 0.2)',
              padding: '20px',
              borderRadius: '16px',
              fontSize: '20px',
              color: '#d1fae5'
            }}>
              <strong>Cockpit Solution:</strong> ROI Waterfall simulations via <code>audit roi</code> and caching pivots.
            </div>
          </div>
        </div>

        {/* Footer: Executive Summary */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '24px 40px',
          background: 'linear-gradient(90deg, rgba(59, 130, 246, 0.2), rgba(16, 185, 129, 0.2))',
          border: '1px solid rgba(255,255,255,0.1)',
          borderRadius: '16px'
        }}>
          <div style={{ fontSize: '24px', color: '#fff' }}>
            🎨 <strong>Vibe Coding</strong> is for the <span style={{ color: '#60a5fa' }}>Creator</span> (Velocity).
          </div>
          <div style={{ fontSize: '24px', color: '#fff' }}>
            🛡️ <strong>AgentOps Cockpit</strong> is for the <span style={{ color: '#34d399' }}>Ecosystem</span> (Reliability, Economics, Security).
          </div>
        </div>

      </div>
    </AbsoluteFill>
  );
};
