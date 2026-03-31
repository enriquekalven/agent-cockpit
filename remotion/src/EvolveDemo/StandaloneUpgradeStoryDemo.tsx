import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { StoryCard } from './StoryCard';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const StandaloneUpgradeStoryDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        {/* Step 1: Title */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="Why You Need Upgrade" command="uvx agentops-cockpit upgrade --docs-url" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 2: Problem */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="The Problem" 
            subtitle="The Technical Bankruptcy of Breaking Changes."
            themeColor="#ef4444"
            points={[
              { icon: '🌪️', text: 'Frameworks evolve rapidly, leaving your agents stranded on deprecated APIs.' },
              { icon: '📖', text: 'Reading 100-page migration guides is an exhausting, manual burden.' },
              { icon: '🧩', text: 'Tracking down and refactoring every deprecated method takes weeks.' },
              { icon: '⏳', text: 'Velocity grinds to a halt while developers pay off technical debt.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 3: One Command */}
        <TransitionSeries.Sequence durationInFrames={200}>
           <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>The One Command</h2>
             <div style={{ width: '100%', maxWidth: 1350 }}>
               <TerminalBlock 
                 title="Terminal - Engine Core"
                 command="uvx agentops-cockpit upgrade --docs-url 'https://docs.api/v2.0/migrate'"
                 outputLines={[
                   "[DIGEST] Ingesting and analyzing target migration guide...",
                   "[AST-SCAN] Mapping deprecated methods across 42 active files.",
                   "[REWRITE] Synthesizing new v2.0 framework implementation...",
                   "[SUCCESS] Codebase autonomously upgraded on branch 'refactor/autonomous-upgrade'."
                 ]}
                 typeStartFrame={20}
                 framesPerChar={0.8}
                 lineDelay={15}
               />
             </div>
           </AbsoluteFill>
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 4: Outputs */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="What You Get" 
            subtitle="An Autonomous Migration Engineer."
            themeColor="#10b981"
            points={[
              { icon: '🧠', text: 'The Engine autonomously digests the target migration documentation.' },
              { icon: '🔍', text: 'AST-aware scanners pinpoint exact locations of deprecated logic.' },
              { icon: '✨', text: 'Your entire codebase gets surgically rewritten to the new standard.' },
              { icon: '🛡️', text: 'Refactored code is sandboxed into a clean, ready-to-test PR branch.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 5: Summary */}
        <TransitionSeries.Sequence durationInFrames={300}>
          <StoryCard 
            title="Summary" 
            themeColor="#a855f7"
            points={[
              { icon: '⏱️', text: 'Saves weeks of manual reading, hunting, and explicitly replacing logic.' },
              { icon: '📈', text: 'Keeps your fleet permanently aligned with cutting-edge frameworks.' },
              { icon: '🚫', text: 'Prevents the slow decay and technical bankruptcy of AI payloads.' },
              { icon: '✅', text: 'A completely autonomous framework migration with zero human fatigue.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 6: Closing */}
        <TransitionSeries.Sequence durationInFrames={150}>
          <ClosingScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
