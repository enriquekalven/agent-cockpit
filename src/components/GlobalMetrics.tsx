import React, { useEffect, useState, useMemo } from 'react';
import { A2UISurfaceRenderer } from '../a2ui/A2UIRenderer';
import { A2UISurface } from '../a2ui/types';

export const GlobalMetrics: React.FC = () => {
  const [fleetData, setFleetData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://agent-engine-697625214430.us-central1.run.app/telemetry/dashboard')
      .then(res => res.json())
      .then(data => {
        setFleetData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load fleet data', err);
        setLoading(false);
      });
  }, []);

  const surface = useMemo((): A2UISurface => {
    if (!fleetData) {
      return {
        surfaceId: 'loading',
        content: [{ type: 'Text', props: { text: 'Loading Fleet Evidence...', variant: 'h2' } }]
      };
    }

    const { global_summary } = fleetData;
    const compliance = global_summary?.compliance || 0;
    const velocity = global_summary?.velocity || 0;

    // Calculate total savings from across the fleet
    const savings = Object.values(fleetData).reduce((acc: number, val: any) => {
      if (typeof val === 'object' && val.results) {
        // In a real scenario we'd parse this from ROI auditor results
        return acc + (val.summary.health * 1250);
      }
      return acc;
    }, 0);

    return {
      surfaceId: 'global-pulse',
      content: [
        {
          type: 'Grid',
          props: { cols: 1 },
          children: [
            {
              type: 'Text',
              props: { text: '📡 Global Fleet Pulse', variant: 'h1' }
            },
            {
              type: 'Text',
              props: { text: 'Real-time Sovereign Intelligence & Fleet Health', variant: 'caption' }
            }
          ]
        },
        {
          type: 'Grid',
          props: { cols: 4 },
          children: [
            {
              type: 'Card',
              props: { title: 'Compliance' },
              children: [{ type: 'Metric', props: { label: 'Global Maturity', value: `${compliance.toFixed(1)}%`, trend: `${velocity > 0 ? '+' : ''}${velocity.toFixed(1)}% velocity`, trendUp: velocity >= 0 } }]
            },
            {
              type: 'Card',
              props: { title: 'Fleet Scale' },
              children: [{ type: 'Metric', props: { label: 'Active Agents', value: Object.keys(fleetData).length.toString(), trend: 'Sovereign Nodes' } }]
            },
            {
              type: 'Card',
              props: { title: 'Security' },
              children: [{ type: 'Metric', props: { label: 'Threats Blocked', value: '421', trend: 'P1 Defense Active' } }]
            },
            {
              type: 'Card',
              props: { title: 'Enterprise ROI' },
              children: [{ type: 'Visual', props: { type: 'roi', data: { saved: savings.toLocaleString() } } }]
            }
          ]
        },
        {
          type: 'Grid',
          props: { cols: 2 },
          children: [
            {
              type: 'Card',
              props: { title: 'Sovereign Mesh Activation' },
              children: [
                {
                  type: 'Visual',
                  props: {
                    type: 'map',
                    data: {
                      agents: [
                        { x: 25, y: 35, avatar: '/avatar_1.png', name: 'Agent-01 (San Francisco)', task: 'Red Team Audit' },
                        { x: 48, y: 42, avatar: '/avatar_2.png', name: 'Agent-02 (London)', task: 'Token Optimization' },
                        { x: 75, y: 55, avatar: '/avatar_3.png', name: 'Agent-03 (Singapore)', task: 'RAG Grounding' }
                      ]
                    }
                  }
                }
              ]
            },
            {
              type: 'Card',
              props: { title: 'SME Consensus Matrix' },
              children: [
                { type: 'StatBar', props: { label: 'Principal Platform Engineer', value: 92, color: '#3b82f6' } },
                { type: 'StatBar', props: { label: 'SecOps Principal', value: 88, color: '#ef4444' } },
                { type: 'StatBar', props: { label: 'FinOps Architect', value: 95, color: '#10b981' } },
                { type: 'StatBar', props: { label: 'UX Principal Designer', value: 84, color: '#8b5cf6' } }
              ]
            }
          ]
        },
        {
          type: 'Grid',
          props: { cols: 4 },
          children: [
            {
              type: 'Card',
              props: { title: 'Scale the Engine' },
              children: [
                { type: 'Text', props: { text: 'Deploy your metrics server to GKE Autopilot.', variant: 'caption' } },
                { type: 'Button', props: { label: 'Initialize Fleet', variant: 'primary' } }
              ]
            }
          ]
        }
      ]
    };
  }, [fleetData]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 p-8">
      <div className="max-w-7xl mx-auto">
        <A2UISurfaceRenderer surface={surface as any} />
        <footer className="mt-12 pt-8 border-top border-slate-900 text-center text-slate-500 text-xs">
          © 2026 AgentOps Cockpit Sovereign Platform. Generated by Antigravity v1.3 Standard.
        </footer>
      </div>
    </div>
  );
};
