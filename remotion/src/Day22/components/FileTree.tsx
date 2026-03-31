import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { COLORS, FONT } from '../styles';

interface FileTreeEntry {
  name: string;
  description?: string;
  indent?: number;
  isFolder?: boolean;
  color?: string;
}

interface FileTreeProps {
  entries: FileTreeEntry[];
  startDelay?: number;
  staggerFrames?: number;
}

export const FileTree: React.FC<FileTreeProps> = ({
  entries,
  startDelay = 10,
  staggerFrames = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        background: COLORS.bgCode,
        borderRadius: 16,
        padding: '28px 32px',
        border: `1px solid ${COLORS.codeBorder}`,
        display: 'flex',
        flexDirection: 'column',
        gap: 6,
      }}
    >
      {entries.map((entry, i) => {
        const entrySpring = spring({
          frame,
          fps,
          delay: startDelay + i * staggerFrames,
          config: { damping: 200 },
        });

        const indent = (entry.indent ?? 0) * 28;
        const folderColor = entry.color ?? (entry.isFolder ? COLORS.blue : COLORS.textMuted);

        return (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              paddingLeft: indent,
              opacity: entrySpring,
              transform: `translateX(${interpolate(entrySpring, [0, 1], [20, 0])}px)`,
            }}
          >
            <span style={{ fontSize: 18, color: folderColor, width: 22, textAlign: 'center' }}>
              {entry.isFolder ? '📁' : '📄'}
            </span>
            <span
              style={{
                fontFamily: FONT.mono,
                fontSize: 20,
                color: entry.isFolder ? folderColor : COLORS.codeText,
                fontWeight: entry.isFolder ? 600 : 400,
              }}
            >
              {entry.name}
            </span>
            {entry.description && (
              <span
                style={{
                  fontSize: 16,
                  color: COLORS.textMuted,
                  marginLeft: 8,
                  fontStyle: 'italic',
                }}
              >
                {entry.description}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
};
