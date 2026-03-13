"""Auth endpoints: login, refresh, logout (RF-01, RF-02, RF-03).

These endpoints handle authentication. Login is public (no auth required).
Refresh and logout require a valid token.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.domain import auth_service
from src.schemas.tokens import TokenPair, RefreshRequest
from src.schemas.users import LoginRequest
from src.transport.dependencies import get_current_user
from src.schemas.tokens import TokenPayload

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
async def login(body: LoginRequest):
    """POST /auth/login — Authenticate user and return token pair (RF-01).

    No auth required. Returns generic 401 on failure (RF-04, RF-09).
    """
    result = auth_service.login(body.email, body.password)

    if result is None:
        # RF-04: Generic message — never distinguish email vs password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshRequest):
    """POST /auth/refresh — Get new token pair from refresh token (RF-02).

    Validates the refresh token, revokes it, and issues a new pair.
    """
    result = auth_service.refresh_tokens(body.refresh_token)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result


@router.post("/logout")
async def logout(
    current_user: TokenPayload = Depends(get_current_user),
):
    """POST /auth/logout — Revoke the current token (RF-03).

    Adds the token's jti to the revoked tokens cache (O(1) dict).
    """
    auth_service.revoke_token(current_user.jti, current_user.exp)

    return {"detail": "Token revocado exitosamente."}
