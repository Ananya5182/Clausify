import React from 'react';

export default function Logo({ 
  size = 'md', 
  showText = true, 
  subtitle = true, 
  className = '' 
}) {
  const sizeMap = {
    sm: { icon: 'w-7 h-7', text: 'text-lg', scale: 28 },
    md: { icon: 'w-9 h-9', text: 'text-xl', scale: 36 },
    lg: { icon: 'w-12 h-12', text: 'text-2xl', scale: 48 },
    xl: { icon: 'w-16 h-16', text: 'text-3xl', scale: 64 },
  };

  const currentSize = sizeMap[size] || sizeMap.md;

  return (
    <div className={`flex items-center gap-3 select-none ${className}`}>
      {/* Glow Container */}
      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-500 rounded-2xl blur-sm opacity-50 group-hover:opacity-80 transition duration-500" />
        
        {/* Shield + Scales Vector Mark */}
        <div className={`relative ${currentSize.icon} rounded-xl bg-slate-950 border border-emerald-500/40 p-1 flex items-center justify-center shadow-lg shadow-emerald-500/20`}>
          <svg
            viewBox="0 0 100 100"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-full h-full"
          >
            <defs>
              <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#34d399" />
                <stop offset="50%" stopColor="#10b981" />
                <stop offset="100%" stopColor="#059669" />
              </linearGradient>
              <linearGradient id="innerGlow" x1="50%" y1="0%" x2="50%" y2="100%">
                <stop offset="0%" stopColor="#6ee7b7" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#047857" stopOpacity="0.2" />
              </linearGradient>
            </defs>

            {/* Outer Shield Path */}
            <path
              d="M50 8L18 22V50C18 70 32 87 50 92C68 87 82 70 82 50V22L50 8Z"
              stroke="url(#shieldGrad)"
              strokeWidth="5"
              strokeLinejoin="round"
              fill="url(#innerGlow)"
            />

            {/* Central Pillar of Justice */}
            <path
              d="M50 24V74"
              stroke="#ecfdf5"
              strokeWidth="4"
              strokeLinecap="round"
            />
            {/* Top Balance Beam */}
            <path
              d="M32 38C38 34 62 34 68 38"
              stroke="#6ee7b7"
              strokeWidth="3.5"
              strokeLinecap="round"
            />
            {/* Left Pan Strings & Pan */}
            <path
              d="M32 38L25 54H39L32 38Z"
              stroke="#34d399"
              strokeWidth="2.5"
              strokeLinejoin="round"
              fill="#064e3b"
              fillOpacity="0.6"
            />
            {/* Right Pan Strings & Pan */}
            <path
              d="M68 38L61 54H75L68 38Z"
              stroke="#34d399"
              strokeWidth="2.5"
              strokeLinejoin="round"
              fill="#064e3b"
              fillOpacity="0.6"
            />

            {/* Lower Contract Clause Horizontal Micro-Lines */}
            <line x1="42" y1="62" x2="47" y2="62" stroke="#34d399" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="40" y1="67" x2="47" y2="67" stroke="#34d399" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="53" y1="62" x2="58" y2="62" stroke="#34d399" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="53" y1="67" x2="60" y2="67" stroke="#34d399" strokeWidth="2.5" strokeLinecap="round" />
          </svg>
        </div>
      </div>

      {/* Typography */}
      {showText && (
        <div>
          <div className="flex items-center gap-2">
            <span className={`${currentSize.text} font-black tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent font-sans`}>
              Clausify
            </span>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/25">
              AI
            </span>
          </div>
          {subtitle && (
            <p className="text-[11px] text-slate-400 leading-tight">
              Legal Contract Scanner & Grievance Shield
            </p>
          )}
        </div>
      )}
    </div>
  );
}
