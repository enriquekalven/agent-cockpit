import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { CertifyScene } from './CertifyScene';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

export const StandaloneCertifyDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="Governance Seal" command="uvx agentops-cockpit certify" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />
        <TransitionSeries.Sequence durationInFrames={280}>
          <CertifyScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />
        <TransitionSeries.Sequence durationInFrames={150}>
          <ClosingScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
