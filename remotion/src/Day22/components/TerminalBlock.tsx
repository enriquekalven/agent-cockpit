import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { COLORS, FONT } from '../styles';

interface TerminalBlockProps {
  title?: string;
  command: string;
  outputLines: string[];
  /** Frame at which typing starts (relative to scene) */
  typeStartFrame?: number;
  /** Frames per character for the command */
  framesPerChar?: number;
  /** Delay between output lines in frames */
  lineDelay?: number;
}

export const TerminalBlock: React.FC<TerminalBlockProps> = ({
  title = 'Terminal',
  command,
  outputLines,
  typeStartFrame = 20,
  framesPerChar = 2,
  lineDelay = 12,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const windowSpring = spring({ frame, fps, config: { damping: 200 } });

  // Typewriter: reveal characters of the command
  const charsToShow = Math.max(
    0,
    Math.floor((frame - typeStartFrame) / framesPerChar)
  );
  const visibleCommand = command.slice(0, charsToShow);
  const commandDone = charsToShow >= command.length;
  const commandDoneFrame = typeStartFrame + command.length * framesPerChar;

  // Blinking cursor
  const cursorVisible = !commandDone || Math.floor(frame / 15) % 2 === 0;

  return (
    <div
      style={{
        background: '#1e1e2e',
        borderRadius: 16,
        overflow: 'hidden',
        border: `1px solid ${COLORS.codeBorder}`,
        opacity: windowSpring,
        transform: `translateY(${interpolate(windowSpring, [0, 1], [30, 0])}px)`,
        width: '100%',
      }}
    >
      {/* Title bar */}
      <div
        style={{
          background: '#16162a',
          padding: '12px 20px',
          display: 'flex',
          alignItems: 'center',
          gap: 10,
        }}
      >
        <div style={{ display: 'flex', gap: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ff5f57' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ffbd2e' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#28c840' }} />
        </div>
        <div
          style={{
            fontFamily: FONT.mono,
            fontSize: 14,
            color: COLORS.textMuted,
            marginLeft: 8,
          }}
        >
          {title}
        </div>
      </div>

      {/* Terminal body */}
      <div style={{ padding: '24px 28px', minHeight: 120 }}>
        {/* Command line */}
        <div
          style={{
            fontFamily: FONT.mono,
            fontSize: 22,
            lineHeight: 1.6,
            display: 'flex',
          }}
        >
          <span style={{ color: COLORS.green, marginRight: 12 }}>$</span>
          <span style={{ color: COLORS.codeText }}>{visibleCommand}</span>
          {!commandDone && cursorVisible && (
            <span style={{ color: COLORS.green, fontWeight: 700 }}>|</span>
          )}
        </div>

        {/* Output lines */}
        {commandDone && (
          <div style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 4 }}>
            {outputLines.map((line, i) => {
              const lineStart = commandDoneFrame + 8 + i * lineDelay;
              const lineOpacity = interpolate(frame, [lineStart, lineStart + 6], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });

              return (
                <div
                  key={i}
                  style={{
                    fontFamily: FONT.mono,
                    fontSize: 18,
                    color: COLORS.textMuted,
                    lineHeight: 1.7,
                    opacity: lineOpacity,
                    whiteSpace: 'pre',
                  }}
                >
                  {line}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
