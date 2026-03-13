"""FastAPI application entry point.

Registers all routers and configures the application.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from src.data import store
from src.transport.auth_router import router as auth_router
from src.transport.resources_router import router as resources_router
from src.transport.admin_router import router as admin_router

# Ensure seed data is loaded
from src.data import seed as _seed  # noqa: F401

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mini Platform API — Auth + RBAC + Rate Limiting + Audit Trail",
    description="POC: JWT auth, role-based access control, rate limiting, audit trail. All in-memory.",
    version="2.0.0",
)


# --- Middleware order: last registered = innermost (runs first on response) ---

# MIDDLEWARE 1 (outermost): Security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next) -> Response:
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-XSS-Protection"] = "0"
    # HSTS: instruct browsers to use HTTPS only for 1 year
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# MIDDLEWARE 2 (innermost): Audit log — captures real status_code after handler executes
@app.middleware("http")
async def audit_log_middleware(request: Request, call_next) -> Response:
    """Complete pending audit entries with the real response status_code.

    check_rate stores a pending entry in request.state.audit_entry for success
    paths. This middleware finalizes it after the handler runs, capturing the
    actual code (200, 404, 422...) instead of assuming 200.

    403/429/401 events are appended directly before their exceptions are raised
    and do not go through this middleware.
    """
    response = await call_next(request)
    audit_entry = getattr(request.state, "audit_entry", None)
    if audit_entry is not None:
        audit_entry["status_code"] = response.status_code
        store.audit_log.append(audit_entry)
    return response


# --- Global exception handler: prevents stack trace leakage on 500s ---

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch unhandled exceptions, log server-side, return generic 500.

    Prevents internal details from reaching clients (information disclosure).
    """
    logger.exception(
        "Unhandled exception on %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor."},
    )


app.include_router(auth_router)
app.include_router(resources_router)
app.include_router(admin_router)
