# PLAN: T-05 transport-layer
## RF cubiertos: RF-01 through RF-09

## Archivos:
1. src/transport/__init__.py
2. src/transport/dependencies.py — FastAPI Depends: get_current_user (auth + RBAC + rate limit)
3. src/transport/auth_router.py — POST /auth/login, /auth/refresh, /auth/logout
4. src/transport/resources_router.py — GET/POST /resources, PUT/DELETE /resources/{id}
5. src/transport/admin_router.py — GET /admin/audit-log
6. src/main.py — FastAPI app, include routers

## Middleware/Dependency Chain Order (CRITICAL):
1. Auth verification (decode JWT, check revocation)
2. RBAC check (verify role has permission for endpoint)
3. Rate limit check (verify user within rate window)

This order is enforced via FastAPI Depends() chain in dependencies.py.
Auth routers (/auth/login) are EXEMPT from auth middleware.

## Audit Trail:
Every authenticated request logs: user_id, role, endpoint, method, timestamp, status_code
