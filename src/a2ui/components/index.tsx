import React from 'react';
import { motion } from 'framer-motion';

export const Text: React.FC<{ text: string; variant?: 'h1' | 'h2' | 'body' | 'caption' | 'error' | 'warning' }> = ({ text, variant = 'body' }) => {
  const styles = {
    h1: "text-4xl font-extrabold tracking-tight text-white mb-4 bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent",
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

export const Card: React.FC<{ children: React.ReactNode; title?: string; glass?: boolean }> = ({ children, title, glass = true }) => {
  return (
    <div className={`p-6 rounded-3xl border transition-all duration-500 ${glass ? 'bg-slate-900/40 backdrop-blur-xl border-slate-800/50 hover:border-blue-500/30' : 'bg-slate-900 border-slate-800'}`}>
      {title && <div className="text-xs font-black text-slate-500 uppercase tracking-widest mb-4">{title}</div>}
      <div className="a2-card-content">{children}</div>
    </div>
  );
};

export const Image: React.FC<{ src: string; alt?: string; caption?: string }> = ({ src, alt, caption }) => {
  return (
    <div className="relative group overflow-hidden rounded-2xl border border-slate-800">
      <img src={src} alt={alt} className="w-full h-auto transition-transform duration-700 group-hover:scale-105" />
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

// Rich Dashboard Components
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

export const Visual: React.FC<{ type: 'radar' | 'map' | 'roi'; data: any }> = ({ type, data }) => {
  // Simplified high-fidelity visualization placeholders
  if (type === 'map') {
    return (
      <div className="h-64 w-full bg-slate-950/50 rounded-2xl border border-slate-800 relative overflow-hidden flex items-center justify-center">
        <div className="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/world-map.png')] bg-center bg-no-repeat bg-contain" />
        <div className="relative z-10 flex gap-4">
          {data?.points?.map((p: any, i: number) => (
            <motion.div
              key={i}
              animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
              transition={{ repeat: Infinity, duration: 2, delay: i * 0.5 }}
              className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,1)]"
            />
           ))}
        </div>
        <div className="absolute bottom-2 right-4 text-[8px] font-mono text-slate-500 uppercase">Sovereign Global Mesh Active</div>
      </div>
    );
  }

  if (type === 'roi') {
    return (
      <div className="py-4">
        <div className="text-center">
          <span className="text-5xl font-black text-white">${data?.saved}</span>
          <p className="text-blue-400 text-xs font-bold mt-2 uppercase tracking-tighter">Savings Realized via Cache</p>
        </div>
      </div>
    );
  }

  return <div className="h-32 bg-slate-800/30 rounded-xl border border-dashed border-slate-700 flex items-center justify-center text-xs text-slate-500 italic">Visual: {type} placeholder</div>;
};
