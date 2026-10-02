"""Generate an executive-grade, beautifully formatted PDF report for Clausify:
Architecture, 5 Development Phases, System Endpoints, and Operational Guide.
Saves copies to project root and User Downloads folder.
"""
import os
import sys
from pathlib import Path
from xhtml2pdf import pisa

# Base directories
BASE_DIR = Path(__file__).resolve().parent
PROJECT_COPY_PDF = BASE_DIR / "Clausify_Complete_System_Report.pdf"
PROJECT_COPY_MD = BASE_DIR / "Clausify_Architecture_and_Phase_Report.md"

DOWNLOADS_DIR = Path(os.path.expanduser("~")) / "Downloads"
DOWNLOADS_COPY_PDF = DOWNLOADS_DIR / "Clausify_Complete_System_Report.pdf"

LOGO_PATH = (BASE_DIR / "clausify_logo.jpg").as_posix()

HTML_CONTENT = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Clausify - Complete Technical & System Architecture Report</title>
<style>
  @page {{
    size: a4 portrait;
    margin: 2.0cm 1.8cm 2.0cm 1.8cm;
    @bottom-right {{
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      color: #64748b;
      font-family: Helvetica, Arial, sans-serif;
    }}
    @bottom-left {{
      content: "Clausify — AI Legal Assistant Report";
      font-size: 8pt;
      color: #64748b;
      font-family: Helvetica, Arial, sans-serif;
    }}
  }}

  body {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 9pt;
    line-height: 1.45;
    color: #1e293b;
  }}

  .header-table {{
    width: 100%;
    border-bottom: 2.5px solid #4f46e5;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }}

  .header-logo {{
    width: 65px;
    height: auto;
    vertical-align: middle;
  }}

  .header-title-box {{
    padding-left: 14px;
    vertical-align: middle;
  }}

  .app-name {{
    font-size: 20pt;
    font-weight: bold;
    color: #1e1b4b;
    letter-spacing: 0.5px;
    margin: 0;
  }}

  .app-subtitle {{
    font-size: 9.5pt;
    color: #4f46e5;
    font-weight: bold;
    margin-top: 2px;
  }}

  .doc-meta {{
    font-size: 8pt;
    color: #64748b;
    margin-top: 4px;
  }}

  h1 {{
    font-size: 14pt;
    color: #1e1b4b;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  h2 {{
    font-size: 11pt;
    color: #4338ca;
    margin-top: 14px;
    margin-bottom: 6px;
    border-left: 3px solid #6366f1;
    padding-left: 6px;
  }}

  h3 {{
    font-size: 9.5pt;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 4px;
    font-weight: bold;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 7px;
    text-align: justify;
  }}

  ul, ol {{
    margin-top: 2px;
    margin-bottom: 8px;
    padding-left: 18px;
  }}

  li {{
    margin-bottom: 3px;
  }}

  .badge {{
    display: inline-block;
    padding: 2px 6px;
    font-size: 7.5pt;
    font-weight: bold;
    border-radius: 3px;
    text-transform: uppercase;
  }}
  .badge-critical {{ background-color: #fee2e2; color: #991b1b; }}
  .badge-high {{ background-color: #ffedd5; color: #9a3412; }}
  .badge-medium {{ background-color: #fef3c7; color: #92400e; }}
  .badge-safe {{ background-color: #dcfce7; color: #166534; }}
  .badge-info {{ background-color: #e0e7ff; color: #3730a3; }}

  table.data-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
    margin-bottom: 12px;
    font-size: 8.5pt;
  }}

  table.data-table th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: bold;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
  }}

  table.data-table td {{
    padding: 5px 8px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}

  .card-box {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 9px 12px;
    margin-bottom: 10px;
  }}

  .alert-box {{
    background-color: #eef2ff;
    border-left: 3.5px solid #4f46e5;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: 8.5pt;
  }}

  .code-text {{
    font-family: Courier, monospace;
    font-size: 8pt;
    background-color: #f1f5f9;
    padding: 1px 4px;
    color: #0f172a;
  }}

  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

  <!-- HEADER -->
  <table class="header-table">
    <tr>
      <td style="width: 75px; vertical-align: top;">
        <img src="{LOGO_PATH}" class="header-logo" alt="Clausify Logo" />
      </td>
      <td class="header-title-box">
        <div class="app-name">CLAUSIFY</div>
        <div class="app-subtitle">AI Legal Agreement Scanner & Consumer Grievance Assistant</div>
        <div class="doc-meta">Comprehensive System Architecture, 5 Development Phases & Technical Reference Report | Generated: October 2026</div>
      </td>
    </tr>
  </table>

  <!-- EXECUTIVE SUMMARY -->
  <div class="alert-box">
    <b>Executive Overview:</b> Clausify is an end-to-end legal intelligence platform built to protect consumers against unfair contract terms, unilateral contract alterations, hidden recurring charges, and invasive data harvesting. It pairs dense local vector embeddings with high-speed LLM reasoning to evaluate agreements, ground live conversational dialogue, and compile formal dispute notices in accordance with modern consumer protection statutes.
  </div>

  <!-- SECTION: ACCESS URLS & PORT TOPOLOGY -->
  <h1>1. System Access Points & Network Topology</h1>
  <p>The platform runs three interconnected background services ensuring seamless local access across web interfaces and developer endpoints:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Service / Interface</th>
        <th style="width: 25%;">Address / URL</th>
        <th style="width: 15%;">Default Port</th>
        <th style="width: 35%;">Functional Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Unified Gateway Proxy</b></td>
        <td><span class="code-text">http://localhost:8080</span></td>
        <td><span class="badge badge-info">8080</span></td>
        <td><b>Unified Entry Point:</b> Dynamically routes UI requests to port 5173 and API/Swagger requests to port 8000.</td>
      </tr>
      <tr>
        <td><b>Interactive Web UI</b></td>
        <td><span class="code-text">http://localhost:5173</span></td>
        <td><span class="badge badge-info">5173</span></td>
        <td>Vite + React 19 Frontend application featuring dynamic risk visualizers and live chat.</td>
      </tr>
      <tr>
        <td><b>Core FastAPI Server</b></td>
        <td><span class="code-text">http://localhost:8000</span></td>
        <td><span class="badge badge-info">8000</span></td>
        <td>High-performance ASGI backend serving ingestion, AI inference, and notice generation.</td>
      </tr>
      <tr>
        <td><b>Swagger UI (Docs)</b></td>
        <td><span class="code-text">http://localhost:8000/docs</span></td>
        <td>8000 / 8080</td>
        <td>OpenAPI 3.1 interactive testing console for all endpoints.</td>
      </tr>
      <tr>
        <td><b>ReDoc Documentation</b></td>
        <td><span class="code-text">http://localhost:8000/redoc</span></td>
        <td>8000 / 8080</td>
        <td>Formal specification documentation view.</td>
      </tr>
      <tr>
        <td><b>Operational Health Check</b></td>
        <td><span class="code-text">http://localhost:8000/health</span></td>
        <td>8000 / 8080</td>
        <td>JSON health heartbeat returning backend status, version, and active AI model names.</td>
      </tr>
    </tbody>
  </table>

  <!-- SECTION: THE 5 DEVELOPMENT PHASES -->
  <h1>2. Complete Breakdown of the 5 Development Phases</h1>

  <!-- PHASE 1 -->
  <h2>Phase 1: Architecture, Environment & Core Foundation</h2>
  <p>Phase 1 established the infrastructural bedrock, external service integrations, and relational/vector storage schemas:</p>
  <ul>
    <li><b>Framework & Application Scaffolding:</b> Configured FastAPI with strict CORS middleware (<span class="code-text">backend/app/main.py</span>), environment parsing via python-dotenv and Pydantic (<span class="code-text">backend/app/core/config.py</span>).</li>
    <li><b>Supabase PostgreSQL + pgvector Database:</b> Designed 3 core relational tables equipped with 384-dimensional vector columns:
      <ul>
        <li><span class="code-text">documents</span>: Tracks ingested PDFs, file names, timestamps, and overall aggregate risk scores.</li>
        <li><span class="code-text">document_chunks</span>: Stores individual ~500-token text chunks, risk level ratings (<span class="badge badge-critical">HIGH</span>, <span class="badge badge-medium">MEDIUM</span>, <span class="badge badge-safe">LOW</span>, <span class="badge badge-safe">NONE</span>), plain-language flag reasons, and 384-d vector embeddings.</li>
        <li><span class="code-text">faqs</span>: Pre-seeded curated legal questions and answers with 384-d vector embeddings for zero-latency retrieval.</li>
      </ul>
    </li>
    <li><b>Local In-Memory Vector Embedding Engine:</b> Integrated HuggingFace <span class="code-text">sentence-transformers/all-MiniLM-L6-v2</span> in <span class="code-text">backend/app/services/embedding_service.py</span>, producing normalized 384-dimensional dense vectors locally without cloud API costs or latency.</li>
    <li><b>Groq AI Cloud SDK:</b> Initialized the high-speed inference client (<span class="code-text">backend/app/core/groq_client.py</span>) supporting <span class="code-text">openai/gpt-oss-120b</span>, <span class="code-text">openai/gpt-oss-20b</span>, and <span class="code-text">qwen/qwen3.8-27b</span>.</li>
  </ul>

  <!-- PHASE 2 -->
  <h2>Phase 2: Document Ingestion, PDF Processing & Admin Knowledge Base</h2>
  <p>Phase 2 implemented the end-to-end document intake and chunking pipeline alongside knowledge-base administrative capabilities:</p>
  <ul>
    <li><b>PyPDF Extraction & Sanitization:</b> In <span class="code-text">backend/app/api/routes_scan.py</span>, <span class="code-text">extract_text_from_pdf</span> parses binary PDF data, decrypts blank password protections, and strips malformed characters.</li>
    <li><b>Sliding-Window Token Chunking:</b> Implemented <span class="code-text">split_into_chunks</span> utilizing a standard NLP token-to-word ratio (1 token is approx 0.75 words) to create ~500-token chunks with 50-token overlaps (~375 words per window, 38 words overlap) to ensure cross-boundary legal context retention.</li>
    <li><b>Heuristic Keyword Pre-screening:</b> Evaluates clauses against predatory keywords (<i>"arbitrat", "class action", "unilateral modify", "personal data", "tracking", "auto-renew", "non-refundable", "indemnif"</i>) to prioritize deep LLM analysis.</li>
    <li><b>Admin FAQ CRUD API:</b> In <span class="code-text">backend/app/api/routes_admin.py</span>, implemented <span class="code-text">POST /api/v1/admin/faq</span> (vectorizes questions and stores them in Supabase) and <span class="code-text">GET /api/v1/admin/faqs</span> for knowledge base updates.</li>
  </ul>

  <div class="page-break"></div>

  <!-- PHASE 3 -->
  <h2>Phase 3: Deep AI Clause Risk Analysis & Scoring Formulation</h2>
  <p>Phase 3 engineered the specialized LLM evaluation prompts, structured JSON schema outputs, and composite risk scoring formulation:</p>

  <div class="card-box">
    <b>The 4 Primary Predatory Clause Categories Monitored:</b>
    <ol>
      <li><b>Forced Arbitration & Class Action Waivers:</b> Clauses stripping consumers of constitutional rights to open court jury trials or collective dispute aggregation.</li>
      <li><b>Unilateral Modifications:</b> Clauses permitting providers to alter prices, terms, or service scopes at sole discretion without advance notice.</li>
      <li><b>Third-Party Data Selling / Harvesting:</b> Broad permissions to monetize, trade, or transfer personal or behavioral data without explicit consumer consent.</li>
      <li><b>Auto-Renewal & Non-Refundable Payment Locks:</b> Involuntary subscription renewals paired with total zero-refund stipulations.</li>
    </ol>
  </div>

  <p><b>Aggregate Document Risk Formulation:</b><br />
  To balance overall breadth with the presence of critical terms, Clausify uses a weighted hybrid formula in <span class="code-text">compute_overall_risk_score</span>:</p>
  <div class="alert-box">
    <center><b>Risk Score = (0.75 × Peak Severity Score) + (0.25 × Average of Flagged Scores)</b></center>
    <p style="margin-top: 4px; font-size: 8pt; margin-bottom: 0;">This prevents agreements with a single catastrophic clause (e.g. 95/100 arbitration waiver) from being hidden by benign introductory boilerplate, while adjusting higher if multiple violations exist.</p>
  </div>

  <!-- PHASE 4 -->
  <h2>Phase 4: Multi-Step Interactive RAG Chat & Legal Dispute Notice Engine</h2>
  <p>Phase 4 engineered the interactive conversational intelligence pipeline and document compilation engine:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Workflow Step</th>
        <th style="width: 35%;">Technical Mechanism</th>
        <th style="width: 40%;">Operational Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Step A: FAQ Pre-Check</b></td>
        <td>Cosine similarity check (<span class="code-text">threshold &gt;= 0.82</span>) against Supabase knowledge base vectors.</td>
        <td>Returns verified legal guidance instantly without model latency or hallucinations.</td>
      </tr>
      <tr>
        <td><b>Step B: Document RAG Grounding</b></td>
        <td>Vector similarity search across active document chunks via <span class="code-text">match_document_chunks</span>.</td>
        <td>Forces the assistant to cite exact clauses; strictly refuses to fabricate missing contract terms.</td>
      </tr>
      <tr>
        <td><b>Step C: Slot Entity Extraction</b></td>
        <td>Analyzes intent and extracts 5 structured consumer grievance fields:
          <ul>
            <li><span class="code-text">company_name</span></li>
            <li><span class="code-text">transaction_id</span></li>
            <li><span class="code-text">incident_date</span></li>
            <li><span class="code-text">disputed_amount</span></li>
            <li><span class="code-text">issue_summary</span></li>
          </ul>
        </td>
        <td>Transforms unstructured complaints into actionable dispute parameters. When all 5 slots are populated, <span class="code-text">notice_ready = True</span> is triggered.</td>
      </tr>
      <tr>
        <td><b>Step D: Notice Compilation</b></td>
        <td>Jinja2 template (<span class="code-text">legal_notice.html</span>) compiled into binary PDF stream via <span class="code-text">xhtml2pdf</span>.</td>
        <td>Streams formal dispute notice citing the Consumer Protection Act 2019, EFTA, or UCC Section 2-302 directly to the user.</td>
      </tr>
    </tbody>
  </table>

  <!-- PHASE 5 -->
  <h2>Phase 5: Modern Interactive Web Application (React 19 + Tailwind CSS)</h2>
  <p>Phase 5 created a responsive, rich user experience (<span class="code-text">frontend/src/App.jsx</span>) built around two modes:</p>
  <ul>
    <li><b>Mode 1: Agreement Scanner:</b>
      <ul>
        <li><span class="code-text">DocUploader.jsx</span>: Drag-and-drop PDF uploader with live upload progress tracking and 3 pre-built sample contracts.</li>
        <li><span class="code-text">RiskGauge.jsx</span>: Animated SVG radial gauge visually representing the 0–100 risk score with dynamic color grading.</li>
        <li><span class="code-text">RedFlagList.jsx</span>: Categorized clause cards displaying plain-language summaries, violation reasons, and "Ask Assistant" shortcuts.</li>
      </ul>
    </li>
    <li><b>Mode 2: Grievance Notice Assistant:</b>
      <ul>
        <li><span class="code-text">ChatWindow.jsx</span>: Interactive conversation stream with verified FAQ chips, citation indicators, and quick prompts.</li>
        <li><span class="code-text">GrievanceTracker.jsx</span>: Real-time visual slot progress tracker showing which details are confirmed, with editable inputs and a 1-click <b>Generate & Download Legal Notice (PDF)</b> action.</li>
        <li><span class="code-text">LoginPage.jsx</span>: Multi-role authentication (Individual Consumer, Legal Advocate, Enterprise Compliance Officer).</li>
      </ul>
    </li>
  </ul>

  <div class="page-break"></div>

  <!-- SECTION: PRE-PACKAGED TEST AGREEMENTS -->
  <h1>3. Test Agreements & Validation Artifacts</h1>
  <p>The workspace includes a generator script (<span class="code-text">generate_sample_pdfs.py</span>) that outputs 3 agreements for demonstration and evaluation:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th>Sample Agreement</th>
        <th>File Name</th>
        <th>Expected Score</th>
        <th>Key Clauses Included</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>StreamPlay Subscription</b></td>
        <td><span class="code-text">streamplay_high_risk_agreement.pdf</span></td>
        <td><span class="badge badge-critical">85–95 Critical</span></td>
        <td>Forced binding arbitration, class action waiver, unilateral price modifications, and unrestricted data monetization.</td>
      </tr>
      <tr>
        <td><b>CloudVault Terms</b></td>
        <td><span class="code-text">cloudvault_moderate_risk_agreement.pdf</span></td>
        <td><span class="badge badge-medium">45–55 Moderate</span></td>
        <td>Auto-renewal with notice, standard liability caps, and notice-based unilateral modifications.</td>
      </tr>
      <tr>
        <td><b>FairDocs Agreement</b></td>
        <td><span class="code-text">fairdocs_consumer_agreement.pdf</span></td>
        <td><span class="badge badge-safe">0–15 Safe</span></td>
        <td>Pro-rata refund policy, transparent dispute resolution in court, zero data selling, and explicit user consent for changes.</td>
      </tr>
    </tbody>
  </table>

  <!-- SECTION: OPERATIONAL RUNBOOK -->
  <h1>4. Operational Runbook & Maintenance Commands</h1>

  <h3>Starting Services Manually (PowerShell):</h3>
  <div class="card-box">
    <b>1. Core Backend (FastAPI on Port 8000):</b><br />
    <span class="code-text">&amp; "d:/AI&amp;SC/Clausify/backend/venv/Scripts/python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000</span><br /><br />
    <b>2. Frontend (Vite on Port 5173):</b><br />
    <span class="code-text">cd "d:/AI&amp;SC/Clausify/frontend"; node "node_modules/vite/bin/vite.js"</span><br /><br />
    <b>3. Unified Gateway (Reverse Proxy on Port 8080):</b><br />
    <span class="code-text">&amp; "d:/AI&amp;SC/Clausify/backend/venv/Scripts/python.exe" "d:/AI&amp;SC/Clausify/backend/gateway_8080.py"</span>
  </div>

  <h3>Running Test Suites:</h3>
  <div class="card-box">
    <b>Document Ingestion & Risk Scoring Suite:</b><br />
    <span class="code-text">&amp; "d:/AI&amp;SC/Clausify/backend/venv/Scripts/python.exe" "d:/AI&amp;SC/Clausify/backend/test_pipeline.py"</span><br /><br />
    <b>RAG Chat, FAQ Pre-check & Legal Notice Compilation Suite:</b><br />
    <span class="code-text">&amp; "d:/AI&amp;SC/Clausify/backend/venv/Scripts/python.exe" "d:/AI&amp;SC/Clausify/backend/test_chat_and_notice.py"</span>
  </div>

  <!-- FOOTER NOTICE -->
  <div style="margin-top: 25px; border-top: 1px solid #cbd5e1; padding-top: 8px; font-size: 8pt; color: #64748b; text-align: center;">
    <i>Report compiled autonomously by Clausify AI Engine. Retain this document for project submissions, architecture reviews, and team handoffs.</i>
  </div>

</body>
</html>
"""


def compile_pdf(html_string: str, output_path: Path):
    """Compile HTML string into a PDF file using xhtml2pdf."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_string, dest=pdf_file)
    if pisa_status.err:
        raise RuntimeError(f"xhtml2pdf encountered {pisa_status.err} errors while compiling {output_path}")
    print(f"Successfully generated PDF: {output_path} ({output_path.stat().st_size} bytes)")


def save_markdown_copy(output_path: Path):
    """Save an editable markdown version for ongoing reporting."""
    md_content = """# Clausify - Technical Architecture & 5-Phase Project Report

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
& "d:\AI&SC\Clausify\backend\venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Start Frontend (Port 5173)
cd "d:\AI&SC\Clausify\frontend"; node "node_modules/vite/bin/vite.js"

# 3. Start Gateway Proxy (Port 8080)
& "d:\AI&SC\Clausify\backend\venv\Scripts\python.exe" "d:\AI&SC\Clausify\backend\gateway_8080.py"

# 4. Run Test Suites
& "d:\AI&SC\Clausify\backend\venv\Scripts\python.exe" "d:\AI&SC\Clausify\backend\test_pipeline.py"
& "d:\AI&SC\Clausify\backend\venv\Scripts\python.exe" "d:\AI&SC\Clausify\backend\test_chat_and_notice.py"
```
"""
    output_path.write_text(md_content, encoding="utf-8")
    print(f"Successfully saved Markdown reference: {output_path}")


def main():
    print("=" * 65)
    print("COMPILING CLAUSIFY SYSTEM REPORT TO PDF & MARKDOWN")
    print("=" * 65)

    # 1. Compile project copy PDF
    compile_pdf(HTML_CONTENT, PROJECT_COPY_PDF)

    # 2. Compile user downloads copy PDF
    try:
        compile_pdf(HTML_CONTENT, DOWNLOADS_COPY_PDF)
    except Exception as exc:
        print(f"Warning: Could not save directly to Downloads ({exc}). Saving to project only.")

    # 3. Save project markdown reference
    save_markdown_copy(PROJECT_COPY_MD)

    print("\nAll deliverables compiled successfully!")


if __name__ == "__main__":
    main()
