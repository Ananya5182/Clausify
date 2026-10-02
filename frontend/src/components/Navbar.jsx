import React from 'react';
import Logo from './Logo';
import { 
  ShieldAlert, 
  Scale, 
  FileSearch, 
  RotateCcw, 
  FileText,
  LogOut,
  User as UserIcon
} from 'lucide-react';

export default function Navbar({ 
  currentMode, 
  onModeChange, 
  onRestartChat, 
  activeDoc,
  currentUser,
  onLogout,
  serverStatus = 'healthy'
}) {
  return (
    <header className="sticky top-0 z-40 w-full glass-panel border-b border-slate-800/80 bg-slate-950/85 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand Logo with dynamic emblem */}
        <Logo size="md" showText={true} subtitle={true} />

        {/* Center: Mode Pill Toggle */}
        <div className="flex items-center bg-slate-900/90 p-1 rounded-full border border-slate-800 shadow-inner">
          <button
            type="button"
            id="mode-scanner-btn"
            onClick={() => onModeChange('scanner')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
              currentMode === 'scanner'
                ? 'bg-gradient-to-r from-brand-600 to-emerald-500 text-white shadow-md shadow-brand-500/25 font-semibold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <FileSearch className="w-3.5 h-3.5" />
            <span>Document Scanner</span>
            {activeDoc && (
              <span className="w-2 h-2 rounded-full bg-emerald-300 animate-pulse" title="Document active" />
            )}
          </button>

          <button
            type="button"
            id="mode-grievance-btn"
            onClick={() => onModeChange('grievance')}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
              currentMode === 'grievance'
                ? 'bg-gradient-to-r from-indigo-600 to-blue-500 text-white shadow-md shadow-indigo-500/25 font-semibold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Scale className="w-3.5 h-3.5" />
            <span>Consumer Grievance</span>
          </button>
        </div>

        {/* Right Actions: Active Doc pill + Clear Chat + User Profile & Sign Out */}
        <div className="flex items-center gap-2.5">
          {activeDoc && (
            <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900/80 border border-slate-800 text-slate-300 text-xs max-w-[160px] truncate">
              <FileText className="w-3.5 h-3.5 text-brand-400 flex-shrink-0" />
              <span className="truncate font-mono text-[11px]">{activeDoc.file_name}</span>
            </div>
          )}

          <button
            type="button"
            id="restart-chat-btn"
            onClick={onRestartChat}
            title="Restart conversation & clear context"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 transition-colors shadow-sm"
          >
            <RotateCcw className="w-3.5 h-3.5 text-slate-400 hover:rotate-180 transition-transform" />
            <span className="hidden sm:inline">Clear Chat</span>
          </button>

          {/* User Profile Chip & Logout */}
          {currentUser ? (
            <div className="flex items-center gap-2 pl-1 border-l border-slate-800">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-brand-600 to-emerald-400 p-[1px] flex-shrink-0">
                  <div className="w-full h-full rounded-full bg-slate-950 flex items-center justify-center overflow-hidden">
                    {currentUser.avatar ? (
                      <img src={currentUser.avatar} alt={currentUser.name} className="w-full h-full object-cover" />
                    ) : (
                      <UserIcon className="w-3.5 h-3.5 text-brand-400" />
                    )}
                  </div>
                </div>
                <div className="hidden xl:block text-left">
                  <span className="text-xs font-semibold text-slate-200 block leading-tight">
                    {currentUser.name}
                  </span>
                  <span className={`text-[10px] font-medium inline-flex items-center gap-1 ${
                    currentUser.role === 'counsel' ? 'text-indigo-400' : 'text-emerald-400'
                  }`}>
                    {currentUser.role === 'counsel' ? '⚖️ Legal Counsel' : '🛡️ Consumer'}
                  </span>
                </div>
              </div>

              <button
                type="button"
                onClick={onLogout}
                title="Sign out of Clausify"
                className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-950/20 border border-transparent hover:border-red-900/40 transition-colors cursor-pointer"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : null}
        </div>

      </div>
    </header>
  );
}
