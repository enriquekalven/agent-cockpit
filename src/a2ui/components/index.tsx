import React, { useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Cell, PieChart, Pie, RadarChart, PolarGrid, PolarAngleAxis, Radar
} from 'recharts';
import { Activity, Shield, TrendingUp, DollarSign, Cpu, AlertTriangle } from 'lucide-react';

export const Text: React.FC<{ text: string; variant?: 'h1' | 'h2' | 'body' | 'caption' | 'error' | 'warning' }> = ({ text, variant = 'body' }) => {
  const styles = {
    h1: "text-4xl font-extrabold tracking-tight text-white mb-4 bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent",
    h2: "text-2xl font-bold text-slate-100 mb-3",
    body: "text-slate-400 leading-relaxed mb-4",
    caption: "text-xs font-medium text-slate-500 uppercase tracking-widest",
    error: "text-red-400 font-semibold",
    warning: "text-amber-400 font-semibold"
  };

  const Tag = variant === 'h1' ? 'h1' : variant === 'h2' ? 'h2' : 'p';
  return <Tag className={styles[variant]}>{text}</Tag>;
};

export const Button: React.FC<{ label: string; onClick?: () => void; variant?: 'primary' | 'secondary' }> = ({ label, onClick, variant = 'primary' }) => {
  const base = "px-6 py-2.5 rounded-full font-bold transition-all active:scale-95 flex items-center gap-2";
  const styles = {
    primary: "bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_20px_rgba(37,99,235,0.4)]",
    secondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700"
  };
  return (
    <button className={`${base} ${styles[variant]}`} onClick={onClick}>
      {label}
    </button>
  );
};

export const Card: React.FC<{ children: React.ReactNode; title?: string; glass?: boolean; icon?: string }> = ({ children, title, glass = true, icon }) => {
  const Icon = icon === 'security' ? Shield : icon === 'performance' ? Cpu : icon === 'cost' ? DollarSign : icon === 'risk' ? AlertTriangle : null;

  return (
    <div className={`p-6 rounded-3xl border transition-all duration-500 ${glass ? 'bg-slate-900/40 backdrop-blur-xl border-slate-800/50 hover:border-blue-500/30' : 'bg-slate-900 border-slate-800'}`}>
      <div className="flex justify-between items-start mb-4">
        {title && <div className="text-xs font-black text-slate-500 uppercase tracking-widest">{title}</div>}
        {Icon && <Icon className="w-4 h-4 text-slate-600" />}
      </div>
      <div className="a2-card-content">{children}</div>
    </div>
  );
};

export const Image: React.FC<{ src: string; alt?: string; caption?: string }> = ({ src, alt, caption }) => {
  return (
    <div className="relative group overflow-hidden rounded-2xl border border-slate-800">
      <img src={src} alt={alt} className="w-full h-auto" />
      {caption && (
        <div className="absolute bottom-0 inset-x-0 p-4 bg-gradient-to-t from-black/80 to-transparent">
          <p className="text-xs text-white/80">{caption}</p>
        </div>
      )}
    </div>
  );
};

