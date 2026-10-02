"""API router for generating and downloading compiled legal dispute notices."""
import io
import logging
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.pdf_service import generate_legal_notice_pdf

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/notice", tags=["Legal Notice"])


class NoticeGenerateRequest(BaseModel):
    """Payload schema for generating a formal legal dispute notice."""
    complainant_name: str = Field(..., min_length=1, description="Full name of the aggrieved complainant")
    company_name: str = Field(..., min_length=1, description="Respondent company or service provider name")
    incident_date: str = Field(..., min_length=1, description="Date of dispute or transaction occurrence")
    transaction_id: str = Field(..., min_length=1, description="Reference order or transaction ID")
    disputed_amount: str = Field(..., min_length=1, description="Disputed amount with currency (e.g. ₹14,500 or Rs. 2,499)")
    issue_summary: str = Field(..., min_length=5, description="Clear factual summary of the grievance")
    legal_statutes: Union[List[str], str] = Field(
        ...,
        description="Statutes, consumer rights acts, or contractual provisions violated"
    )
    notice_date: Optional[str] = Field(
        default=None,
        description="Optional date for notice issue (defaults to current date if omitted)"
    )
    complainant_email: Optional[str] = Field(default=None, description="Optional complainant email contact")
    complainant_address: Optional[str] = Field(default=None, description="Optional complainant physical address")


@router.post(
    "/generate",
    response_class=StreamingResponse,
    summary="Compile and download a formal legal notice PDF",
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "Returns compiled binary PDF stream attachment.",
        }
    },
)
async def generate_notice(payload: NoticeGenerateRequest):
    """Accept dispute parameters, render legal notice Jinja2 template, and stream compiled PDF."""
    try:
        pdf_bytes = generate_legal_notice_pdf(payload.model_dump())
    except Exception as exc:
        logger.error(f"Error compiling legal notice PDF: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate legal notice document: {str(exc)}",
        )

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="Legal_Notice.pdf"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )
