import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Determine paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Load .env file
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseModel):
    """Application configuration settings loaded safely via python-dotenv and Pydantic."""

    PROJECT_NAME: str = "Clausify"
    VERSION: str = "1.0.0"

    # Supabase configuration
    SUPABASE_URL: str = Field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    SUPABASE_KEY: str = Field(default_factory=lambda: os.getenv("SUPABASE_KEY", ""))

    # Groq configuration
    GROQ_API_KEY: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))

    # Configured Groq Models
    GROQ_REASONING_MODEL: str = Field(
        default_factory=lambda: os.getenv("GROQ_REASONING_MODEL", "openai/gpt-oss-120b")
    )
    GROQ_FAST_SCAN_MODEL: str = Field(
        default_factory=lambda: os.getenv("GROQ_FAST_SCAN_MODEL", "openai/gpt-oss-20b")
    )

    # CORS configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
