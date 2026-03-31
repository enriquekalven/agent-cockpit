import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Img, staticFile } from 'remotion';

const Card = ({ title, content, icon, delay, themeColor }: { title: string, content: string, icon: string, delay: number, themeColor: string }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame: frame - delay, fps, config: { damping: 14 } });
  return (
    <div style={{
      background: 'rgba(255,255,255,0.05)',
      border: `1px solid rgba(255,255,255,0.1)`,
      borderLeft: `5px solid ${themeColor}`,
      borderRadius: 12,
      padding: 24,
      marginBottom: 20,
      opacity: enter,
      transform: `translateY(${interpolate(enter, [0, 1], [20, 0])}px)`,
      boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
        <span style={{ fontSize: 24 }}>{icon}</span>
        <h4 style={{ color: 'white', margin: 0, fontSize: 22, fontFamily: 'Inter', fontWeight: 600 }}>{title}</h4>
      </div>
      <div style={{ color: '#d1d5db', fontSize: 18, fontFamily: 'Inter', lineHeight: 1.5 }}>
        {title === 'One Command' ? 
          <span style={{ fontFamily: 'Fira Code, monospace', color: '#60a5fa', background: 'rgba(0,0,0,0.3)', padding: '6px 10px', borderRadius: 6, display: 'inline-block', marginTop: 8 }}>$&gt; {content}</span> 
          : content}
      </div>
    </div>
  );
};

export const EvolveSampleScene: React.FC<{
  pillarName: string;
  problem: string;
  command: string;
  benefits: string;
  summary: string;
  legacyCode: string;
  newCode: string;
  filename: string;
}> = ({ pillarName, problem, command, benefits, summary, legacyCode, newCode, filename }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Screen splits smoothly at frame 20
  const splitProgress = spring({ frame: frame - 20, fps, config: { damping: 14 } });
  
  // Left width shrinks to 45% to reveal code IDE
  const leftWidth = interpolate(splitProgress, [0, 1], [80, 45]);
  const ideOpacity = interpolate(splitProgress, [0.5, 1], [0, 1], { extrapolateRight: 'clamp' });

  // Code state switches instantly at frame 160
  const isEvolved = frame > 160;

  const cardEnter = (delayFrames: number) => spring({ frame: frame - delayFrames, fps, config: { damping: 14 } });

  return (
    <AbsoluteFill style={{ 
      padding: 40, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)',
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      gap: 60
    }}>
      
      {/* Left Side: Cards */}
      <div style={{ width: `${leftWidth}%`, height: '80%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h2 style={{ color: '#fff', fontSize: 44, fontWeight: 900, marginBottom: 30, opacity: cardEnter(10), fontFamily: 'Inter' }}>
          Evolution: <span style={{ color: '#3b82f6' }}>{pillarName}</span>
        </h2>
        
        <Card title="Problem" content={problem} icon="⚠️" delay={30} themeColor="#ef4444" />
        <Card title="One Command" content={command} icon="⚡" delay={50} themeColor="#3b82f6" />
        <Card title="What You Get" content={benefits} icon="🎁" delay={70} themeColor="#10b981" />
        <Card title="Summary" content={summary} icon="📈" delay={90} themeColor="#a855f7" />
      </div>

      {/* Right Side: IDE Github Sandbox View */}
      <div style={{ 
        width: '50%', 
        height: '80%',
        opacity: ideOpacity,
        background: '#1e1e1e',
        borderRadius: 12,
        border: '1px solid #333',
        boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
        display: splitProgress > 0 ? 'flex' : 'none',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        {/* IDE Header */}
        <div style={{ background: '#2d2d2d', padding: '10px 20px', display: 'flex', gap: 10, alignItems: 'center' }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ff5f56' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ffbd2e' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#27c93f' }} />
          <span style={{ color: '#888', fontSize: 13, marginLeft: 15, fontFamily: 'Fira Code, monospace' }}>
            {filename} — fix/autonomous-refactor
          </span>
        </div>
        
        {/* IDE Code Area */}
        <div style={{ padding: 25, flex: 1, position: 'relative', overflow: 'hidden' }}>
          
          <div style={{ marginBottom: 20 }}>
             <span style={{color: '#60a5fa', fontFamily: 'Inter, sans-serif', fontSize: 13, fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: 1}}>
                {isEvolved ? `✅ ${pillarName} Remediation Applied` : "🔍 Scanning Legacy Code..."}
             </span>
          </div>

          <pre style={{ 
            color: isEvolved ? '#4ade80' : '#f87171', 
            fontFamily: 'Fira Code, monospace', 
            fontSize: 16, 
            lineHeight: 1.6,
            margin: 0,
            whiteSpace: 'pre-wrap',
            transition: 'color 0.3s ease'
          }}>
            {isEvolved ? newCode : legacyCode}
          </pre>
          
          {/* Laser Scan Line effect during Evolution */}
          {!isEvolved && frame > 100 && (
             <div style={{
               position: 'absolute',
               top: interpolate(frame, [100, 160], [0, 100], {extrapolateRight: 'clamp'}) + '%',
               left: 0,
               width: '100%',
               height: 4,
               background: '#3b82f6',
               boxShadow: '0 0 20px #3b82f6, 0 0 40px #3b82f6',
               opacity: interpolate(frame, [100, 110, 150, 160], [0, 1, 1, 0], {extrapolateRight: 'clamp'}),
               zIndex: 10
             }} />
          )}

          {/* Kokpi Victory */}
          <Img 
            src={staticFile("kokpi_simplistic.png")} 
            style={{
              position: 'absolute',
              bottom: 20,
              right: 20,
              width: 120,
              height: 120,
              objectFit: 'contain',
              opacity: interpolate(frame, [140, 160], [0, 1], {extrapolateLeft: 'clamp'}),
              transform: `scale(${interpolate(spring({ frame: frame - 150, fps, config: { damping: 12 } }), [0, 1], [0.5, 1])}) rotate(${Math.sin(frame / 5) * 10}deg)`
            }} 
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};
