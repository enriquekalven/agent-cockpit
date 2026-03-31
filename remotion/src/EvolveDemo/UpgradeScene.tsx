import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Img, staticFile } from 'remotion';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const UpgradeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Screen splits smoothly at frame 60
  const splitProgress = spring({ frame: frame - 60, fps, config: { damping: 14 } });
  
  // Terminal width shrinks from 80% to 45% to reveal code IDE
  const terminalWidth = interpolate(splitProgress, [0, 1], [80, 45]);
  const ideOpacity = interpolate(splitProgress, [0.5, 1], [0, 1], { extrapolateRight: 'clamp' });

  // Code state switches instantly exactly when the terminal hits AST migrations
  const isUpgraded = frame > 160;

  const mascotHover = Math.sin(frame / 10) * 10;
  const mascotPop = spring({ frame: frame - 160, fps, config: { damping: 12 } });
  
  const vanillaCode = `class CustomerSupportAgent:
    def __init__(self):
        self.history = []

    def generate(self, user_msg: str):
        self.history.append(user_msg)
        # Using basic genai call without tracking
        response = genai.generate_text(user_msg)
        self.history.append(response)
        return response`;

  const adkCode = `from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService

customer_support = Agent(
    name="customer_support",
    model="gemini-2.0-flash",
    instruction="Provide support. Retain context.",
    memory_service=InMemoryMemoryService() # 🚀 ADK Injected
)

async def generate(user_msg: str, session_id: str):
    # 🛡️ ADK Managed Execution & Telemetry
    async for event in customer_support.run_async(
        session_id=session_id,
        new_message=user_msg
    ):
        yield event`;

  return (
    <AbsoluteFill style={{ 
      padding: 40, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(circle at 80% 20%, #0c2a1a, #03040a 90%)',
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      gap: 40
    }}>
      
      {/* Left Side: The Cockpit Terminal */}
      <div style={{ width: `${terminalWidth}%`, height: '80%' }}>
        <div style={{ marginBottom: 25, transition: 'all 0.3s', opacity: splitProgress > 0.5 ? 0 : 1, height: splitProgress > 0.5 ? 0 : 'auto', overflow: 'hidden' }}>
           <h2 style={{ color: '#4ade80', fontSize: 40, margin: 0, letterSpacing: 1, fontFamily: 'Inter, sans-serif' }}>Upgrade Your Fleet</h2>
           <p style={{ color: '#888', fontSize: 20, marginTop: 5, fontFamily: 'Inter, sans-serif' }}>Injecting advanced ADK Skills directly into legacy Agents.</p>
        </div>
        <TerminalBlock
          title="Terminal - agent-cockpit"
          command="uvx agentops-cockpit upgrade --skills=ADK"
          outputLines={[
            "[INIT] Scanning for Legacy Vanilla Python Agents...",
            "[MATCH] Found 'customer_support' missing ADK skills.",
            "[AGENT] Executing structural AST code migrations...",
            "  -> Injecting Memory Bank persistence layers",
            "  -> Upgrading generation pipelines to ADK standards",
            "  -> Wrapping core endpoints in official orchestrators",
            "[PASS] Successfully upgraded agent to full Google ADK compliance.",
            "✨ Fleet architectural upgrade finalized."
          ]}
          typeStartFrame={20}
          framesPerChar={1.5}
          lineDelay={15}
        />
      </div>

      {/* Right Side: IDE Github Sandbox View */}
      <div style={{ 
        width: '45%', 
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
            agent.py — ADK Overhaul Refactor
          </span>
        </div>
        
        {/* IDE Code Area */}
        <div style={{ padding: 25, flex: 1, position: 'relative', overflow: 'hidden' }}>
          
          <div style={{ marginBottom: 20 }}>
             <span style={{color: '#4ade80', fontFamily: 'Inter, sans-serif', fontSize: 13, fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: 1}}>
                {isUpgraded ? "🚀 ADK Structure Synthesized" : "🔍 Scanning Vanilla Code Structure"}
             </span>
          </div>

          {/* Animated Code Overlay */}
          <pre style={{ 
            color: isUpgraded ? '#a6e3a1' : '#f38ba8', 
            fontFamily: 'Fira Code, monospace', 
            fontSize: 14, 
            lineHeight: 1.6,
            margin: 0,
            whiteSpace: 'pre-wrap',
            transition: 'color 0.3s ease'
          }}>
            {isUpgraded ? adkCode : vanillaCode}
          </pre>
          
          {/* Laser Scan Line effect during Evolution */}
          {!isUpgraded && frame > 90 && (
             <div style={{
               position: 'absolute',
               top: interpolate(frame, [90, 160], [0, 100], {extrapolateRight: 'clamp'}) + '%',
               left: 0,
               width: '100%',
               height: 4,
               background: '#4ade80',
               boxShadow: '0 0 20px #4ade80, 0 0 40px #4ade80',
               opacity: interpolate(frame, [90, 100, 150, 160], [0, 1, 1, 0], {extrapolateRight: 'clamp'}),
               zIndex: 10
             }} />
          )}

          {/* Kokpi Mascot Celebration */}
          <Img 
            src={staticFile('kokpi_simplistic.png')} 
            style={{
              position: 'absolute',
              bottom: -20,
              right: 20,
              width: 150,
              zIndex: 20,
              opacity: mascotPop,
              transform: `scale(${mascotPop}) translateY(${mascotHover}px)`
            }} 
          />

        </div>
      </div>
    </AbsoluteFill>
  );
};
