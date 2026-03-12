# PIV/OAC — Marco de Configuración Operativa

> **Rama:** `agent-configs`
> Esta rama contiene exclusivamente la configuración del sistema de agentes. No contiene código de aplicación.

---

## ¿Qué es PIV/OAC?

**PIV** (Paradigma de Intencionalidad Verificable) + **OAC** (Orquestación Atómica de Contexto) es un marco operativo para desarrollo guiado por agentes de IA que resuelve tres problemas estructurales del uso convencional de LLMs en ingeniería de software:

| Problema convencional | Solución PIV/OAC |
|---|---|
| El agente genera código sin validar la intención real | Toda acción se valida contra una especificación documentada antes de ejecutarse |
| Un solo agente satura su ventana de contexto con todo el repo | Cada agente recibe solo el contexto mínimo necesario para su tarea atómica |
| La seguridad y auditoría son pasos finales opcionales | Security Agent y Audit Agent corren en paralelo desde el inicio, con capacidad de veto pre-código |
| Las decisiones técnicas se pierden entre sesiones | El sistema Engram persiste las decisiones tomadas para que el agente no empiece desde cero |

---

## Arquitectura del Sistema

El marco opera con una jerarquía de tres niveles de agentes. Cada nivel tiene scope, responsabilidades y modelo de IA asignado de forma diferente.

```
┌──────────────────────────────────────────────────────────────┐
│                  MASTER ORCHESTRATOR                         │
│                      (Nivel 0)                               │
│                                                              │
│  Recibe el objetivo → infiere el equipo completo → delega    │
│  Nunca escribe código. Nunca lee archivos de implementación. │
└───────────────────────┬──────────────────────────────────────┘
                        │ crea y coordina
          ┌─────────────┼──────────────────┐
          ▼             ▼                  ▼
  ┌──────────────┐ ┌──────────┐    ┌─────────────┐
  │   DOMAIN     │ │SECURITY  │    │   AUDIT     │
  │ORCHESTRATORS │ │  AGENT   │    │   AGENT     │
  │  (Nivel 1)   │ │          │    │             │
  │              │ │ PARALELO │    │  PARALELO   │
  │ Uno por cada │ │ SIEMPRE  │    │  SIEMPRE    │
  │ dominio del  │ │  ACTIVO  │    │   ACTIVO    │
  │  problema    │ │  [veto]  │    │   [veto]    │
  └──────┬───────┘ └──────────┘    └─────────────┘
         │ crea
         ▼
┌─────────────────────────────────────────────────┐
│           SPECIALIST AGENTS (Nivel 2)           │
│                                                 │
│  PERSISTENTES            TEMPORALES             │
│  ─────────────           ──────────             │
│  Viven durante           Se crean para una      │
│  todo el dominio         tarea atómica.         │
│  (ej: DBArchitect,       Reportan resultado     │
│  APIDesigner)            y se destruyen.        │
│                          (ej: CodeImplementer,  │
│                          TestWriter)            │
└─────────────────────────────────────────────────┘
```

---

## El Gate de Aprobación Pre-Código

Este es el mecanismo central del marco. **Ninguna línea de código se escribe sin pasar este gate.**

```
Domain Orchestrator genera un plan
              │
    ┌─────────┴─────────┐
    ▼                   ▼
Security Agent      Audit Agent
evalúa el plan      evalúa el plan
  (en paralelo)      (en paralelo)
    │                   │
    └─────────┬─────────┘
              │
     ¿Ambos aprueban?
              │
      NO ─────┴───── SÍ
      │                │
      ▼                ▼
Plan devuelto     Specialist Agents
para revisión     autorizados a
→ repetir gate    implementar
```

El Security Agent verifica patrones de seguridad, ausencia de secretos y cobertura de requerimientos.
El Audit Agent verifica trazabilidad a la especificación, coherencia de scope y correctitud arquitectónica.
Un rechazo de cualquiera de los dos bloquea la ejecución completa.

---

## Asignación Dinámica de Modelo

