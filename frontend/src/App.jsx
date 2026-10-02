import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import RiskGauge from './components/RiskGauge';
import RedFlagList from './components/RedFlagList';
import GrievanceTracker from './components/GrievanceTracker';
import ChatWindow from './components/ChatWindow';
import DocUploader from './components/DocUploader';
import LoginPage from './components/LoginPage';
import { sendChatMessage, fetchFaqs, checkBackendHealth } from './services/api';
import { 
  FileText, 
  Scale, 
  Sparkles
} from 'lucide-react';

const SAMPLE_GRIEVANCE_PROMPTS = {
  flight: "On 15 January 2025, FlyAirways cancelled flight FL-892 without notice. My booking reference is BK-994120. They are refusing to refund my ticket amount of ₹14,500 despite multiple customer support tickets. Please help me draft a formal legal notice.",
  subscription: "StreamMax charged my credit card ₹1,999 on 3 February 2025 for an automatic annual renewal without sending any advance reminder notice. Reference txn ID is TXN-449182. They refused my cancellation request.",
  ecommerce: "I bought a laptop on 20 December 2024 from TechRetail under order #TR-10293 for ₹48,000. It arrived with a dead screen, and customer service has refused replacement or refund.",
};

export default function App() {
  // Authentication state: starts as null so application ALWAYS lands on the Login Page first
  const [currentUser, setCurrentUser] = useState(null);

  const [currentMode, setCurrentMode] = useState(() => {
    try {
      const params = new URLSearchParams(window.location.search);
      return params.get('mode') === 'grievance' ? 'grievance' : 'scanner';
    } catch {
      return 'scanner';
    }
  }); // 'scanner' | 'grievance'
  const [sessionId, setSessionId] = useState(() => `session_${Date.now()}`);
  const [serverHealth, setServerHealth] = useState('checking');
  
  // Document scan state
  const [activeDoc, setActiveDoc] = useState(null);
  const [docSummary, setDocSummary] = useState(null);
  const [clauses, setClauses] = useState([]);
  const [isScanning, setIsScanning] = useState(false);

  // Chat state
  const [messages, setMessages] = useState([]);
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [faqs, setFaqs] = useState([]);

  // Grievance slot state
  const [slots, setSlots] = useState({
    company_name: null,
    transaction_id: null,
    incident_date: null,
    disputed_amount: null,
    issue_summary: null,
  });
  const [noticeReady, setNoticeReady] = useState(false);

  // Initial setup: check backend health and load FAQs
  useEffect(() => {
    async function init() {
      try {
        const health = await checkBackendHealth();
        setServerHealth(health.status || 'healthy');
      } catch (e) {
        setServerHealth('offline');
      }

      try {
        const loadedFaqs = await fetchFaqs();
        if (Array.isArray(loadedFaqs)) {
          setFaqs(loadedFaqs);
        }
      } catch (e) {
        console.warn('Could not load dynamic FAQs');
      }
    }
    init();
  }, []);

  const handleLoginSuccess = (user) => {
    // If user changed or role changed, clear the chat so it does not continue
    if (!currentUser || currentUser.role !== user.role || currentUser.email !== user.email) {
      setMessages([]);
      setSessionId(`session_${Date.now()}`);
      setSlots({
        company_name: null,
        transaction_id: null,
        incident_date: null,
        disputed_amount: null,
        issue_summary: null,
      });
      setNoticeReady(false);
    }
    setCurrentUser(user);
  };

  const handleSwitchRole = (targetRole) => {
    const newRole = targetRole || (currentUser?.role === 'counsel' ? 'consumer' : 'counsel');
    const newUser = newRole === 'counsel' ? {
      name: 'Adv. Priya Sharma',
      email: 'priya.sharma@legalshield.org',
      role: 'counsel',
      organization: 'High Court Bar Council / LexAdvocates',
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=Priya+Sharma',
    } : {
      name: 'Rahul Verma',
      email: 'rahul.verma@example.com',
      role: 'consumer',
      organization: 'Individual Consumer',
      avatar: 'https://api.dicebear.com/7.x/initials/svg?seed=Rahul+Verma',
    };

    localStorage.setItem('clausify_user', JSON.stringify(newUser));
    setCurrentUser(newUser);

    // CRITICAL: Chat should NOT continue when switching between demo consumer and demo counsel!
    setMessages([]);
    setSessionId(`session_${Date.now()}`);
    setSlots({
      company_name: null,
      transaction_id: null,
      incident_date: null,
      disputed_amount: null,
      issue_summary: null,
    });
    setNoticeReady(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('clausify_user');
    setCurrentUser(null);
    setMessages([]);
    setSessionId(`session_${Date.now()}`);
    setSlots({
      company_name: null,
      transaction_id: null,
      incident_date: null,
      disputed_amount: null,
      issue_summary: null,
    });
    setNoticeReady(false);
  };

  // Handle PDF scan completion
  const handleScanComplete = (scanResult) => {
    if (scanResult && scanResult.document) {
      setActiveDoc(scanResult.document);
      setDocSummary(scanResult.summary);
      setClauses(scanResult.flagged_clauses || scanResult.chunks || []);

      const highCount = scanResult.summary?.high_risk_count || 0;
      const totalCount = scanResult.summary?.total_chunks || 0;
      const score = scanResult.document.overall_risk_score || 0;

      const scanMessage = {
        role: 'assistant',
        content: `### 📄 Agreement Analyzed: **${scanResult.document.file_name}**\n\n` +
          `- **Overall Risk Score:** **${score}/100**\n` +
          `- **Total Clauses Analyzed:** ${totalCount}\n` +
          `- **Critical Red-Flags:** ${highCount}\n\n` +
          `I have indexed all provisions into the vector memory. You can ask me specific questions like:\n` +
          `* *"Does this contract include a class action waiver?"*\n` +
          `* *"Can the company terminate my account without cause?"*\n` +
          `* *"Are there automatic recurring renewals or hidden cancellation penalties?"*`,
        source: 'rag',
      };

      setMessages(prev => [...prev, scanMessage]);
    }
  };

  // Reset document
  const handleResetDoc = () => {
    setActiveDoc(null);
    setDocSummary(null);
    setClauses([]);
  };

  // Clear / restart conversation
  const handleRestartChat = () => {
    setMessages([]);
    setSessionId(`session_${Date.now()}`);
    setSlots({
      company_name: null,
      transaction_id: null,
      incident_date: null,
      disputed_amount: null,
      issue_summary: null,
    });
    setNoticeReady(false);
  };

  // Send message through chat engine
  const handleSendMessage = async (text) => {
    if (!text || !text.trim() || isChatLoading) return;

    const userMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setIsChatLoading(true);

    const historyPayload = messages.map(m => ({
      role: m.role,
      content: m.content,
    }));

    try {
      const data = await sendChatMessage({
        sessionId,
        message: text,
        docId: activeDoc?.id,
        history: historyPayload,
      });

      const assistantMsg = {
        role: 'assistant',
        content: data.response || 'I have reviewed your query.',
        source: data.source || 'direct',
        context_snippets: data.context_snippets || [],
        faq_match: data.faq_match || null,
        grievance_detected: data.grievance_detected,
      };

      setMessages(prev => [...prev, assistantMsg]);

      // If slots were extracted, merge them into current slots
      if (data.slots && typeof data.slots === 'object') {
        setSlots(prev => {
          const updated = { ...prev };
          if (data.slots.company_name) updated.company_name = data.slots.company_name;
          if (data.slots.transaction_id) updated.transaction_id = data.slots.transaction_id;
          if (data.slots.incident_date) updated.incident_date = data.slots.incident_date;
          if (data.slots.disputed_amount) updated.disputed_amount = data.slots.disputed_amount;
          if (data.slots.issue_summary) updated.issue_summary = data.slots.issue_summary;
          return updated;
        });
      }

      if (data.notice_ready !== undefined) {
        setNoticeReady(data.notice_ready);
      }

      // If grievance was detected and user is in scanner mode, switch to grievance
      if (data.grievance_detected && currentMode === 'scanner') {
        setCurrentMode('grievance');
      }
    } catch (err) {
      console.error('Chat error:', err);
      const errMsg = err.response?.data?.detail || err.message || 'Error communicating with Clausify engine.';
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `⚠️ **Service Notification:** ${errMsg}\n\nPlease verify that the backend API is running on \`http://localhost:8000\`.`,
          source: 'direct',
        }
      ]);
    } finally {
      setIsChatLoading(false);
    }
  };

  // Handle clicking "Ask AI about this clause" from RedFlagList
  const handleAskClause = (clause) => {
    const clauseQuery = `Please analyze Clause #${(clause.chunk_index !== undefined ? clause.chunk_index : 0) + 1} (${clause.detected_categories?.join(', ') || 'Risk clause'}):\n"${clause.clause_preview || clause.summary}".\n\nIs this clause legally enforceable under consumer protection standards, and what are my consumer rights?`;
    handleSendMessage(clauseQuery);
  };

  // Handle quick-filling a sample grievance scenario
  const handlePrefillSample = (key) => {
    const sampleText = SAMPLE_GRIEVANCE_PROMPTS[key];
    if (sampleText) {
      handleSendMessage(sampleText);
    }
  };

  // If not authenticated, render LoginPage
  if (!currentUser) {
    return <LoginPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-brand-500/20 selection:text-brand-300">
      
      {/* Top Navigation */}
      <Navbar
        currentMode={currentMode}
        onModeChange={(mode) => setCurrentMode(mode)}
        onRestartChat={handleRestartChat}
        activeDoc={activeDoc}
        currentUser={currentUser}
        onLogout={handleLogout}
        serverStatus={serverHealth}
      />

      {/* Main 2-Column Dashboard Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 flex flex-col">
        
        {/* Mode Info Banner */}
        <div className="mb-4 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-2">
            {currentMode === 'scanner' ? (
              <>
                <FileText className="w-4 h-4 text-brand-400" />
                <span>
                  <strong className="text-slate-200">Mode: Contract Risk Scanner</strong> — Upload PDF agreements to compute risk indices and verify red-flags.
                </span>
              </>
            ) : (
              <>
                <Scale className="w-4 h-4 text-indigo-400" />
                <span>
                  <strong className="text-slate-200">Mode: Consumer Grievance Shield</strong> — Converse to extract dispute entities and generate an enforceable legal notice.
                </span>
              </>
            )}
          </div>

          <div className="hidden sm:flex items-center gap-2 text-[11px] font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span className="text-slate-400">Groq Llama 3.3 RAG Active</span>
          </div>
        </div>

        {/* 2-Column Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-1 min-h-[720px]">
          
          {/* LEFT COLUMN: Chat Window */}
          <div className="lg:col-span-7 flex flex-col h-[740px] lg:h-[calc(100vh-140px)]">
            <ChatWindow
              messages={messages}
              isLoading={isChatLoading}
              onSendMessage={handleSendMessage}
              activeDoc={activeDoc}
              currentMode={currentMode}
              onUploadClick={() => setCurrentMode('scanner')}
              faqs={faqs}
              currentUser={currentUser}
            />
          </div>

          {/* RIGHT COLUMN: Dynamic Risk/Grievance Panel */}
          <div className="lg:col-span-5 flex flex-col space-y-5 h-[740px] lg:h-[calc(100vh-140px)] overflow-y-auto pr-1">
            
            {currentMode === 'scanner' ? (
              <>
                <DocUploader
                  onScanComplete={handleScanComplete}
                  activeDoc={activeDoc}
                  onResetDoc={handleResetDoc}
                  isScanning={isScanning}
                  setIsScanning={setIsScanning}
                />

                <RiskGauge
                  score={docSummary?.overall_risk_score || activeDoc?.overall_risk_score || 0}
                  totalChunks={docSummary?.total_chunks || 0}
                  highRiskCount={docSummary?.high_risk_count || 0}
                  mediumRiskCount={docSummary?.medium_risk_count || 0}
                  isScanning={isScanning}
                />

                <RedFlagList
                  clauses={clauses}
                  onAskClause={handleAskClause}
                />
              </>
            ) : (
              <>
                <GrievanceTracker
                  slots={slots}
                  noticeReady={noticeReady}
                  onSlotUpdate={(newSlots) => setSlots(newSlots)}
                  onPrefillSample={handlePrefillSample}
                  currentUser={currentUser}
                />
              </>
            )}

          </div>

        </div>

      </main>

    </div>
  );
}
