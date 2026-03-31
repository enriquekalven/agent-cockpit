import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';

const PROBLEMS = [
  { icon: '📋', text: 'Boilerplate: agent, tools, deploy, CI/CD' },
  { icon: '🔄', text: 'Refresh prompt, hope for the best' },
  { icon: '🙈', text: 'No regression detection' },
  { icon: '✨', text: '"Trust the vibes" testing' },
];

export const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 30% 50%, #1a0a0a 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        padding: 100,
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: 40,
        }}
      >
        <div
          style={{
            fontSize: 24,
            fontWeight: 600,
            color: COLORS.red,
            letterSpacing: 4,
            textTransform: 'uppercase',
            opacity: headerSpring,
          }}
        >
          The Problem
        </div>

        <div
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: COLORS.text,
            opacity: headerSpring,
            transform: `translateX(${interpolate(headerSpring, [0, 1], [-40, 0])}px)`,
          }}
        >
          Starting from Scratch
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 24, marginTop: 20 }}>
          {PROBLEMS.map((problem, i) => {
            const itemSpring = spring({
              frame,
              fps,
              delay: 20 + i * 15,
              config: { damping: 200 },
            });

            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 20,
                  opacity: itemSpring,
                  transform: `translateX(${interpolate(itemSpring, [0, 1], [60, 0])}px)`,
                }}
              >
                <span style={{ fontSize: 36 }}>{problem.icon}</span>
                <span
                  style={{
                    fontSize: 32,
                    color: COLORS.textMuted,
                    fontWeight: 400,
                  }}
                >
                  {problem.text}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
