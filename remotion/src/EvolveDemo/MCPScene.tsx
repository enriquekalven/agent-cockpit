import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Img, staticFile } from 'remotion';

export const MCPScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const chatEnter = spring({ frame: frame - 20, fps, config: { damping: 14 } });
  
  const mascotHover = Math.sin(frame / 10) * 10;
  const mascotPop = spring({ frame: frame - 200, fps, config: { damping: 12 } });
  
  return (
    <AbsoluteFill style={{ 
      padding: 60, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #1a1b26, #000000 80%)',
      justifyContent: 'center',
      alignItems: 'center'
    }}>
       {/* Background MCP Terminal Server Window */}
       <div style={{
         position: 'absolute',
         top: 80,
         left: 80,
         width: 450,
         height: 250,
         background: '#0c0c0c',
         borderRadius: 8,
         border: '1px solid #333',
         padding: 20,
         opacity: chatEnter,
         transform: `translateY(${interpolate(chatEnter, [0, 1], [40, 0])}px)`
       }}>
          <div style={{ color: '#5b5b5b', fontSize: 13, marginBottom: 15, fontFamily: 'Fira Code, monospace' }}>
             $ uvx agentops-cockpit mcp-server
          </div>
          <div style={{ color: '#4ade80', fontSize: 13, fontFamily: 'Fira Code, monospace', opacity: frame > 40 ? 1 : 0 }}>
             [MCP] Serving AgentOps Cockpit over stdio
          </div>
          <div style={{ color: '#3b82f6', fontSize: 13, fontFamily: 'Fira Code, monospace', marginTop: 15, opacity: frame > 120 ? 1 : 0 }}>
             [MCP] ADK Tool Called: red_team_attack
          </div>
          <div style={{ color: '#facc15', fontSize: 13, fontFamily: 'Fira Code, monospace', marginTop: 15, opacity: frame > 180 ? 1 : 0 }}>
             [MCP] ADK Tool Called: architecture_review
          </div>
       </div>

       {/* IDE Chat Overlay */}
       <div style={{
         width: 650,
         background: '#1e1e2e',
         borderRadius: 12,
         boxShadow: '0 30px 60px rgba(0,0,0,0.8)',
         border: '1px solid #4ade80',
         opacity: chatEnter,
         transform: `scale(${interpolate(chatEnter, [0, 1], [0.95, 1])})`,
         overflow: 'hidden',
         marginLeft: 250,
         marginTop: 50
       }}>
          {/* Header */}
          <div style={{ padding: '15px 20px', background: '#11111b', borderBottom: '1px solid #313244', display: 'flex', alignItems: 'center', gap: 15 }}>
             <div style={{ color: '#a6adc8', fontSize: 15, fontWeight: 'bold' }}>Chat</div>
             <div style={{ background: '#4ade8022', color: '#4ade80', padding: '4px 10px', borderRadius: 6, fontSize: 11, fontWeight: 'bold' }}>
               AgentOps MCP Connected 🚀
             </div>
          </div>
          
          <div style={{ padding: 25, display: 'flex', flexDirection: 'column', gap: 20 }}>
             
             {/* User Message */}
             <div style={{ alignSelf: 'flex-end', background: '#3b82f6', color: 'white', padding: '15px', borderRadius: '15px 15px 0 15px', maxWidth: '85%', opacity: frame > 60 ? 1 : 0, transform: `translateY(${frame > 60 ? 0 : 10}px)`, transition: 'all 0.3s', fontSize: 15 }}>
                Run an adversarial red team attack on my ADK agent!
             </div>
             
             {/* AI Response */}
             <div style={{ alignSelf: 'flex-start', background: '#313244', color: '#cdd6f4', padding: '15px', borderRadius: '15px 15px 15px 0', maxWidth: '90%', opacity: frame > 150 ? 1 : 0, transform: `translateY(${frame > 150 ? 0 : 10}px)`, transition: 'all 0.3s', fontSize: 15 }}>
                <div style={{ fontSize: 13, marginBottom: 12, color: '#f38ba8', display: 'flex', alignItems: 'center', gap: 8 }}>
                   Using local ADK Tool: red_team_attack
                </div>
                <div style={{ opacity: frame > 200 ? 1 : 0.2, transition: 'opacity 0.5s', lineHeight: 1.5 }}>
                   I executed the ADK Red Team audit! Findings:<br/><br/>
                   <span style={{ color: '#a6e3a1', fontWeight: 'bold' }}>✅ Prompt Injection: High Resilience</span><br/>
                   <span style={{ color: '#fab387', fontWeight: 'bold' }}>⚠️ Exfiltration: Minor gap in agent state isolation.</span><br/>
                   <br/>
                   Would you like me to autonomously synthesize the Governance Framework fix?
                </div>
             </div>
             
          </div>
       </div>

       {/* Kokpi Mascot Celebration */}
       <Img 
         src={staticFile('kokpi_simplistic.png')} 
         style={{
           position: 'absolute',
           bottom: 10,
           right: 40,
           width: 150,
           zIndex: 20,
           opacity: mascotPop,
           transform: `scale(${mascotPop}) translateY(${mascotHover}px)`
         }} 
       />

    </AbsoluteFill>
  );
};
