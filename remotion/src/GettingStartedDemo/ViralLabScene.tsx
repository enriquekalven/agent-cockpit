import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const ViralLabScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEnter = spring({ frame: frame - 10, fps, config: { damping: 14 } });
  
  const term1Enter = spring({ frame: frame - 30, fps, config: { damping: 14 } });
  const term2Enter = spring({ frame: frame - 250, fps, config: { damping: 14 } });
  const term3Enter = spring({ frame: frame - 480, fps, config: { damping: 14 } });

  return (
    <AbsoluteFill style={{ 
      padding: 60, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)',
      alignItems: 'center',
    }}>
      
      <div style={{
        opacity: titleEnter,
        transform: `translateY(${interpolate(titleEnter, [0, 1], [-50, 0])}px)`,
        color: 'white',
        fontSize: 56,
        fontWeight: '900',
        marginBottom: 60,
        textAlign: 'center',
        background: 'linear-gradient(to right, #ef4444, #f59e0b)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
      }}>
        Zero2Hero: The Rogue Agent Lab
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 30, width: '100%', maxWidth: 1050 }}>
        
        {/* Step 1: Create */}
        <div style={{ 
          opacity: term1Enter, 
          transform: `translateX(${interpolate(term1Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 15, color: '#9ca3af', fontSize: 24, fontWeight: 'bold' }}>
            1. Bootstrap
          </div>
          <TerminalBlock
            title="Terminal - Bootstrap"
            command="uvx --python 3.12 --refresh agentops-cockpit@latest create rogue-agent"
            outputLines={[
              "🧪 Bootstrapping Rogue Agent for viral lab...",
              "✅ Viral Lab environment ready. The Rogue Agent is live in ./my_super_agent"
            ]}
            typeStartFrame={40}
            framesPerChar={1}
            lineDelay={10}
            height={160}
          />
        </div>

        {/* Step 2: Certify (Fail) */}
        <div style={{ 
          opacity: term2Enter, 
          transform: `translateX(${interpolate(term2Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 15, color: '#9ca3af', fontSize: 24, fontWeight: 'bold' }}>
            2. Hard-Gate
          </div>
          <TerminalBlock
            title="Terminal - Certify Audit"
            command="cd my_super_agent && uvx --python 3.12 --refresh agentops-cockpit@latest certify"
            outputLines={[
              "🛫 LAUNCHING PRE-FLIGHT SYSTEM VERIFICATION...",
              "❌ Red Team Security (Full) Failed",
              "🛑 CERTIFICATION DENIED: Critical gaps detected in Security."
            ]}
            typeStartFrame={260}
            framesPerChar={1.5}
            lineDelay={12}
            height={190}
          />
        </div>

        {/* Step 3: Evolve */}
        <div style={{ 
          opacity: term3Enter, 
          transform: `translateX(${interpolate(term3Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 15, color: '#9ca3af', fontSize: 24, fontWeight: 'bold' }}>
            3. Automediate
          </div>
          <TerminalBlock
            title="Terminal - Evolve Engine"
            command="uvx --python 3.12 --refresh agentops-cockpit@latest evolve"
            outputLines={[
              "🤖 TRINITY AUTONOMOUS EVOLUTION",
              "📦 Autonomous Remediation Staged: Patch created for agent.py",
              "✨ Architecture & Security limits enforced. Agent is hardened."
            ]}
            typeStartFrame={490}
            framesPerChar={1.5}
            lineDelay={20}
            height={190}
          />
        </div>

      </div>

    </AbsoluteFill>
  );
};
