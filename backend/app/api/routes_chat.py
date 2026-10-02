"""Interactive RAG chat engine with FAQ pre-check, context grounding, and slot extraction."""
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.groq_client import groq_client
from app.core.supabase_client import supabase_client
from app.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chat", tags=["Chat"])

# Priority list of Groq models to execute
CHAT_MODELS_TO_TRY = [
    getattr(settings, "GROQ_REASONING_MODEL", "openai/gpt-oss-120b"),
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "llama-3.3-70b-versatile",
]

CHAT_SYSTEM_PROMPT = """You are Clausify's AI Legal Counsel and Consumer Rights Assistant.
You assist consumers in reviewing agreements, understanding unfair clauses, evaluating disputes, and drafting formal legal dispute notices.

STRICT GROUNDING & ANTI-HALLUCINATION RULES:
1. When contract context snippets are provided, you MUST ground your analysis strictly on them.
2. If the user asks about specific clauses, rights, or contract provisions and the information is NOT present in the provided context snippets, you MUST explicitly state that the provided document excerpts do not mention or address that topic. Do NOT assume, fabricate, or hallucinate terms.
3. Cite the exact clause or wording from the excerpts whenever referring to contract terms.
4. Provide helpful, legally sound guidance under consumer protection principles.

CONVERSATIONAL SLOT EXTRACTION & GRIEVANCE INTENT:
1. Detect whether the user is expressing a consumer dispute, grievance, wrongful charge, service deficiency, breach, or requesting a formal legal notice.
2. Extract the following 5 slot entities if mentioned in the message or conversational history:
   - company_name: Name of the company/merchant (or null if not found)
   - transaction_id: Order number, transaction ID, reference ID (or null if not found)
   - incident_date: Date of dispute, charge, or incident (or null if not found)
   - disputed_amount: Currency and amount involved, e.g. "₹2,500", "Rs 1,499", or "₹14,500" (or null if not found)
   - issue_summary: Concise 1-2 sentence factual summary of the consumer grievance (or null if no grievance)
3. If the user is expressing a grievance, politely acknowledge the dispute in your response, indicate what details you have noted, and if any key slots (company_name, transaction_id, incident_date, disputed_amount) are still missing, invite them to provide them so a formal legal notice can be generated.

OUTPUT FORMAT:
You MUST respond ONLY with a valid JSON object adhering to this schema:
{
  "response": "<Your conversational answer to the user>",
  "grievance_detected": <true or false>,
  "slots": {
    "company_name": <string or null>,
    "transaction_id": <string or null>,
    "incident_date": <string or null>,
    "disputed_amount": <string or null>,
    "issue_summary": <string or null>
  }
}
"""


class ChatRequest(BaseModel):
    """Payload schema for conversational RAG chat."""
    session_id: Optional[str] = Field(default=None, description="Optional conversational session ID")
    message: str = Field(..., min_length=1, description="User question or grievance description")
    doc_id: Optional[str] = Field(default=None, description="Optional UUID of scanned agreement document")
    history: Optional[List[Dict[str, Any]]] = Field(
        default_factory=list,
        description="Prior conversational turns: [{'role': 'user'|'assistant', 'content': '...'}]"
    )


class SlotEntities(BaseModel):
    """Extracted consumer grievance slot entities."""
    company_name: Optional[str] = None
    transaction_id: Optional[str] = None
    incident_date: Optional[str] = None
    disputed_amount: Optional[str] = None
    issue_summary: Optional[str] = None


class ContextSnippet(BaseModel):
    """Retrieved document context chunk snippet."""
    id: Optional[str] = None
    chunk_text: str
    risk_level: Optional[str] = None
    similarity: Optional[float] = None


class FAQMatchDetails(BaseModel):
    """Matched FAQ entry from Supabase knowledge base."""
    id: Optional[str] = None
    question: str
    answer: str
    category: Optional[str] = None
    similarity: float


class ChatResponse(BaseModel):
    """Structured response schema for chat engine."""
    session_id: Optional[str] = None
    response: str
    source: str = Field(..., description="Response origin: 'faq', 'rag', or 'direct'")
    faq_match: Optional[FAQMatchDetails] = None
    context_snippets: List[ContextSnippet] = Field(default_factory=list)
    grievance_detected: bool = False
    slots: SlotEntities = Field(default_factory=SlotEntities)
    notice_ready: bool = False


