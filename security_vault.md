# VAULT - PROTOCOLO DE SEGURIDAD ZERO-TRUST v1.0

## 1. Configuración de Conexiones MCP (Model Context Protocol)
Este sistema utiliza el protocolo **MCP** como interfaz estándar para conectar herramientas externas sin exponer credenciales en el contexto del modelo.

- **mcp_azure_key_vault:** `mcp://azure-vault-connector:5000` (Conexión enmascarada para recuperación de secretos de entorno).
- **mcp_postgresql_prod:** `mcp://supabase-db-proxy:5432` (Acceso vía token efímero configurado en el servidor local de MCP).
- **mcp_github_enterprise:** `mcp://github-audit-tool` (Token con Scope limitado exclusivamente a la lectura de Pull Requests para el Auditor).

## 2. Parámetros de Infraestructura (Anclaje de Verdad)
Valores críticos que los agentes pueden consultar pero **NUNCA** modificar:
- `PROD_DEPLOY_URL`: `https://api.produccion.empresa.com`
- `SECURITY_AUDIT_WEBHOOK`: `https://audit.logs.interno/v1/ingest`

## 3. Reglas de Acceso para Agentes (Protocolo de Defensa)
Para prevenir ataques de **Prompt Injection** o **Autonomous Agent Overreach**, se imponen las siguientes restricciones técnicas:

1.  **Prohibición de Indexación:** Los agentes tienen estrictamente prohibido resumir, indexar o incluir el contenido íntegro de este archivo en su memoria persistente o sistema **Engram**.
2.  **Validación Human-in-the-loop:** Cualquier solicitud de lectura de un parámetro de este archivo por parte de un agente (ej: Claude Code o Cursor) DEBE disparar una solicitud de aprobación manual en la terminal del usuario.
3.  **Aislamiento de Logs:** El Agente Auditor debe verificar que ningún valor extraído de este vault sea escrito en texto plano dentro de la carpeta `/logs_veracidad/`.
4.  **Zero-Persistence:** Al finalizar la tarea, la información extraída de este vault debe ser purgada de la **ventana de contexto** efímera del subagente especialista.

## 4. Auditoría de Acceso
Cualquier intento de lectura no autorizado por un agente sin el rol `SecOps-Orchestrator` debe ser registrado inmediatamente como una violación de política de **Gobernanza y Cumplimiento**.
