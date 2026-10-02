import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
  },
});

/**
 * Upload a PDF document for chunking, vector embedding, and clause risk analysis.
 * @param {File} file
 * @param {Function} [onUploadProgress]
 */
export async function scanPdfDocument(file, onUploadProgress) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await client.post('/api/v1/scan/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  });
  return response.data;
}

/**
 * Send conversational query to Clausify RAG engine with anti-hallucination grounding.
 * @param {Object} params
 * @param {string} [params.sessionId]
 * @param {string} params.message
 * @param {string} [params.docId]
 * @param {Array<{role: string, content: string}>} [params.history]
 */
export async function sendChatMessage({ sessionId, message, docId, history = [] }) {
  const payload = {
    session_id: sessionId || undefined,
    message,
    doc_id: docId || undefined,
    history,
  };

  const response = await client.post('/api/v1/chat', payload);
  return response.data;
}

/**
 * Generate formal legal dispute notice PDF and download binary stream.
 * @param {Object} noticeData
 */
export async function generateLegalNotice(noticeData) {
  const payload = {
    complainant_name: noticeData.complainant_name || 'Aggrieved Consumer',
    company_name: noticeData.company_name,
    incident_date: noticeData.incident_date,
    transaction_id: noticeData.transaction_id,
    disputed_amount: noticeData.disputed_amount,
    issue_summary: noticeData.issue_summary,
    legal_statutes: noticeData.legal_statutes || [
      'Consumer Protection Act, 2019',
      'Unfair Contract Terms & Deficiency in Service'
    ],
    notice_date: noticeData.notice_date || new Date().toISOString().split('T')[0],
    complainant_email: noticeData.complainant_email || undefined,
    complainant_address: noticeData.complainant_address || undefined,
  };

  const response = await client.post('/api/v1/notice/generate', payload, {
    responseType: 'blob',
  });
  return response.data;
}

/**
 * Fetch knowledge base FAQs for quick prompt suggestions.
 */
export async function fetchFaqs() {
  try {
    const response = await client.get('/api/v1/admin/faqs');
    return response.data || [];
  } catch (error) {
    console.warn('Failed to load dynamic FAQs, using default suggestions:', error);
    return [];
  }
}

/**
 * Health check verification.
 */
export async function checkBackendHealth() {
  try {
    const response = await client.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'offline', error: error.message };
  }
}
