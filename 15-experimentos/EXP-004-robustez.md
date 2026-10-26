---
titulo: "EXP-004 Robustez a iluminación y posición"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-060]
tags: [femeci, experimento, exp-004]
---

# EXP-004 · Robustez a iluminación y posición

**Objetivo.** Medir cuánto cae la sensibilidad cuando cambian la iluminación o la colocación de la tarjeta.

**Meta (protocolo §5).** **M6:** caída absoluta de sensibilidad ≤ 0.05 respecto de la condición nominal.

**Variables.** Independientes: iluminación (dos niveles y un ángulo adicional) y desplazamiento de la tarjeta en el soporte (±3 mm). Dependiente: sensibilidad.

**Procedimiento.**
1. Capturar las tarjetas de prueba en cada condición (`--iluminacion 2`, `--iluminacion 3`; desplazamientos medidos con regla).
2. Evaluar con el mismo modelo entrenado en condición nominal.
3. Comparar contra la sensibilidad nominal de EXP-002.

**Métricas y criterio.** Cumple si la caída es ≤ 0.05 en cada condición. Se reporta con IC por bootstrap por tarjeta.

**Amenazas a la validez.** Las variaciones probadas no cubren todas las de una planta.

## Registro

- **Planeado:** 2026-10-26, a partir de [[protocolo-v1]] §6.5. Los criterios de aceptación quedan fijos desde esta fecha; cualquier cambio se anota aquí con fecha y razón antes de ejecutar.
- **Ejecutado:** pendiente.
- **Responsables:** por asignar.
- **Commit del código:** se anota al ejecutar (`git rev-parse HEAD`).
- **Resultados crudos:** `datos/resultados/` (archivo JSON con fecha que genera el comando).
