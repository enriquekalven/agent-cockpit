import React, { useMemo } from 'react';
import { Globe, Activity, Shield, Zap, TrendingUp, Users } from 'lucide-react';
import { motion } from 'framer-motion';

export const GlobalMetrics: React.FC = () => {
  // Simulated data - in real life this would come from your telemetry backend
  const stats = useMemo(() => ({
    totalInstalls: 12542,
    activeAgents: 890,
    successRate: 84.4,
    threatsBlocked: 421,
    costSaved: 15400,
    topRegions: [
      { name: 'North America', count: 4500, color: '#3b82f6' },
      { name: 'Europe', count: 3200, color: '#10b981' },
      { name: 'Asia Pacific', count: 2800, color: '#8b5cf6' },
      { name: 'Others', count: 2042, color: '#64748b' }
    ]
  }), []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="mb-12 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2">
              📡 Global <span className="text-blue-500">Fleet Pulse</span>
            </h1>
            <p className="text-slate-400 text-lg">Real-time metrics from the AgentOps Cockpit ecosystem.</p>
          </div>
          <div className="flex items-center gap-3 bg-slate-900/50 border border-slate-800 px-4 py-2 rounded-full">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
            </span>
            <span className="text-sm font-bold text-blue-400">LIVE NETWORK STATUS</span>
          </div>
        </header>

        {/* Global Map & High-Level Stats */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
          <div className="lg:col-span-2 bg-slate-900/40 border border-slate-800 rounded-3xl p-8 backdrop-blur-xl relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-transparent pointer-events-none" />
            <h3 className="text-xl font-bold text-white mb-8 flex items-center gap-2">
              <Globe className="text-blue-500" />
              Global Activation Map
            </h3>
            
            <div className="relative h-[400px] flex items-center justify-center">
              {/* This is a visual representation of the map since we don't have a map library here */}
              <div className="w-full h-full border border-slate-800/50 rounded-2xl bg-slate-950/50 relative overflow-hidden">
                <div className="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/world-map.png')] bg-center bg-no-repeat bg-contain" />
                
                {/* Simulated Data Points */}
                {[...Array(15)].map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: i * 0.1, duration: 0.5 }}
                    className="absolute w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.8)]"
                    style={{
                      top: `${Math.random() * 80 + 10}%`,
                      left: `${Math.random() * 80 + 10}%`,
                    }}
                  >
                    <span className="absolute inset-0 animate-ping bg-blue-400 rounded-full opacity-75"></span>
                  </motion.div>
                ))}
              </div>

              <div className="absolute bottom-4 left-4 flex flex-wrap gap-4">
                {stats.topRegions.map(region => (
                  <div key={region.name} className="flex items-center gap-2 text-xs font-bold text-slate-400">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: region.color }} />
                    {region.name}: {region.count.toLocaleString()}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-6">
            <MetricCard 
              icon={<Users className="text-blue-400" />} 
              label="Total Installations" 
              value={stats.totalInstalls.toLocaleString()} 
              color="blue"
              trend="+12% this week"
            />
            <MetricCard 
              icon={<Activity className="text-green-400" />} 
              label="Active Audits (24h)" 
              value={stats.activeAgents.toLocaleString()} 
              color="green"
              trend="84.4% success rate"
            />
            <MetricCard 
              icon={<Shield className="text-red-400" />} 
              label="Threats Neutralized" 
              value={stats.threatsBlocked.toLocaleString()} 
              color="red"
              trend="Zero-day coverage"
            />
          </div>
        </div>

        {/* Detailed Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-2xl">
            <h4 className="text-slate-500 text-xs font-black uppercase tracking-widest mb-4">SME Consensus</h4>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm">Platform SME</span>
              <span className="text-green-500 font-mono text-sm">92%</span>
            </div>
            <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-green-500" style={{ width: '92%' }} />
            </div>
            <div className="flex items-center justify-between mt-4 mb-2">
              <span className="text-sm">SecOps SME</span>
              <span className="text-blue-500 font-mono text-sm">88%</span>
            </div>
            <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500" style={{ width: '88%' }} />
            </div>
          </div>

          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-2xl flex flex-col justify-center">
            <h4 className="text-slate-500 text-xs font-black uppercase tracking-widest mb-2 text-center">ROI Waterfall</h4>
            <div className="text-center">
              <span className="text-4xl font-extrabold text-white">${(stats.costSaved / 1000).toFixed(1)}K</span>
              <p className="text-slate-500 text-sm mt-1">Saved via Context Caching</p>
            </div>
          </div>

          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-2xl">
            <h4 className="text-slate-500 text-xs font-black uppercase tracking-widest mb-4 text-center">Top Commands</h4>
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center bg-slate-800/30 p-2 rounded-lg">
                <code className="text-xs text-blue-400">report --deep</code>
                <span className="text-xs font-bold text-slate-300">42%</span>
              </div>
              <div className="flex justify-between items-center bg-slate-800/30 p-2 rounded-lg">
                <code className="text-xs text-blue-400">evolve --branch</code>
                <span className="text-xs font-bold text-slate-300">28%</span>
              </div>
              <div className="flex justify-between items-center bg-slate-800/30 p-2 rounded-lg">
                <code className="text-xs text-blue-400">red-team</code>
                <span className="text-xs font-bold text-slate-300">15%</span>
              </div>
            </div>
          </div>

          <div className="bg-blue-600/10 border border-blue-500/30 p-6 rounded-2xl flex flex-col items-center justify-center text-center group transition-all hover:bg-blue-600/20">
            <div className="w-12 h-12 bg-blue-500 rounded-2xl flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(59,130,246,0.4)] group-hover:scale-110 transition-transform">
              <Zap className="text-white fill-white" />
            </div>
            <h4 className="text-white font-bold mb-1">Scale the Engine</h4>
            <p className="text-blue-200/60 text-xs">Deploy your metrics server to GKE Autopilot.</p>
          </div>
        </div>

        <footer className="mt-12 pt-8 border-top border-slate-800 text-center text-slate-500 text-xs">
          © 2026 AgentOps Cockpit Sovereign Platform. Generated by Antigravity v1.3 Standard.
        </footer>
      </div>
    </div>
  );
};

const MetricCard: React.FC<{ icon: React.ReactNode, label: string, value: string, color: string, trend: string }> = ({ icon, label, value, color, trend }) => {
  const colorMap: any = {
    blue: "border-blue-500/30 bg-blue-500/5 hover:bg-blue-500/10 text-blue-400",
    green: "border-green-500/30 bg-green-500/5 hover:bg-green-500/10 text-green-400",
    red: "border-red-500/30 bg-red-500/5 hover:bg-red-500/10 text-red-400",
  };

  return (
    <div className={`p-6 border rounded-3xl transition-all ${colorMap[color]}`}>
      <div className="flex items-center gap-3 mb-2">
        <div className="p-2 bg-slate-900 rounded-xl">
          {icon}
        </div>
        <span className="text-sm font-bold uppercase tracking-wider opacity-60 text-slate-300">{label}</span>
      </div>
      <div className="text-3xl font-black text-white mb-2">{value}</div>
      <div className="flex items-center gap-1 text-xs font-bold">
        <TrendingUp size={14} />
        {trend}
      </div>
    </div>
  );
};
