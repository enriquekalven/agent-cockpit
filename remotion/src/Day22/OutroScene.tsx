import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({ frame, fps, config: { damping: 200 } });
  const cmdSpring = spring({ frame, fps, delay: 15, config: { damping: 200 } });
  const linkSpring = spring({ frame, fps, delay: 30, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 50%, ${COLORS.bgLight} 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 30,
        }}
      >
        <div
          style={{
            fontSize: 28,
            fontWeight: 600,
            color: COLORS.blue,
            letterSpacing: 6,
            textTransform: 'uppercase',
            opacity: titleSpring,
          }}
        >
          Advent of Agents — Day 22
        </div>

        <div
          style={{
            fontSize: 56,
            fontWeight: 700,
            color: COLORS.text,
            textAlign: 'center',
            opacity: titleSpring,
            transform: `translateY(${interpolate(titleSpring, [0, 1], [20, 0])}px)`,
          }}
        >
          Try it yourself
        </div>

        <div
          style={{
            width: interpolate(
              spring({ frame, fps, delay: 10, config: { damping: 200 } }),
              [0, 1],
              [0, 300]
            ),
            height: 3,
            background: `linear-gradient(90deg, ${COLORS.blue}, ${COLORS.green})`,
            borderRadius: 2,
          }}
        />

        <div
          style={{
            display: 'flex',
            gap: 24,
            opacity: cmdSpring,
            transform: `translateY(${interpolate(cmdSpring, [0, 1], [20, 0])}px)`,
          }}
        >
          <div
            style={{
              fontFamily: FONT.mono,
              fontSize: 26,
              color: COLORS.blue,
              padding: '14px 32px',
              background: `${COLORS.blue}10`,
              borderRadius: 12,
              border: `1px solid ${COLORS.blue}30`,
            }}
          >
            uvx agent-starter-pack create
          </div>

          <div
            style={{
              fontFamily: FONT.mono,
              fontSize: 26,
              color: COLORS.green,
              padding: '14px 32px',
              background: `${COLORS.green}10`,
              borderRadius: 12,
              border: `1px solid ${COLORS.green}30`,
            }}
          >
            make eval
          </div>
        </div>

        <div
          style={{
            fontSize: 22,
            color: COLORS.textMuted,
            opacity: linkSpring,
            marginTop: 10,
          }}
        >
          github.com/google/agent-starter-pack
        </div>
      </div>
    </AbsoluteFill>
  );
};
