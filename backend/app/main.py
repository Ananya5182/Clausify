import sys
from pathlib import Path

# Ensure backend root is always in sys.path regardless of execution working directory
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_admin import router as admin_router
from app.api.routes_chat import router as chat_router
from app.api.routes_notice import router as notice_router
from app.api.routes_scan import router as scan_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI legal agreement scanner and consumer grievance notice assistant API",
)

# CORS middleware configuration allowing frontend origin (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(admin_router)
app.include_router(scan_router)
app.include_router(chat_router)
app.include_router(notice_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify backend operational readiness."""
    return {
        "status": "healthy",
        "service": "Clausify Backend",
        "version": settings.VERSION,
        "models": {
            "reasoning": settings.GROQ_REASONING_MODEL,
            "fast_scan": settings.GROQ_FAST_SCAN_MODEL,
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
