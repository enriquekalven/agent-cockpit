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

export const ScaffoldScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 40% 50%, #0a1a14 0%, ${COLORS.bg} 70%)`,
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
            color: COLORS.green,
            letterSpacing: 4,
            textTransform: 'uppercase',
            opacity: headerSpring,
          }}
        >
          One Command
        </div>

        <div
          style={{
            fontSize: 52,
            fontWeight: 700,
            color: COLORS.text,
            opacity: headerSpring,
            transform: `translateX(${interpolate(headerSpring, [0, 1], [-40, 0])}px)`,
          }}
        >
          Scaffold Your Agent
        </div>

        <div style={{ maxWidth: 1200, marginTop: 10 }}>
          <TerminalBlock
            title="zsh — my-agent"
            command="uvx agent-starter-pack create my-agent"
            outputLines={[
              '🔧 Scaffolding agent project...',
              '📁 Created my-agent/',
              '✅ Agent, evals, CI/CD, deployment — all wired up',
            ]}
            typeStartFrame={25}
            framesPerChar={2}
            lineDelay={14}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};
