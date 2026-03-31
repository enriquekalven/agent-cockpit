import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { COLORS, FONT } from './styles';
import { FileTree } from './components/FileTree';

const TREE_ENTRIES = [
  { name: 'my-agent/', isFolder: true, color: COLORS.blue },
  { name: 'agent.py', indent: 1, description: 'ADK agent definition' },
  { name: 'tools/', isFolder: true, indent: 1, color: COLORS.green },
  { name: 'evals/', isFolder: true, indent: 1, color: COLORS.yellow },
  { name: 'evalset.json', indent: 2, description: 'golden test cases' },
  { name: 'Makefile', indent: 1, description: 'eval & deploy targets' },
  { name: 'cloudbuild.yaml', indent: 1, description: 'CI/CD pipeline' },
  { name: 'deployment/', isFolder: true, indent: 1, color: COLORS.blue },
  { name: 'Dockerfile', indent: 2, description: 'containerized agent' },
];

export const FileTreeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 60% 40%, #0a1428 0%, ${COLORS.bg} 70%)`,
        fontFamily: FONT.sans,
        padding: 80,
        justifyContent: 'center',
      }}
    >
      <div style={{ display: 'flex', gap: 60, alignItems: 'center' }}>
        {/* Left: heading */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div
            style={{
              fontSize: 24,
              fontWeight: 600,
              color: COLORS.blue,
              letterSpacing: 4,
              textTransform: 'uppercase',
              opacity: headerSpring,
            }}
          >
            What You Get
          </div>

          <div
            style={{
              fontSize: 48,
              fontWeight: 700,
              color: COLORS.text,
              lineHeight: 1.2,
              opacity: headerSpring,
              transform: `translateX(${interpolate(headerSpring, [0, 1], [-30, 0])}px)`,
            }}
          >
            Production-Ready Structure
          </div>

          <div
            style={{
              fontSize: 24,
              color: COLORS.textMuted,
              lineHeight: 1.5,
              opacity: spring({ frame, fps, delay: 15, config: { damping: 200 } }),
              maxWidth: 420,
            }}
          >
            Agent, tools, evals, CI/CD, and deployment config — all pre-wired.
          </div>
        </div>

        {/* Right: file tree */}
        <div style={{ flex: 1 }}>
          <FileTree entries={TREE_ENTRIES} startDelay={15} staggerFrames={7} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
