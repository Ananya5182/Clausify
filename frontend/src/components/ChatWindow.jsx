import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  HelpCircle, 
  Bookmark, 
  AlertCircle, 
  CheckCircle, 
  Loader2, 
  Paperclip, 
  ExternalLink,
  BookOpen,
  Info,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';

const ALL_RECOMMENDED_QUESTIONS = [
  // General / Consumer Focus
  {
    id: 'q1',
    question: "Does this agreement contain a mandatory binding arbitration clause or class action waiver?",
    category: "arbitration",
    categoryLabel: "Arbitration",
    role: "all",
    badgeColor: "text-amber-400 bg-amber-500/10 border-amber-500/20",
  },
  {
    id: 'q2',
    question: "Can this company unilaterally modify contract terms and pricing without notice?",
    category: "clauses",
    categoryLabel: "Unilateral Terms",
    role: "all",
    badgeColor: "text-red-400 bg-red-500/10 border-red-500/20",
  },
  {
    id: 'q3',
    question: "What is the refund policy and are there hidden automatic renewal locks?",
    category: "billing",
    categoryLabel: "Billing & Refund",
    role: "consumer",
    badgeColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  },
  {
    id: 'q4',
    question: "Is my personal data, browsing behavior, or location sold to third parties or advertisers?",
    category: "privacy",
    categoryLabel: "Data Privacy",
    role: "all",
    badgeColor: "text-blue-400 bg-blue-500/10 border-blue-500/20",
  },
  {
    id: 'q5',
    question: "Can the provider terminate my account or access without cause or refund?",
    category: "clauses",
    categoryLabel: "Termination",
    role: "consumer",
    badgeColor: "text-orange-400 bg-orange-500/10 border-orange-500/20",
  },
  {
    id: 'q6',
    question: "I was charged ₹1,499 on 12 Oct without consent by StreamPlay. Help draft a notice.",
    category: "notices",
    categoryLabel: "Dispute Notice",
    role: "consumer",
    badgeColor: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20",
  },
  {
    id: 'q7',
    question: "What legal remedies do I have under the Consumer Protection Act for deficiency of service?",
    category: "arbitration",
    categoryLabel: "Consumer Rights",
    role: "consumer",
    badgeColor: "text-teal-400 bg-teal-500/10 border-teal-500/20",
  },
  {
    id: 'q8',
    question: "On 15 Jan, FlyAirways cancelled flight FL-892 refusing ₹14,500 refund. Draft a legal notice.",
    category: "notices",
    categoryLabel: "Dispute Notice",
    role: "consumer",
    badgeColor: "text-purple-400 bg-purple-500/10 border-purple-500/20",
  },
  // Counsel Specific Focus
  {
    id: 'c1',
    question: "Evaluate the enforceability of the arbitration clause under Section 2(47) of Consumer Protection Act 2019.",
    category: "arbitration",
    categoryLabel: "Arbitration Law",
    role: "counsel",
    badgeColor: "text-indigo-400 bg-indigo-500/10 border-indigo-500/20",
  },
  {
    id: 'c2',
    question: "Audit this agreement for unilateral modification provisions and unconscionable standard terms.",
    category: "clauses",
    categoryLabel: "Clause Audit",
    role: "counsel",
    badgeColor: "text-red-400 bg-red-500/10 border-red-500/20",
  },
  {
    id: 'c3',
    question: "Does the limitation of liability provision violate statutory liability limits under contract law?",
    category: "clauses",
    categoryLabel: "Liability Cap",
    role: "counsel",
    badgeColor: "text-amber-400 bg-amber-500/10 border-amber-500/20",
  },
  {
    id: 'c4',
    question: "Assess personal data processing and transfer clauses against Digital Personal Data Protection standards.",
    category: "privacy",
    categoryLabel: "DPDP Compliance",
    role: "counsel",
    badgeColor: "text-blue-400 bg-blue-500/10 border-blue-500/20",
  },
  {
    id: 'c5',
    question: "Draft a formal statutory legal notice claiming ₹45,000 for service deficiency and unfair trade practice.",
    category: "notices",
    categoryLabel: "Formal Notice",
    role: "counsel",
    badgeColor: "text-purple-400 bg-purple-500/10 border-purple-500/20",
  },
  {
    id: 'c6',
    question: "Examine governing law, dispute resolution venue, and jurisdiction clauses for unilateral bias.",
    category: "arbitration",
    categoryLabel: "Jurisdiction",
    role: "counsel",
    badgeColor: "text-teal-400 bg-teal-500/10 border-teal-500/20",
  },
  {
    id: 'c7',
    question: "Identify automatic recurring billing terms conflicting with consumer e-mandate guidelines.",
    category: "billing",
    categoryLabel: "E-Mandates",
    role: "counsel",
    badgeColor: "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
  },
  {
    id: 'c8',
    question: "Check for one-sided indemnity obligations placing disproportional liability on the consumer.",
    category: "clauses",
    categoryLabel: "Indemnification",
    role: "counsel",
    badgeColor: "text-rose-400 bg-rose-500/10 border-rose-500/20",
  },
];

