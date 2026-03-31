import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

import { TitleScene } from './TitleScene';
import { TerminalScene } from './TerminalScene';
import { UpgradeScene } from './UpgradeScene';
import { MCPScene } from './MCPScene';
import { CertifyScene } from './CertifyScene';
import { ClosingScene } from './ClosingScene';

export const AgentOpsCockpitDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        {/* Title */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="AgentOps Cockpit" command="The Autonomous Framework" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* 1. Terminal (Evolve) */}
        <TransitionSeries.Sequence durationInFrames={360}>
          <TerminalScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* 2. Upgrade (ADK) */}
        <TransitionSeries.Sequence durationInFrames={280}>
          <UpgradeScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* 3. MCP (Handshake) */}
        <TransitionSeries.Sequence durationInFrames={300}>
          <MCPScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* 4. Certify (Governance Seal) */}
        <TransitionSeries.Sequence durationInFrames={280}>
          <CertifyScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />

        {/* Closing */}
        <TransitionSeries.Sequence durationInFrames={150}>
          <ClosingScene />
        </TransitionSeries.Sequence>

      </TransitionSeries>
    </AbsoluteFill>
  );
};
