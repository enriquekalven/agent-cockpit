import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export const StoryCard: React.FC<{
  title: string;
  subtitle?: string;
  points: { icon: string, text: string }[];
  themeColor?: string;
}> = ({ title, subtitle, points, themeColor = "#3b82f6" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enter = spring({ frame: frame - 15, fps, config: { damping: 14 } });
  
  return (
    <AbsoluteFill style={{ 
      padding: 60, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <div style={{
         background: 'rgba(255,255,255,0.03)',
         border: `1px solid rgba(255,255,255,0.1)`,
         borderTop: `8px solid ${themeColor}`,
         borderRadius: 24,
         padding: 60,
         maxWidth: 1100,
         width: '100%',
         opacity: enter,
         transform: `translateY(${interpolate(enter, [0, 1], [50, 0])}px)`,
         boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
      }}>
         <h2 style={{ color: 'white', fontSize: 64, fontWeight: 900, marginBottom: subtitle ? 20 : 50, textAlign: 'center', fontFamily: 'Inter' }}>{title}</h2>
         {subtitle && <p style={{ color: '#9ca3af', fontSize: 32, textAlign: 'center', marginBottom: 60, fontWeight: 500 }}>{subtitle}</p>}
         
         <div style={{ display: 'flex', flexDirection: 'column', gap: 35 }}>
           {points.map((p, i) => {
             const pEnter = spring({ frame: frame - 30 - (i * 10), fps, config: { damping: 14 } });
             return (
               <div key={i} style={{ 
                 display: 'flex', 
                 alignItems: 'center', 
                 gap: 24,
                 opacity: pEnter,
                 transform: `translateX(${interpolate(pEnter, [0, 1], [-30, 0])}px)`
               }}>
                 <span style={{ fontSize: 44 }}>{p.icon}</span>
                 <span style={{ color: '#f3f4f6', fontSize: 30, fontWeight: 500, lineHeight: 1.4 }}>{p.text}</span>
               </div>
             )
           })}
         </div>
      </div>
    </AbsoluteFill>
  );
};
