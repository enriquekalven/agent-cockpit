import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { GettingStartedScene } from './GettingStartedScene';
import { TitleScene } from '../EvolveDemo/TitleScene';
import { ClosingScene } from '../EvolveDemo/ClosingScene';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

export const StandaloneGettingStartedDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="Getting Started Guide" command="uv tool install agentops-cockpit" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />
        <TransitionSeries.Sequence durationInFrames={550}>
          <GettingStartedScene />
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
