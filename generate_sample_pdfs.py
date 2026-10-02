"""Generate 3 realistic sample legal agreements for Clausify testing:
1. High Risk StreamPlay Subscription (Critical clauses, arbitration, unilateral change, data selling)
2. Moderate Risk CloudVault Terms (Standard auto-renew, notice-based change, limited liability)
3. Safe FairDocs Consumer Agreement (Fair consumer terms, pro-rata refund, no waivers, zero data selling)
"""
import os
import sys
from pathlib import Path
from xhtml2pdf import pisa

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "sample_agreements"
PUBLIC_DIR = BASE_DIR / "frontend" / "public" / "samples"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {
    size: a4 portrait;
    margin: 2.2cm 2cm 2.2cm 2cm;
    @bottom-center {
      content: "Page " counter(page) " of " counter(pages);
      font-size: 8pt;
      color: #64748b;
    }
  }
  body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.5;
    color: #1e293b;
  }
  .header {
    border-bottom: 2px solid {{ primary_color }};
    padding-bottom: 12px;
    margin-bottom: 20px;
  }
  .company {
    font-size: 16pt;
    font-weight: bold;
    color: {{ primary_color }};
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .doc-title {
    font-size: 12pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 4px;
  }
  .meta {
    font-size: 8pt;
    color: #64748b;
    margin-top: 4px;
  }
  .badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 7.5pt;
    font-weight: bold;
    color: #ffffff;
    background-color: {{ badge_color }};
    border-radius: 4px;
    text-transform: uppercase;
    margin-top: 6px;
  }
  h2 {
    font-size: 10.5pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 14px;
    margin-bottom: 6px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 3px;
  }
  p {
    margin-bottom: 8px;
    text-align: justify;
  }
  .highlight-clause {
    background-color: {{ clause_bg }};
    border-left: 3px solid {{ primary_color }};
    padding: 6px 10px;
    margin: 8px 0;
    font-size: 9pt;
  }
  .footer-note {
    margin-top: 24px;
    padding-top: 10px;
    border-top: 1px dashed #cbd5e1;
    font-size: 8pt;
    color: #64748b;
    font-style: italic;
  }
</style>
</head>
<body>

<div class="header">
  <div class="company">{{ company_name }}</div>
  <div class="doc-title">{{ title }}</div>
  <div class="meta">Effective Date: October 01, 2025 | Document Version: 4.2 | Jurisdiction: Global</div>
  <div class="badge">{{ risk_tier }} Sample Document</div>
</div>

<p>This Agreement governs the relationship, rights, liabilities, and statutory obligations between the Subscriber ("User") and {{ company_name }} ("Company"). By clicking "Accept", accessing, subscribing, or using any associated software platforms, digital services, or streaming media, the user unequivocally assents to be bound by the clauses detailed herein.</p>

<h2>Section 1: Service Eligibility & Scope of License</h2>
<p>The Company provides digital platform services subject to strict compliance with these provisions. The license granted is personal, revocable, non-exclusive, and strictly limited to non-commercial consumption. Any unauthorized reverse engineering, modification, or sharing of user credentials constitutes an immediate material breach.</p>

<h2>Section 2: {{ clause_2_title }}</h2>
<div class="highlight-clause">
  {{ clause_2_text }}
</div>

<h2>Section 3: {{ clause_3_title }}</h2>
<div class="highlight-clause">
  {{ clause_3_text }}
</div>

<h2>Section 4: {{ clause_4_title }}</h2>
<div class="highlight-clause">
  {{ clause_4_text }}
</div>

<h2>Section 5: {{ clause_5_title }}</h2>
<div class="highlight-clause">
  {{ clause_5_text }}
</div>

<h2>Section 6: {{ clause_6_title }}</h2>
<div class="highlight-clause">
  {{ clause_6_text }}
</div>

<h2>Section 7: Severability & Entire Agreement</h2>
<p>If any clause of this Agreement is held to be invalid or unenforceable by a tribunal of competent jurisdiction, such provision shall be severed and the remaining covenants shall continue in full legal force. This document constitutes the sole agreement between the parties superseding all prior verbal or written understandings.</p>

