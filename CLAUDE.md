# Bóveda FEMECI-PUEBLA 2026 (semiconductores)

Bóveda de Obsidian versionada con git (D-004). Es la fuente persistente del proyecto: las decisiones importantes viven aquí, no en la memoria del agente.

## Leer al empezar, en este orden

1. `00-contexto/INSTRUCCIONES_PROYECTO.md`: documento maestro (rol, objetivo, fases, reglas de trabajo).
2. `00-contexto/convenciones.md`: etiquetas (`#hecho`, `#inferencia`, `#supuesto`, `#hipotesis`, `#idea-equipo`, `#pregunta`), identificadores (F-###, D-###, Q-###), frontmatter y estilo de notas.
3. `00-contexto/inicio.md`: mapa del proyecto, equipo y estado por fase.
4. `11-decisiones/registro-de-decisiones.md`: decisiones tomadas.
5. `02-bitacora/`: última entrada y `bitacora-indice.md`, para saber en qué quedó el trabajo.

## Reglas

- Escribir en español. Toda afirmación relevante lleva etiqueta y cita a una fuente del registro (`03-fuentes/registro-de-fuentes.md`).
- No elegir proyecto ni tecnología por preferencia: la decisión es del equipo.
- Cada sesión de trabajo se registra en `02-bitacora/` (evidencia cronológica exigida por la convocatoria).
- Python: usar `uv`.
- Autoría: las notas hechas por IA llevan `autor: "Claude (IA)"`; el equipo las revisa (`revisado_por`).
- Usar enlaces `[[wikilink]]` entre notas; actualizar `inicio.md` si cambia el estado de una fase.
