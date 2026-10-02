from groq import Groq
from app.core.config import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)

# Add these two model constants:
DEFAULT_CHAT_MODEL = "llama-3.3-70b-versatile"
FAST_SCAN_MODEL = "llama-3.1-8b-instant"

# Aliases for backward compatibility
MODEL_REASONING = DEFAULT_CHAT_MODEL
MODEL_FAST_SCAN = FAST_SCAN_MODEL


def get_groq_client() -> Groq:
    """Initialize and return a Groq client instance."""
    return groq_client


def create_chat_completion(messages: list[dict], model: str = DEFAULT_CHAT_MODEL, temperature: float = 0.2, **kwargs):
    """Generate completion using Groq with reasoning or fast scan models."""
    return groq_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        **kwargs,
    )


def fast_scan_completion(prompt: str, system_prompt: str = "You are a legal agreement analyzer specializing in quick clause scans.", **kwargs):
    """Convenience helper for fast scans using llama-3.1-8b-instant."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    return create_chat_completion(messages=messages, model=FAST_SCAN_MODEL, temperature=0.1, **kwargs)


def reasoning_completion(messages: list[dict], system_prompt: str = "You are an expert legal counsel and consumer grievance notice assistant.", **kwargs):
    """Convenience helper for deep reasoning and chat using llama-3.3-70b-versatile."""
    formatted_messages = [{"role": "system", "content": system_prompt}] + messages
    return create_chat_completion(messages=formatted_messages, model=DEFAULT_CHAT_MODEL, temperature=0.2, **kwargs)
