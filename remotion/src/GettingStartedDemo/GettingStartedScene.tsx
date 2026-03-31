import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const GettingStartedScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleEnter = spring({ frame: frame - 10, fps, config: { damping: 14 } });
  
  const term1Enter = spring({ frame: frame - 30, fps, config: { damping: 14 } });
  const term2Enter = spring({ frame: frame - 150, fps, config: { damping: 14 } });
  const term3Enter = spring({ frame: frame - 280, fps, config: { damping: 14 } });

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
        background: 'linear-gradient(to right, #60a5fa, #a855f7)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
      }}>
        Getting Started with AgentOps Cockpit
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 30, width: '100%', maxWidth: 1000 }}>
        
        {/* Step 1: Install */}
        <div style={{ 
          opacity: term1Enter, 
          transform: `translateX(${interpolate(term1Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 15, color: '#9ca3af', fontSize: 24, fontWeight: 'bold' }}>
            1. Install Engine
          </div>
          <TerminalBlock
            title="Terminal - Setup"
            command="uv tool install agentops-cockpit"
            outputLines={[
              "Fetching package agentops-cockpit v2.0.11...",
              "Installed 1 executable: agentops-cockpit"
            ]}
            typeStartFrame={40}
            framesPerChar={1}
            lineDelay={10}
          />
        </div>

        {/* Step 2: Initialize */}
        <div style={{ 
          opacity: term2Enter, 
          transform: `translateX(${interpolate(term2Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 15, color: '#9ca3af', fontSize: 24, fontWeight: 'bold' }}>
            2. Scan Repository
          </div>
          <TerminalBlock
            title="Terminal - Audit"
            command="uvx agentops-cockpit audit report"
            outputLines={[
              "[INIT] Bootstrapping Cockpit environment...",
              "[AUDIT] Scanning AST trees for Architecture & Security gaps...",
              "[ALERT] 3 Critical Code Smells Detected. Report generated."
            ]}
            typeStartFrame={160}
            framesPerChar={1.5}
            lineDelay={12}
          />
        </div>

        {/* Step 3: Run Audit / Evolve */}
        <div style={{ 
          opacity: term3Enter, 
          transform: `translateX(${interpolate(term3Enter, [0, 1], [-100, 0])}px)`,
          position: 'relative'
        }}>
          <div style={{ position: 'absolute', left: -220, top: 15, color: '#9ca3af', fontSize: 24, fontWeight: 'bold' }}>
            3. Evolve Code
          </div>
          <TerminalBlock
            title="Terminal - Evolve"
            command="uvx agentops-cockpit evolve"
            outputLines={[
              "[AGENT] Engaging Autonomous Remediator Engine.",
              "[FIX] Applying Architectural & FinOps patches...",
              "[SUCCESS] Branch 'fix/autonomous-refactor' created.",
              "Run `uvx agentops-cockpit certify` to seal."
            ]}
            typeStartFrame={290}
            framesPerChar={1.5}
            lineDelay={20}
          />
        </div>

      </div>

    </AbsoluteFill>
  );
};
