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

// Individual Card Component with distinct animation timing
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

  // Global Entrance Animation
  const headerAnim = spring({ frame, fps, config: { damping: 12 } });
  const headerOpacity = interpolate(headerAnim, [0, 1], [0, 1]);
  const headerY = interpolate(headerAnim, [0, 1], [-40, 0]);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#090d16',
      color: 'white',
      fontFamily: 'system-ui, sans-serif',
      overflow: 'hidden'
    }}>
      {/* Ambient Audio Track (Mocked via standard static file/theme) */}
      <Audio src={staticFile('background_beat.mp3')} volume={0.4} />

      {/* Gorgeous Moving Background Blob */}
      <div style={{
        position: 'absolute',
        inset: -200,
        background: 'radial-gradient(circle at 30% 20%, rgba(16, 185, 129, 0.1), transparent 50%), radial-gradient(circle at 70% 80%, rgba(59, 130, 246, 0.1), transparent 50%)',
        filter: 'blur(80px)',
        zIndex: 0
      }} />

      <div style={{
        display: 'flex',
        flexDirection: 'column',
        padding: '80px 120px',
        height: '100%',
        zIndex: 1,
      }}>
        {/* Animated Header & Breadcrumb */}
        <div style={{
          opacity: headerOpacity,
          transform: `translateY(${headerY}px)`,
          marginBottom: '60px'
        }}>
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

        {/* Multi-card Sequence Carousel (Staggered Entrances) */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '40px',
          flex: 1,
        }}>
          {/* SRE Card: Animates at frame 15 */}
          <AudienceCard
            delay={15}
            icon="🛡️"
            title="Enterprise SREs"
            problem="Vibe-coding creates fragile, single-machine prototypes that fail under concurrent multi-cloud traffic."
            solution="Autonomous Release Engine (Zero2Hero) & structural binary gates for serverless deployments."
            borderColor="#38bdf8"
            glowColor="rgba(56, 189, 248, 0.15)"
          />

          {/* Red Team Card: Animates at frame 35 */}
          <AudienceCard
            delay={35}
            icon="🚨"
            title="Security & Red Teams"
            problem="Individual developers rarely test for advanced adversarial attacks, jailbreaks, or domain drift."
            solution="Dedicated auditing via 'audit security' for active Brand Safety Playbooks & payload splitting tests."
            borderColor="#f43f5e"
            glowColor="rgba(244, 63, 94, 0.15)"
          />

          {/* FinOps Card: Animates at frame 55 */}
          <AudienceCard
            delay={55}
            icon="💰"
            title="FinOps & Strategists"
            problem="Scaling 1.5M token dev sessions to enterprise volume creates huge unauthorized economic liabilities."
            solution="FinOps ROI Waterfalls modeling optimal model tiers & semantic context caching pivots."
            borderColor="#10b981"
            glowColor="rgba(16, 185, 129, 0.15)"
          />
        </div>

        {/* Staggered Animated Footer at frame 75 */}
        <Sequence from={75}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '28px 48px',
            background: 'linear-gradient(90deg, rgba(59, 130, 246, 0.2), rgba(16, 185, 129, 0.2))',
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: '20px',
            marginTop: 'auto',
          }}>
            <div style={{ fontSize: '26px', color: '#fff' }}>
              🎨 <strong>Vibe Coding</strong> is for the <span style={{ color: '#60a5fa' }}>Creator</span> (Focusing on Velocity)
            </div>
            <div style={{ fontSize: '26px', color: '#fff' }}>
              🛡️ <strong>AgentOps Cockpit</strong> is for the <span style={{ color: '#34d399' }}>Ecosystem</span> (Reliability, Economics, Security)
            </div>
          </div>
        </Sequence>
      </div>
    </AbsoluteFill>
  );
};
