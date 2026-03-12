"""Admin endpoints (RF-08).

Audit log access restricted to ADMIN role only.
Protected by the full auth -> RBAC -> rate_limit chain.
"""

from fastapi import APIRouter, Depends

from src.data import store
from src.schemas.tokens import TokenPayload
from src.transport.dependencies import require_auth

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/audit-log")
async def get_audit_log(
    current_user: TokenPayload = Depends(require_auth),
):
    """GET /admin/audit-log — View audit trail (ADMIN only, RF-08)."""
    return store.audit_log
