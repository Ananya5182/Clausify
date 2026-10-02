"""Unified Gateway and Reverse Proxy on Port 8080 for Clausify.
Routes /api, /health, /docs, /openapi.json to FastAPI (http://localhost:8000)
and all other web traffic to the Vite React Frontend (http://localhost:5173).
"""
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Clausify Unified Gateway (Port 8080)", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_BASE = "http://localhost:8000"
FRONTEND_BASE = "http://localhost:5173"

# Persistent async HTTP client for proxying
http_client = httpx.AsyncClient(timeout=120.0)


@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def gateway_proxy(request: Request, path: str):
    full_path = request.url.path
    # Route backend endpoints to port 8000
    if (
        full_path.startswith("/api/")
        or full_path == "/api"
        or full_path == "/health"
        or full_path.startswith("/docs")
        or full_path.startswith("/redoc")
        or full_path == "/openapi.json"
    ):
        target_url = f"{BACKEND_BASE}{full_path}"
    else:
        # Route frontend endpoints to port 5173
        target_url = f"{FRONTEND_BASE}{full_path}"

    if request.url.query:
        target_url += f"?{request.url.query}"

    body = await request.body()
    forward_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length", "connection")
    }

    try:
        upstream_res = await http_client.request(
            method=request.method,
            url=target_url,
            headers=forward_headers,
            content=body,
            follow_redirects=True,
        )

        excluded_headers = {
            "content-length", "content-encoding", "transfer-encoding", "connection"
        }
        res_headers = {
            k: v for k, v in upstream_res.headers.items()
            if k.lower() not in excluded_headers
        }

        return Response(
            content=upstream_res.content,
            status_code=upstream_res.status_code,
            headers=res_headers,
            media_type=upstream_res.headers.get("content-type"),
        )
    except httpx.ConnectError:
        return Response(
            content=f"Gateway service unavailable: Could not connect to upstream target {target_url}.",
            status_code=503,
            media_type="text/plain",
        )
    except Exception as exc:
        return Response(
            content=f"Gateway error proxying to {target_url}: {str(exc)}",
            status_code=502,
            media_type="text/plain",
        )


if __name__ == "__main__":
    uvicorn.run("gateway_8080:app", host="0.0.0.0", port=8080, reload=False)
