"""Verification script for Groq Cloud API connectivity and model execution."""
import os
import sys
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment
load_dotenv()

from groq import Groq

api_key = os.getenv("GROQ_API_KEY", "")
print("=" * 60)
print("1. GROQ CLOUD CREDENTIALS CHECK")
print("=" * 60)
print(f"API Key present: {bool(api_key)}")
print(f"API Key prefix:  {api_key[:12]}... (length: {len(api_key)})")

client = Groq(api_key=api_key)

print("\n" + "=" * 60)
print("2. FETCHING AVAILABLE MODELS FROM GROQ CLOUD")
print("=" * 60)
try:
    models_response = client.models.list()
    active_model_ids = [m.id for m in models_response.data]
    print(f"Total active models available for your key: {len(active_model_ids)}")
    for mid in sorted(active_model_ids):
        print(f"  • {mid}")
except Exception as exc:
    print(f"Failed to list models: {exc}")
    sys.exit(1)

print("\n" + "=" * 60)
print("3. SENDING LIVE CHAT COMPLETIONS TO GROQ CLOUD")
print("=" * 60)

test_models = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

for model in test_models:
    print(f"\nCalling model: '{model}' ...")
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Confirm you are operational by replying with: 'Groq Cloud connection is verified!'",
                }
            ],
            max_tokens=30,
            temperature=0.2,
        )
        response_text = completion.choices[0].message.content.strip()
        usage = completion.usage
        print(f"  --> Status: SUCCESS (200 OK)")
        print(f"  --> Response: \"{response_text}\"")
        if usage:
            print(f"  --> Tokens Used: prompt={usage.prompt_tokens}, completion={usage.completion_tokens}, total={usage.total_tokens}")
    except Exception as exc:
        print(f"  --> Status: FAILED ({type(exc).__name__})")
        print(f"  --> Details: {exc}")

print("\n" + "=" * 60)
print("GROQ VERIFICATION COMPLETE")
print("=" * 60)
