"""Document scan and ingestion API routes."""
import io
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.supabase_client import supabase_client
from app.services.embedding_service import embedding_service
from app.services.groq_service import analyze_clause_risk

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/scan", tags=["Scan"])

# Keywords commonly indicating high/medium consumer risk clauses
RISK_KEYWORDS = [
    "arbitrat", "dispute", "class action", "jury", "waiver", "tribunal",
    "modify", "modification", "amend", "sole discretion", "unilateral", "without notice",
    "personal data", "sell", "share", "third party", "tracking", "cookies", "advertising", "biometric",
    "auto-renew", "automatic renewal", "recurring", "cancel", "non-refundable", "no refund", "forfeit",
    "indemnif", "liability", "warranty", "governing law", "termination"
]


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract raw textual content from an uploaded PDF file using PyPDF."""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The provided PDF is encrypted or password-protected.",
                )

        extracted_pages: List[str] = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text and page_text.strip():
                extracted_pages.append(page_text.strip())

        full_text = "\n\n".join(extracted_pages).strip()
        if not full_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No readable text could be extracted from this PDF. It may be scanned or empty.",
            )
        return full_text
    except PdfReadError as exc:
        logger.error(f"PyPDF read error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid or corrupt PDF document: {str(exc)}",
        )


def split_into_chunks(text: str, chunk_size_tokens: int = 500, overlap_tokens: int = 50) -> List[str]:
    """Split text into ~500-token chunks with 50-token overlap.

    Standard NLP token approximation: 1 token ≈ 0.75 words.
    500 tokens ≈ 375 words, 50 tokens ≈ 38 words.
    """
    words = text.split()
    if not words:
        return []

    words_per_chunk = max(20, int(chunk_size_tokens * 0.75))
    overlap_words = max(5, int(overlap_tokens * 0.75))
    step = max(1, words_per_chunk - overlap_words)

    chunks: List[str] = []
    for i in range(0, len(words), step):
        chunk_words = words[i : i + words_per_chunk]
        chunk_text = " ".join(chunk_words).strip()
        if chunk_text:
            chunks.append(chunk_text)
        if i + words_per_chunk >= len(words):
            break

    return chunks


def is_candidate_chunk(chunk_text: str, total_chunks: int) -> bool:
    """Determine whether a chunk should undergo deep LLM clause risk analysis."""
    # If the document has 10 or fewer chunks, analyze every chunk
    if total_chunks <= 10:
        return True

    # Otherwise, check for presence of consumer risk trigger keywords
    lowered = chunk_text.lower()
    return any(keyword in lowered for keyword in RISK_KEYWORDS)


def compute_overall_risk_score(analyses: List[Dict[str, Any]]) -> int:
    """Compute aggregate risk score (0-100) from chunk analyses."""
    scores = [a.get("risk_score", 0) for a in analyses if isinstance(a.get("risk_score"), (int, float))]
    if not scores or max(scores) == 0:
        return 0

    max_score = max(scores)
    flagged_scores = [s for s in scores if s >= 40]

    if not flagged_scores:
        # Only minor flags
        return max(0, min(100, int(max_score * 0.6)))

    # Weighted blend prioritizing maximum severity while factoring in breadth of issues
    avg_flagged = sum(flagged_scores) / len(flagged_scores)
    aggregate = (max_score * 0.75) + (avg_flagged * 0.25)
    return max(0, min(100, int(round(aggregate))))


@router.post("/upload", status_code=status.HTTP_201_CREATED, summary="Ingest PDF, embed chunks, and analyze risk")
async def scan_pdf_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload a PDF agreement, chunk it into ~500 tokens with 50-token overlap,

    generate vector embeddings, store records in Supabase, and evaluate clause risks.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a PDF (.pdf) file.",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF file is empty.",
        )

    # Step 1: Extract text using PyPDF
    extracted_text = extract_text_from_pdf(file_bytes)

    # Step 2: Split into ~500-token chunks with 50-token overlap
    chunks = split_into_chunks(extracted_text, chunk_size_tokens=500, overlap_tokens=50)
    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid text chunks could be generated from the document.",
        )

    total_chunks = len(chunks)
    logger.info(f"Extracted {total_chunks} chunks from '{file.filename}'")

    # Step 3: Create initial document record in Supabase
    doc_insert = {
        "file_name": file.filename,
        "overall_risk_score": 0,
    }
    try:
        doc_res = supabase_client.table("documents").insert(doc_insert).execute()
        if not doc_res.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create document record in Supabase.",
            )
        document_record = doc_res.data[0]
        document_id = document_record["id"]
    except Exception as exc:
        logger.error(f"Error creating document in Supabase: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error creating document record: {str(exc)}",
        )

    # Step 4: Generate vector embeddings for all chunks
    try:
        embeddings = embedding_service.embed_batch(chunks)
    except Exception as exc:
        logger.error(f"Error generating embeddings: {exc}", exc_info=True)
        # Fallback to single text embeddings if batch fails
        embeddings = [embedding_service.embed_text(c) for c in chunks]

    # Step 5: Run clause risk analysis on candidate chunks
    chunk_analyses: List[Dict[str, Any]] = []
    for idx, chunk in enumerate(chunks):
        if is_candidate_chunk(chunk, total_chunks):
            try:
                analysis = analyze_clause_risk(chunk)
            except Exception as exc:
                logger.warning(f"Error analyzing chunk {idx}: {exc}")
                analysis = {
                    "risk_level": "LOW",
                    "risk_score": 10,
                    "detected_categories": [],
                    "flag_reason": "Analysis could not be completed for this clause.",
                    "summary": chunk[:150],
                }
        else:
            analysis = {
                "risk_level": "NONE",
                "risk_score": 0,
                "detected_categories": [],
                "flag_reason": None,
                "summary": "Standard operational or administrative provision.",
            }
        chunk_analyses.append(analysis)

    # Step 6: Compute overall risk score and update document record
    overall_risk_score = compute_overall_risk_score(chunk_analyses)

    try:
        supabase_client.table("documents").update(
            {"overall_risk_score": overall_risk_score}
        ).eq("id", document_id).execute()
    except Exception as exc:
        logger.error(f"Error updating document overall_risk_score: {exc}", exc_info=True)

    # Step 7: Bulk-upsert chunks into Supabase `document_chunks`
    chunk_records = []
    for idx, chunk in enumerate(chunks):
        analysis = chunk_analyses[idx]
        chunk_records.append({
            "document_id": document_id,
            "chunk_text": chunk,
            "risk_level": analysis.get("risk_level", "NONE"),
            "flag_reason": analysis.get("flag_reason") or None,
            "embedding": embeddings[idx],
        })

    # Bulk insert/upsert in batches of 25 to respect network payload thresholds
    batch_size = 25
    try:
        for i in range(0, len(chunk_records), batch_size):
            batch = chunk_records[i : i + batch_size]
            supabase_client.table("document_chunks").upsert(batch).execute()
    except Exception as exc:
        logger.error(f"Error bulk-upserting document_chunks: {exc}", exc_info=True)
        # Attempt fallback standard insert if upsert had conflict
        try:
            for i in range(0, len(chunk_records), batch_size):
                batch = chunk_records[i : i + batch_size]
                supabase_client.table("document_chunks").insert(batch).execute()
        except Exception as inner_exc:
            logger.error(f"Secondary insert attempt also failed: {inner_exc}", exc_info=True)

    # Step 8: Assemble and return aggregated JSON payload
    flagged_clauses = [
        {
            "chunk_index": idx,
            "risk_level": a.get("risk_level", "NONE"),
            "risk_score": a.get("risk_score", 0),
            "detected_categories": a.get("detected_categories", []),
            "flag_reason": a.get("flag_reason"),
            "summary": a.get("summary"),
            "clause_preview": chunks[idx][:300] + ("..." if len(chunks[idx]) > 300 else ""),
        }
        for idx, a in enumerate(chunk_analyses)
        if a.get("risk_level") in ("HIGH", "MEDIUM")
    ]

    return {
        "status": "success",
        "document": {
            "id": document_id,
            "file_name": file.filename,
            "overall_risk_score": overall_risk_score,
            "created_at": document_record.get("created_at"),
        },
        "summary": {
            "total_chunks": total_chunks,
            "flagged_chunks_count": len(flagged_clauses),
            "high_risk_count": len([c for c in flagged_clauses if c["risk_level"] == "HIGH"]),
            "medium_risk_count": len([c for c in flagged_clauses if c["risk_level"] == "MEDIUM"]),
            "overall_risk_score": overall_risk_score,
        },
        "flagged_clauses": flagged_clauses,
        "chunks": [
            {
                "chunk_index": idx,
                "risk_level": a.get("risk_level", "NONE"),
                "risk_score": a.get("risk_score", 0),
                "detected_categories": a.get("detected_categories", []),
                "flag_reason": a.get("flag_reason"),
                "preview": chunks[idx][:180] + ("..." if len(chunks[idx]) > 180 else ""),
            }
            for idx, a in enumerate(chunk_analyses)
        ],
    }
