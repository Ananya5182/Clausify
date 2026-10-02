"""Service for compiling legal dispute notice documents into downloadable PDFs."""
import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Union
from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)

# Locate template directory relative to this service file
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def render_notice_html(context: Dict[str, Any]) -> str:
    """Render the legal notice Jinja2 template with provided data context."""
    ctx = dict(context)

    # Supply default date if not provided
    if not ctx.get("notice_date"):
        ctx["notice_date"] = datetime.now().strftime("%B %d, %Y")

    # Format legal statutes if string or list
    statutes = ctx.get("legal_statutes")
    if isinstance(statutes, str):
        # If passed as a comma-separated or newline-separated string, convert or keep
        if "\n" in statutes:
            ctx["legal_statutes"] = [s.strip() for s in statutes.split("\n") if s.strip()]
        elif ";" in statutes:
            ctx["legal_statutes"] = [s.strip() for s in statutes.split(";") if s.strip()]

    template = jinja_env.get_template("legal_notice.html")
    return template.render(**ctx)


def generate_legal_notice_pdf(context: Dict[str, Any]) -> bytes:
    """Compile legal dispute notice into in-memory PDF bytes using xhtml2pdf without external C dependencies.

    Args:
        context: Dictionary containing dispute notice parameters:
            - complainant_name: str
            - company_name: str
            - incident_date: str
            - transaction_id: str
            - disputed_amount: str
            - issue_summary: str
            - legal_statutes: Union[str, List[str]]
            - notice_date: Optional[str]
            - complainant_email: Optional[str]
            - complainant_address: Optional[str]

    Returns:
        bytes of the generated PDF document.
    """
    html_content = render_notice_html(context)

    html_bytes = html_content.encode("utf-8")
    pdf_stream = io.BytesIO()
    pisa_status = pisa.pisaDocument(
        src=io.BytesIO(html_bytes),
        dest=pdf_stream,
        encoding="utf-8",
    )

    if pisa_status.err:
        logger.error(f"xhtml2pdf encountered errors during PDF compilation: {pisa_status.err}")
        raise RuntimeError(f"xhtml2pdf failed to compile PDF: {pisa_status.err}")

    pdf_bytes = pdf_stream.getvalue()
    if not pdf_bytes:
        raise RuntimeError("PDF generation produced empty byte payload.")

    return pdf_bytes
