import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { StoryCard } from './StoryCard';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const StandaloneQwiklabsDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        {/* Step 1: Title Card */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="NEXT'26 SOL 331 Mini Labs" command="Taming the Rogue Agent" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 2: Overview Scenario Card */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="Overview & Context" 
            subtitle="The Ladder of Autonomy"
            themeColor="#3b82f6"
            points={[
              { icon: '📜', text: 'AgentOps Cockpit is the ultimate control surface for scaling AI.' },
              { icon: '🪜', text: 'Treats your agent code as a malleable asset via AST analysis.' },
              { icon: '🏛️', text: 'Transforms a dangerous, non-compliant Rogue Agent into a certified system.' },
              { icon: '🍝', text: 'Fixes architectural debt: missing retries, unoptimized caching.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 3: Learning Objectives */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="Learning Objectives" 
            subtitle="What you will achieve in this lab"
            themeColor="#8b5cf6"
            points={[
              { icon: '⚡', text: 'Zero-Install Magic: Execute Cockpit seamlessly via uvx.' },
              { icon: '🪜', text: 'The Ladder of Autonomy: Identify maturity levels of AI pipelines.' },
              { icon: '🕵️', text: 'The Roast: Use Cockpit to audit and assess architectural debt.' },
              { icon: '🤖', text: 'Automated Evolution: Remediate the code without writing boilerplate.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 4: Module 0 */}
        <TransitionSeries.Sequence durationInFrames={180}>
          <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: '#9ca3af', fontSize: 36, fontWeight: 700, marginBottom: 20, fontFamily: 'Inter' }}>Module 0</h2>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>Zero Install Magic</h2>
             <div style={{ width: '100%', maxWidth: 1200 }}>
               <TerminalBlock 
                 title="Terminal - Zero Install"
                 command="uvx agentops-cockpit --help"
                 outputLines={[
                   "Usage: agentops-cockpit [OPTIONS] COMMAND [ARGS]...",
                   "The Ultimate AgentOps CLI."
                 ]}
                 typeStartFrame={20}
                 framesPerChar={1}
                 lineDelay={5}
               />
             </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 5: Module 1 */}
        <TransitionSeries.Sequence durationInFrames={200}>
          <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: '#9ca3af', fontSize: 36, fontWeight: 700, marginBottom: 20, fontFamily: 'Inter' }}>Module 1</h2>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>Scaffold Rogue Agent</h2>
             <div style={{ width: '100%', maxWidth: 1200 }}>
               <TerminalBlock 
                 title="Terminal - Scaffold"
                 command="uvx --python 3.12 --refresh agentops-cockpit@latest create rogue-agent"
                 outputLines={[
                   "🧪 Bootstrapping Rogue Agent for viral lab...",
                   "✅ Viral Lab environment ready. The Rogue Agent is live in ./my_super_agent"
                 ]}
                 typeStartFrame={20}
                 framesPerChar={1}
                 lineDelay={10}
               />
             </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 6: Module 2 */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: '#9ca3af', fontSize: 36, fontWeight: 700, marginBottom: 20, fontFamily: 'Inter' }}>Module 2</h2>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>The Roast</h2>
             <div style={{ width: '100%', maxWidth: 1200 }}>
               <TerminalBlock 
                 title="Terminal - The Roast"
                 command="cd ./my_super_agent && uvx agentops-cockpit audit report"
                 outputLines={[
                   "🕵️‍♂️ Initializing Principal SME Board...",
                   "❌ P1 Security: Hardcoded Credentials Detected",
                   "❌ P4 FinOps: Context Caching Missing (Massive token waste)",
                   "📄 Printable HTML Report generated."
                 ]}
                 typeStartFrame={20}
                 framesPerChar={1}
                 lineDelay={15}
               />
             </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 7: Module 3 */}
        <TransitionSeries.Sequence durationInFrames={200}>
          <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: '#9ca3af', fontSize: 36, fontWeight: 700, marginBottom: 20, fontFamily: 'Inter' }}>Module 3</h2>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>Climbing the Ladder</h2>
             <div style={{ width: '100%', maxWidth: 1200 }}>
               <TerminalBlock 
                 title="Terminal - Climbing the Ladder"
                 command="uvx agentops-cockpit evolve"
                 outputLines={[
                   "🤖 TRINITY AUTONOMOUS EVOLUTION",
                   "📦 Patching AST: Injecting @cockpit_reflection & tenacity...",
                   "✨ Architecture upgraded without breaking business logic!"
                 ]}
                 typeStartFrame={20}
                 framesPerChar={1}
                 lineDelay={12}
               />
             </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 8: Module 4 */}
        <TransitionSeries.Sequence durationInFrames={200}>
          <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: '#9ca3af', fontSize: 36, fontWeight: 700, marginBottom: 20, fontFamily: 'Inter' }}>Module 4</h2>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>The Production Gate</h2>
             <div style={{ width: '100%', maxWidth: 1200 }}>
               <TerminalBlock 
                 title="Terminal - The Production Gate"
                 command="uvx agentops-cockpit certify"
                 outputLines={[
                   "🛫 LAUNCHING PRE-FLIGHT SYSTEM VERIFICATION...",
                   "✅ Red Team Security (Full) Passed",
                   "🏆 CERTIFICATION GRANTED: Ready for Production Deployment."
                 ]}
                 typeStartFrame={20}
                 framesPerChar={1}
                 lineDelay={12}
               />
             </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 9: Summary */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="Lab Summary" 
            subtitle="Key Takeaways & Commands"
            themeColor="#10b981"
            points={[
              { icon: '🎯', text: 'You tamed a non-compliant Rogue Agent into a production-ready asset.' },
              { icon: '🔍', text: 'uvx agentops-cockpit audit report: The rigorous automated Roast.' },
              { icon: '✨', text: 'uvx agentops-cockpit evolve: Autonomous AST-based remediation.' },
              { icon: '🏆', text: 'uvx agentops-cockpit certify: Pre-flight Production Gate Validation.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 10: Closing */}
        <TransitionSeries.Sequence durationInFrames={150}>
          <ClosingScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
