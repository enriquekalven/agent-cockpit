import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Img, staticFile } from 'remotion';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const CertifyScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Screen splits smoothly at frame 60
  const splitProgress = spring({ frame: frame - 60, fps, config: { damping: 14 } });
  
  // Terminal width shrinks from 80% to 45% to reveal code IDE
  const terminalWidth = interpolate(splitProgress, [0, 1], [80, 45]);
  const ideOpacity = interpolate(splitProgress, [0.5, 1], [0, 1], { extrapolateRight: 'clamp' });

  // Code state switches instantly exactly when the terminal says "[PASS] Certified"
  const isCertified = frame > 170;

  const mascotHover = Math.sin(frame / 10) * 10;
  const mascotPop = spring({ frame: frame - 170, fps, config: { damping: 12 } });
  
  const originalCode = `"""
SUPER AGENTIC SOVEREIGN MIND CLOUD
"""
class OmnipotentTrader:
    def execute(self):
        # Magically predicts the stock market using AI
        # Make sure not to error out here!
        pass`;

  const certifiedCode = `"""
Capital Allocation Strategy Agent
Version: 2.0.11 (Autonomous Core)
"""
class CapitalStrategyAgent:
    def execute(self):
        # Execute validated trading heuristics.
        # Enforcing struct-log compliance boundary.
        pass`;

  return (
    <AbsoluteFill style={{ 
      padding: 40, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #1e1e24, #050508 100%)',
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      gap: 40
    }}>
      
      {/* Left Side: The Cockpit Terminal */}
      <div style={{ width: `${terminalWidth}%`, height: '80%' }}>
        <div style={{ marginBottom: 25, transition: 'all 0.3s', opacity: splitProgress > 0.5 ? 0 : 1, height: splitProgress > 0.5 ? 0 : 'auto', overflow: 'hidden' }}>
           <h2 style={{ color: '#6ee7b7', fontSize: 40, margin: 0, letterSpacing: 1, fontFamily: 'Inter, sans-serif' }}>The Governance Seal</h2>
           <p style={{ color: '#888', fontSize: 20, marginTop: 5, fontFamily: 'Inter, sans-serif' }}>Enforcing strict maturity PR standards.</p>
        </div>
        <TerminalBlock
          title="Terminal - agent-cockpit"
          command="uvx agentops-cockpit certify --path=./agents"
          outputLines={[
            "[INIT] Booting Governance Engine (v2.0.11)...",
            "[SCAN] Analyzing AST patterns in /agents/omnipotent_trader.py",
            "[FAIL] Detected non-compliant 'AI-Fluff' terminology.",
            "[FIX] Eradicating 'Sovereign Mind Cloud' marketing jargon.",
            "[FIX] Renaming agent to 'CapitalStrategyAgent'.",
            "[AUDIT] Enforcing struct-log boundaries & guardrails...",
            "[PASS] Code architecture certified against Governance Framework.",
            "✅ Ready for Production Release."
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
        background: '#18181b', // darker zinc
        borderRadius: 12,
        border: '1px solid #3f3f46',
        boxShadow: '0 20px 50px rgba(0,0,0,0.8)',
        display: splitProgress > 0 ? 'flex' : 'none',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        {/* IDE Header */}
        <div style={{ background: '#27272a', padding: '10px 20px', display: 'flex', gap: 10, alignItems: 'center' }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#f87171' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#fbbf24' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#34d399' }} />
          <span style={{ color: '#a1a1aa', fontSize: 13, marginLeft: 15, fontFamily: 'Fira Code, monospace' }}>
            capital_strategy.py — Governance Auditor
          </span>
        </div>
        
        {/* IDE Code Area */}
        <div style={{ padding: 25, flex: 1, position: 'relative', overflow: 'hidden' }}>
          
          <div style={{ marginBottom: 20 }}>
             <span style={{color: isCertified ? '#34d399' : '#fbbf24', fontFamily: 'Inter, sans-serif', fontSize: 13, fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: 1}}>
                {isCertified ? "✅ Governance Engine Passed" : "⚠️ Auditing Code Boundaries"}
             </span>
          </div>

          <pre style={{ 
            color: isCertified ? '#a7f3d0' : '#fca5a5', 
            fontFamily: 'Fira Code, monospace', 
            fontSize: 14, 
            lineHeight: 1.6,
            margin: 0,
            whiteSpace: 'pre-wrap',
            transition: 'color 0.3s ease'
          }}>
            {isCertified ? certifiedCode : originalCode}
          </pre>
          
          {/* Laser Scan Line effect during Evolution */}
          {!isCertified && frame > 90 && (
             <div style={{
               position: 'absolute',
               top: interpolate(frame, [90, 160], [0, 100], {extrapolateRight: 'clamp'}) + '%',
               left: 0,
               width: '100%',
               height: 4,
               background: '#fbbf24',
               boxShadow: '0 0 20px #fbbf24, 0 0 40px #fbbf24',
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
