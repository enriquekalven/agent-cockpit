import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';

export const TitleScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const daySpring = spring({ frame, fps, config: { damping: 200 } });
  const titleSpring = spring({ frame, fps, delay: 10, config: { damping: 200 } });
  const subtitleOpacity = interpolate(frame, [20, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const lineWidth = interpolate(frame, [15, 45], [0, 400], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 40%, ${COLORS.bgLight} 0%, ${COLORS.bg} 70%)`,
        justifyContent: 'center',
        alignItems: 'center',
        fontFamily: FONT.sans,
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 20,
        }}
      >
        <div
          style={{
            fontSize: 32,
            fontWeight: 600,
            color: COLORS.blue,
            letterSpacing: 6,
            textTransform: 'uppercase',
            opacity: daySpring,
            transform: `translateY(${interpolate(daySpring, [0, 1], [-30, 0])}px)`,
          }}
        >
          Day 22 — Season 2
        </div>

        <div
          style={{
            fontSize: 72,
            fontWeight: 800,
            color: COLORS.text,
            textAlign: 'center',
            lineHeight: 1.1,
            opacity: titleSpring,
            transform: `translateY(${interpolate(titleSpring, [0, 1], [40, 0])}px)`,
          }}
        >
          Agent Starter Pack
        </div>

        <div
          style={{
            fontSize: 72,
            fontWeight: 800,
            color: COLORS.text,
            textAlign: 'center',
            lineHeight: 1.1,
            opacity: titleSpring,
            transform: `translateY(${interpolate(titleSpring, [0, 1], [40, 0])}px)`,
          }}
        >
          & ADK Evaluation
        </div>

        <div
          style={{
            width: lineWidth,
            height: 3,
            background: `linear-gradient(90deg, ${COLORS.blue}, ${COLORS.green})`,
            borderRadius: 2,
          }}
        />

        <div
          style={{
            fontSize: 34,
            fontWeight: 400,
            color: COLORS.textMuted,
            textAlign: 'center',
            opacity: subtitleOpacity,
            maxWidth: 800,
          }}
        >
          From Zero to Battle-Tested Agent
        </div>
      </div>
    </AbsoluteFill>
  );
};
