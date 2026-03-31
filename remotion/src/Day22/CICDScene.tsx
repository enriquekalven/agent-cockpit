import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';

const PIPELINE_STEPS = [
  { label: 'git push', icon: '📦', color: COLORS.textMuted },
  { label: 'make eval', icon: '🧪', color: COLORS.blue },
  { label: 'trajectory check', icon: '🛤️', color: COLORS.yellow },
  { label: 'rubric score', icon: '⚖️', color: COLORS.green },
];

export const CICDScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });
  const resultSpring = spring({ frame, fps, delay: 70, config: { damping: 15, stiffness: 80 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 60% 50%, #0a0a28 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        padding: 100,
        justifyContent: 'center',
      }}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 50 }}>
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: 12,
            opacity: headerSpring,
          }}
        >
          <div
            style={{
              fontSize: 24,
              fontWeight: 600,
              color: COLORS.blue,
              letterSpacing: 4,
              textTransform: 'uppercase',
            }}
          >
            Automate It
          </div>
          <div
            style={{
              fontSize: 52,
              fontWeight: 700,
              color: COLORS.text,
              transform: `translateX(${interpolate(headerSpring, [0, 1], [-40, 0])}px)`,
            }}
          >
            CI/CD Guardrails
          </div>
        </div>

        {/* Pipeline visualization */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 0,
            justifyContent: 'center',
          }}
        >
          {PIPELINE_STEPS.map((step, i) => {
            const stepSpring = spring({
              frame,
              fps,
              delay: 15 + i * 12,
              config: { damping: 200 },
            });
            const arrowSpring = spring({
              frame,
              fps,
              delay: 22 + i * 12,
              config: { damping: 200 },
            });

            return (
              <React.Fragment key={i}>
                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: 12,
                    opacity: stepSpring,
                    transform: `scale(${interpolate(stepSpring, [0, 1], [0.7, 1])})`,
                  }}
                >
                  <div
                    style={{
                      width: 80,
                      height: 80,
                      borderRadius: 20,
                      background: COLORS.bgCode,
                      border: `1px solid ${COLORS.codeBorder}`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: 36,
                    }}
                  >
                    {step.icon}
                  </div>
                  <div
                    style={{
                      fontFamily: FONT.mono,
                      fontSize: 18,
                      color: step.color,
                      fontWeight: 500,
                    }}
                  >
                    {step.label}
                  </div>
                </div>

                {i < PIPELINE_STEPS.length - 1 && (
                  <div
                    style={{
                      fontSize: 32,
                      color: COLORS.textMuted,
                      margin: '0 24px',
                      marginBottom: 30,
                      opacity: arrowSpring,
                    }}
                  >
                    →
                  </div>
                )}
              </React.Fragment>
            );
          })}

          {/* Result arrow */}
          <div
            style={{
              fontSize: 32,
              color: COLORS.textMuted,
              margin: '0 24px',
              marginBottom: 30,
              opacity: spring({ frame, fps, delay: 62, config: { damping: 200 } }),
            }}
          >
            →
          </div>

          {/* Pass result */}
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 12,
              opacity: resultSpring,
              transform: `scale(${interpolate(resultSpring, [0, 1], [0.5, 1])})`,
            }}
          >
            <div
              style={{
                width: 80,
                height: 80,
                borderRadius: 20,
                background: `${COLORS.green}20`,
                border: `2px solid ${COLORS.green}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 36,
              }}
            >
              ✅
            </div>
            <div
              style={{
                fontFamily: FONT.mono,
                fontSize: 18,
                color: COLORS.green,
                fontWeight: 700,
              }}
            >
              PASS
            </div>
          </div>
        </div>

        {/* YAML snippet */}
        <div
          style={{
            background: COLORS.bgCode,
            borderRadius: 12,
            padding: '20px 28px',
            border: `1px solid ${COLORS.codeBorder}`,
            opacity: resultSpring,
            maxWidth: 600,
            alignSelf: 'center',
          }}
        >
          <div
            style={{
              fontFamily: FONT.mono,
              fontSize: 16,
              color: COLORS.codeText,
              lineHeight: 1.7,
              whiteSpace: 'pre',
            }}
          >
            <span style={{ color: COLORS.codeKeyword }}>steps</span>
            {':\n  - '}
            <span style={{ color: COLORS.codeKeyword }}>name</span>
            {': '}
            <span style={{ color: COLORS.codeString }}>Run ADK Eval</span>
            {'\n    '}
            <span style={{ color: COLORS.codeKeyword }}>run</span>
            {': '}
            <span style={{ color: COLORS.codeString }}>make eval</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