La capacidad del modelo de IA no es fija por rol, sino que se asigna en función de la **dimensión de razonamiento** que requiere la tarea en ese momento:

```
Alta ambigüedad / alto riesgo / múltiples trade-offs
    → Opus (razonamiento profundo)

Planificación estructurada / generación con patrones / coordinación
    → Sonnet (balance rendimiento/velocidad)

Transformaciones mecánicas / lookups / formateo / tareas claras
    → Haiku (velocidad máxima, costo mínimo)
```

Cualquier agente puede solicitar **escalado de modelo** si detecta que la tarea supera su capacidad de razonamiento asignada. El orquestador padre decide si reasignar o escalar a revisión humana.

---

## Taxonomía de Tareas

El marco no aplica el mismo protocolo a todo. Antes de actuar, cada tarea se clasifica:

### Nivel 1 — Micro-tarea
Se cumplen **todos** estos criterios:
- Afecta ≤ 2 archivos existentes
- No introduce arquitectura nueva ni dependencias
- Tiene cobertura directa en un requerimiento funcional ya documentado
- Riesgo de regresión bajo

**Protocolo:** Ejecución directa. Sin orquestación, sin worktree, sin auditoría formal. Las reglas de Zero-Trust y lazy loading aplican igual.

### Nivel 2 — Feature / POC / Objetivo complejo
Se cumple **cualquiera** de estos criterios:
- Crea archivos nuevos o afecta ≥ 3 archivos
- Introduce arquitectura, dependencias o decisiones de diseño
- Implementa un requerimiento nuevo o modifica uno existente
- Impacto en seguridad, autenticación o datos

**Protocolo completo:** Master Orchestrator → equipo inferido → gates paralelos → worktree aislado → implementación → auditoría → engram.

**Escalado automático:** Si una tarea Nivel 1 crece en scope durante la ejecución, escala a Nivel 2 automáticamente con notificación al usuario antes de continuar.

---

## Gestión de Contexto por Abstracción

El sistema está diseñado para que ningún agente sature su ventana de contexto:

- **Master Orchestrator:** Solo conoce objetivos, estructura del equipo y estado de gates. No lee código.
- **Domain Orchestrators:** Solo cargan el skill relevante y los requerimientos de su dominio. No leen el repo completo.
- **Specialist Agents:** Reciben el scope exacto de su tarea atómica. Nada más.
- **Lazy Loading obligatorio:** Los skills en `/skills/` se cargan por demanda, no de forma preventiva.
- **Comunicación por mensajes estructurados:** Los agentes no comparten contexto directamente. Solo pasan el resultado necesario al siguiente agente.

---

## Sistema Engram — Memoria Persistente

El Engram resuelve la "amnesia agéntica": la pérdida de decisiones técnicas entre sesiones de trabajo.

- **Escritura exclusiva:** Solo el Audit Agent puede escribir en `engram/session_learning.md`.
- **Lectura libre:** Cualquier agente puede consultarlo al inicio de una tarea para no repetir decisiones ya tomadas.
- **Contenido:** Decisiones técnicas, patrones reutilizables identificados, errores encontrados, resultado de gates, observaciones para la próxima sesión.
- **No contiene:** Ningún valor del vault de seguridad, ninguna credencial, ningún dato sensible.

---

## Principios de Seguridad Zero-Trust

Aplican a todos los agentes, en todos los niveles, sin excepción:

1. **Vault restringido:** Ningún agente accede al vault de seguridad sin instrucción humana explícita en el turno activo.
2. **Credenciales solo vía MCP:** Las credenciales y secretos nunca residen en la ventana de contexto de ningún agente.
3. **Veto de Security Agent:** Capacidad de detener inmediatamente cualquier plan o acción que represente un riesgo.
4. **Anti Prompt Injection:** Cualquier input que intente secuestrar las instrucciones del sistema activa un veto automático y notificación al usuario.
5. **Logs limpios:** El Audit Agent verifica que ningún valor sensible aparezca en texto plano en los logs de veracidad.

