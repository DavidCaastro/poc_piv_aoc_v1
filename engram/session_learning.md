# PERSISTENCIA DE MEMORIA — Sistema Engram PIV/OAC
> Este archivo es la memoria a largo plazo del agente. Se actualiza al finalizar cada sesión.
> RESTRICCIÓN: No incluir valores del security_vault.md. Solo decisiones técnicas y patrones.

---

## Sesión 2026-03-12 — Inicialización del Marco PIV/OAC

**Tarea:** Completar la infraestructura de configuración del marco operativo.

**Decisiones técnicas tomadas:**
- `CLAUDE.md` establecido como punto de entrada para Claude Code (cargado automáticamente en cada sesión).
- `skills/backend-security.md` creado con patrones para FastAPI + JWT + BCrypt.
- `registry/security_auditor.md` creado con protocolo de auditoría de 6 pasos.
- **Corrección de imprecisión conceptual:** La caché de tokens usa `dict` (hashmap), NO un array/lista. Razón: la operación de lookup es por clave string (token ID/jti), lo que requiere O(1) por clave. Un array es O(1) solo por índice numérico y O(n) para búsqueda por valor. Esta corrección se aplicó en `agent.md`, `project_spec.md` y en el patrón 4 de `skills/backend-security.md`.

**Patrones establecidos:**
- Arquitectura por Capas: Transporte → Dominio → Datos (flujo unidireccional).
- BCrypt con cost factor 12 como mínimo.
- JWT con campo `jti` para soporte de revocación.
- Mensaje de error 401 unificado para prevenir enumeración de usuarios.
- Timing-safe comparison: ejecutar `verify_password` incluso si el usuario no existe.

**Estructura de archivos confirmada:**
- `CLAUDE.md` → instrucciones operativas para Claude Code (cargar siempre)
- `agent.md` → marco extendido PIV/OAC (referencia, no cargar por defecto)
- `skills/` → carga perezosa por tarea
- `registry/` → definiciones de subagentes
- `worktrees/` → no versionado (en .gitignore)

**Resultado auditoría de sesión:** N/A (sesión de configuración, no de implementación)

**Observaciones para próxima sesión:**
- El worktree `./worktrees/poc-login` debe crearse antes de iniciar la implementación del endpoint.
- SECRET_KEY para JWT debe obtenerse vía MCP antes de cualquier prueba local.
- Cargar `skills/backend-security.md` como primer paso de la implementación.
