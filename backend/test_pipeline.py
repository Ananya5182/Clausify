"""End-to-end integration test script for Clausify document ingestion, vector embedding, and Admin FAQ."""
import io
import json
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from fastapi.testclient import TestClient

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.main import app
from app.services.embedding_service import embedding_service, embed_text
from app.services.groq_service import analyze_clause_risk

client = TestClient(app)


def test_embedding_service():
    print("\n--- 1. Testing Embedding Service ---")
    query = "Can a company unilaterally change terms of service without notification?"
    vec = embed_text(query)
    assert isinstance(vec, list), "Embedding should be a list"
    assert len(vec) == 384, f"Expected 384 dimensions, got {len(vec)}"
    print(f"Embedding generated successfully. Dimensions: {len(vec)}, Sample: {vec[:3]}")


def test_groq_risk_analysis():
    print("\n--- 2. Testing Groq Clause Risk Analysis ---")
    test_clauses = [
        (
            "Forced Arbitration",
            "Any dispute shall be submitted to confidential binding arbitration. You waive any right to bring claims as a class representative or class member in any class action lawsuit."
        ),
        (
            "Unilateral Modifications",
            "We reserve the right to amend or update these terms and fee schedules at any time at our sole discretion without prior notice to you."
        ),
        (
            "Data Tracking/Selling",
            "We may collect, sell, lease, and share your personal identifiable information, location logs, and browsing behavior with third-party advertisers and commercial affiliates."
        ),
        (
            "Auto-Renewal/Non-Refundable",
            "Subscriptions will renew automatically each billing cycle indefinitely. All fees and charges are strictly non-refundable and cannot be prorated under any circumstances."
        ),
    ]

    for category, clause in test_clauses:
        res = analyze_clause_risk(clause)
        print(f"Category: {category}")
        print(f"  Risk Level: {res.get('risk_level')}")
        print(f"  Risk Score: {res.get('risk_score')}")
        print(f"  Detected Categories: {res.get('detected_categories')}")
        print(f"  Flag Reason: {res.get('flag_reason')}")
        assert res.get("risk_level") in ["HIGH", "MEDIUM"], f"Expected HIGH or MEDIUM for {category}"


def test_admin_faq_routes():
    print("\n--- 3. Testing Admin FAQ Routes ---")
    # Test POST /api/v1/admin/faq
    post_payload = {
        "question": "What is a mandatory binding arbitration clause in consumer agreements?",
        "answer": "A mandatory arbitration clause requires consumers to resolve disputes through an arbitrator rather than in a court of law, often stripping rights to trial by jury or class actions.",
        "category": "arbitration"
    }
    response = client.post("/api/v1/admin/faq", json=post_payload)
    print("POST /api/v1/admin/faq response status:", response.status_code)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    created_faq = response.json()
    print("Created FAQ id:", created_faq.get("faq", {}).get("id"))

    # Test GET /api/v1/admin/faqs
    get_response = client.get("/api/v1/admin/faqs")
    print("GET /api/v1/admin/faqs response status:", get_response.status_code)
    assert get_response.status_code == 200, f"Expected 200, got {get_response.status_code}"
    faqs = get_response.json()
    print(f"Total FAQs retrieved: {len(faqs)}")
    assert len(faqs) > 0, "Expected at least 1 FAQ"


def create_sample_pdf() -> bytes:
    """Generate a sample legal agreement PDF in-memory using reportlab."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    text = c.beginText(50, 750)
    text.setFont("Helvetica", 10)

    paragraphs = [
        "SAMPLE CONSUMER SUBSCRIPTION TERMS OF SERVICE",
        "",
        "Section 1: Service Overview",
        "The Company provides an online AI assistant platform. By registering an account, you agree to these Terms.",
        "",
        "Section 2: Mandatory Arbitration & Class Action Waiver",
        "All claims, disputes, or controversies arising out of or related to this Agreement shall be settled exclusively by individual binding arbitration administered by the American Arbitration Association, and you expressly waive your constitutional right to a jury trial and your right to participate in any class action or collective litigation.",
        "",
        "Section 3: Unilateral Changes to Terms",
        "The Company reserves the unilateral right to revise, modify, or adjust these Terms, pricing, and service tiers at any time without advance written notice. Continued use following any changes constitutes deemed acceptance of the modified Terms.",
        "",
        "Section 4: Data Monetization and Third-Party Sharing",
        "You grant the Company perpetual license to track your browsing activities and transfer, sell, or disclose your personal identifiable data, location history, and profile metrics to marketing partners and third-party advertising networks without additional consent.",
        "",
        "Section 5: Automatic Renewal and No-Refund Policy",
        "All memberships renew automatically each month at the prevailing rate without prior notice. All subscription fees and charges paid are strictly non-refundable under all circumstances, and cancellations must be made 90 days prior to the billing cycle.",
        "",
        "Section 6: General Administrative Provisions",
        "These terms shall be governed by the laws of the jurisdiction where the company is headquartered without giving effect to conflicts of law principles. If any clause is found invalid, the remaining provisions shall remain in full force.",
    ]

    for p in paragraphs:
        text.textLine(p)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()


def test_pdf_scan_route():
    print("\n--- 4. Testing PDF Upload & Scan Route ---")
    pdf_bytes = create_sample_pdf()
    files = {
        "file": ("sample_agreement.pdf", pdf_bytes, "application/pdf")
    }
    response = client.post("/api/v1/scan/upload", files=files)
    print("POST /api/v1/scan/upload response status:", response.status_code)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
    data = response.json()
    print("Document ID:", data["document"]["id"])
    print("Overall Risk Score:", data["document"]["overall_risk_score"])
    print("Total Chunks:", data["summary"]["total_chunks"])
    print("Flagged Chunks Count:", data["summary"]["flagged_chunks_count"])
    print("High Risk Count:", data["summary"]["high_risk_count"])
    print("Medium Risk Count:", data["summary"]["medium_risk_count"])
    print("\nFlagged Clauses Details:")
    for clause in data.get("flagged_clauses", []):
        print(f" - [{clause['risk_level']}] Categories: {clause.get('detected_categories')}")
        print(f"   Reason: {clause.get('flag_reason')}")
        print(f"   Score: {clause.get('risk_score')}")

    assert data["document"]["overall_risk_score"] > 50, "Expected a high overall risk score given the predatory clauses"
    assert data["summary"]["flagged_chunks_count"] > 0, "Expected at least one flagged chunk"


if __name__ == "__main__":
    print("=== Starting Clausify Ingestion and Vector Pipeline Tests ===")
    test_embedding_service()
    test_groq_risk_analysis()
    test_admin_faq_routes()
    test_pdf_scan_route()
    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")
