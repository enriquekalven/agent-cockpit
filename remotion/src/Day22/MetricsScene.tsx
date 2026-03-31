import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';
import { ScoreBar } from './components/ScoreBar';

const METRICS = [
  {
    name: 'tool_trajectory_avg_score',
    description: 'Right tools, right order',
    color: COLORS.blue,
    score: 0.95,
    badge: 'IN_ORDER',
  },
  {
    name: 'rubric_based_scoring',
    description: 'LLM-as-Judge with custom rubrics',
    color: COLORS.green,
    score: 0.88,
    badge: 'RUBRIC',
  },
  {
    name: 'final_response_match_v2',
    description: 'Semantic response comparison',
    color: COLORS.yellow,
    score: 0.92,
    badge: 'SEMANTIC',
  },
];

export const MetricsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 60%, #0a1a14 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        padding: 80,
        justifyContent: 'center',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 44 }}>
        <div
          style={{
            fontSize: 52,
            fontWeight: 700,
            color: COLORS.text,
            opacity: headerSpring,
            transform: `translateY(${interpolate(headerSpring, [0, 1], [-20, 0])}px)`,
          }}
        >
          Three Evaluation Metrics
        </div>

        <div style={{ display: 'flex', gap: 32 }}>
          {METRICS.map((metric, i) => {
            const cardSpring = spring({
              frame,
              fps,
              delay: 10 + i * 12,
              config: { damping: 200 },
            });

            return (
              <div
                key={i}
                style={{
                  flex: 1,
                  background: `${metric.color}08`,
                  border: `1px solid ${metric.color}30`,
                  borderRadius: 20,
                  padding: 32,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 18,
                  opacity: cardSpring,
                  transform: `translateY(${interpolate(cardSpring, [0, 1], [50, 0])}px)`,
                }}
              >
                <div
                  style={{
                    fontFamily: FONT.mono,
                    fontSize: 13,
                    color: metric.color,
                    padding: '5px 12px',
                    background: `${metric.color}15`,
                    borderRadius: 6,
                    alignSelf: 'flex-start',
                    fontWeight: 600,
                    letterSpacing: 1,
                  }}
                >
                  {metric.badge}
                </div>

                <div
                  style={{
                    fontFamily: FONT.mono,
                    fontSize: 17,
                    color: metric.color,
                    fontWeight: 600,
                    wordBreak: 'break-all',
                    lineHeight: 1.3,
                  }}
                >
                  {metric.name}
                </div>

                <div
                  style={{
                    fontSize: 20,
                    color: COLORS.textMuted,
                    lineHeight: 1.4,
                  }}
                >
                  {metric.description}
                </div>

                <div style={{ marginTop: 'auto' }}>
                  <ScoreBar
                    label="score"
                    score={metric.score}
                    color={metric.color}
                    delay={25 + i * 15}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
