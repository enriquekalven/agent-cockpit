import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';
import { slide } from '@remotion/transitions/slide';
import { TitleScene } from './TitleScene';
import { ProblemScene } from './ProblemScene';
import { ScaffoldScene } from './ScaffoldScene';
import { FileTreeScene } from './FileTreeScene';
import { EvalConceptScene } from './EvalConceptScene';
import { MetricsScene } from './MetricsScene';
import { EvalRunScene } from './EvalRunScene';
import { CICDScene } from './CICDScene';
import { TemplatesScene } from './TemplatesScene';
import { OutroScene } from './OutroScene';
import { loadFont as loadInter } from '@remotion/google-fonts/Inter';
import { loadFont as loadFiraCode } from '@remotion/google-fonts/FiraCode';

loadInter('normal', { weights: ['400', '600', '700', '800'], subsets: ['latin'] });
loadFiraCode('normal', { weights: ['400', '500', '600', '700'], subsets: ['latin'] });

// 10 scenes: 120 + 135 + 180 + 165 + 150 + 165 + 165 + 165 + 135 + 120 = 1500 frames
// 9 transitions: 9 * 15 = 135 frames overlap
// Net: 1500 - 135 = 1365 frames = 45.5s at 30fps

export const Day22: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        {/* Scene 1: Title */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 2: Problem */}
        <TransitionSeries.Sequence durationInFrames={135}>
          <ProblemScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: 'from-right' })}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 3: Scaffold */}
        <TransitionSeries.Sequence durationInFrames={180}>
          <ScaffoldScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 4: File Tree */}
        <TransitionSeries.Sequence durationInFrames={165}>
          <FileTreeScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: 'from-right' })}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 5: Eval Concept */}
        <TransitionSeries.Sequence durationInFrames={150}>
          <EvalConceptScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 6: Metrics */}
        <TransitionSeries.Sequence durationInFrames={165}>
          <MetricsScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: 'from-right' })}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 7: Eval Run */}
        <TransitionSeries.Sequence durationInFrames={165}>
          <EvalRunScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 8: CI/CD */}
        <TransitionSeries.Sequence durationInFrames={165}>
          <CICDScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: 'from-right' })}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 9: Templates */}
        <TransitionSeries.Sequence durationInFrames={135}>
          <TemplatesScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        {/* Scene 10: Outro */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <OutroScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
