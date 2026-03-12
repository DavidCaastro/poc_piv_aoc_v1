"""Resources endpoints: CRUD operations (RF-06).

All endpoints require authentication, RBAC, and rate limiting
via the require_auth dependency chain.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.data import store
from src.schemas.resources import Resource, ResourceCreate, ResourceUpdate
from src.schemas.tokens import TokenPayload
from src.transport.dependencies import require_auth

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("", response_model=list[Resource])
async def list_resources(
    current_user: TokenPayload = Depends(require_auth),
):
    """GET /resources — List all resources (VIEWER, EDITOR, ADMIN)."""
    return [Resource(**r) for r in store.resources]


@router.post("", response_model=Resource, status_code=status.HTTP_201_CREATED)
async def create_resource(
    body: ResourceCreate,
    current_user: TokenPayload = Depends(require_auth),
):
    """POST /resources — Create a new resource (EDITOR, ADMIN)."""
    resource_data = {
        "id": store.get_next_resource_id(),
        "title": body.title,
        "description": body.description,
        "owner_id": current_user.sub,
    }
    store.resources.append(resource_data)
    return Resource(**resource_data)


@router.put("/{resource_id}", response_model=Resource)
async def update_resource(
    resource_id: int,
    body: ResourceUpdate,
    current_user: TokenPayload = Depends(require_auth),
):
    """PUT /resources/{id} — Update a resource (EDITOR, ADMIN)."""
    for resource in store.resources:
        if resource["id"] == resource_id:
            if body.title is not None:
                resource["title"] = body.title
            if body.description is not None:
                resource["description"] = body.description
            return Resource(**resource)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Recurso no encontrado.",
    )


@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: int,
    current_user: TokenPayload = Depends(require_auth),
):
    """DELETE /resources/{id} — Delete a resource (ADMIN only)."""
    for i, resource in enumerate(store.resources):
        if resource["id"] == resource_id:
            store.resources.pop(i)
            return {"detail": "Recurso eliminado."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Recurso no encontrado.",
    )