export const List: React.FC<{ items: string[]; title?: string }> = ({ items, title }) => {
  return (
    <div className="space-y-3">
      {title && <h4 className="text-sm font-bold text-slate-300">{title}</h4>}
      <ul className="space-y-2">
        {items.map((item, i) => (
          <li key={i} className="flex items-center gap-3 text-sm text-slate-400">
            <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

export const StatBar: React.FC<{ label: string; value: number; color?: string }> = ({ label, value, color = '#3b82f6' }) => {
  return (
    <div className="mb-4">
      <div className="flex justify-between items-end mb-2">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">{label}</span>
        <span className="text-sm font-mono font-bold" style={{ color }}>{value}%</span>
      </div>
      <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="h-full rounded-full"
          style={{ backgroundColor: color }}
        />
      </div>
    </div>
  );
};

export const Metric: React.FC<{ label: string; value: string; trend?: string; trendUp?: boolean }> = ({ label, value, trend, trendUp = true }) => {
  return (
    <div className="p-1">
      <p className="text-xs font-black text-slate-500 uppercase tracking-widest mb-1">{label}</p>
      <div className="text-3xl font-black text-white tracking-tight">{value}</div>
      {trend && (
        <div className={`text-[10px] font-bold mt-1 flex items-center gap-1 ${trendUp ? 'text-emerald-400' : 'text-red-400'}`}>
          {trendUp ? '↑' : '↓'} {trend}
        </div>
      )}
    </div>
  );
};

export const Grid: React.FC<{ children: React.ReactNode; cols?: number }> = ({ children, cols = 2 }) => {
  const colClass = cols === 1 ? 'grid-cols-1' : cols === 2 ? 'grid-cols-1 md:grid-cols-2' : cols === 3 ? 'grid-cols-1 md:grid-cols-3' : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4';
  return <div className={`grid ${colClass} gap-6`}>{children}</div>;
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900 border border-slate-800 p-3 rounded-xl shadow-2xl">
        <p className="text-xs font-bold text-slate-400 mb-1">{label}</p>
        <p className="text-sm font-black text-white px-2 py-1 rounded bg-blue-500/20 text-blue-400 inline-block">
          {payload[0].value.toFixed(1)}
        </p>
      </div>
    );
  }
  return null;
};

export const Visual: React.FC<{ type: 'trend' | 'bar' | 'radar' | 'roi'; data: any }> = ({ type, data }) => {
  if (type === 'trend') {
    return (
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data?.points || []}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (type === 'radar') {
    return (
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data?.metrics || []}>
            <PolarGrid stroke="#334155" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10 }} />
            <Radar
              name="Maturity"
              dataKey="value"
              stroke="#8b5cf6"
              fill="#8b5cf6"
              fillOpacity={0.5}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (type === 'roi') {
    return (
      <div className="py-4 text-center">
        <div className="inline-flex items-center justify-center p-4 rounded-full bg-emerald-500/10 border border-emerald-500/20 mb-3">
          <TrendingUp className="w-8 h-8 text-emerald-400" />
        </div>
        <div className="text-4xl font-black text-white tracking-tight">${data?.saved}</div>
        <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest mt-1">Savings Realized</p>
      </div>
    );
  }

  if (type === 'bar') {
    return (
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data?.items || []}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
            <Tooltip cursor={{ fill: '#1e293b' }} content={<CustomTooltip />} />
            <Bar dataKey="value" radius={[4, 4, 0, 0]}>
              {data?.items?.map((entry: any, index: number) => (
                <Cell key={`cell-${index}`} fill={entry.color || '#3b82f6'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (type === 'map') {
    return <FleetMap agents={data?.agents} />;
  }

  return <div className="h-32 bg-slate-800/30 rounded-xl border border-dashed border-slate-700 flex items-center justify-center text-xs text-slate-500 italic">Chart: {type} ready</div>;
};

export const FleetMap: React.FC<{ agents?: any[] }> = ({ agents = [] }) => {
  const [zoom, setZoom] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<any>(null);

  return (
    <div
      className="relative w-full aspect-[2/1] bg-slate-950 rounded-3xl border border-slate-800/50 overflow-hidden shadow-2xl cursor-crosshair group"
      onClick={() => setZoom(!zoom)}
    >
      {/* Dynamic Background Map with Zoom Logic */}
      <motion.div
        animate={{
          scale: zoom ? 2 : 1,
          x: zoom && selectedAgent ? `${50 - selectedAgent.x}%` : '0%',
          y: zoom && selectedAgent ? `${50 - selectedAgent.y}%` : '0%'
        }}
        transition={{ type: 'spring', stiffness: 100, damping: 20 }}
        className="absolute inset-0 w-full h-full"
      >
        <img
          src="/fleet-map.png"
          alt="Sovereign Fleet Map"
          className="absolute inset-0 w-full h-full object-cover opacity-40 mix-blend-screen"
        />

        {/* Connection Lines (Optional/Decorative) */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
          <defs>
            <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity="0" />
              <stop offset="50%" stopColor="#3b82f6" stopOpacity="1" />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity="0" />
            </linearGradient>
          </defs>
        </svg>

        {/* Agents */}
        {agents.map((agent, i) => (
          <motion.div
            key={i}
            initial={{ scale: 0, opacity: 0 }}
            animate={{
              scale: 1,
              opacity: 1,
              x: `${agent.x}%`,
              y: `${agent.y}%`
            }}
            transition={{ delay: i * 0.05 }}
            className="absolute z-10"
            style={{ left: 0, top: 0 }}
          >
            <div
              className="relative group/node"
              onMouseEnter={(e) => {
                if (zoom) e.stopPropagation();
                setSelectedAgent(agent);
              }}
            >
              <div className="absolute -inset-4 bg-blue-500/10 rounded-full animate-ping" />
              <div className="absolute -inset-2 bg-blue-400/20 rounded-full blur-sm" />
              <div className={`w-3 h-3 rounded-full border-2 border-white/20 transition-all ${selectedAgent === agent ? 'bg-blue-400 scale-150 shadow-[0_0_20px_rgba(96,165,250,1)]' : 'bg-blue-600 shadow-[0_0_10px_rgba(37,99,235,0.8)]'}`} />

              {/* Node Label (Visible on Zoom) */}
              {zoom && (
                <div className="absolute top-4 left-1/2 -translate-x-1/2 text-[8px] font-black text-blue-400/80 uppercase tracking-tighter whitespace-nowrap">
                  {agent.name}
                </div>
              )}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Interface Overlays (Static) */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_rgba(15,23,42,0.4)_100%)] pointer-events-none" />

      {/* Zoom Controls Overlay */}
      <div className="absolute top-6 left-6 flex flex-col gap-2 z-20">
        <div className={`px-3 py-1.5 rounded-full border text-[10px] font-black uppercase tracking-widest transition-all ${zoom ? 'bg-blue-600 border-blue-400 text-white' : 'bg-slate-900/80 border-slate-700 text-slate-500'}`}>
          {zoom ? 'Target Lock: Active' : 'Global Overview'}
        </div>
      </div>

      {/* Fleet Stats Card */}
      <div className="absolute bottom-6 left-6 p-4 bg-slate-900/80 backdrop-blur-md border border-white/10 rounded-2xl shadow-2xl z-20">
        <div className="flex items-center gap-4">
          <div className="p-2 rounded-lg bg-blue-500/10 border border-blue-500/20">
            <Activity className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Global Fleet Pulse</div>
            <div className="flex items-center gap-2 mt-0.5">
              <div className="text-2xl font-black text-white tracking-tighter">{agents.length}</div>
              <div className="text-[10px] font-bold text-emerald-400 bg-emerald-400/10 px-1.5 py-0.5 rounded leading-none">LIVE</div>
            </div>
          </div>
        </div>
      </div>

      {/* Zoom Instruction */}
      <div className="absolute bottom-6 right-6 text-right z-20 opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Interactivity</div>
        <div className="text-xs font-bold text-blue-400 mt-1">Click to {zoom ? 'Reset View' : 'Zoom Target'}</div>
      </div>

      {/* Selected Agent Details Overlay */}
      {selectedAgent && (
        <div className="absolute top-6 right-6 p-4 bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-2xl shadow-2xl z-20 min-w-[200px] animate-in fade-in slide-in-from-right-4">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xl">🤖</div>
            <div>
              <div className="text-[9px] font-black text-blue-400 uppercase tracking-widest">Sovereign Node</div>
              <div className="text-sm font-bold text-white">{selectedAgent.name}</div>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-[10px]">
              <span className="text-slate-500 font-bold uppercase">Status</span>
              <span className="text-emerald-400 font-mono">{selectedAgent.task || 'IDLE'}</span>
            </div>
            <div className="flex justify-between text-[10px]">
              <span className="text-slate-500 font-bold uppercase">Uptime</span>
              <span className="text-slate-300 font-mono">99.98%</span>
            </div>
            <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden mt-2">
              <div className="h-full bg-blue-500 w-[85%] rounded-full" />
            </div>
          </div>
        </div>
      )}

      {/* Grid Scan Lines Overlay */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.05] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_4px,3px_100%]" />
    </div>
  );
};
