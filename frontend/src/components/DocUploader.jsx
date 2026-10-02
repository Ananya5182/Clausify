import React, { useState, useRef } from 'react';
import { 
  UploadCloud, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  Loader2, 
  X, 
  Sparkles,
  Download,
  Flame,
  AlertTriangle,
  ShieldCheck
} from 'lucide-react';
import { scanPdfDocument } from '../services/api';

const SAMPLE_FILES = [
  {
    name: 'Sample1_High_Risk_StreamPlay_Subscription.pdf',
    label: 'High Risk (StreamPlay)',
    desc: 'Mandatory arbitration, data selling & liability caps',
    badge: 'Critical',
    badgeClass: 'bg-red-500/15 text-red-400 border-red-500/30',
    icon: Flame,
  },
  {
    name: 'Sample2_Moderate_Risk_CloudVault_TOS.pdf',
    label: 'Moderate Risk (CloudVault)',
    desc: 'Notice modifications, 48hr cancel & regional venue',
    badge: 'Moderate',
    badgeClass: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
    icon: AlertTriangle,
  },
  {
    name: 'Sample3_Safe_FairDocs_Consumer_Agreement.pdf',
    label: 'Safe (FairDocs)',
    desc: 'No waivers, pro-rata refund & zero data selling',
    badge: 'Safe',
    badgeClass: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
    icon: ShieldCheck,
  },
];

export default function DocUploader({ 
  onScanComplete, 
  activeDoc, 
  onResetDoc,
  isScanning,
  setIsScanning 
}) {
  const [dragActive, setDragActive] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  };

  const handleFileSelected = async (file) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setUploadError('Only PDF files are supported. Please upload a .pdf agreement.');
      return;
    }

    try {
      setIsScanning(true);
      setUploadError(null);
      setUploadProgress(20);

      const result = await scanPdfDocument(file, (progressEvent) => {
        if (progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 50) / progressEvent.total);
          setUploadProgress(percent);
        }
      });

      setUploadProgress(100);
      onScanComplete(result);
    } catch (err) {
      console.error('Scan error:', err);
      const msg = err.response?.data?.detail || err.message || 'Failed to scan and analyze PDF document';
      setUploadError(msg);
    } finally {
      setIsScanning(false);
      setUploadProgress(0);
    }
  };

  // Instant 1-click Sample Agreement Loader
  const handleLoadSample = async (filename) => {
    try {
      setIsScanning(true);
      setUploadError(null);
      setUploadProgress(25);

      const response = await fetch(`/samples/${filename}`);
      if (!response.ok) {
        throw new Error(`Could not fetch ${filename}`);
      }
      const blob = await response.blob();
      const file = new File([blob], filename, { type: 'application/pdf' });
      await handleFileSelected(file);
    } catch (err) {
      console.error('Sample load error:', err);
      setUploadError('Failed to load sample document: ' + err.message);
      setIsScanning(false);
    }
  };

  return (
    <div className="glass-card rounded-2xl p-5 border border-slate-800 shadow-xl space-y-3">
      <div className="flex items-center justify-between pb-1">
        <div className="flex items-center gap-2">
          <UploadCloud className="w-4 h-4 text-brand-400" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Agreement Document Ingestion
          </h3>
        </div>
        {activeDoc && (
          <button
            type="button"
            onClick={onResetDoc}
            className="text-[11px] text-slate-400 hover:text-red-400 flex items-center gap-1 transition-colors"
          >
            <X className="w-3 h-3" />
            <span>Remove</span>
          </button>
        )}
      </div>

      {activeDoc ? (
        /* Active Document Banner */
        <div className="p-3.5 rounded-xl bg-slate-900/90 border border-brand-500/30 flex items-center justify-between gap-3">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-9 h-9 rounded-lg bg-brand-500/10 border border-brand-500/20 flex items-center justify-center flex-shrink-0">
              <FileText className="w-5 h-5 text-brand-400" />
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-slate-200 truncate">
                {activeDoc.file_name}
              </p>
              <div className="flex items-center gap-2 text-[10px] text-slate-400 mt-0.5">
                <span className="text-emerald-400 font-mono">Scanned & Indexed</span>
                <span>•</span>
                <span className="font-mono">UUID: {activeDoc.id.slice(0, 8)}...</span>
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition-colors flex-shrink-0"
          >
            Replace
          </button>
        </div>
      ) : (
        /* Upload Drag-and-Drop Area */
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => !isScanning && fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-all ${
            dragActive
              ? 'border-brand-400 bg-brand-500/10 scale-[1.01]'
              : 'border-slate-800 hover:border-slate-700 bg-slate-900/40 hover:bg-slate-900/60'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
          />

          <div className="flex flex-col items-center justify-center space-y-2">
            <div className="w-10 h-10 rounded-full bg-brand-500/10 border border-brand-500/20 flex items-center justify-center text-brand-400">
              {isScanning ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <UploadCloud className="w-5 h-5" />
              )}
            </div>

            <div>
              <p className="text-xs font-semibold text-slate-200">
                {isScanning ? 'Ingesting, Chunking & Embedding PDF...' : 'Click to upload or drag & drop PDF'}
              </p>
              <p className="text-[11px] text-slate-500 mt-0.5">
                Upload terms of service, consumer contracts, privacy policies
              </p>
            </div>
          </div>

          {isScanning && (
            <div className="mt-3 w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
              <div 
                className="bg-brand-500 h-full transition-all duration-300"
                style={{ width: `${uploadProgress || 65}%` }}
              />
            </div>
          )}
        </div>
      )}

      {/* Error Message */}
      {uploadError && (
        <div className="p-2.5 rounded-lg bg-red-950/40 border border-red-800 text-red-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{uploadError}</span>
        </div>
      )}

      {/* 1-Click Sample Test Agreements */}
      <div className="pt-2 border-t border-slate-800/80">
        <span className="text-[10px] text-slate-400 uppercase font-bold tracking-wider block mb-1.5">
          One-Click Test Agreements:
        </span>
        <div className="grid grid-cols-1 gap-1.5">
          {SAMPLE_FILES.map((sample) => {
            const Icon = sample.icon;
            return (
              <div
                key={sample.name}
                className="p-2 rounded-xl bg-slate-900/60 hover:bg-slate-900 border border-slate-800/80 hover:border-slate-700 flex items-center justify-between gap-2 text-xs transition-colors"
              >
                <div className="flex items-center gap-2 min-w-0">
                  <Icon className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                  <div className="min-w-0">
                    <div className="flex items-center gap-1.5">
                      <span className="font-semibold text-slate-200 truncate">
                        {sample.label}
                      </span>
                      <span className={`text-[9px] px-1.5 py-0.2 rounded font-bold border ${sample.badgeClass}`}>
                        {sample.badge}
                      </span>
                    </div>
                    <p className="text-[10px] text-slate-500 truncate">
                      {sample.desc}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-1 flex-shrink-0">
                  <button
                    type="button"
                    disabled={isScanning}
                    onClick={() => handleLoadSample(sample.name)}
                    className="px-2 py-1 rounded bg-brand-500/10 hover:bg-brand-500/20 text-brand-400 border border-brand-500/30 text-[11px] font-semibold transition-colors disabled:opacity-50"
                  >
                    Load & Scan
                  </button>
                  <a
                    href={`/samples/${sample.name}`}
                    download={sample.name}
                    title="Download PDF to computer"
                    className="p-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white border border-slate-700 transition-colors"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
