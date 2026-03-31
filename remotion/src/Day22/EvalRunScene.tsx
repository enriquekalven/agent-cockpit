import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';
import { TerminalBlock } from './components/TerminalBlock';

export const EvalRunScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 50%, #0a0a28 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        padding: 80,
        justifyContent: 'center',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 36 }}>
        <div
          style={{
            fontSize: 24,
            fontWeight: 600,
            color: COLORS.yellow,
            letterSpacing: 4,
            textTransform: 'uppercase',
            opacity: headerSpring,
          }}
        >
          Run Evaluation
        </div>

        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: COLORS.text,
            opacity: headerSpring,
            transform: `translateX(${interpolate(headerSpring, [0, 1], [-40, 0])}px)`,
          }}
        >
          One Command, Full Report
        </div>

        <div style={{ maxWidth: 1200, marginTop: 10 }}>
          <TerminalBlock
            title="zsh — evals"
            command="adk eval evals/evalset.json"
            outputLines={[
              '📋 Loading evalset... 4 test cases',
              '🔄 Running eval 1/4 — sync_issue ............ ✅',
              '🔄 Running eval 2/4 — create_ticket ......... ✅',
              '🔄 Running eval 3/4 — search_docs ........... ✅',
              '🔄 Running eval 4/4 — summarize_thread ...... ✅',
              '',
              '✅ All 4 evals passed — avg score: 0.92',
            ]}
            typeStartFrame={20}
            framesPerChar={2}
            lineDelay={10}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};
