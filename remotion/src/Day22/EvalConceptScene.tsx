import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';

export const EvalConceptScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });
  const codeSpring = spring({ frame, fps, delay: 15, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 70% 40%, #0a1a28 0%, ${COLORS.bg} 70%)`,
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
          ADK Evaluation
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
          Define the Golden Path
        </div>

        {/* Evalset JSON */}
        <div
          style={{
            background: COLORS.bgCode,
            borderRadius: 16,
            padding: 32,
            border: `1px solid ${COLORS.codeBorder}`,
            opacity: codeSpring,
            transform: `translateY(${interpolate(codeSpring, [0, 1], [30, 0])}px)`,
            maxWidth: 900,
          }}
        >
          <div
            style={{
              fontFamily: FONT.mono,
              fontSize: 20,
              color: COLORS.codeText,
              lineHeight: 1.8,
              whiteSpace: 'pre',
            }}
          >
            <span style={{ color: COLORS.codeKeyword }}>{'['}</span>
            {'\n  '}
            <span style={{ color: COLORS.codeKeyword }}>{'{'}</span>
            {'\n    '}
            <span style={{ color: COLORS.codeString }}>"query"</span>
            {': '}
            <span style={{ color: COLORS.codeString }}>"Sync issue PROJ-42 to GitHub"</span>
            {','}
            {'\n    '}
            <span style={{ color: COLORS.codeString }}>"expected_tool_use"</span>
            {': ['}
            {'\n      '}
            <span style={{ color: COLORS.codeKeyword }}>{'{ '}</span>
            <span style={{ color: COLORS.codeString }}>"tool_name"</span>
            {': '}
            <span style={{ color: COLORS.blue }}>"linear_get_issue"</span>
            <span style={{ color: COLORS.codeKeyword }}>{' }'}</span>
            {','}
            {'\n      '}
            <span style={{ color: COLORS.codeKeyword }}>{'{ '}</span>
            <span style={{ color: COLORS.codeString }}>"tool_name"</span>
            {': '}
            <span style={{ color: COLORS.green }}>"github_create_issue"</span>
            <span style={{ color: COLORS.codeKeyword }}>{' }'}</span>
            {'\n    ],'}
            {'\n    '}
            <span style={{ color: COLORS.codeString }}>"reference"</span>
            {': '}
            <span style={{ color: COLORS.codeString }}>"Issue synced successfully"</span>
            {'\n  '}
            <span style={{ color: COLORS.codeKeyword }}>{'}'}</span>
            {'\n'}
            <span style={{ color: COLORS.codeKeyword }}>{']'}</span>
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
