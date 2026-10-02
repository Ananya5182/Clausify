"""Seed rich legal FAQs into Supabase for Clausify knowledge base."""
import sys
from pathlib import Path

# Add backend to path
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.core.supabase_client import supabase_client
from app.services.embedding_service import embedding_service

FAQS_TO_SEED = [
    {
        "question": "Can this company unilaterally modify contract terms without notice?",
        "answer": "Under general consumer protection statutes and contract jurisprudence, unilateral modification clauses that allow a company to amend fees, service tiers, or dispute rules at its sole discretion without advance notice or cancellation opt-outs are frequently deemed unconscionable and legally unenforceable.",
        "category": "modifications",
    },
    {
        "question": "Does this agreement contain a mandatory binding arbitration clause or class action waiver?",
        "answer": "A mandatory arbitration clause requires consumers to waive their constitutional right to a public jury trial or class action lawsuit, forcing disputes into private, confidential arbitration. Consumer Protection laws in many jurisdictions restrict mandatory pre-dispute arbitration when it deprives consumers of statutory remedies.",
        "category": "arbitration",
    },
    {
        "question": "What is the refund policy and are there hidden automatic renewal locks?",
        "answer": "Predatory subscription models often pair automatic perpetual renewals with strict 'no refund under any circumstance' terms. Regulatory standards (such as FTC guidelines and consumer e-mandate rules) require unambiguous advance disclosure, clear renewal reminder notices, and an easy one-click cancellation mechanism.",
        "category": "billing",
    },
    {
        "question": "Is my personal data or biometric information sold to third parties or advertisers?",
        "answer": "Under data privacy regulations (such as DPDP, GDPR, and CCPA), selling or sharing personal, behavioral, or biometric data with commercial brokers without clear, affirmative opt-in consent and a direct mechanism to revoke consent is unlawful.",
        "category": "privacy",
    },
    {
        "question": "Can a service provider exclude all liability for damages or service deficiency?",
        "answer": "Clauses that attempt to disclaim all liability, including for gross negligence, service deficiencies, or statutory consumer guarantees, are generally void as contrary to public policy under contract law.",
        "category": "liability",
    },
    {
        "question": "How do I draft a formal statutory legal notice for consumer grievance?",
        "answer": "A formal consumer dispute notice must state: the complainant's identity, the respondent company details, the date and transaction/order ID, the disputed amount, a factual summary of the grievance/deficiency, statutory violations (e.g. Consumer Protection Act, Section 2(47)), and a 15-to-30 day cure period before filing a consumer court complaint.",
        "category": "notices",
    },
    {
        "question": "Evaluate the enforceability of arbitration clauses under Consumer Protection Act 2019.",
        "answer": "Under Section 2(47) of the Consumer Protection Act 2019 and relevant Apex Court precedents, consumer complaints before Consumer Dispute Redressal Commissions are additional statutory remedies that cannot be extinguished by pre-dispute arbitration agreements.",
        "category": "statutes",
    },
    {
        "question": "What legal recourse exists if an airline or merchant cancels a service and refuses a refund?",
        "answer": "If a merchant cancels a confirmed service (such as a flight, subscription, or delivered order) and withholds funds, it constitutes an actionable 'Deficiency in Service' and 'Unfair Trade Practice'. Consumers are entitled to full reimbursement plus statutory interest and compensation for harassment.",
        "category": "disputes",
    },
]

def seed():
    print("Seeding FAQs into Supabase...")
    for item in FAQS_TO_SEED:
        q = item["question"]
        # Check if already exists
        check = supabase_client.table("faqs").select("id").eq("question", q).execute()
        if check.data:
            print(f"  [Exists] {q[:50]}...")
            continue
        
        vec = embedding_service.embed_text(q)
        record = {
            "question": q,
            "answer": item["answer"],
            "category": item["category"],
            "embedding": vec,
        }
        res = supabase_client.table("faqs").insert(record).execute()
        if res.data:
            print(f"  [Inserted] {q[:50]}...")
        else:
            print(f"  [Failed] {q[:50]}...")
    print("FAQ Seeding complete!")

if __name__ == "__main__":
    seed()
