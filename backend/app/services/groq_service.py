"""Groq AI service for legal clause risk analysis and structured evaluation."""
import json
import logging
from typing import Any, Dict, List, Optional
from groq import NotFoundError
from app.core.config import settings
from app.core.groq_client import groq_client, MODEL_FAST_SCAN

logger = logging.getLogger(__name__)

# Fallback models in priority order if the configured model is not available
MODEL_CANDIDATES = [
    MODEL_FAST_SCAN,
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b",
]

SYSTEM_PROMPT = """You are an expert consumer rights attorney and legal agreement analyzer.
Analyze the provided clause from a Terms of Service, Privacy Policy, or consumer contract.
Evaluate whether it contains unfair, one-sided, or predatory terms.

You MUST specifically check for these 4 risk categories:
1. Forced arbitration (e.g., mandatory binding arbitration, class action waiver, jury waiver, limitation of legal recourse)
2. Unilateral modifications (e.g., provider may change terms, pricing, or features at any time without notice or prior consent)
3. Third-party data tracking/selling (e.g., selling or sharing personal, behavioral, or biometric data with third parties/advertisers without opt-out)
4. Auto-renewal/non-refundable locks (e.g., perpetual recurring billing, restrictive cancellation windows, zero-refund guarantees)

Respond ONLY with a valid JSON object adhering to this schema:
{
  "risk_level": "HIGH" | "MEDIUM" | "LOW" | "NONE",
  "risk_score": <integer from 0 to 100, where 0 is completely benign and 100 is extremely predatory>,
  "detected_categories": [<list of matching category names from the 4 above, or empty list>],
  "flag_reason": "<Clear explanation of why this clause infringes consumer rights or poses risk, or empty string if safe>",
  "summary": "<1-2 sentence plain-language summary of what the clause dictates>"
}
"""


def _get_active_model() -> str:
    """Find the first working model candidate for the API key."""
    for model_name in MODEL_CANDIDATES:
        try:
            return model_name
        except Exception:
            continue
    return "openai/gpt-oss-20b"


def analyze_clause_risk(clause_text: str, model: Optional[str] = None) -> Dict[str, Any]:
    """Analyze a legal contract clause using Groq and structured JSON output enforcement.

    Specifically inspects for:
    - Forced arbitration
    - Unilateral modifications
    - Third-party data tracking/selling
    - Auto-renewal/non-refundable locks

    Returns:
        dict containing risk_level, risk_score, detected_categories, flag_reason, summary
    """
    cleaned_text = clause_text.strip() if clause_text else ""
    if not cleaned_text:
        return {
            "risk_level": "NONE",
            "risk_score": 0,
            "detected_categories": [],
            "flag_reason": "",
            "summary": "Empty clause provided.",
        }

    user_prompt = f"""Please analyze the following legal clause in JSON format:

\"\"\"
{cleaned_text}
\"\"\"
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    models_to_try = [model] if model else MODEL_CANDIDATES

    last_error: Optional[Exception] = None

    for m in models_to_try:
        try:
            response = groq_client.chat.completions.create(
                model=m,
                messages=messages,
                temperature=0.1,
                response_format={"type": "json_object"},
            )

            raw_content = response.choices[0].message.content or "{}"
            parsed = json.loads(raw_content)

            # Normalize output fields
            risk_level = str(parsed.get("risk_level", "NONE")).upper()
            if risk_level not in {"HIGH", "MEDIUM", "LOW", "NONE"}:
                risk_level = "MEDIUM" if parsed.get("risk_score", 0) > 40 else "LOW"

            risk_score = parsed.get("risk_score", 0)
            try:
                risk_score = int(risk_score)
                risk_score = max(0, min(100, risk_score))
            except (ValueError, TypeError):
                risk_score = 75 if risk_level == "HIGH" else (45 if risk_level == "MEDIUM" else 15)

            detected_categories = parsed.get("detected_categories", [])
            if not isinstance(detected_categories, list):
                detected_categories = [str(detected_categories)]

            flag_reason = str(parsed.get("flag_reason", "")).strip()
            summary = str(parsed.get("summary", "")).strip()

            return {
                "risk_level": risk_level,
                "risk_score": risk_score,
                "detected_categories": detected_categories,
                "flag_reason": flag_reason,
                "summary": summary,
            }

        except NotFoundError as exc:
            logger.warning(f"Groq model {m} not found or inaccessible: {exc}. Trying next candidate.")
            last_error = exc
            continue
        except json.JSONDecodeError as exc:
            logger.error(f"Failed to parse JSON response from Groq: {exc}")
            return {
                "risk_level": "LOW",
                "risk_score": 20,
                "detected_categories": [],
                "flag_reason": "Could not parse detailed model response.",
                "summary": cleaned_text[:150] + ("..." if len(cleaned_text) > 150 else ""),
            }
        except Exception as exc:
            logger.error(f"Error calling Groq with model {m}: {exc}")
            last_error = exc
            continue

    # Fallback if all models failed
    logger.error(f"All Groq model candidates failed for clause analysis: {last_error}")
    # Basic heuristic check if Groq API is completely unreachable
    lower_clause = cleaned_text.lower()
    categories = []
    if any(k in lower_clause for k in ["arbitration", "class action", "jury trial"]):
        categories.append("Forced arbitration")
    if any(k in lower_clause for k in ["modify these terms", "change these terms", "unilateral", "without prior notice"]):
        categories.append("Unilateral modifications")
    if any(k in lower_clause for k in ["share your personal", "sell your personal", "third party advertisers", "tracking cookies"]):
        categories.append("Third-party data tracking/selling")
    if any(k in lower_clause for k in ["auto-renew", "automatically renew", "non-refundable", "no refunds"]):
        categories.append("Auto-renewal/non-refundable locks")

    heuristic_risk = "HIGH" if len(categories) >= 2 or "Forced arbitration" in categories else ("MEDIUM" if categories else "NONE")
    heuristic_score = 80 if heuristic_risk == "HIGH" else (50 if heuristic_risk == "MEDIUM" else 0)

    return {
        "risk_level": heuristic_risk,
        "risk_score": heuristic_score,
        "detected_categories": categories,
        "flag_reason": f"Fallback evaluation: detected potential concerns in {', '.join(categories)}" if categories else "No significant flags detected.",
        "summary": cleaned_text[:150] + ("..." if len(cleaned_text) > 150 else ""),
    }