const QUESTION_CATEGORIES = [
  { id: 'all', label: 'All' },
  { id: 'clauses', label: 'Unfair Terms' },
  { id: 'arbitration', label: 'Arbitration' },
  { id: 'billing', label: 'Billing & Refund' },
  { id: 'privacy', label: 'Data & Privacy' },
  { id: 'notices', label: 'Dispute Notices' },
];

export default function ChatWindow({
  messages = [],
  isLoading = false,
  onSendMessage,
  activeDoc = null,
  currentMode = 'scanner',
  onUploadClick = null,
  faqs = [],
  currentUser = null,
}) {
  const [inputText, setInputText] = useState('');
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom of chat when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const isCounsel = currentUser?.role === 'counsel';

  // Filter questions by active role
  const roleFilteredQuestions = ALL_RECOMMENDED_QUESTIONS.filter(q => {
    if (isCounsel) {
      return q.role === 'counsel' || q.role === 'all';
    }
    return q.role === 'consumer' || q.role === 'all';
  });

  // Filter by category tab
  const displayedQuestions = activeCategory === 'all'
    ? roleFilteredQuestions
    : roleFilteredQuestions.filter(q => q.category === activeCategory);

  const handleSubmit = (e) => {
    e?.preventDefault();
    const trimmed = inputText.trim();
    if (!trimmed || isLoading) return;

    onSendMessage(trimmed);
    setInputText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSuggestionClick = (prompt) => {
    onSendMessage(prompt);
  };

  return (
    <div className="flex flex-col h-full glass-card rounded-2xl border border-slate-800 shadow-2xl overflow-hidden relative">
      
      {/* Chat Window Header Bar */}
      <div className="px-5 py-3.5 border-b border-slate-800 bg-slate-950/60 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="relative w-8 h-8 rounded-lg bg-gradient-to-tr from-brand-600 to-teal-400 p-[1px] flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-lg flex items-center justify-center">
              <Bot className="w-4 h-4 text-brand-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-slate-200">
                {isCounsel ? 'Clausify Legal Counsel Suite' : 'Clausify Consumer Assistant'}
              </h2>
              <span className={`flex items-center gap-1 text-[10px] font-medium px-1.5 py-0.5 rounded border ${
                isCounsel 
                  ? 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20' 
                  : 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
              }`}>
                <span className={`w-1.5 h-1.5 rounded-full ${isCounsel ? 'bg-indigo-400' : 'bg-emerald-400'} animate-pulse`} />
                {isCounsel ? 'Counsel Grounding' : 'Consumer Shield'}
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              {activeDoc 
                ? `Analyzing: ${activeDoc.file_name}`
                : isCounsel
                  ? 'Statutory section citations & clause enforceability auditing active'
                  : currentMode === 'scanner'
                    ? 'Upload an agreement or pick a recommended question below'
                    : 'Describe your consumer dispute to extract entities and generate legal notice'}
            </p>
          </div>
        </div>

        {/* If in scanner mode and no active doc, show quick upload trigger button */}
        {currentMode === 'scanner' && !activeDoc && onUploadClick && (
          <button
            type="button"
            onClick={onUploadClick}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand-500/10 hover:bg-brand-500/20 text-brand-400 border border-brand-500/30 text-xs font-medium transition-colors"
          >
            <Paperclip className="w-3.5 h-3.5" />
            <span>Upload PDF</span>
          </button>
        )}
      </div>

      {/* Message Stream Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
        {messages.length === 0 ? (
          /* Empty State Welcoming Screen */
          <div className="h-full flex flex-col items-center justify-start text-center p-2 sm:p-4 space-y-4 max-w-xl mx-auto select-none overflow-y-auto">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-brand-600/20 to-indigo-600/20 border border-brand-500/30 flex items-center justify-center shadow-lg shadow-brand-500/10 flex-shrink-0 mt-2">
              <Sparkles className="w-7 h-7 text-brand-400" />
            </div>

            <div>
              <h3 className="text-base font-bold text-slate-200">
                {isCounsel ? 'Welcome, Adv. Priya Sharma' : 'Welcome to Clausify AI'}
              </h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed max-w-md mx-auto">
                {isCounsel 
                  ? 'Audit contract enforceability, examine arbitration waivers, and compile statutory consumer dispute notices with full legal grounding.'
                  : 'Review consumer agreements with zero hallucinations, discover hidden predatory clauses, or generate a legal notice in minutes.'}
              </p>
            </div>

            {/* Category Filter Pills */}
            <div className="w-full flex items-center justify-center gap-1.5 flex-wrap pt-1">
              {QUESTION_CATEGORIES.map(cat => (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setActiveCategory(cat.id)}
                  className={`px-2.5 py-1 rounded-full text-[11px] font-semibold transition-all ${
                    activeCategory === cat.id
                      ? 'bg-brand-600 text-white shadow-sm shadow-brand-500/30'
                      : 'bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>

            {/* Quick Suggestion Prompts Grid */}
            <div className="w-full space-y-2 pt-1 text-left">
              <div className="flex items-center justify-between text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-1">
                <span className="flex items-center gap-1.5">
                  <HelpCircle className="w-3.5 h-3.5 text-brand-400" />
                  <span>Recommended Questions ({displayedQuestions.length}):</span>
                </span>
                <span className="text-[10px] text-slate-500 normal-case">Click any question to ask</span>
              </div>

              <div className="grid grid-cols-1 gap-2">
                {displayedQuestions.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => handleSuggestionClick(item.question)}
                    className="p-2.5 rounded-xl bg-slate-900/90 hover:bg-slate-850 border border-slate-800 hover:border-brand-500/50 text-slate-300 hover:text-white text-xs text-left transition-all flex items-center justify-between group shadow-sm"
                  >
                    <div className="flex items-center gap-2 pr-2">
                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded border uppercase flex-shrink-0 ${item.badgeColor}`}>
                        {item.categoryLabel}
                      </span>
                      <span className="line-clamp-1">{item.question}</span>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-brand-400 group-hover:translate-x-0.5 transition-all flex-shrink-0" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* Render Messages */
          messages.map((msg, index) => {
            const isUser = msg.role === 'user';

            return (
              <div
                key={index}
                className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}
              >
                {/* Assistant Avatar */}
                {!isUser && (
                  <div className="w-8 h-8 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <Bot className="w-4 h-4 text-brand-400" />
                  </div>
                )}

                <div className={`max-w-[85%] sm:max-w-[78%] space-y-2`}>
                  {/* Message Bubble */}
                  <div
                    className={`rounded-2xl p-4 text-xs leading-relaxed ${
                      isUser
                        ? 'bg-gradient-to-r from-brand-700 to-emerald-600 text-white shadow-md shadow-brand-900/40 rounded-tr-none'
                        : 'bg-slate-900/90 text-slate-200 border border-slate-800/90 shadow-md rounded-tl-none'
                    }`}
                  >
                    {isUser ? (
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    ) : (
                      <div className="prose prose-invert max-w-none text-xs space-y-2">
                        <ReactMarkdown
                          components={{
                            p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
                            strong: ({ children }) => <strong className="font-semibold text-emerald-300">{children}</strong>,
                            ul: ({ children }) => <ul className="list-disc pl-4 space-y-1 my-2">{children}</ul>,
                            ol: ({ children }) => <ol className="list-decimal pl-4 space-y-1 my-2">{children}</ol>,
                            li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                            code: ({ children }) => (
                              <code className="px-1.5 py-0.5 rounded bg-slate-950 font-mono text-[11px] text-amber-300 border border-slate-800">
                                {children}
                              </code>
                            ),
                            blockquote: ({ children }) => (
                              <blockquote className="border-l-2 border-brand-500 pl-3 italic text-slate-300 my-2">
                                {children}
                              </blockquote>
                            ),
                          }}
                        >
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    )}
                  </div>

                  {/* Context Citations Badges (Grounding snippets) */}
                  {!isUser && msg.context_snippets && msg.context_snippets.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1.5 pt-1 pl-1">
                      <span className="text-[10px] uppercase font-bold tracking-wider text-slate-500 flex items-center gap-1">
                        <Bookmark className="w-3 h-3 text-brand-400" />
                        Grounding Citations:
                      </span>
                      {msg.context_snippets.map((snippet, sIdx) => (
                        <button
                          key={sIdx}
                          type="button"
                          onClick={() => setSelectedCitation(snippet)}
                          className="px-2 py-0.5 rounded-full bg-slate-900 hover:bg-slate-800 border border-slate-700/80 hover:border-brand-500/60 text-[10px] text-slate-300 hover:text-brand-300 font-mono transition-colors flex items-center gap-1"
                        >
                          <span>Clause #{sIdx + 1}</span>
                          {snippet.risk_level && (
                            <span className={`w-1.5 h-1.5 rounded-full ${
                              snippet.risk_level === 'HIGH' ? 'bg-red-400' :
                              snippet.risk_level === 'MEDIUM' ? 'bg-amber-400' : 'bg-emerald-400'
                            }`} />
                          )}
                        </button>
                      ))}
                    </div>
                  )}

                  {/* FAQ Matched Badge */}
                  {!isUser && msg.source === 'faq' && (
                    <div className="flex items-center gap-1.5 text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-lg border border-emerald-500/20 max-w-fit">
                      <ShieldCheck className="w-3 h-3" />
                      <span>Verified Knowledge Base Answer ({Math.round((msg.faq_match?.similarity || 0.9) * 100)}% Match)</span>
                    </div>
                  )}
                </div>

                {/* User Avatar */}
                {isUser && (
                  <div className="w-8 h-8 rounded-xl bg-brand-600/30 border border-brand-500/40 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <User className="w-4 h-4 text-brand-300" />
                  </div>
                )}
              </div>
            );
          })
        )}

        {/* Loading Indicator Bubble */}
        {isLoading && (
          <div className="flex gap-3 justify-start items-center">
            <div className="w-8 h-8 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-brand-400 animate-pulse" />
            </div>
            <div className="bg-slate-900/90 rounded-2xl rounded-tl-none px-4 py-3 border border-slate-800 flex items-center gap-2 text-xs text-slate-400 shadow-md">
              <Loader2 className="w-4 h-4 animate-spin text-brand-400" />
              <span>Analyzing contract clauses with Groq Llama 3.3...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Floating Citation Modal / Popover */}
      {selectedCitation && (
        <div className="absolute inset-x-4 bottom-24 z-30 p-4 rounded-xl glass-panel bg-slate-900/95 border border-brand-500/40 shadow-2xl backdrop-blur-md animate-in fade-in slide-in-from-bottom-2">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-brand-400" />
              <h4 className="text-xs font-bold text-slate-200">
                Grounding Document Clause Excerpt
              </h4>
              {selectedCitation.risk_level && (
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  Risk: {selectedCitation.risk_level}
                </span>
              )}
            </div>
            <button
              type="button"
              onClick={() => setSelectedCitation(null)}
              className="text-xs text-slate-400 hover:text-white px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700"
            >
              Close
            </button>
          </div>
          <p className="mt-2 text-xs font-mono text-slate-300 leading-relaxed max-h-36 overflow-y-auto whitespace-pre-wrap bg-slate-950/70 p-2.5 rounded-lg border border-slate-800">
            "{selectedCitation.chunk_text}"
          </p>
        </div>
      )}

      {/* Quick Suggestion Chips Bar above input (when there are messages) */}
      {messages.length > 0 && (
        <div className="px-4 py-1.5 border-t border-slate-800/80 bg-slate-950/40 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider flex-shrink-0">
            Suggested Prompts:
          </span>
          {roleFilteredQuestions.slice(0, 5).map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => handleSuggestionClick(item.question)}
              className="px-2.5 py-1 rounded-full bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-brand-500/40 text-slate-400 hover:text-slate-200 text-[11px] whitespace-nowrap transition-colors flex-shrink-0 flex items-center gap-1.5"
            >
              <span className={`text-[8px] font-bold px-1 py-0.2 rounded uppercase ${item.badgeColor}`}>
                {item.categoryLabel}
              </span>
              <span className="max-w-[180px] sm:max-w-[240px] truncate">{item.question}</span>
            </button>
          ))}
        </div>
      )}

      {/* Input Form Bar */}
      <form
        onSubmit={handleSubmit}
        className="p-3 sm:p-4 border-t border-slate-800 bg-slate-950/80 flex items-end gap-2"
      >
        <div className="relative flex-1">
          <textarea
            ref={inputRef}
            rows={1}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              currentMode === 'scanner'
                ? activeDoc
                  ? `Ask questions about ${activeDoc.file_name} clauses...`
                  : 'Ask about contract terms or upload a document...'
                : 'State your complaint (e.g., Company, Date, Order ID, Amount, Issue)...'
            }
            className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-800 text-slate-100 placeholder-slate-500 text-xs focus:outline-none focus:ring-1 focus:ring-brand-500/80 focus:border-brand-500/80 resize-none max-h-32 transition-all"
          />
        </div>

        <button
          type="submit"
          id="send-message-btn"
          disabled={!inputText.trim() || isLoading}
          className={`p-2.5 rounded-xl text-white transition-all flex items-center justify-center flex-shrink-0 ${
            inputText.trim() && !isLoading
              ? 'bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 shadow-md shadow-brand-500/20 active:scale-95 cursor-pointer'
              : 'bg-slate-800/80 text-slate-500 cursor-not-allowed border border-slate-800'
          }`}
          title="Send message (Enter)"
        >
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin text-slate-400" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </form>

    </div>
  );
}
