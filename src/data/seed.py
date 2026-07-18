"""Seed data: predefined test users with BCrypt-hashed passwords.

Users defined here are loaded into the in-memory store at startup.
Passwords are hashed with BCrypt cost factor 12 as required by RF-04.

Default demo users (override via environment variables for non-demo deployments):
  SEED_ADMIN_PASSWORD  (default: Admin123!)  -> admin@test.com  / ADMIN
  SEED_EDITOR_PASSWORD (default: Editor123!) -> editor@test.com / EDITOR
  SEED_VIEWER_PASSWORD (default: Viewer123!) -> viewer@test.com / VIEWER

WARNING: The default passwords are PUBLIC demo credentials.
         Always set custom passwords via env vars in any shared or production deployment.
"""

import os

import bcrypt

from src.schemas.roles import Role
from src.schemas.users import UserInDB


def _hash_password(plain_password: str) -> str:
    """Hash a password with BCrypt cost factor 12."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


# Pre-computed hashes to avoid re-hashing on every import.
# These are generated once at first import.
_SEED_USERS: list[dict] | None = None

# Read passwords from env vars with public demo defaults.
_ADMIN_PW = os.environ.get("SEED_ADMIN_PASSWORD", "Admin123!")
_EDITOR_PW = os.environ.get("SEED_EDITOR_PASSWORD", "Editor123!")
_VIEWER_PW = os.environ.get("SEED_VIEWER_PASSWORD", "Viewer123!")


def _build_seed_users() -> list[UserInDB]:
    """Build seed users with hashed passwords."""
    return [
        UserInDB(
            id="user_admin_001",
            email="admin@test.com",
            hashed_password=_hash_password(_ADMIN_PW),
            role=Role.ADMIN,
        ),
        UserInDB(
            id="user_editor_001",
            email="editor@test.com",
            hashed_password=_hash_password(_EDITOR_PW),
            role=Role.EDITOR,
        ),
        UserInDB(
            id="user_viewer_001",
            email="viewer@test.com",
            hashed_password=_hash_password(_VIEWER_PW),
            role=Role.VIEWER,
        ),
    ]


def seed_users() -> None:
    """Populate the user store with predefined test users."""
    from src.data import store

    for user in _build_seed_users():
        store.users[user.email] = user


# Auto-seed on first import
seed_users()
