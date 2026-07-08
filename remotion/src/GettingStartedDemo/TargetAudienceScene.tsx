import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  spring,
  useVideoConfig,
  Sequence,
  Audio,
  staticFile
} from 'remotion';

// Individual Audience Card
const AudienceCard: React.FC<{
  delay: number;
  icon: string;
  title: string;
  problem: string;
  solution: string;
  borderColor: string;
  glowColor: string;
}> = ({ delay, icon, title, problem, solution, borderColor, glowColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const anim = spring({
    frame: frame - delay,
    fps,
    config: { damping: 14, mass: 0.8 },
  });

  const opacity = interpolate(anim, [0, 1], [0, 1]);
  const scale = interpolate(anim, [0, 1], [0.85, 1]);
  const translateY = interpolate(anim, [0, 1], [50, 0]);

  return (
    <div style={{
      background: 'rgba(30, 41, 59, 0.85)',
      backdropFilter: 'blur(24px)',
      border: `2px solid ${borderColor}`,
      borderRadius: '24px',
      padding: '40px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      opacity,
      transform: `scale(${scale}) translateY(${translateY}px)`,
      boxShadow: `0 10px 40px -10px ${glowColor}`,
      height: '450px',
    }}>
      <div>
        <div style={{ fontSize: '56px', marginBottom: '20px' }}>{icon}</div>
        <h3 style={{ fontSize: '36px', margin: '0 0 20px 0', color: borderColor }}>
          {title}
        </h3>
        <p style={{ fontSize: '22px', color: '#e2e8f0', lineHeight: '1.6', margin: 0 }}>
          <strong style={{ color: '#f87171' }}>The Problem:</strong> {problem}
        </p>
      </div>
      <div style={{
        background: `rgba(255,255,255,0.03)`,
        borderTop: `1px solid rgba(255,255,255,0.1)`,
        padding: '24px',
        borderRadius: '16px',
        marginTop: '20px',
        fontSize: '20px',
        color: '#10b981'
      }}>
        <strong style={{ color: '#34d399' }}>Cockpit Solution:</strong> {solution}
      </div>
    </div>
  );
};

export const TargetAudienceScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Scene 1 (Intro) exit transition
  const introFadeOut = spring({ frame: frame - 100, fps, config: { damping: 10 } });
  const introOpacity = interpolate(introFadeOut, [0, 1], [1, 0]);

  // Scene 3 (Outro) entrance transition
  const outroAnim = spring({ frame: frame - 470, fps, config: { damping: 12 } });
  const outroOpacity = interpolate(outroAnim, [0, 1], [0, 1]);
  const outroScale = interpolate(outroAnim, [0, 1], [0.9, 1]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#090d16',
      color: 'white',
      fontFamily: 'system-ui, sans-serif',
      overflow: 'hidden'
    }}>
      {/* Audio Backdrop */}
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />

      {/* Beautiful Moving Ambient Light Source */}
      <div style={{
        position: 'absolute',
        inset: -200,
        background: 'radial-gradient(circle at 30% 20%, rgba(16, 185, 129, 0.1), transparent 50%), radial-gradient(circle at 70% 80%, rgba(59, 130, 246, 0.1), transparent 50%)',
        filter: 'blur(80px)',
        zIndex: 0
      }} />

      {/* ==================== SCENE 1: INTRO (Frames 0 - 120) ==================== */}
      <Sequence durationInFrames={120}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100%',
          width: '100%',
          opacity: introOpacity,
          zIndex: 2
        }}>
          <div style={{
            fontSize: '100px',
            fontWeight: 900,
            letterSpacing: '-0.04em',
            background: 'linear-gradient(135deg, #60a5fa, #34d399)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '24px'
          }}>
            AgentOps Cockpit
          </div>
          <div style={{ fontSize: '32px', color: '#94a3b8', fontWeight: 500, letterSpacing: '0.1em' }}>
            Evolving Individual Contributor Agents into Enterprise Operational Fleets.
          </div>
        </div>
      </Sequence>

      {/* ==================== SCENE 2: THREE-PILLAR COMPARISON (Frames 120 - 480) ==================== */}
      <Sequence from={120} durationInFrames={360}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          padding: '80px 120px',
          height: '100%',
          width: '100%',
          zIndex: 1,
        }}>
          {/* Header */}
          <div style={{ marginBottom: '60px' }}>
            <div style={{
              display: 'inline-block',
              background: 'rgba(255,255,255,0.1)',
              padding: '8px 24px',
              borderRadius: '40px',
              fontSize: '18px',
              fontWeight: 600,
              letterSpacing: '0.1em',
              textTransform: 'uppercase',
              marginBottom: '20px',
              color: '#38bdf8'
            }}>
              Day-2 Governance Platform
            </div>
            <h1 style={{
              fontSize: '76px',
              fontWeight: 800,
              letterSpacing: '-0.03em',
              margin: 0,
              background: 'linear-gradient(to right, #ffffff, #94a3b8)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              🎯 Target Audience: Who Uses the Cockpit?
            </h1>
          </div>

          {/* Carousel Grid */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '40px',
            flex: 1,
          }}>
            <AudienceCard
              delay={135}
              icon="🛡️"
              title="Enterprise SREs"
              problem="Vibe-coding creates single-machine prototypes that fail under concurrent multi-cloud traffic."
              solution="Autonomous Release Engine (Zero2Hero) & structural binary gates for deployments."
              borderColor="#38bdf8"
              glowColor="rgba(56, 189, 248, 0.15)"
            />

            <AudienceCard
              delay={145}
              icon="🚨"
              title="Security Auditors"
              problem="Individual developers rarely test for adversarial attacks, jailbreaks, or domain drift."
              solution="Dedicated checks via 'audit security' for active Brand Safety Playbooks & payload splitting."
              borderColor="#f43f5e"
              glowColor="rgba(244, 63, 94, 0.15)"
            />

            <AudienceCard
              delay={155}
              icon="💰"
              title="FinOps Strategy"
              problem="Scaling 1.5M token dev sessions to enterprise volume creates heavy authorized OpEx liabilities."
              solution="ROI Waterfalls via 'audit roi', optimizing model tiers & semantic context caching pivots."
              borderColor="#10b981"
              glowColor="rgba(16, 185, 129, 0.15)"
            />
          </div>
        </div>
      </Sequence>

      {/* ==================== SCENE 3: OUTRO / CALL TO ACTION (Frames 480 - 600) ==================== */}
      <Sequence from={480}>
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100%',
          width: '100%',
          opacity: outroOpacity,
          transform: `scale(${outroScale})`,
          zIndex: 2
        }}>
          {/* Sleek AgentOps Shield Logo / CTA */}
          <div style={{ fontSize: '80px', marginBottom: '24px' }}>🛰️</div>
          <div style={{
            fontSize: '56px',
            fontWeight: 800,
            color: '#ffffff',
            marginBottom: '16px',
            letterSpacing: '-0.02em'
          }}>
            Ship SRE-Ready Autonomous Agents.
          </div>
          <div style={{
            fontSize: '24px',
            color: '#94a3b8',
            fontFamily: 'monospace',
            background: 'rgba(255,255,255,0.05)',
            padding: '16px 32px',
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.1)'
          }}>
            uvx agentops-cockpit cockpit
          </div>
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
