---
titulo: "EXP-002 Desempeño del sistema"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-060]
tags: [femeci, experimento, exp-002]
---

# EXP-002 · Desempeño del sistema

**Objetivo.** Medir sensibilidad, falsas alarmas y desempeño por clase de la línea base clásica y del clasificador ligero sobre el conjunto de prueba.

**Metas (protocolo §5).**
- **M1:** sensibilidad ≥ 0.90 con límite inferior del IC 95 % (Wilson) ≥ 0.85.
- **M2:** tasa de falsas alarmas ≤ 0.15.

**Variables.** Independiente: modelo (línea base, clasificador ligero). Dependientes: sensibilidad, falsas alarmas, precisión y matriz de confusión. Controladas: mismo conjunto de prueba, mismas etiquetas de consenso, misma alineación.

**Datos.** [[DS-01-tarjetas-propias]]: entrenamiento y validación para ajustar; prueba solo para esta evaluación final.

**Procedimiento.**
1. `uv run tht particion` (una sola vez; congela la prueba).
2. `uv run tht entrenar` y, con el clasificador ligero, su script equivalente.
3. `uv run tht evaluar` sobre `prueba`.
4. Con el clasificador ligero: cinco semillas de entrenamiento; se reportan las cinco.

**Métricas y criterio.** Cumple M1 si sensibilidad ≥ 0.90 y límite inferior de Wilson ≥ 0.85. Cumple M2 si falsas alarmas ≤ 0.15. Se reportan también los IC por bootstrap por tarjeta, el desempeño por clase y ejemplos de falsos positivos y falsos negativos.

**Amenazas a la validez.** Defectos sembrados distintos a los de producción; ruido de etiqueta en la clase "fría"; pocas tarjetas en prueba (IC por clase amplios).

## Registro

- **Planeado:** 2026-10-26, a partir de [[protocolo-v1]] §6.5. Los criterios de aceptación quedan fijos desde esta fecha; cualquier cambio se anota aquí con fecha y razón antes de ejecutar.
- **Ejecutado:** pendiente.
- **Responsables:** por asignar.
- **Commit del código:** se anota al ejecutar (`git rev-parse HEAD`).
- **Resultados crudos:** `datos/resultados/` (archivo JSON con fecha que genera el comando).
