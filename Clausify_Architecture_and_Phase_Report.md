# Clausify - Technical Architecture & 5-Phase Project Report

## System Overview
Clausify is an AI legal assistant designed to scan consumer agreements (Terms of Service, Privacy Policies), detect unfair/predatory clauses, ground conversational dialogue against uploaded documents, and draft formal legal dispute notices under Consumer Protection statutes.

---

## Localhost Access URLs

| Service / Interface | Localhost URL | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **Unified Gateway Proxy** | http://localhost:8080 | 8080 | Routes both Web UI and API requests seamlessly |
| **React Web App** | http://localhost:5173 | 5173 | Interactive Single-Page Application |
| **FastAPI Backend** | http://localhost:8000 | 8000 | Core ASGI server |
| **Swagger UI Documentation**| http://localhost:8000/docs | 8000 / 8080 | Interactive OpenAPI test console |
| **ReDoc Documentation** | http://localhost:8000/redoc | 8000 / 8080 | Alternative formal API documentation |
| **Backend Health Check** | http://localhost:8000/health | 8000 / 8080 | Live JSON health heartbeat |

---

## The 5 Development Phases

### Phase 1: Environment, Configuration, Supabase pgvector & AI Foundation
- **FastAPI Scaffold**: ASGI server with CORS middleware allowing `http://localhost:5173`.
- **Supabase PostgreSQL + pgvector**:
  - `documents` table: Metadata, file names, aggregate risk score.
  - `document_chunks` table: Ingested chunks, risk levels, reasons, and 384-dimensional dense vectors.
  - `faqs` table: Pre-seeded legal knowledge base with 384-dimensional embeddings.
  - RPC Functions: `match_faqs` and `match_document_chunks` using cosine distance `<->`.
- **Local Embedding Service**: `sentence-transformers/all-MiniLM-L6-v2` generating normalized 384-d vectors.
- **Groq Cloud Integration**: Active inference models: `openai/gpt-oss-120b`, `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`.

### Phase 2: Document Ingestion, PDF Processing & Admin FAQ
- **PyPDF Ingestion**: Sanitizes, decrypts, and extracts text.
- **Sliding-Window Chunking**: ~500 tokens with 50-token overlap (~375 words, 38-word overlap).
- **Heuristic Keyword Pre-screening**: Matches predatory triggers (`arbitrat`, `dispute`, `class action`, `unilateral modify`, `tracking`, `auto-renew`, `non-refundable`, `liability waiver`).
- **Admin FAQ Endpoints**: `POST /api/v1/admin/faq` and `GET /api/v1/admin/faqs`.

### Phase 3: Deep AI Clause Risk Analysis & Scoring Formulation
- **The 4 Monitored Predatory Categories**:
  1. Forced Arbitration & Class Action Waivers.
  2. Unilateral Modifications without notice.
  3. Third-party Personal Data Tracking & Selling.
  4. Auto-renewal & Non-refundable Payment Locks.
- **Composite Risk Score Formulation**:
  `Score = (0.75 * Max Severity) + (0.25 * Average of Flagged Scores)`

### Phase 4: Multi-Step Interactive RAG Chat & Legal Dispute Notice Engine
- **Step A: FAQ Pre-check**: Instant verified response if similarity >= 0.82.
- **Step B: Document Context Grounding**: RAG vector search with anti-hallucination prompt.
- **Step C & D: Slot Extraction**: Detects dispute and extracts 5 slots: `company_name`, `transaction_id`, `incident_date`, `disputed_amount`, and `issue_summary`. When all 5 are present, triggers `notice_ready: true`.
- **Legal Notice PDF Compilation**: Jinja2 template (`legal_notice.html`) compiled via `xhtml2pdf` into a downloadable binary PDF stream (`POST /api/v1/notice/generate`).

### Phase 5: Modern Interactive Web Application (React 19 + Tailwind CSS)
- **Mode 1: Agreement Scanner**: Drag-and-drop PDF uploader, animated radial SVG Risk Gauge (0-100), and expandable red-flag clause cards.
- **Mode 2: Grievance Notice Assistant**: Interactive grounded chat, real-time 5-slot checklist, and 1-click legal dispute notice generation.
- **Multi-Role Authentication**: Consumer, Legal Advocate, Compliance Officer.

---

## Operational Commands (PowerShell)

```powershell
# 1. Start Backend (Port 8000)
& "d:\AI&SC\Clausifyackendenv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Start Frontend (Port 5173)
cd "d:\AI&SC\Clausifyrontend"; node "node_modules/vite/bin/vite.js"

# 3. Start Gateway Proxy (Port 8080)
& "d:\AI&SC\Clausifyackendenv\Scripts\python.exe" "d:\AI&SC\Clausifyackend\gateway_8080.py"

# 4. Run Test Suites
& "d:\AI&SC\Clausifyackendenv\Scripts\python.exe" "d:\AI&SC\Clausifyackend	est_pipeline.py"
& "d:\AI&SC\Clausifyackendenv\Scripts\python.exe" "d:\AI&SC\Clausifyackend	est_chat_and_notice.py"
```
