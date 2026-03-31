import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const LadderScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const stages = [
    { 
       title: 'Level 1: Read-Only Audit', 
       cmd: 'uvx agentops-cockpit audit report', 
       desc: 'Scans for logic flaws, PII leaks, and FinOps loops. Never touches your code.', 
       color: '#a855f7',
       output: '[START] Governance Audit\n✓ Architecture Context Verified\n✓ FinOps Loops Checked\n❌ Security: PII Detection in memory bank\n\n[SCORE] 85/100 (Read-Only Mode)'
    },
    { 
       title: 'Level 2: In-Place Linter', 
       cmd: 'uvx agentops-cockpit audit report --apply-fixes', 
       desc: 'Reads the report matrix and autonomously overwrites live files in-place to fix vulnerabilities.', 
       color: '#3b82f6',
       output: '[FIX] Starting Auto-Remediation...\n  > Patching src/agent.py (PII scrub)\n  > Fixing infinite recursive tool loop\n✓ 2 fixes applied directly to active tree.\n[DONE] Code is hardened.'
    },
    { 
       title: 'Level 3: Autonomous Sandbox', 
       cmd: 'uvx agentops-cockpit evolve', 
       desc: 'Isolates into a secure Git sandbox branch. Rewrites AST logic, runs regressions, and PRs.', 
       color: '#22c55e',
       output: '[GIT] Branching into secure sandbox: `fix/autonomous-refactor`\n[AST] Analyzing deep graph relations...\n[FIX] Resolving cross-module side-effects\n[TEST] 230/230 PyTest passes ✔️\n[GIT] Pull Request Created.'
    },
    { 
       title: 'Level 4: Framework Migration', 
       cmd: 'uvx agentops-cockpit upgrade [URL]', 
       desc: 'Tears down legacy architecture and restructures the codebase to perfectly mirror new API standards.', 
       color: '#f59e0b',
       output: '[DOCS] Ingesting ADK v2.0 Standard (125 rules)\n[ARCH] Tearing down legacy LangChain logic...\n[ARCH] Synthesizing new AgentEngine layout...\n[MIGRATE] 45 files transformed.\n✓ Total Framework Migration Complete.'
    }
  ];

  const totalFrames = 2460;
  const stageDuration = Math.floor(totalFrames / stages.length);
  const activeStageIdx = Math.min(3, Math.max(0, Math.floor(frame / stageDuration)));
  const stageFrame = frame % stageDuration;

  const currentOutput = stages[activeStageIdx].output;
  // Type command out first (0-30 frames)
  const cmdLength = stages[activeStageIdx].cmd.length;
  const charsCmd = Math.floor(interpolate(stageFrame, [10, 40], [0, cmdLength], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' }));
  const visibleCmd = stages[activeStageIdx].cmd.slice(0, charsCmd);

  // Then type output (60-200 frames)
  const charsOutput = Math.floor(interpolate(stageFrame, [60, 200], [0, currentOutput.length], { extrapolateRight: 'clamp', extrapolateLeft: 'clamp' }));
  const visibleOutput = currentOutput.slice(0, charsOutput);

  return (
    <AbsoluteFill style={{ 
      justifyContent: 'center', 
      alignItems: 'center', 
      fontFamily: 'Inter, sans-serif',
      background: 'radial-gradient(ellipse at 50% 50%, #1a1a3a, #0a0a1a 70%)',
      padding: 60
    }}>
      <div style={{ display: 'flex', width: '100%', height: '100%', gap: 60, maxWidth: 1600, maxHeight: 900 }}>
        
        {/* LEFT COLUMN: The Ladder */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 24, justifyContent: 'center' }}>
          {stages.map((step, i) => {
            const isActive = i === activeStageIdx;
            const isPast = i < activeStageIdx;
            
            return (
              <div key={i} style={{
                display: 'flex',
                alignItems: 'center',
                background: isActive ? 'rgba(255, 255, 255, 0.08)' : 'rgba(255, 255, 255, 0.02)',
                border: `1px solid ${isActive ? step.color : '#333'}`,
                boxShadow: isActive ? `0 10px 30px rgba(0,0,0,0.4)` : 'none',
                borderRadius: 16,
                padding: '24px 32px',
                opacity: isActive ? 1 : (isPast ? 0.4 : 0.1),
                transform: `scale(${isActive ? 1.05 : 1})`,
                transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
              }}>
                <div style={{
                  width: 60, height: 60, borderRadius: '50%', 
                  background: isActive ? `${step.color}20` : '#222',
                  border: `2px solid ${isActive ? step.color : '#555'}`, 
                  display: 'flex', justifyContent: 'center', alignItems: 'center',
                  color: isActive ? step.color : '#555', fontSize: 24, fontWeight: 'bold', marginRight: 32, flexShrink: 0
                }}>
                  {i + 1}
                </div>
                <div style={{ flex: 1 }}>
                  <h3 style={{ color: isActive ? step.color : '#888', margin: '0 0 8px 0', fontSize: 24, letterSpacing: 1, textTransform: 'uppercase' }}>{step.title}</h3>
                  <p style={{ color: '#a1a1aa', margin: 0, fontSize: 18, lineHeight: 1.4 }}>{step.desc}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* RIGHT COLUMN: Terminal Windows */}
        <div style={{ flex: 1.2, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
           <div style={{ 
              width: '100%', 
              height: 600,
              background: 'rgba(10, 10, 15, 0.95)', 
              border: `1px solid ${stages[activeStageIdx].color}40`, 
              borderRadius: 20, 
              padding: 40, 
              boxShadow: `0 30px 60px ${stages[activeStageIdx].color}20`, 
              display: 'flex', 
              flexDirection: 'column',
              transition: 'all 0.5s ease'
           }}>
              {/* Terminal Header */}
              <div style={{ display: 'flex', gap: 10, marginBottom: 30 }}>
                 <div style={{ width: 14, height: 14, borderRadius: 7, background: '#ff5f56' }} />
                 <div style={{ width: 14, height: 14, borderRadius: 7, background: '#ffbd2e' }} />
                 <div style={{ width: 14, height: 14, borderRadius: 7, background: '#27c93f' }} />
              </div>

              {/* Terminal Body */}
              <div style={{ fontFamily: 'Fira Code, monospace', fontSize: 24, flex: 1, overflow: 'hidden' }}>
                 <div style={{ color: '#a1a1aa', marginBottom: 20 }}>
                    <span style={{ color: '#22c55e', marginRight: 15 }}>~</span> 
                    $ {visibleCmd}
                    {stageFrame < 40 && <span style={{ opacity: Math.sin(frame/5)>0?1:0 }}>█</span>}
                 </div>
                 
                 {stageFrame >= 60 && (
                   <div style={{ color: stages[activeStageIdx].color, whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                      {visibleOutput}
                      {stageFrame >= 60 && stageFrame < 200 && <span style={{ opacity: Math.sin(frame/3)>0?1:0 }}>█</span>}
                   </div>
                 )}
              </div>
           </div>
        </div>

      </div>
    </AbsoluteFill>
  );
};
