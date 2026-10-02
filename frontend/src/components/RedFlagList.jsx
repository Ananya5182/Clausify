import React, { useState } from 'react';
import { 
  ChevronDown, 
  ChevronUp, 
  AlertCircle, 
  AlertTriangle, 
  CheckCircle, 
  HelpCircle, 
  MessageSquareShare, 
  Copy, 
  Check, 
  Tag, 
  FileText 
} from 'lucide-react';

export default function RedFlagList({ clauses = [], onAskClause }) {
  const [expandedIndices, setExpandedIndices] = useState([0]); // First clause opened by default
  const [filter, setFilter] = useState('ALL');
  const [copiedIndex, setCopiedIndex] = useState(null);

  const toggleAccordion = (index) => {
    setExpandedIndices(prev => 
      prev.includes(index) ? prev.filter(i => i !== index) : [...prev, index]
    );
  };

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  // Filter clauses
  const filteredClauses = clauses.filter(c => {
    const level = (c.risk_level || 'SAFE').toUpperCase();
    if (filter === 'CRITICAL') return level === 'HIGH' || level === 'CRITICAL';
    if (filter === 'MODERATE') return level === 'MEDIUM' || level === 'MODERATE';
    if (filter === 'SAFE') return level === 'LOW' || level === 'SAFE' || level === 'NONE';
    return true;
  });

  const getSeverityConfig = (riskLevel) => {
    const level = (riskLevel || '').toUpperCase();
    if (level === 'HIGH' || level === 'CRITICAL') {
      return {
        label: 'Critical',
        badgeClass: 'bg-red-500/15 text-red-400 border-red-500/30',
        borderClass: 'border-red-500/30 hover:border-red-500/50',
        cardBg: 'bg-red-950/10',
        icon: AlertCircle,
        iconColor: 'text-red-400',
      };
    }
    if (level === 'MEDIUM' || level === 'MODERATE') {
      return {
        label: 'Moderate',
        badgeClass: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
        borderClass: 'border-amber-500/30 hover:border-amber-500/50',
        cardBg: 'bg-amber-950/10',
        icon: AlertTriangle,
        iconColor: 'text-amber-400',
      };
    }
    return {
      label: 'Safe',
      badgeClass: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
      borderClass: 'border-emerald-500/20 hover:border-emerald-500/40',
      cardBg: 'bg-emerald-950/10',
      icon: CheckCircle,
      iconColor: 'text-emerald-400',
    };
  };

  if (!clauses || clauses.length === 0) {
    return (
      <div className="glass-card rounded-2xl p-6 border border-slate-800 text-center">
        <FileText className="w-10 h-10 text-slate-500 mx-auto mb-2" />
        <h4 className="text-sm font-semibold text-slate-300">No Clauses Scanned Yet</h4>
        <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
          Upload an agreement PDF above to run automated legal risk deconstruction and red-flag classification.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl space-y-4">
      {/* Header and Filter Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-bold text-slate-200">
              Detected Contract Clauses
            </h3>
            <span className="text-xs font-mono font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
              {clauses.length}
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Categorized by consumer protection risk severity
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1 bg-slate-900/90 p-1 rounded-lg border border-slate-800 text-xs">
          {['ALL', 'CRITICAL', 'MODERATE', 'SAFE'].map((f) => (
            <button
              key={f}
              type="button"
              onClick={() => setFilter(f)}
              className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-all ${
                filter === f
                  ? 'bg-slate-700 text-white shadow-sm font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {f.charAt(0) + f.slice(1).toLowerCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Accordion List */}
      <div className="space-y-2.5 max-h-[560px] overflow-y-auto pr-1">
        {filteredClauses.map((clause, idx) => {
          const originalIndex = clause.chunk_index !== undefined ? clause.chunk_index : idx;
          const isExpanded = expandedIndices.includes(originalIndex);
          const config = getSeverityConfig(clause.risk_level);
          const Icon = config.icon;

          return (
            <div
              key={originalIndex}
              className={`rounded-xl border transition-all duration-200 ${config.borderClass} ${config.cardBg}`}
            >
              {/* Accordion Header */}
              <button
                type="button"
                onClick={() => toggleAccordion(originalIndex)}
                className="w-full text-left p-3.5 flex items-start justify-between gap-3 focus:outline-none"
              >
                <div className="flex items-start gap-2.5 min-w-0">
                  <Icon className={`w-4 h-4 mt-0.5 flex-shrink-0 ${config.iconColor}`} />
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full border ${config.badgeClass}`}>
                        {config.label}
                      </span>
                      {clause.risk_score !== undefined && (
                        <span className="text-[11px] font-mono text-slate-400">
                          Score: <span className="font-semibold text-slate-200">{clause.risk_score}</span>/100
                        </span>
                      )}
                      <span className="text-[11px] font-mono text-slate-500">
                        Clause #{originalIndex + 1}
                      </span>
                    </div>

                    <p className="text-xs font-semibold text-slate-200 line-clamp-1">
                      {clause.flag_reason || clause.summary || `Clause Excerpt ${originalIndex + 1}`}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 flex-shrink-0 pt-0.5">
                  {isExpanded ? (
                    <ChevronUp className="w-4 h-4 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400" />
                  )}
                </div>
              </button>

              {/* Accordion Body */}
              {isExpanded && (
                <div className="px-4 pb-4 pt-1 border-t border-slate-800/60 space-y-3 text-xs">
                  {/* Category Tags */}
                  {clause.detected_categories && clause.detected_categories.length > 0 && (
                    <div className="flex items-center gap-1.5 flex-wrap pt-1">
                      <Tag className="w-3 h-3 text-slate-400" />
                      {clause.detected_categories.map((cat, catIdx) => (
                        <span
                          key={catIdx}
                          className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono border border-slate-700/60 uppercase"
                        >
                          {cat}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Plain English Flag Explanation */}
                  {clause.flag_reason && (
                    <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800/90 text-slate-300 leading-relaxed">
                      <span className="font-semibold text-amber-400 block mb-0.5 text-[11px] uppercase tracking-wide">
                        Risk Analysis
                      </span>
                      {clause.flag_reason}
                    </div>
                  )}

                  {/* Original Clause Excerpt */}
                  {(clause.clause_preview || clause.summary) && (
                    <div>
                      <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1">
                        <span className="font-medium">Original Contract Excerpt:</span>
                        <button
                          type="button"
                          onClick={() => handleCopy(clause.clause_preview || clause.summary, originalIndex)}
                          className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-slate-200 transition-colors"
                        >
                          {copiedIndex === originalIndex ? (
                            <>
                              <Check className="w-3 h-3 text-emerald-400" />
                              <span className="text-emerald-400">Copied</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Copy Quote</span>
                            </>
                          )}
                        </button>
                      </div>
                      <blockquote className="p-2.5 rounded-lg bg-slate-950/70 border-l-2 border-brand-500 text-slate-300 italic font-mono text-[11px] leading-relaxed">
                        "{clause.clause_preview || clause.summary}"
                      </blockquote>
                    </div>
                  )}

                  {/* Interactive Action: Ask AI */}
                  {onAskClause && (
                    <div className="pt-1 flex justify-end">
                      <button
                        type="button"
                        onClick={() => onAskClause(clause)}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand-500/10 hover:bg-brand-500/20 text-brand-400 border border-brand-500/30 text-xs font-medium transition-colors"
                      >
                        <MessageSquareShare className="w-3.5 h-3.5" />
                        <span>Ask AI about this clause</span>
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
