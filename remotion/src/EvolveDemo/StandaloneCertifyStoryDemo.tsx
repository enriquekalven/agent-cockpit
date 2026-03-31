import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { StoryCard } from './StoryCard';
import { TerminalBlock } from '../Day22/components/TerminalBlock';

export const StandaloneCertifyStoryDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        {/* Step 1: Title */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="Why You Need Certify" command="uvx agentops-cockpit certify" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Step 2: Problem */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <StoryCard 
            title="The Problem" 
            subtitle="Closing the loop to Production."
            themeColor="#ef4444"
            points={[
              { icon: '🛑', text: 'You’ve tested your agent locally, but leadership won’t deploy.' },
              { icon: '🕵️', text: 'SecOps teams treat AI code as opaque, untrustworthy black-boxes.' },
              { icon: '📜', text: 'Missing immutable proof that the agent is actually compliant.' },
              { icon: '☁️', text: 'Deployment gets explicitly blocked due to lack of an SLA.' }
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
                 command="uvx agentops-cockpit certify"
                 outputLines={[
                   "[CERTIFY] Validating Governance and Remediation integrity...",
                   "[PASS] All critical code smells resolved.",
                   "[SLA] Cryptographic 'Seal of Approval' generated.",
                   "[READY] Agent is officially Production-Ready."
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
            subtitle="The Ultimate Go/No-Go Gatekeeper."
            themeColor="#10b981"
            points={[
              { icon: '🏆', text: 'Cryptographic SLA Seal applied cleanly to the codebase.' },
              { icon: '📑', text: 'Executive `report.md` permanently published to the Evidence Lake.' },
              { icon: '📡', text: 'Health telemetry automatically synced to the Master Registry.' },
              { icon: '🌉', text: 'Unlocked multi-cloud deployments (GCP, AWS, Azure).' }
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
              { icon: '🛡️', text: 'The absolute final governance gate before production debut.' },
              { icon: '💯', text: 'Ensures 100% compliance across FinOps, SecOps, and Architecture.' },
              { icon: '🏛️', text: 'Provides immutable safety assurance for Principal Engineers.' },
              { icon: '✅', text: 'Ready to launch with `uvx agentops-cockpit deploy`.' }
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