def call_groq_chat(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Call Groq API with model fallback handling and JSON response parsing."""
    last_error: Optional[Exception] = None

    for model in CHAT_MODELS_TO_TRY:
        try:
            res = groq_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            raw_content = res.choices[0].message.content or "{}"
            parsed = json.loads(raw_content)
            return parsed
        except Exception as exc:
            logger.warning(f"Groq chat attempt failed with model {model}: {exc}")
            last_error = exc
            continue

    logger.error(f"All Groq models failed for chat completion: {last_error}")
    # Return basic fallback payload
    return {
        "response": "I encountered a temporary service issue analyzing your request. Please try again shortly.",
        "grievance_detected": False,
        "slots": {
            "company_name": None,
            "transaction_id": None,
            "incident_date": None,
            "disputed_amount": None,
            "issue_summary": None,
        },
    }


@router.post("", response_model=ChatResponse, summary="Interactive RAG chat, FAQ check, and slot extraction")
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """Execute end-to-end chat pipeline:

    - Step A: Embed message, query Supabase FAQs via match_faqs. If similarity > 0.82, return system FAQ answer immediately.
    - Step B: If doc_id supplied, query match_document_chunks for grounded context snippets.
    - Step C: Call Groq llama-3.3-70b-versatile with history and strict anti-hallucination grounding.
    - Step D: Detect grievance intent and extract slot entities: [company_name, transaction_id, incident_date, disputed_amount, issue_summary].
    """
    clean_message = payload.message.strip()
    if not clean_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty.",
        )

    # ---------------------------------------------------------
    # Step A: Vector Embed message and Pre-check FAQ Knowledge Base
    # ---------------------------------------------------------
    try:
        query_embedding = embedding_service.embed_text(clean_message)
    except Exception as exc:
        logger.error(f"Error generating query embedding: {exc}", exc_info=True)
        query_embedding = [0.0] * 384

    try:
        faq_res = supabase_client.rpc(
            "match_faqs",
            {
                "query_embedding": query_embedding,
                "match_threshold": 0.82,
                "match_count": 1,
            },
        ).execute()

        if faq_res.data and len(faq_res.data) > 0:
            top_faq = faq_res.data[0]
            raw_sim = top_faq.get("similarity")
            try:
                sim_float = float(raw_sim) if raw_sim is not None else 0.0
            except (ValueError, TypeError):
                sim_float = 0.0

            if sim_float > 0.82:
                # High confidence FAQ match found - return answer immediately
                return ChatResponse(
                    session_id=payload.session_id,
                    response=top_faq.get("answer", ""),
                    source="faq",
                    faq_match=FAQMatchDetails(
                        id=top_faq.get("id"),
                        question=top_faq.get("question", ""),
                        answer=top_faq.get("answer", ""),
                        category=top_faq.get("category"),
                        similarity=sim_float,
                    ),
                    context_snippets=[],
                    grievance_detected=False,
                    slots=SlotEntities(),
                    notice_ready=False,
                )
    except Exception as exc:
        logger.warning(f"FAQ pre-check query encountered error (continuing to RAG): {exc}")

    # ---------------------------------------------------------
    # Step B: Document Chunk RAG Retrieval (if doc_id supplied)
    # ---------------------------------------------------------
    context_snippets: List[ContextSnippet] = []
    rag_context_text = ""

    if payload.doc_id and payload.doc_id.strip():
        clean_doc_id = payload.doc_id.strip()
        try:
            chunks_res = supabase_client.rpc(
                "match_document_chunks",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": 0.05,
                    "match_count": 4,
                    "filter_doc_id": clean_doc_id,
                },
            ).execute()

            if chunks_res.data:
                for idx, c in enumerate(chunks_res.data):
                    raw_sim = c.get("similarity")
                    try:
                        sim_val = float(raw_sim) if raw_sim is not None else None
                    except (ValueError, TypeError):
                        sim_val = None

                    snippet = ContextSnippet(
                        id=c.get("id"),
                        chunk_text=c.get("chunk_text", ""),
                        risk_level=c.get("risk_level"),
                        similarity=sim_val,
                    )
                    context_snippets.append(snippet)

                rag_context_text = "\n\n".join(
                    f"[Document Clause {i+1} | Risk Level: {s.risk_level or 'NONE'}]:\n\"{s.chunk_text}\""
                    for i, s in enumerate(context_snippets)
                )
        except Exception as exc:
            logger.error(f"Error matching document chunks for doc_id {clean_doc_id}: {exc}", exc_info=True)

    # ---------------------------------------------------------
    # Step C & D: Groq Reasoning, History, and Slot Extraction
    # ---------------------------------------------------------
    prompt_messages: List[Dict[str, str]] = [
        {"role": "system", "content": CHAT_SYSTEM_PROMPT}
    ]

    # Append RAG context as system grounding if available
    if rag_context_text:
        grounding_content = (
            f"RELEVANT DOCUMENT EXCERPTS (Doc ID: {payload.doc_id}):\n\n"
            f"{rag_context_text}\n\n"
            "Ground your answer strictly on these excerpts if the user is asking about the agreement. "
            "Cite exact phrases. If the user's question is not addressed in these excerpts, explicitly state so."
        )
        prompt_messages.append({"role": "system", "content": grounding_content})

    # Append prior conversation history
    if payload.history:
        for turn in payload.history:
            role = turn.get("role")
            content = turn.get("content")
            if role in ("user", "assistant") and content:
                prompt_messages.append({"role": role, "content": str(content)})

    # Append current user query
    prompt_messages.append({"role": "user", "content": clean_message})

    # Execute Groq call
    llm_result = call_groq_chat(prompt_messages)

    response_text = str(llm_result.get("response", "")).strip()
    grievance_detected = bool(llm_result.get("grievance_detected", False))
    raw_slots = llm_result.get("slots", {})
    if not isinstance(raw_slots, dict):
        raw_slots = {}

    slots = SlotEntities(
        company_name=raw_slots.get("company_name") or None,
        transaction_id=raw_slots.get("transaction_id") or None,
        incident_date=raw_slots.get("incident_date") or None,
        disputed_amount=raw_slots.get("disputed_amount") or None,
        issue_summary=raw_slots.get("issue_summary") or None,
    )

    # Notice is ready if grievance detected and primary slots are populated
    notice_ready = bool(
        grievance_detected
        and slots.company_name
        and (slots.disputed_amount or slots.issue_summary)
    )

    source = "rag" if context_snippets else "direct"

    return ChatResponse(
        session_id=payload.session_id,
        response=response_text,
        source=source,
        faq_match=None,
        context_snippets=context_snippets,
        grievance_detected=grievance_detected,
        slots=slots,
        notice_ready=notice_ready,
    )
