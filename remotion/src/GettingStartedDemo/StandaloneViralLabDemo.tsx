import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ViralLabScene } from './ViralLabScene';

export const StandaloneViralLabDemo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#03040a' }}>
      <Sequence from={0}>
        <ViralLabScene />
      </Sequence>
    </AbsoluteFill>
  );
};
