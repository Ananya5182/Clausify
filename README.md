# Clausify ⚖️🛡️
### AI Legal Agreement Scanner & Statutory Consumer Grievance Shield

Clausify is an end-to-end legal intelligence platform built to protect consumers against unfair contract terms, unilateral contract alterations, hidden recurring charges, and invasive data harvesting. It pairs dense local vector embeddings with high-speed LLM reasoning to evaluate agreements, ground live conversational dialogue, and compile formal dispute notices in accordance with modern consumer protection statutes.

---

## 🌟 Key Features

1. **Document Risk Scanner**:
   - Ingests Terms of Service and Privacy Policies (PDF).
   - ~500-token sliding-window chunking with 50-token overlap.
   - Evaluates 4 major predatory clause categories:
     - ⚖️ **Forced Arbitration & Class Action Waivers**
     - 🔄 **Unilateral Contract Modifications**
     - 🔒 **Third-Party Data Selling / Tracking**
     - 💰 **Auto-Renewals & Non-Refundable Payment Locks**
   - Computes an aggregate **Risk Score (0–100)** with animated radial gauge visualization.

2. **Grounded RAG Legal Chatbot**:
   - Zero-hallucination conversational assistant strictly grounded on ingested document excerpts.
   - Step A: Instant verified knowledge-base matching ($\ge 82\%$ similarity) against Supabase FAQ vectors.
   - Step B: Context retrieval from active document chunks.

3. **Conversational Grievance Entity Extraction**:
   - Automatically detects consumer dispute intent.
   - Extracts 5 statutory slots: `company_name`, `transaction_id`, `incident_date`, `disputed_amount`, and `issue_summary`.

4. **1-Click Legal Dispute Notice Generation**:
   - Compiles formal legal notices citing the Consumer Protection Act 2019, EFTA, and UCC Section 2-302.
   - Generates and downloads styled binary PDF documents.

---

## 🏗️ Architecture & Technology Stack

- **Frontend**: React 19, Vite, Tailwind CSS, Lucide Icons, Axios.
- **Backend**: FastAPI, Uvicorn, Pydantic, PyPDF, ReportLab, xhtml2pdf, Jinja2.
- **Database & Vectors**: Supabase PostgreSQL + `pgvector` extension (Cosine Distance `<->`).
- **AI Models**:
  - Local Embeddings: HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors).
  - LLM Reasoning & Risk Extraction: Groq Cloud (`openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`).

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and supply your SUPABASE_URL, SUPABASE_KEY, and GROQ_API_KEY
```

Run the backend server:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Access the application at `http://localhost:5173`.

### 4. Unified Gateway (Optional)
To access both frontend and backend seamlessly on port `8080`:
```bash
python backend/gateway_8080.py
```
Open `http://localhost:8080`.

---

## 🧪 Testing

```bash
# Test document ingestion, vector embeddings & Admin FAQ routes
python backend/test_pipeline.py

# Test RAG chat, FAQ pre-checks, slot extraction & PDF compilation
python backend/test_chat_and_notice.py
```

---

## 📄 License
This project is licensed under the MIT License.
