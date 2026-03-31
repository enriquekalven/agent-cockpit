import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Img, staticFile } from 'remotion';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const TerminalScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Screen splits smoothly at frame 40
  const splitProgress = spring({ frame: frame - 40, fps, config: { damping: 14 } });
  
  // Terminal width shrinks from 80% to 45% to reveal code IDE
  const terminalWidth = interpolate(splitProgress, [0, 1], [80, 45]);
  const ideOpacity = interpolate(splitProgress, [0.5, 1], [0, 1], { extrapolateRight: 'clamp' });

  // Code state switches instantly exactly when the terminal says "[AGENT] Refactoring"
  const isEvolved = frame > 180;
  
  const legacyCode = `@app.command(name="evolve", hidden=True)
def legacy_evolve(path: str):
    # DEBT: No caching, synchronous, insecure execution
    console.print("Running legacy pipeline")
    execute(path)`;

  const newCode = `@app.command(name="evolve")
async def evolve(path: Annotated[str, typer.Option('--path')] = '.'):
    """Autonomous Evolution: Surgically fixes gaps."""
    # SECURITY: Executing in isolated Git Sandbox
    sandbox = await GitSandbox.create(path)
    
    # AST SCAN: Resolving dependency drift
    await sandbox.synthesize_fixes(mode="deep")
    
    # HARDENING: Pre-flight regressions checked automatically
    sandbox.commit(message="fix: autonomous refactor")`;

  return (
    <AbsoluteFill style={{ 
      padding: 40, 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)',
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      gap: 40
    }}>
      
      {/* Left Side: The Cockpit Terminal */}
      <div style={{ width: `${terminalWidth}%`, height: '80%' }}>
        <TerminalBlock
          title="Terminal - agent-cockpit"
          command="uvx agentops-cockpit evolve --branch"
          outputLines={[
            "[INIT] Scaffolding Autonomous Execution Core...",
            "[GIT] Branching into secure sandbox: 'fix/autonomous-refactor'",
            "[AUDIT] Scanning AST trees for architectural drift...",
            "[AGENT] Legacy debt identified in /cli/main.py",
            "[AGENT] Refactoring legacy logic -> async optimized tools",
            "[TEST] Running full regression suite against sandbox...",
            "[PASS] Regression Suite: 231 tests cleared.",
            "[GIT] Committing hardened fixes to Origin. ✨"
          ]}
          typeStartFrame={10}
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
            main.py — fix/autonomous-refactor (Git Sandbox)
          </span>
        </div>
        
        {/* IDE Code Area */}
        <div style={{ padding: 25, flex: 1, position: 'relative', overflow: 'hidden' }}>
          
          <div style={{ marginBottom: 20 }}>
             <span style={{color: '#60a5fa', fontFamily: 'Inter, sans-serif', fontSize: 13, fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: 1}}>
                {isEvolved ? "✅ Optimized Code Synthesized" : "🔍 Scanning Legacy Code"}
             </span>
          </div>

          {/* Animated Code Overlay */}
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
               top: interpolate(frame, [100, 180], [0, 100], {extrapolateRight: 'clamp'}) + '%',
               left: 0,
               width: '100%',
               height: 4,
               background: '#3b82f6',
               boxShadow: '0 0 20px #3b82f6, 0 0 40px #3b82f6',
               opacity: interpolate(frame, [100, 110, 170, 180], [0, 1, 1, 0], {extrapolateRight: 'clamp'}),
               zIndex: 10
             }} />
          )}

          {/* Mascot Kokpi Victory Appearance */}
          <Img 
            src={staticFile("kokpi_simplistic.png")} 
            style={{
              position: 'absolute',
              bottom: 20,
              right: 20,
              width: 120,
              height: 120,
              objectFit: 'contain',
              opacity: interpolate(frame, [160, 180], [0, 1], {extrapolateLeft: 'clamp'}),
              transform: `scale(${interpolate(spring({ frame: frame - 170, fps, config: { damping: 12 } }), [0, 1], [0.5, 1])}) rotate(${Math.sin(frame / 5) * 10}deg)`
            }} 
          />

        </div>
      </div>
    </AbsoluteFill>
  );
};
