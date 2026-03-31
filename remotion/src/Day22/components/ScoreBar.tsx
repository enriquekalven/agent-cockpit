import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { COLORS, FONT } from '../styles';

interface ScoreBarProps {
  label: string;
  score: number;
  color: string;
  delay?: number;
}

export const ScoreBar: React.FC<ScoreBarProps> = ({
  label,
  score,
  color,
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const barSpring = spring({
    frame,
    fps,
    delay,
    config: { damping: 20, stiffness: 60 },
  });

  const fillWidth = interpolate(barSpring, [0, 1], [0, score * 100]);
  const displayScore = interpolate(barSpring, [0, 1], [0, score], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span
          style={{
            fontFamily: FONT.mono,
            fontSize: 18,
            color: COLORS.codeText,
            fontWeight: 500,
          }}
        >
          {label}
        </span>
        <span
          style={{
            fontFamily: FONT.mono,
            fontSize: 20,
            color,
            fontWeight: 700,
          }}
        >
          {displayScore.toFixed(2)}
        </span>
      </div>

      <div
        style={{
          width: '100%',
          height: 8,
          background: `${color}20`,
          borderRadius: 4,
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${fillWidth}%`,
            height: '100%',
            background: color,
            borderRadius: 4,
          }}
        />
      </div>
    </div>
  );
};
