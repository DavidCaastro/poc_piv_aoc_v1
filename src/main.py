"""FastAPI application entry point.

Registers all routers and configures the application.
"""

from fastapi import FastAPI, Request
from fastapi.responses import Response

from src.transport.auth_router import router as auth_router
from src.transport.resources_router import router as resources_router
from src.transport.admin_router import router as admin_router

# Ensure seed data is loaded
from src.data import seed as _seed  # noqa: F401


app = FastAPI(
    title="Mini Platform API — Auth + RBAC + Rate Limiting + Audit Trail",
    description="POC: JWT auth, role-based access control, rate limiting, audit trail. All in-memory.",
    version="1.0.0",
)


# FIX VULN-004: Security headers on every response
@app.middleware("http")
async def add_security_headers(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "0"  # CSP preferred over legacy header
    return response


app.include_router(auth_router)
app.include_router(resources_router)
app.include_router(admin_router)
