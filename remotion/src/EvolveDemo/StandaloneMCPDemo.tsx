import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { MCPScene } from './MCPScene';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

export const StandaloneMCPDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="MCP Handshake" command="uvx agentops-cockpit mcp-server" />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />
        <TransitionSeries.Sequence durationInFrames={300}>
          <MCPScene />
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
