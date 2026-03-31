import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

interface TitleSceneProps {
  title?: string;
  command?: string;
}

export const TitleScene: React.FC<TitleSceneProps> = ({ 
  title = "Autonomous Evolution", 
  command = "uvx agentops-cockpit evolve" 
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProgress = spring({
    frame: frame - 15,
    fps,
    config: { damping: 200 }
  });

  return (
    <AbsoluteFill style={{ 
      justifyContent: 'center', 
      alignItems: 'center', 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #1a1a3a, #0a0a1a 70%)'
    }}>
      <h2 style={{ color: '#4CAF50', fontSize: 40, letterSpacing: 4, transform: `translateY(${interpolate(titleProgress, [0, 1], [50, 0])}px)`, opacity: titleProgress }}>
        AGENTOPS COCKPIT
      </h2>
      <h1 style={{ color: 'white', fontSize: 100, fontWeight: 800, margin: '20px 0', transform: `scale(${interpolate(titleProgress, [0, 1], [0.9, 1])})`, opacity: titleProgress }}>
        {title}
      </h1>
      <p style={{ color: '#888', fontSize: 32, opacity: interpolate(frame - 45, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) }}>
        {command}
      </p>
    </AbsoluteFill>
  );
};
