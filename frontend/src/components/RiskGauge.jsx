import React from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle, Layers, Flame } from 'lucide-react';

export default function RiskGauge({
  score = 0,
  totalChunks = 0,
  highRiskCount = 0,
  mediumRiskCount = 0,
  isScanning = false,
}) {
  // Normalize score between 0 and 100
  const normalizedScore = Math.max(0, Math.min(100, Math.round(score)));

  // SVG parameters
  const size = 180;
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  // Arc calculation (270 degree gauge for speedometer feel or full 360)
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  // Determine severity tier
  let tier = {
    label: 'Low Risk',
    color: '#10b981', // emerald-500
    glowClass: 'shadow-emerald-500/20',
    badgeClass: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    gradientId: 'emeraldGradient',
    gradientColors: ['#34d399', '#10b981'],
    icon: ShieldCheck,
    description: 'Document clauses adhere to standard consumer fairness norms.',
  };

  if (normalizedScore > 65) {
    tier = {
      label: 'Critical Risk',
      color: '#ef4444', // red-500
      glowClass: 'shadow-red-500/30',
      badgeClass: 'bg-red-500/15 text-red-400 border-red-500/30',
      gradientId: 'roseGradient',
      gradientColors: ['#fb7185', '#ef4444'],
      icon: Flame,
      description: 'Severe consumer rights restrictions and high liability waivers detected.',
    };
  } else if (normalizedScore > 30) {
    tier = {
      label: 'Moderate Risk',
      color: '#f59e0b', // amber-500
      glowClass: 'shadow-amber-500/20',
      badgeClass: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
      gradientId: 'amberGradient',
      gradientColors: ['#fcd34d', '#f59e0b'],
      icon: AlertTriangle,
      description: 'Contains unilateral terms or automatic renewals requiring caution.',
    };
  }

  const TierIcon = tier.icon;

  if (isScanning) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-slate-800 flex flex-col items-center justify-center text-center min-h-[280px]">
        <div className="relative w-28 h-28 flex items-center justify-center mb-4">
          <div className="absolute inset-0 rounded-full border-4 border-brand-500/20 border-t-brand-400 animate-spin" />
          <div className="w-16 h-16 rounded-full bg-brand-500/10 flex items-center justify-center animate-pulse">
            <ShieldAlert className="w-8 h-8 text-brand-400" />
          </div>
        </div>
        <h3 className="text-sm font-semibold text-slate-200">Analyzing Agreement Clauses</h3>
        <p className="text-xs text-slate-400 mt-1 max-w-xs">
          Deconstructing contractual language and evaluating against consumer protection statutes...
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800/90 shadow-xl relative overflow-hidden">
      {/* Subtle background ambient glow */}
      <div 
        className="absolute -top-12 left-1/2 -translate-x-1/2 w-48 h-48 rounded-full blur-3xl opacity-15 pointer-events-none transition-all duration-700"
        style={{ backgroundColor: tier.color }}
      />

      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <TierIcon className="w-4 h-4" style={{ color: tier.color }} />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Contract Risk Index
          </h3>
        </div>
        <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${tier.badgeClass}`}>
          {tier.label}
        </span>
      </div>

      {/* Circular SVG Gauge */}
      <div className="relative flex items-center justify-center my-3">
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          className="transform -rotate-90"
        >
          <defs>
            <linearGradient id={tier.gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={tier.gradientColors[0]} />
              <stop offset="100%" stopColor={tier.gradientColors[1]} />
            </linearGradient>
            <filter id="gaugeShadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor={tier.color} floodOpacity="0.4" />
            </filter>
          </defs>

          {/* Background track circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#1e293b"
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeLinecap="round"
          />

          {/* Animated active score circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={`url(#${tier.gradientId})`}
            strokeWidth={strokeWidth}
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            filter="url(#gaugeShadow)"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center numerical readout */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none">
          <span className="text-4xl font-black tracking-tight text-white font-mono">
            {normalizedScore}
          </span>
          <span className="text-[10px] uppercase font-bold tracking-widest text-slate-400 mt-0.5">
            / 100 Score
          </span>
        </div>
      </div>

      {/* Risk Summary Description */}
      <p className="text-xs text-slate-400 text-center px-2 line-clamp-2 min-h-[32px] mb-3">
        {tier.description}
      </p>

      {/* Metrics Row */}
      <div className="grid grid-cols-3 gap-2 pt-3 border-t border-slate-800/80 text-center">
        <div className="bg-slate-900/60 rounded-lg p-2 border border-slate-800/60">
          <div className="flex items-center justify-center gap-1 text-[11px] text-slate-400">
            <Layers className="w-3 h-3 text-slate-400" />
            <span>Clauses</span>
          </div>
          <div className="text-sm font-bold text-slate-200 mt-0.5 font-mono">
            {totalChunks}
          </div>
        </div>

        <div className="bg-slate-900/60 rounded-lg p-2 border border-slate-800/60">
          <div className="flex items-center justify-center gap-1 text-[11px] text-red-400">
            <span className="w-1.5 h-1.5 rounded-full bg-red-400" />
            <span>Critical</span>
          </div>
          <div className="text-sm font-bold text-red-400 mt-0.5 font-mono">
            {highRiskCount}
          </div>
        </div>

        <div className="bg-slate-900/60 rounded-lg p-2 border border-slate-800/60">
          <div className="flex items-center justify-center gap-1 text-[11px] text-amber-400">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
            <span>Moderate</span>
          </div>
          <div className="text-sm font-bold text-amber-400 mt-0.5 font-mono">
            {mediumRiskCount}
          </div>
        </div>
      </div>
    </div>
  );
}
