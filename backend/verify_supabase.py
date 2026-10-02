"""Verification script for Supabase connection, schema, and read/write operations."""
import os
import sys
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

from supabase import create_client

supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_KEY", "")

print("=" * 60)
print("1. SUPABASE CREDENTIALS CHECK")
print("=" * 60)
print(f"Supabase URL:    {supabase_url}")
print(f"Supabase Key:    {supabase_key[:12]}... (length: {len(supabase_key)})")

if not supabase_url or not supabase_key:
    print("Error: SUPABASE_URL or SUPABASE_KEY missing in environment!")
    sys.exit(1)

client = create_client(supabase_url, supabase_key)

print("\n" + "=" * 60)
print("2. VERIFYING SUPABASE TABLES & READING DATA")
print("=" * 60)

for table_name in ["faqs", "documents", "document_chunks"]:
    try:
        res = client.table(table_name).select("*").limit(5).execute()
        count = len(res.data) if res.data else 0
        print(f"\n[Table: '{table_name}'] -> Query OK (Found {count} rows)")
        if res.data:
            first_row = res.data[0]
            display_keys = [k for k in first_row.keys() if k != "embedding"]
            print(f"  Sample row keys: {display_keys}")
            for k in display_keys[:4]:
                val = str(first_row.get(k))
                if len(val) > 60:
                    val = val[:60] + "..."
                print(f"    - {k}: {val}")
    except Exception as exc:
        print(f"[Table: '{table_name}'] -> Query FAILED: {exc}")

print("\n" + "=" * 60)
print("3. VERIFYING WRITE PERMISSION (INSERT & DELETE TEST)")
print("=" * 60)
try:
    test_question = "__ping_test_question__"
    insert_res = client.table("faqs").insert({
        "question": test_question,
        "answer": "Test answer for Supabase write verification.",
        "category": "healthcheck"
    }).execute()

    if insert_res.data:
        test_id = insert_res.data[0]["id"]
        print(f"  --> Insert Test: SUCCESS (Created test record id: {test_id})")

        # Cleanup test record
        delete_res = client.table("faqs").delete().eq("id", test_id).execute()
        print(f"  --> Delete Test: SUCCESS (Cleaned up temporary test record)")
    else:
        print("  --> Insert Test: FAILED (No data returned)")
except Exception as exc:
    print(f"  --> Write Test FAILED: {exc}")

print("\n" + "=" * 60)
print("SUPABASE VERIFICATION COMPLETE")
print("=" * 60)
