---
titulo: "Registro de decisiones"
tipo: registro
estado: vigente
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, decisiones]
aliases: ["Decisiones", "Registro de decisiones"]
---

# Registro de decisiones

Cada decisión registra contexto, opciones, decisión, razones, consecuencias y quién decidió. Estados: **propuesta** (espera aprobación del equipo) · **adoptada** · **reemplazada por D-###** · **descartada**. Las decisiones no se borran; si cambian, se registra una nueva que reemplaza a la anterior.

## Resumen

| ID | Decisión | Estado | Fecha | Decide |
|---|---|---|---|---|
| D-001 | Estructura y convenciones de la bóveda | Adoptada (revisable) | 2026-10-01 | Claude (IA), por encargo del documento maestro |
| D-002 | Formato de la bitácora | Propuesta (sin respuesta sobre la bitácora manuscrita) | 2026-10-01 | Equipo |
| D-003 | Política de uso de IA | Propuesta (pendiente de aprobación explícita) | 2026-10-01 | Equipo |
| D-004 | Versionado de la bóveda con git | **Adoptada** | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-005 | Modalidad (Ciencias o Ingenierías) | Pendiente (G1) | — | Equipo |
| D-006 | Categoría temática | Pendiente (G1) | — | Equipo |
| D-007 | Líder de Proyecto | **Adoptada: Fortino Romero Mantilla** | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-008 | Asesor institucional y posible asesor científico externo | **Adoptada (asesor institucional): Prof. José Francisco Espinosa Garita**; asesor externo pendiente | 2026-10-01 | Equipo (comunicado por Fortino) |

## D-001 · Estructura y convenciones de la bóveda

- **Contexto:** el documento maestro pide una estructura lógica para convocatoria, rúbrica, investigación, actores, fuentes, proyecto 2024, problemas, entrevistas, ideas, decisiones, arquitectura, experimentos, dataset, bitácora, protocolo y documentación final, y distinguir hechos, inferencias, hipótesis e ideas del equipo.
- **Opciones:** (a) estructura plana con etiquetas; (b) carpetas numeradas en el orden del flujo de trabajo, con una nota índice por carpeta; (c) una nota por fuente desde el inicio.
- **Decisión:** (b), con un registro único de fuentes (que puede dividirse después), IDs estables y etiquetas de tipo de afirmación. Detalle en [[convenciones]] y mapa en [[inicio]].
- **Razones:** trazabilidad para el criterio C3; el orden de carpetas refleja el principio "problema antes que tecnología"; nombres sin acentos ni espacios funcionan bien con git y en cualquier sistema operativo; cada carpeta tiene contenido, así que se conserva aunque se versione.
- **Consecuencias:** las notas nuevas siguen las convenciones; el equipo puede cambiarlas registrando una nueva decisión.

## D-002 · Formato de la bitácora (propuesta)

- **Contexto:** Puebla exige una "Bitácora de Investigación: registro cronológico de actividades" en PDF [F-001 §5] y evalúa su "coherencia y evidencia cronológica" (C3). Otro capítulo estatal exige bitácora manuscrita presente en el stand [F-004]. Puebla no especifica el formato (Q-006).
- **Opciones:** (a) solo digital en la bóveda, exportada a PDF; (b) bitácora manuscrita oficial + bitácora digital detallada; (c) solo manuscrita.
- **Propuesta:** (b) hasta que la DME responda. La manuscrita (cuaderno cosido, páginas numeradas, entradas fechadas con responsable, sin arrancar hojas) es el documento oficial que resguarda el líder; la digital ([[bitacora-indice]]) guarda el detalle, los enlaces y la evidencia, y la manuscrita la referencia.
- **Razones:** cubre ambos escenarios sin rehacer trabajo; la versión digital facilita la trazabilidad con datos y decisiones.
- **Si la DME acepta bitácora digital:** se puede simplificar a (a).

## D-003 · Política de uso de IA (propuesta)

- **Contexto:** la convocatoria descalifica por "suplantación de autoría" [§9.1], exige que solo los estudiantes expongan y respondan [§7.4] y evalúa el "manejo ético de la información" (B3). Otro capítulo estatal prohíbe redactar con IA generativa la justificación, la metodología, los resultados o las conclusiones y exige declarar su uso [F-004]. Este proyecto usa a Claude (IA) como apoyo de investigación y documentación.
- **Propuesta:**
  1. Fortino e Israel redactan todo lo entregable: protocolo, F-01, cartel, guion y bitácora oficial.
  2. La IA apoya en búsqueda, organización, revisión crítica, depuración de código y preparación de preguntas; no redacta secciones de entregables.
  3. Toda afirmación aportada por la IA se verifica contra la fuente original antes de usarse.
  4. Las notas de la bóveda indican su autor; la bitácora registra cuándo y para qué se usó IA.
  5. El protocolo incluye una declaración breve de uso de herramientas de IA en la metodología, ajustada a lo que responda la DME (Q-010).
- **Razones:** protege contra descalificación, fortalece B3 y obliga a dominar el contenido para la defensa (C1, C2).

## D-004 · Versionado de la bóveda con git (adoptada)

- **Contexto:** C3 evalúa la evidencia cronológica; un historial de versiones da sellos de tiempo verificables y respaldo.
- **Decisión (2026-10-01, ≈ 09:08):** el equipo decide versionar la bóveda con git.
- **Implementación (2026-10-01, ≈ 09:10):** repositorio local en la carpeta `semiconductores/` (la carpeta padre `ObsidianVault/` no es un repositorio), rama `main`, `.gitignore` para archivos locales de Obsidian y del sistema. Primer commit: estado al cierre de la Fase 1. Autor de los commits: Fortino Romero Mantilla; los commits preparados con apoyo de IA llevan la línea `Co-Authored-By: Claude`.
- **Nota técnica:** para que git pueda borrar sus archivos temporales y de bloqueo desde la sesión de trabajo de Claude se habilitó el borrado en esta carpeta durante la sesión; solo se usa para archivos internos de `.git`.
- **Pendiente:** remoto privado (por ejemplo, GitHub) y si el código del prototipo irá en un repositorio aparte.

## D-005 · Modalidad (pendiente, G1)

Opciones y criterios en [[analisis-estrategico-convocatoria]] §3. Se decide al elegir el problema.

## D-006 · Categoría temática (pendiente, G1)

Opciones y criterios en [[analisis-estrategico-convocatoria]] §3. Considerar la fase nacional, donde se compite por categoría [F-003].

## D-007 · Líder de Proyecto (adoptada)

- **Decisión (2026-10-01):** **Fortino Romero Mantilla** es el Líder de Proyecto: responsable del registro formal, del canal oficial de comunicación y del resguardo de la bitácora [§3.3].
- **Equipo registrado:** Fortino Romero Mantilla (líder) e Israel Jesus Garcia Osorio. Los integrantes registrados son irremplazables [§3.3].
- **Avance:** el líder creó la cuenta en la plataforma de registro el 2026-10-01.

## D-008 · Asesor institucional y asesor científico externo (adoptada en parte)

- **Decisión (2026-10-01):** asesor institucional: **Prof. José Francisco Espinosa Garita** (UTP) [§3.5].
- **Pendiente:** justificar la congruencia de su perfil con la temática cuando se defina el problema; confirmar su disponibilidad para revisar el protocolo (14 oct) y firmar F-02 (15–16 oct) (Q-019).
- **Asesor científico externo** (universidad, centro de investigación o industria, opcional y recomendado para temas especializados [§3.6]): pendiente; se evaluará con los contactos del sector (Q-024).
