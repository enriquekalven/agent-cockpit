import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const QwiklabsDemoScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEnter = spring({ frame: frame - 10, fps, config: { damping: 14 } });
  
  const step0Enter = spring({ frame: frame - 40, fps, config: { damping: 14 } });
  const step1Enter = spring({ frame: frame - 140, fps, config: { damping: 14 } });
  const step2Enter = spring({ frame: frame - 300, fps, config: { damping: 14 } });
  const step3Enter = spring({ frame: frame - 550, fps, config: { damping: 14 } });
  const step4Enter = spring({ frame: frame - 750, fps, config: { damping: 14 } });

  return (
    <AbsoluteFill style={{ 
      padding: 50, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)',
      alignItems: 'center',
    }}>
      
      <div style={{
        opacity: titleEnter,
        transform: `translateY(${interpolate(titleEnter, [0, 1], [-50, 0])}px)`,
        color: 'white',
        fontSize: 48,
        fontWeight: '900',
        marginBottom: 40,
        textAlign: 'center',
        background: 'linear-gradient(to right, #4ade80, #3b82f6)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
      }}>
        NEXT'26 SOL331: Taming the Rogue Agent
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 20, width: '100%', maxWidth: 1100 }}>
        
        {/* Module 0: Zero Install Magic */}
        <div style={{ 
          opacity: step0Enter, 
          transform: `translateX(${interpolate(step0Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 10, color: '#9ca3af', fontSize: 20, fontWeight: 'bold' }}>
            Module 0
          </div>
          <TerminalBlock
            title="Terminal - Zero Install"
            command="uvx agentops-cockpit --help"
            outputLines={[
              "Usage: agentops-cockpit [OPTIONS] COMMAND [ARGS]...",
              "The Ultimate AgentOps CLI."
            ]}
            typeStartFrame={60}
            framesPerChar={1}
            lineDelay={5}
            height={100}
          />
        </div>

        {/* Module 1: Scaffold Rogue Agent */}
        <div style={{ 
          opacity: step1Enter, 
          transform: `translateX(${interpolate(step1Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 10, color: '#9ca3af', fontSize: 20, fontWeight: 'bold' }}>
            Module 1
          </div>
          <TerminalBlock
            title="Terminal - Scaffold"
            command="uvx --python 3.12 --refresh agentops-cockpit@latest create rogue-agent"
            outputLines={[
              "🧪 Bootstrapping Rogue Agent for viral lab...",
              "✅ Viral Lab environment ready. The Rogue Agent is live in ./my_super_agent"
            ]}
            typeStartFrame={160}
            framesPerChar={1}
            lineDelay={10}
            height={130}
          />
        </div>

        {/* Module 2: The Roast */}
        <div style={{ 
          opacity: step2Enter, 
          transform: `translateX(${interpolate(step2Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 10, color: '#9ca3af', fontSize: 20, fontWeight: 'bold' }}>
            Module 2
          </div>
          <TerminalBlock
            title="Terminal - The Roast"
            command="cd ./my_super_agent && uvx agentops-cockpit audit report"
            outputLines={[
              "🕵️‍♂️ Initializing Principal SME Board...",
              "❌ P1 Security: Hardcoded Credentials Detected",
              "❌ P4 FinOps: Context Caching Missing (Massive token waste)",
              "📄 Printable HTML Report generated."
            ]}
            typeStartFrame={330}
            framesPerChar={1}
            lineDelay={15}
            height={170}
          />
        </div>

        {/* Module 3: Climbing the Ladder */}
        <div style={{ 
          opacity: step3Enter, 
          transform: `translateX(${interpolate(step3Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 10, color: '#9ca3af', fontSize: 20, fontWeight: 'bold' }}>
            Module 3
          </div>
          <TerminalBlock
            title="Terminal - Climbing the Ladder"
            command="uvx agentops-cockpit evolve"
            outputLines={[
              "🤖 TRINITY AUTONOMOUS EVOLUTION",
              "📦 Patching AST: Injecting @cockpit_reflection & tenacity...",
              "✨ Architecture upgraded without breaking business logic!"
            ]}
            typeStartFrame={570}
            framesPerChar={1}
            lineDelay={12}
            height={150}
          />
        </div>

        {/* Module 4: The Production Gate */}
        <div style={{ 
          opacity: step4Enter, 
          transform: `translateX(${interpolate(step4Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 10, color: '#9ca3af', fontSize: 20, fontWeight: 'bold' }}>
            Module 4
          </div>
          <TerminalBlock
            title="Terminal - The Production Gate"
            command="uvx agentops-cockpit certify"
            outputLines={[
              "🛫 LAUNCHING PRE-FLIGHT SYSTEM VERIFICATION...",
              "✅ Red Team Security (Full) Passed",
              "🏆 CERTIFICATION GRANTED: Ready for Production Deployment."
            ]}
            typeStartFrame={780}
            framesPerChar={1}
            lineDelay={12}
            height={140}
          />
        </div>

      </div>

    </AbsoluteFill>
  );
};
