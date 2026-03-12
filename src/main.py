"""FastAPI application entry point.

Registers all routers and configures the application.
"""

from fastapi import FastAPI

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

app.include_router(auth_router)
app.include_router(resources_router)
app.include_router(admin_router)
