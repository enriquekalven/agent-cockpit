import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';

const TEMPLATES = [
  { name: 'ReAct Agent', color: COLORS.blue },
  { name: 'RAG Agent', color: COLORS.green },
  { name: 'Multi-Agent', color: COLORS.yellow },
  { name: 'MCP Agent', color: COLORS.blue },
  { name: 'Multimodal', color: COLORS.green },
  { name: 'Live API', color: COLORS.yellow },
  { name: 'A2A Agent', color: COLORS.blue },
  { name: 'LiteLLM', color: COLORS.green },
];

export const TemplatesScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });
  const starsSpring = spring({ frame, fps, delay: 50, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 40%, ${COLORS.bgLight} 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        padding: 80,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 44,
        }}
      >
        <div
          style={{
            fontSize: 48,
            fontWeight: 700,
            color: COLORS.text,
            textAlign: 'center',
            opacity: headerSpring,
            transform: `translateY(${interpolate(headerSpring, [0, 1], [-20, 0])}px)`,
          }}
        >
          8 Templates, One CLI
        </div>

        {/* Template grid - 2 rows of 4 */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 20,
            justifyContent: 'center',
            maxWidth: 1000,
          }}
        >
          {TEMPLATES.map((template, i) => {
            const badgeSpring = spring({
              frame,
              fps,
              delay: 10 + i * 6,
              config: { damping: 200 },
            });

            return (
              <div
                key={i}
                style={{
                  fontFamily: FONT.mono,
                  fontSize: 22,
                  color: template.color,
                  fontWeight: 600,
                  padding: '14px 28px',
                  background: `${template.color}10`,
                  border: `1px solid ${template.color}35`,
                  borderRadius: 12,
                  opacity: badgeSpring,
                  transform: `scale(${interpolate(badgeSpring, [0, 1], [0.8, 1])})`,
                }}
              >
                {template.name}
              </div>
            );
          })}
        </div>

        {/* Stars counter */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            opacity: starsSpring,
            transform: `translateY(${interpolate(starsSpring, [0, 1], [15, 0])}px)`,
          }}
        >
          <span style={{ fontSize: 32 }}>⭐</span>
          <span
            style={{
              fontSize: 32,
              fontWeight: 700,
              color: COLORS.yellow,
              fontFamily: FONT.mono,
            }}
          >
            6,000+ stars
          </span>
          <span
            style={{
              fontSize: 24,
              color: COLORS.textMuted,
              marginLeft: 8,
            }}
          >
            on GitHub
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
