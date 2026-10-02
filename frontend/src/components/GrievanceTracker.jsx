import React, { useState } from 'react';
import { 
  Building2, 
  Calendar, 
  Hash, 
  IndianRupee, 
  AlertOctagon, 
  FileDown, 
  CheckCircle2, 
  CircleDashed, 
  Edit3, 
  Check, 
  Sparkles,
  Loader2,
  User,
  Mail,
  ShieldAlert
} from 'lucide-react';
import { generateLegalNotice } from '../services/api';

export default function GrievanceTracker({ 
  slots = {}, 
  noticeReady = false, 
  onSlotUpdate,
  onPrefillSample,
  currentUser = null 
}) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState(null);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  // Complainant personal details (auto-populated from logged in user)
  const [complainantName, setComplainantName] = useState(currentUser?.name || 'Rahul Verma');
  const [complainantEmail, setComplainantEmail] = useState(currentUser?.email || 'rahul.verma@example.com');
  const [editingSlotKey, setEditingSlotKey] = useState(null);
  const [tempSlotValue, setTempSlotValue] = useState('');

  // Sync if currentUser updates
  React.useEffect(() => {
    if (currentUser?.name) setComplainantName(currentUser.name);
    if (currentUser?.email) setComplainantEmail(currentUser.email);
  }, [currentUser]);

  const slotDefinitions = [
    {
      key: 'company_name',
      label: 'Company',
      icon: Building2,
      placeholder: 'e.g. Acme Corp / FlyAirways',
      value: slots.company_name,
    },
    {
      key: 'incident_date',
      label: 'Date',
      icon: Calendar,
      placeholder: 'e.g. 15 Jan 2025',
      value: slots.incident_date,
    },
    {
      key: 'transaction_id',
      label: 'Ref ID',
      icon: Hash,
      placeholder: 'e.g. TXN-89218 or Order #',
      value: slots.transaction_id,
    },
    {
      key: 'disputed_amount',
      label: 'Amount (INR)',
      icon: IndianRupee,
      placeholder: 'e.g. ₹14,500 or ₹2,499',
      value: slots.disputed_amount,
    },
    {
      key: 'issue_summary',
      label: 'Deficiency',
      icon: AlertOctagon,
      placeholder: 'e.g. Refusal to refund cancelled flight ticket',
      value: slots.issue_summary,
    },
  ];

  // Count filled slots
  const filledCount = slotDefinitions.filter(s => !!(s.value && s.value.trim())).length;
  const isReady = noticeReady || filledCount >= 4;

  const startEditSlot = (key, currentVal) => {
    setEditingSlotKey(key);
    setTempSlotValue(currentVal || '');
  };

  const saveEditSlot = (key) => {
    if (onSlotUpdate) {
      onSlotUpdate({ ...slots, [key]: tempSlotValue.trim() || null });
    }
    setEditingSlotKey(null);
  };

  const handleDownloadNotice = async () => {
    try {
      setIsDownloading(true);
      setDownloadError(null);
      setDownloadSuccess(false);

      const noticeData = {
        complainant_name: complainantName.trim() || 'Aggrieved Consumer',
        complainant_email: complainantEmail.trim() || undefined,
        company_name: slots.company_name || 'Respondent Merchant',
        incident_date: slots.incident_date || new Date().toLocaleDateString(),
        transaction_id: slots.transaction_id || 'N/A',
        disputed_amount: slots.disputed_amount || 'Not Specified',
        issue_summary: slots.issue_summary || 'Deficiency in service and refusal of rightful consumer redressal.',
        legal_statutes: [
          'Consumer Protection Act, 2019 (Section 2(47) Unfair Trade Practice)',
          'Deficiency of Service and Breach of Statutory Duty'
        ],
      };

      const blobData = await generateLegalNotice(noticeData);

      // Trigger automatic browser download
      const blob = new Blob([blobData], { type: 'application/pdf' });
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      const safeCompanyName = (slots.company_name || 'Notice').replace(/[^a-zA-Z0-9]/g, '_');
      link.download = `Legal_Notice_${safeCompanyName}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);

      setDownloadSuccess(true);
      setTimeout(() => setDownloadSuccess(false), 5000);
    } catch (err) {
      console.error('Failed to generate legal notice:', err);
      setDownloadError(err.response?.data?.detail || err.message || 'Error compiling legal notice PDF');
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <ShieldAlert className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-200">
              Live Grievance Slot Tracker
            </h3>
            <p className="text-xs text-slate-400">
              AI automatically extracts dispute entities from conversational chat
            </p>
          </div>
        </div>

        {/* Extraction Progress Counter */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs font-mono">
          <span className={`w-2 h-2 rounded-full ${isReady ? 'bg-emerald-400 animate-pulse' : 'bg-indigo-400'}`} />
          <span className="font-bold text-slate-200">{filledCount}</span>
          <span className="text-slate-500">/ 5 Slots</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-800/80">
        <div 
          className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-emerald-400 transition-all duration-500 ease-out"
          style={{ width: `${(filledCount / 5) * 100}%` }}
        />
      </div>

      {/* Live Visual Chips Grid */}
      <div className="space-y-2">
        {slotDefinitions.map((slot) => {
          const Icon = slot.icon;
          const isFilled = !!(slot.value && slot.value.trim());
          const isEditing = editingSlotKey === slot.key;

          return (
            <div
              key={slot.key}
              className={`p-2.5 rounded-xl border transition-all ${
                isFilled
                  ? 'bg-slate-900/80 border-slate-700/80'
                  : 'bg-slate-950/40 border-slate-800/60 border-dashed'
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-xs font-medium text-slate-400">
                  <Icon className={`w-3.5 h-3.5 ${isFilled ? 'text-indigo-400' : 'text-slate-500'}`} />
                  <span className="font-semibold text-slate-300">{slot.label}</span>
                </div>

                <div className="flex items-center gap-1.5">
                  {isFilled ? (
                    <span className="flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
                      <CheckCircle2 className="w-3 h-3" />
                      Captured
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-[10px] text-slate-500 bg-slate-900 px-1.5 py-0.5 rounded">
                      <CircleDashed className="w-3 h-3 animate-spin-slow" />
                      Awaiting
                    </span>
                  )}

                  {!isEditing && (
                    <button
                      type="button"
                      onClick={() => startEditSlot(slot.key, slot.value)}
                      title="Edit this slot manually"
                      className="p-1 rounded text-slate-500 hover:text-slate-300 hover:bg-slate-800 transition-colors"
                    >
                      <Edit3 className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>

              {/* Slot Value Display / Quick-Edit Form */}
              <div className="mt-1.5 pl-5">
                {isEditing ? (
                  <div className="flex items-center gap-1.5">
                    <input
                      type="text"
                      value={tempSlotValue}
                      onChange={(e) => setTempSlotValue(e.target.value)}
                      placeholder={slot.placeholder}
                      className="w-full px-2 py-1 text-xs rounded bg-slate-950 border border-indigo-500/60 text-slate-100 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      autoFocus
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') saveEditSlot(slot.key);
                        if (e.key === 'Escape') setEditingSlotKey(null);
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => saveEditSlot(slot.key)}
                      className="p-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white"
                    >
                      <Check className="w-3 h-3" />
                    </button>
                  </div>
                ) : (
                  <p className={`text-xs ${isFilled ? 'text-slate-200 font-medium' : 'text-slate-500 italic'}`}>
                    {isFilled ? slot.value : slot.placeholder}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Complainant Sender Settings */}
      <div className="p-3 rounded-xl bg-slate-900/50 border border-slate-800 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
            Notice Signatory Info
          </span>
          <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium border ${
            currentUser?.role === 'counsel'
              ? 'bg-indigo-500/10 text-indigo-300 border-indigo-500/20'
              : 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20'
          }`}>
            {currentUser?.role === 'counsel' ? 'Advocate / Legal Counsel' : 'Direct Consumer'}
          </span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          <div>
            <label className="text-[10px] text-slate-400 block mb-0.5">Complainant Name</label>
            <div className="relative">
              <User className="w-3 h-3 text-slate-500 absolute left-2 top-2" />
              <input
                type="text"
                value={complainantName}
                onChange={(e) => setComplainantName(e.target.value)}
                className="w-full pl-6 pr-2 py-1 text-xs rounded-lg bg-slate-950 border border-slate-800 text-slate-200 focus:border-indigo-500 focus:outline-none"
              />
            </div>
          </div>
          <div>
            <label className="text-[10px] text-slate-400 block mb-0.5">Email Contact</label>
            <div className="relative">
              <Mail className="w-3 h-3 text-slate-500 absolute left-2 top-2" />
              <input
                type="email"
                value={complainantEmail}
                onChange={(e) => setComplainantEmail(e.target.value)}
                className="w-full pl-6 pr-2 py-1 text-xs rounded-lg bg-slate-950 border border-slate-800 text-slate-200 focus:border-indigo-500 focus:outline-none"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Feedback Messages */}
      {downloadError && (
        <div className="p-2.5 rounded-lg bg-red-950/40 border border-red-800/80 text-red-300 text-xs flex items-center gap-2">
          <AlertOctagon className="w-4 h-4 flex-shrink-0" />
          <span>{downloadError}</span>
        </div>
      )}

      {downloadSuccess && (
        <div className="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-800/80 text-emerald-300 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>Legal Notice PDF downloaded successfully!</span>
        </div>
      )}

      {/* Action Button: Download Legal Notice PDF */}
      <button
        type="button"
        id="download-notice-btn"
        disabled={!isReady || isDownloading}
        onClick={handleDownloadNotice}
        className={`w-full py-3 px-4 rounded-xl text-xs font-bold tracking-wide uppercase flex items-center justify-center gap-2.5 transition-all duration-300 ${
          isReady && !isDownloading
            ? 'bg-gradient-to-r from-indigo-600 via-blue-600 to-emerald-500 text-white shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-[1.01] active:scale-[0.99] cursor-pointer'
            : 'bg-slate-800/60 text-slate-500 border border-slate-800 cursor-not-allowed'
        }`}
      >
        {isDownloading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin text-white" />
            <span>Compiling Legal Notice PDF...</span>
          </>
        ) : (
          <>
            <FileDown className={`w-4 h-4 ${isReady ? 'text-white' : 'text-slate-500'}`} />
            <span>
              {isReady ? 'Download Legal Notice PDF' : `Fill Missing Details (${filledCount}/5)`}
            </span>
          </>
        )}
      </button>

      {/* Sample Quick-Fill Chips for Demo */}
      {onPrefillSample && (
        <div className="pt-1 border-t border-slate-800/60">
          <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1.5 font-semibold">
            Quick-Fill Grievance Scenarios:
          </span>
          <div className="flex flex-wrap gap-1.5">
            <button
              type="button"
              onClick={() => onPrefillSample('flight')}
              className="text-[11px] px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-700 transition-colors"
            >
              ✈️ Flight Delay Refund
            </button>
            <button
              type="button"
              onClick={() => onPrefillSample('subscription')}
              className="text-[11px] px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-700 transition-colors"
            >
              💳 Hidden Auto-Renewal
            </button>
            <button
              type="button"
              onClick={() => onPrefillSample('ecommerce')}
              className="text-[11px] px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-slate-700 transition-colors"
            >
              📦 Defective Product Return
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
