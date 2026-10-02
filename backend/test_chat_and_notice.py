"""Comprehensive test suite for interactive RAG chat engine, FAQ pre-check,
slot extraction, and PDF legal notice compilation.
"""
import io
import sys
from fastapi.testclient import TestClient

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.main import app
from app.services.pdf_service import generate_legal_notice_pdf, render_notice_html
from app.core.supabase_client import supabase_client

client = TestClient(app)


def test_pdf_template_and_compilation():
    print("\n--- 1. Testing PDF Template & Compilation Service ---", flush=True)
    sample_context = {
        "complainant_name": "Marcus Vance",
        "company_name": "CloudStream Digital Inc.",
        "incident_date": "September 18, 2026",
        "transaction_id": "TXN-998812-CS",
        "disputed_amount": "$189.99",
        "issue_summary": "Consumer canceled subscription on Sept 1, but Respondent initiated recurring charge of $189.99 without authorization and refused refund based on unilateral non-refundable terms.",
        "legal_statutes": [
            "Consumer Protection Act 2019, Section 2(47) (Unfair Trade Practice)",
            "Uniform Commercial Code Article 2-302 (Unconscionable Contract or Clause)",
            "Electronic Funds Transfer Act (EFTA), 15 U.S.C. 1693e"
        ],
        "complainant_email": "marcus.vance@example.com",
    }

    # Test Jinja2 HTML rendering
    html = render_notice_html(sample_context)
    assert "CloudStream Digital Inc." in html
    assert "TXN-998812-CS" in html
    assert "$189.99" in html
    assert "Unfair Trade Practice" in html
    print("  -> Jinja2 HTML rendered successfully with all required fields.")

    # Test xhtml2pdf compilation to PDF bytes
    pdf_bytes = generate_legal_notice_pdf(sample_context)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF-")
    print(f"  -> xhtml2pdf compiled {len(pdf_bytes)} bytes of valid PDF data.")


def test_notice_generation_api():
    print("\n--- 2. Testing POST /api/v1/notice/generate API Endpoint ---", flush=True)
    payload = {
        "complainant_name": "Sarah Connor",
        "company_name": "Cyberdyne Logistics",
        "incident_date": "2026-09-20",
        "transaction_id": "ORD-554433-CY",
        "disputed_amount": "$350.00",
        "issue_summary": "Delivery never completed; company unilaterally modified terms to deny refund.",
        "legal_statutes": [
            "Section 5 Federal Trade Commission Act (Deceptive Acts)",
            "Consumer Rights Directive Article 9 (Right of Withdrawal)"
        ],
        "complainant_email": "sarah.connor@example.com",
    }

    response = client.post("/api/v1/notice/generate", json=payload)
    print("  -> POST /api/v1/notice/generate status:", response.status_code, flush=True)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.headers.get("content-type") == "application/pdf"
    assert 'attachment; filename="Legal_Notice.pdf"' in response.headers.get("content-disposition", "")
    assert len(response.content) > 2000
    assert response.content.startswith(b"%PDF-")
    print("  -> Streaming PDF response verified with correct Content-Disposition headers.")


def test_chat_step_a_faq_precheck():
    print("\n--- 3. Testing Chat Step A: FAQ Pre-check with Similarity Threshold ---", flush=True)
    # Query an existing FAQ in Supabase
    faq_query = "What is a mandatory binding arbitration clause in consumer agreements?"
    payload = {
        "session_id": "test-session-faq",
        "message": faq_query,
    }

    response = client.post("/api/v1/chat", json=payload)
    print("  -> POST /api/v1/chat status:", response.status_code, flush=True)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    print("  -> Chat Source:", data.get("source"))
    print("  -> FAQ Match:", data.get("faq_match"))
    print("  -> Response preview:", data.get("response")[:120], "...")

    assert data.get("source") == "faq", f"Expected source 'faq', got {data.get('source')}"
    assert data.get("faq_match") is not None
    assert data["faq_match"]["similarity"] >= 0.82
    print("  -> FAQ pre-check correctly matched and returned system FAQ answer immediately.")


def test_chat_step_b_c_d_rag_and_slot_extraction():
    print("\n--- 4. Testing Chat Steps B, C & D: RAG Grounding & Slot Extraction ---", flush=True)

    # 1. Fetch an existing document ID from Supabase
    docs = supabase_client.table("documents").select("id, file_name").limit(1).execute()
    doc_id = docs.data[0]["id"] if docs.data else None
    print(f"  -> Using test document doc_id: {doc_id}")

    # 2. Test conversational grievance with slots
    grievance_message = (
        "I need help drafting a dispute notice. Apex Fitness LLC charged my card $79.99 on 2026-09-14 "
        "under order TXN-882211 even though I gave cancellation notice 30 days prior. They claim their "
        "terms have a non-refundable clause and refused my refund."
    )

    payload = {
        "session_id": "test-session-grievance",
        "message": grievance_message,
        "doc_id": doc_id,
        "history": [
            {"role": "user", "content": "Hello, I have an issue with a company refusing to refund me."},
            {"role": "assistant", "content": "Hello! I can help you analyze your agreement or draft a formal legal dispute notice. Could you provide details about the merchant and charge?"}
        ]
    }

    response = client.post("/api/v1/chat", json=payload)
    print("  -> POST /api/v1/chat status:", response.status_code, flush=True)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()

    print("  -> Source:", data.get("source"))
    print("  -> Context snippets retrieved:", len(data.get("context_snippets", [])))
    print("  -> Grievance Detected:", data.get("grievance_detected"))
    print("  -> Extracted Slots:", data.get("slots"))
    print("  -> Notice Ready:", data.get("notice_ready"))
    print("  -> Assistant Response:\n", data.get("response")[:250], "...")

    assert data.get("grievance_detected") is True, "Grievance should be detected"
    slots = data.get("slots", {})
    assert slots.get("company_name") is not None
    assert "Apex Fitness" in (slots.get("company_name") or "")
    assert slots.get("disputed_amount") is not None
    assert "79.99" in (slots.get("disputed_amount") or "")
    assert slots.get("transaction_id") is not None
    assert "882211" in (slots.get("transaction_id") or "")
    assert data.get("notice_ready") is True, "Notice should be marked ready"
    print("  -> RAG Grounding & Conversational Slot Extraction passed successfully!")


if __name__ == "__main__":
    print("==================================================================")
    print("STARTING CLAUSIFY CHAT & LEGAL NOTICE INTEGRATION TEST SUITE")
    print("==================================================================")
    test_pdf_template_and_compilation()
    test_notice_generation_api()
    test_chat_step_a_faq_precheck()
    test_chat_step_b_c_d_rag_and_slot_extraction()
    print("\n==================================================================")
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("==================================================================")
