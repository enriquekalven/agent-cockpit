import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Img, staticFile } from 'remotion';

export const ClosingScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animations
  const textEnter = spring({ frame: frame - 15, fps, config: { damping: 14 } });
  const callToActionEnter = spring({ frame: frame - 45, fps, config: { damping: 14 } });
  const mascotHover = Math.sin(frame / 15) * 8;

  return (
    <AbsoluteFill style={{ 
      justifyContent: 'center', 
      alignItems: 'center', 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #1a1a3a, #0a0a1a 70%)'
    }}>
      
      {/* Mascot properly placed */}
      <Img 
         src={staticFile('kokpi_simplistic.png')} 
         style={{
           marginBottom: 60,
           width: 250,
           transform: `translateY(${mascotHover}px) scale(${interpolate(textEnter, [0, 1], [0.8, 1])})`,
           opacity: textEnter
         }} 
      />

      {/* Blue Pill Motto */}
      <div style={{
         background: 'linear-gradient(90deg, #4f46e5, #3b82f6)',
         borderRadius: 60,
         padding: '24px 70px',
         zIndex: 10,
         opacity: textEnter,
         transform: `scale(${interpolate(textEnter, [0, 1], [0.95, 1])})`,
         boxShadow: '0 15px 35px rgba(59, 130, 246, 0.4)'
      }}>
         <h2 style={{color: 'white', margin: 0, fontSize: 40, fontWeight: 700, letterSpacing: 0.5}}>
            Vibe Code with AI. Audit like a Principal. Ship like a Pro.
         </h2>
      </div>

      {/* Call To Action */}
      <h3 style={{
         color: '#a1a1aa', 
         fontSize: 28, 
         marginTop: 40,
         fontWeight: 500,
         letterSpacing: 1.5,
         fontFamily: 'Fira Code, monospace',
         opacity: callToActionEnter,
         transform: `translateY(${interpolate(callToActionEnter, [0, 1], [20, 0])}px)`
      }}>
         Try it yourself: <span style={{ color: '#4ade80', fontWeight: 'bold' }}>agent-cockpit.web.app</span>
      </h3>

    </AbsoluteFill>
  );
};
