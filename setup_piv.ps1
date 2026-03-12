# ==============================================================================
# GENTLE AI STACK - INICIALIZADOR PIV/OAC v1.0 (Windows PowerShell)
# Propósito: Automatizar la creación de la infraestructura de control para el 
# Paradigma de Intencionalidad Verificable (PIV).
# ==============================================================================

$ErrorActionPreference = "Stop" # Detener ejecución ante cualquier error

Write-Host "🚀 Iniciando la instanciación del Framework PIV/OAC..." -ForegroundColor Cyan

# 1. Creación de la Estructura de Carpetas OAC (Atomic Cells)
# Estas carpetas permiten el aislamiento y la carga perezosa de contexto.
Write-Host "📂 Creando jerarquía de carpetas..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "skills" -Force | Out-Null
New-Item -ItemType Directory -Path "registry" -Force | Out-Null
New-Item -ItemType Directory -Path "engram" -Force | Out-Null
New-Item -ItemType Directory -Path "logs_veracidad" -Force | Out-Null
New-Item -ItemType Directory -Path "worktrees" -Force | Out-Null

# 2. Inicialización de los Ficheros del "Cerebro" (Metadatos)
# Estos archivos actúan como el ancla de verdad para los agentes.
Write-Host "🧠 Inicializando ficheros base del marco operativo..." -ForegroundColor Cyan

# Fichero agent.md / .cursorrules
if (-not (Test-Path "agent.md")) {
    @"
# MARCO OPERATIVO PIV/OAC
# Identidad: Arquitecto de Orquestación Senior.
# Regla de Oro: Validar la intención en project_spec.md antes de actuar.
"@ | Set-Content -Path "agent.md" -Encoding UTF8
    Write-Host "- agent.md inicializado." -ForegroundColor Green
}

# Fichero project_spec.md (Spec-as-Source)
if (-not (Test-Path "project_spec.md")) {
    "# ESPECIFICACIÓN TÉCNICA Y CONTRATO DE INTENCIÓN" | Set-Content -Path "project_spec.md" -Encoding UTF8
    Write-Host "- project_spec.md inicializado." -ForegroundColor Green
}

# Fichero security_vault.md (Protocolo Zero-Trust)
if (-not (Test-Path "security_vault.md")) {
    "# VAULT - ACCESO RESTRINGIDO (SOLO MANUAL)" | Set-Content -Path "security_vault.md" -Encoding UTF8
    Write-Host "- security_vault.md inicializado." -ForegroundColor Green
}

# 3. Inicialización del Sistema Engram (Memoria Persistente)
# Previene la 'lobotomía' agéntica entre sesiones.
if (-not (Test-Path "engram/session_learning.md")) {
    "# PERSISTENCIA DE MEMORIA (ENGRAM)" | Set-Content -Path "engram/session_learning.md" -Encoding UTF8
    Write-Host "- engram/session_learning.md inicializado." -ForegroundColor Green
}

# 4. Configuración de Logs de Veracidad
# Espacio reservado para la auditoría física de la POC.
New-Item -ItemType File -Path "logs_veracidad/acciones_realizadas.txt" -Force | Out-Null
New-Item -ItemType File -Path "logs_veracidad/uso_contexto.txt" -Force | Out-Null
New-Item -ItemType File -Path "logs_veracidad/verificacion_intentos.txt" -Force | Out-Null
Write-Host "- Logs de veracidad preparados." -ForegroundColor Green

# 5. Finalización e Instrucciones
Write-Host ""
Write-Host "✅ Estructura PIV/OAC instanciada con éxito." -ForegroundColor Cyan
Write-Host "----------------------------------------------------------------------" -ForegroundColor White
Write-Host "⚠️  PRÓXIMOS PASOS DE SEGURIDAD:" -ForegroundColor Yellow
Write-Host "1. Asegúrate de estar en la rama 'agent-configs'." -ForegroundColor White
Write-Host "2. En 'main', añade estas carpetas al .gitignore para evitar Data Leakage." -ForegroundColor White
Write-Host "3. Para tareas paralelas, usa: git worktree add ./worktrees/feature-name" -ForegroundColor White
Write-Host "----------------------------------------------------------------------" -ForegroundColor White