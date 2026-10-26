---
titulo: "EXP-005 Inspección asistida frente a no asistida"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-060]
tags: [femeci, experimento, exp-005]
---

# EXP-005 · Inspección asistida frente a no asistida (exploratorio)

**Objetivo.** Ver si las marcas del sistema ayudan a los integrantes a detectar más defectos que sin ayuda.

**Meta (protocolo §5).** **M3:** sensibilidad asistida ≥ sensibilidad no asistida, en las mismas tarjetas. Exploratoria.

**Procedimiento.**
1. Después de EXP-001 y con al menos una semana de separación, cada integrante inspecciona las mismas tarjetas en la interfaz ("Inspeccionar"), que registra cada decisión y su tiempo en `decisiones.sqlite`.
2. Se cruzan las decisiones con las etiquetas de consenso.

**Análisis.** Prueba exacta de McNemar sobre las uniones defectuosas (`metricas.mcnemar_exacto`), con el número de defectos que solo detectó cada modalidad. Se reporta también el tiempo por tarjeta.

**Amenazas a la validez.** Tres personas; efecto de aprendizaje entre EXP-001 y EXP-005; los inspectores conocen el sistema.

## Registro

- **Planeado:** 2026-10-26, a partir de [[protocolo-v1]] §6.5. Los criterios de aceptación quedan fijos desde esta fecha; cualquier cambio se anota aquí con fecha y razón antes de ejecutar.
- **Ejecutado:** pendiente.
- **Responsables:** por asignar.
- **Commit del código:** se anota al ejecutar (`git rev-parse HEAD`).
- **Resultados crudos:** `datos/resultados/` (archivo JSON con fecha que genera el comando).