<div class="footer-note">
  Formal notice of dispute or statutory grievance communications must be transmitted to: legal@{{ company_slug }}.com | Clausify Evaluation Benchmark Document.
</div>

</body>
</html>
"""

DOCUMENTS = [
    {
        "filename": "Sample1_High_Risk_StreamPlay_Subscription.pdf",
        "company_name": "StreamPlay Global Media Inc.",
        "company_slug": "streamplay",
        "title": "Universal End-User Subscription & Terms of Service",
        "risk_tier": "CRITICAL RISK (Expected Score: 80-95)",
        "primary_color": "#dc2626", # red
        "badge_color": "#ef4444",
        "clause_bg": "#fef2f2",
        "clause_2_title": "Dispute Resolution, Mandatory Arbitration & Class Action Waiver",
        "clause_2_text": "Any dispute, claim, controversy, or statutory grievance arising out of or relating to this Agreement or the Services shall be settled exclusively through confidential, binding arbitration administered by a private arbitrator chosen in the sole discretion of StreamPlay. The user hereby expressly and irrevocably waives any and all rights to initiate, join, participate in, or seek legal remedy through a class action, collective lawsuit, private attorney general action, or jury trial in any court of law or consumer tribunal.",
        "clause_3_title": "Unilateral Modifications Without Prior Notice",
        "clause_3_text": "StreamPlay reserves the absolute and unilateral right, at its sole discretion, to modify, amend, update, alter, or terminate any terms, features, pricing schedules, subscription fees, or service availability at any time without prior written notice or warning to the subscriber. Continued access or payment following any unilateral modification constitutes full, irrevocable acceptance of the updated terms.",
        "clause_4_title": "Recurring Auto-Renewal, No Refunds & Forfeiture of Balance",
        "clause_4_text": "All memberships automatically renew on an ongoing recurring billing schedule without requirement of advance reminder notice. All billing charges, monthly subscription fees, and prepaid balances are strictly non-refundable and forfeit in their entirety upon cancellation. Under no circumstance shall StreamPlay provide prorated refunds, chargeback acquiescence, or credits for partial billing periods.",
        "clause_5_title": "Data Monetization, Tracking & Third-Party Selling",
        "clause_5_text": "Subscriber grants StreamPlay an unrestricted, perpetual license to collect, store, sell, disclose, and commercially share personal data, behavioral telemetry, location history, cookies, cross-site tracking IDs, and biometric data with affiliated advertising networks, data brokers, and marketing entities for programmatic advertising and automated profiling.",
        "clause_6_title": "Total Disclaimer of Warranties & Capped Liability Waiver",
        "clause_6_text": "The service is provided strictly 'AS-IS' and 'AS-AVAILABLE' without warranties of merchantability, fitness, or non-infringement. Under no theory of liability (whether tort, negligence, or breach of contract) shall StreamPlay's aggregate cumulative liability exceed one hundred Indian Rupees (Rs. 100). User agrees to indemnify, defend, and hold harmless StreamPlay against all legal claims, fines, and consumer disputes.",
    },
    {
        "filename": "Sample2_Moderate_Risk_CloudVault_TOS.pdf",
        "company_name": "CloudVault Technologies Ltd.",
        "company_slug": "cloudvault",
        "title": "Cloud Backup & Storage Services Master Agreement",
        "risk_tier": "MODERATE RISK (Expected Score: 40-60)",
        "primary_color": "#d97706", # amber
        "badge_color": "#f59e0b",
        "clause_bg": "#fffbeb",
        "clause_2_title": "Dispute Resolution & Regional Governing Law",
        "clause_2_text": "In the event of any contractual controversy, the parties agree to participate in informal dispute negotiation for a period of thirty (30) days. If unresolved, claims shall be submitted to standard commercial arbitration under the rules of the American Arbitration Association in the State of Delaware.",
        "clause_3_title": "Modification of Service Fees and Storage Tiers",
        "clause_3_text": "CloudVault may adjust service fees or storage quotas upon thirty (30) days advance notice delivered via email or banner notification. If subscriber does not agree to the revised rates, they retain the option to terminate their plan prior to the next billing cycle.",
        "clause_4_title": "Subscription Auto-Renewal & Cancellation Window",
        "clause_4_text": "Subscriptions renew automatically on a monthly or annual basis. To prevent automatic renewal charges, subscriber must cancel recurring billing through account settings at least 48 hours prior to renewal. Payments for active periods are non-refundable, but access remains through the billing period.",
        "clause_5_title": "Usage Telemetry & Anonymized Analytics",
        "clause_5_text": "CloudVault collects technical metadata, performance diagnostics, and system error logs to maintain infrastructure reliability. Personal data is never sold to third parties; however, aggregated, anonymized analytical telemetry may be processed with third-party hosting partners.",
        "clause_6_title": "Limitation of Liability & Indemnification",
        "clause_6_text": "Neither party shall be liable for indirect, incidental, or consequential damages. CloudVault's total cumulative liability for direct damages under this agreement is capped at the total amount paid by the customer in the three (3) months preceding the incident.",
    },
    {
        "filename": "Sample3_Safe_FairDocs_Consumer_Agreement.pdf",
        "company_name": "FairDocs Open Software Foundation",
        "company_slug": "fairdocs",
        "title": "Consumer-First Document Cloud & Privacy Covenant",
        "risk_tier": "SAFE / LOW RISK (Expected Score: 0-25)",
        "primary_color": "#059669", # emerald
        "badge_color": "#10b981",
        "clause_bg": "#f0fdf4",
        "clause_2_title": "Consumer Redressal & Access to Courts",
        "clause_2_text": "Consumers retain full legal access to their local consumer forums, municipal courts, and statutory tribunals under the Consumer Protection Act and applicable consumer rights statutes. No consumer protection rights, class proceedings, or judicial hearings are waived under this agreement.",
        "clause_3_title": "Transparent Advance Notice for Any Terms Modifications",
        "clause_3_text": "No unilateral changes shall occur. FairDocs shall provide a minimum of thirty (30) days transparent advance written notice before any contractual updates or fee adjustments. Consumers have the absolute right to decline changes and obtain an immediate pro-rated refund.",
        "clause_4_title": "Fair Billing, Opt-In Renewals & Pro-Rata Refunds",
        "clause_4_text": "Renewals require explicit confirmation with an advance reminder notice 7 days prior to billing. Subscribers can cancel at any time with one click. Any unused balance of prepaid subscription fees shall be refunded pro-rata within five (5) business days.",
        "clause_5_title": "Zero Data Monetization & Strict Privacy Guarantee",
        "clause_5_text": "FairDocs adheres to strict zero-knowledge encryption and GDPR/CCPA standards. We never sell, rent, monetize, profile, or disclose your personal data, document content, or telemetry to advertising networks, brokers, or third parties.",
        "clause_6_title": "Balanced Warranties & Service Restoration Redress",
        "clause_6_text": "FairDocs warrants 99.9% service uptime and reasonable commercial care. If a verified technical deficiency or breach causes service disruption, FairDocs provides full restoration and compensation credit up to twelve (12) months of subscription fees.",
    }
]

def compile_pdf(doc_info):
    html = HTML_TEMPLATE
    for key, val in doc_info.items():
        html = html.replace("{{ " + key + " }}", str(val))
    
    out_path = OUTPUT_DIR / doc_info["filename"]
    pub_path = PUBLIC_DIR / doc_info["filename"]

    with open(out_path, "wb") as f_out:
        pisa_status = pisa.pisaDocument(html, f_out)
        if pisa_status.err:
            print(f"Error compiling {doc_info['filename']}: {pisa_status.err}", file=sys.stderr)
            return False

    with open(pub_path, "wb") as f_pub:
        pisa.pisaDocument(html, f_pub)

    print(f"Compiled: {out_path} ({out_path.stat().st_size} bytes)")
    return True

if __name__ == "__main__":
    success = True
    for doc in DOCUMENTS:
        if not compile_pdf(doc):
            success = False
    if success:
        print("\nAll 3 sample agreements compiled successfully!")
    else:
        sys.exit(1)