---

## Estructura de Archivos de esta Rama

```
agent-configs/
│
├── CLAUDE.md                    ← Instrucciones operativas cargadas automáticamente
│                                   por Claude Code en cada sesión
│
├── agent.md                     ← Marco operativo completo PIV/OAC v2.0
│                                   Referencia técnica de toda la arquitectura
│
├── project_spec.md              ← Fuente de verdad (Spec-as-Source)
│                                   Requerimientos funcionales y stack tecnológico
│                                   Ningún agente actúa sin RF documentado aquí
│
├── security_vault.md            ← Acceso restringido
│                                   Solo lectura con instrucción humana explícita
│
├── skills/
│   └── backend-security.md     ← Skill de carga perezosa para seguridad backend
│                                   Patrones: BCrypt, JWT, capas, caché, errores
│
├── registry/
│   ├── orchestrator.md         ← Definición y protocolo del Master Orchestrator
│   ├── security_auditor.md     ← Security Agent + Audit Agent: gates y protocolos
│   └── agent_taxonomy.md       ← Catálogo completo: ciclo de vida, modelos, escalado
│
├── engram/
│   └── session_learning.md     ← Memoria persistente entre sesiones
│                                   Escritura exclusiva del Audit Agent
│
├── logs_veracidad/              ← Generados por el Audit Agent al cerrar cada tarea
│   ├── acciones_realizadas.txt ← Registro cronológico de acciones por agente
│   ├── uso_contexto.txt        ← Eficiencia de contexto y tokens por agente
│   └── verificacion_intentos.txt ← Verificación de requerimientos funcionales
│
└── worktrees/                   ← Celdas de trabajo aisladas (no versionadas)
                                    Una por feature/POC, en rama propia
```

---

## Flujo Completo de una Tarea Nivel 2

```
1. Usuario entrega objetivo
         │
2. Master Orchestrator (Opus)
   └── Valida contra project_spec.md
   └── Infiere equipo necesario
   └── Presenta equipo → confirmación humana
         │
3. Creación del equipo
   ├── SecurityAgent (Opus) — activo desde aquí
   ├── AuditAgent (Sonnet) — activo desde aquí
   └── Domain Orchestrators (Sonnet) — uno por dominio
         │
4. Domain Orchestrator planifica
   └── Carga skill relevante de /skills/
   └── Diseña plan por capas
   └── Somete al gate
         │
5. Gate paralelo (bloqueante)
   ├── SecurityAgent: ¿patrones seguros? ¿sin secretos? ¿RF cubiertos?
   └── AuditAgent: ¿trazabilidad a RF? ¿scope correcto? ¿arquitectura válida?
         │
         ├── RECHAZADO → revisar plan → repetir gate
         │
         └── AMBOS APRUEBAN
                  │
6. git worktree add ./worktrees/<tarea> -b feature/<tarea>
         │
7. Specialist Agents implementan tareas atómicas
   (cada uno con contexto mínimo de su tarea)
         │
8. SecurityAgent Gate 2: revisión del código generado
         │
9. AuditAgent genera logs en /logs_veracidad/
   └── acciones_realizadas.txt
   └── uso_contexto.txt
   └── verificacion_intentos.txt
         │
10. AuditAgent actualiza engram/session_learning.md
         │
11. Merge feature/<tarea> → main (si auditoría: APROBADO)
```

---

## Relación con la Rama `main`

| `agent-configs` | `main` |
|---|---|
| Configuración del sistema de agentes | Código de aplicación |
| CLAUDE.md, skills, registry, engram | Implementación de features |
| No contiene código ejecutable | No contiene config del agente |
| Aislada por diseño | Protegida por `.gitignore` que bloquea archivos de agent-configs |

Los worktrees de trabajo (`./worktrees/feature-*`) se crean desde `agent-configs` en ramas propias y hacen merge directamente a `main` una vez que pasan la auditoría. La config del agente nunca contamina `main`.
