"""Admin API routes for managing legal FAQs and vector embeddings in Supabase."""
import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.core.supabase_client import supabase_client
from app.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


class FAQCreateRequest(BaseModel):
    """Payload schema for creating a new FAQ entry."""
    question: str = Field(..., min_length=3, description="The legal question or consumer query")
    answer: str = Field(..., min_length=3, description="The corresponding answer or explanation")
    category: str = Field(default="general", description="FAQ categorization (e.g., privacy, arbitration, billing)")


class FAQResponse(BaseModel):
    """Response schema for an FAQ record."""
    id: str
    question: str
    answer: str
    category: str
    created_at: Optional[str] = None


@router.post("/faq", status_code=status.HTTP_201_CREATED, summary="Create and embed a new FAQ")
async def create_faq(payload: FAQCreateRequest) -> Dict[str, Any]:
    """Embed the question using sentence-transformers and insert into Supabase `faqs` table."""
    try:
        # Generate 384-dimensional normalized vector embedding for the question
        embedding = embedding_service.embed_text(payload.question)

        record = {
            "question": payload.question.strip(),
            "answer": payload.answer.strip(),
            "category": payload.category.strip() or "general",
            "embedding": embedding,
        }

        result = supabase_client.table("faqs").insert(record).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to insert FAQ record into database.",
            )

        created_faq = result.data[0]
        return {
            "status": "success",
            "message": "FAQ successfully created and embedded",
            "faq": created_faq,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(f"Error creating FAQ: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating FAQ: {str(exc)}",
        )


@router.get("/faqs", summary="Retrieve all stored FAQs")
async def get_all_faqs() -> List[Dict[str, Any]]:
    """Retrieve all stored FAQs ordered by creation date descending."""
    try:
        # Select all FAQ fields
        result = (
            supabase_client.table("faqs")
            .select("id, question, answer, category, created_at")
            .order("created_at", desc=True)
            .execute()
        )
        return result.data or []
    except Exception as exc:
        logger.error(f"Error retrieving FAQs: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching FAQs: {str(exc)}",
        )
