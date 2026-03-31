import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { StoryCard } from './StoryCard';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const StandaloneEvolveStoryDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        {/* Step 1: Title */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="Why You Need Evolve" command="uvx agentops-cockpit evolve" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 2: Problem */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="The Problem" 
            subtitle="When do you need the Closer Engine?"
            themeColor="#ef4444"
            points={[
              { icon: '🏚️', text: 'An ancient, unmaintained production agent sits on your drive.' },
              { icon: '🍝', text: 'The architecture acts as an outdated, monolithic "Spaghetti Agent".' },
              { icon: '🦕', text: 'Frameworks and pip dependencies are wildly outdated.' },
              { icon: '⚠️', text: 'Lacking telemetry, reliability hooks, or modern caching.' }
            ]}
          />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 3: One Command */}
        <TransitionSeries.Sequence durationInFrames={200}>
           <AbsoluteFill style={{ padding: 60, justifyContent: 'center', alignItems: 'center', background: 'radial-gradient(ellipse at 50% 50%, #0c0f1a, #03040a 80%)' }}>
             <h2 style={{ color: 'white', fontSize: 56, fontWeight: 900, marginBottom: 50, fontFamily: 'Inter' }}>The One Command</h2>
             <div style={{ width: '100%', maxWidth: 1200 }}>
               <TerminalBlock 
                 title="Terminal - Engine Core"
                 command="uvx agentops-cockpit evolve"
                 outputLines={[
                   "[AGENT] Scanning agent architecture & environment...",
                   "[AGENT] Detected outdated codebase and missing dependencies.",
                   "[FIX] Engaging Autonomous Code Remediation..."
                 ]}
                 typeStartFrame={20}
                 framesPerChar={1}
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
            subtitle="Code synthetically upgraded in a secure sandbox."
            themeColor="#10b981"
            points={[
              { icon: '🏗️', text: 'Monoliths proactively split into scalable Modular Routers.' },
              { icon: '🛡️', text: 'Poka-Yoke strict timeouts and retry backoff loops baked in.' },
              { icon: '🗂️', text: 'Context-Caching optimizations added to all payload queries.' },
              { icon: '📦', text: 'Dependencies properly pinned and framework SDKs updated.' }
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
              { icon: '🚀', text: 'Unmaintained production agents instantly brought to Enterprise Standards.' },
              { icon: '🤖', text: 'Zero manual refactoring required by human developers.' },
              { icon: '🔒', text: 'Committed safely to an isolated "fix/autonomous-refactor" branch.' },
              { icon: '✅', text: 'Fleet ready for immediate production deployment.' }
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
