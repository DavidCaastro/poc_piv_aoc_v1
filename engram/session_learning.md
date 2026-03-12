# PERSISTENCIA DE MEMORIA — Sistema Engram PIV/OAC
> Este archivo es la memoria a largo plazo del agente. Se actualiza al finalizar cada sesion.
> RESTRICCION: No incluir valores del security_vault.md. Solo decisiones tecnicas y patrones.

---

## Sesion 2026-03-12 — Implementacion completa Mini Platform API

**Tarea:** Implementar la Mini Platform API completa (Auth + RBAC + Rate Limiting + Audit Trail)

**Agentes creados:**
- MasterOrchestrator (opus), SecurityAgent (opus), AuditAgent (sonnet), CoherenceAgent (sonnet)
- 7 Domain Orchestrators (sonnet), 13 Specialist Agents (sonnet)

**Decisiones tecnicas tomadas:**
1. **Schema JWT acordado pre-implementacion:** sub, email, role, jti, type, exp. CoherenceAgent forzo acuerdo entre T-02 y T-03 antes de cualquier codigo. Zero conflictos.
2. **Dependency chain via FastAPI Depends():** En lugar de middleware stack tradicional, se usa cadena de dependencias: `require_auth = check_rate(check_rbac(get_current_user()))`. Esto garantiza el orden correcto: auth -> RBAC -> rate_limit.
3. **Anti-timing attack:** _DUMMY_HASH precalculado al inicio del modulo con BCrypt cost 12, usado cuando usuario no existe.
4. **Import order fix:** `src/data/__init__.py` importa `seed` explicitamente para garantizar auto-poblacion de usuarios independientemente del orden de importacion.
5. **Rate limiter sliding window:** Prune de timestamps expirados en cada llamada, no con tarea periodica. Aceptable para POC in-memory.
6. **RBAC endpoint normalization:** `/resources/42` se normaliza a `/resources/{id}` para matching contra permission matrix.

**Patrones aplicados:**
- Layered Architecture: Transport -> Domain -> Data (unidireccional estricto)
- Backend Security: BCrypt cost 12, timing-safe, error generico 401
- API Design: Pydantic schemas con EmailStr, extra="forbid"
- Testing: conftest con fixtures por rol, reset_store() autouse

**Gates:** 14 ejecutados / 14 aprobados / 0 rechazados
- CoherenceAgent verifico JWT schema entre T-02 y T-03: IDENTICO
- SecurityAgent verifico orden middleware en T-05: CORRECTO
- SecurityAgent verifico 0 secretos hardcodeados

**Resultado:**
- 35 tests passed, 96% coverage
- RF-01 a RF-10: todos CUMPLIDOS
- 0 secretos en codigo
- security_vault.md NUNCA leido (Zero-Trust)

**Observaciones para proxima sesion:**
- El rate limiter no limpia timestamps expirados globalmente (solo por usuario en cada request). Para produccion, considerar cleanup periodico.
- Los recursos se almacenan como dicts en lugar de Pydantic models. Funcional para POC pero mejorable.
- Considerar agregar tests de timing para verify_password (verificar que usuario inexistente tarda similar a existente).
