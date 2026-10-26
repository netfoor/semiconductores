---
titulo: "EXP-003 Latencia y ubicación del procesamiento"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-060]
tags: [femeci, experimento, exp-003]
---

# EXP-003 · Latencia y ubicación del procesamiento

**Objetivo.** Medir el tiempo de captura a resultado en la Raspberry Pi 5 sin red y decidir dónde se procesa (D-009).

**Metas (protocolo §5).**
- **M4:** mediana ≤ 5 s y percentil 95 ≤ 8 s por tarjeta.
- **M5:** 100 % de las funciones de captura, inferencia y registro con la red desconectada.

**Procedimiento.**
1. Desconectar la red de la Raspberry Pi y verificarlo.
2. `uv run tht latencia --imagen <captura real> --diseno <diseño> --repeticiones 30` (registra equipo, mediana, p95 y tiempos crudos).
3. Repetir el flujo completo en la interfaz (capturar, inspeccionar, decidir) y anotar si algo falló sin red.
4. El mismo comando calcula el tiempo de subida de esa imagen a 5, 20 y 100 Mbit/s para comparar con la opción en la nube.

**Regla de decisión fijada de antemano.** Se elige la opción más simple que cumpla M4, M5 y la confidencialidad; la nube solo si lo local no cumple M4.

**Amenazas a la validez.** Temperatura y carga del equipo; tamaño de imagen distinto al de la cámara definitiva.

## Registro

- **Planeado:** 2026-10-26, a partir de [[protocolo-v1]] §6.5. Los criterios de aceptación quedan fijos desde esta fecha; cualquier cambio se anota aquí con fecha y razón antes de ejecutar.
- **Ejecutado:** pendiente.
- **Responsables:** por asignar.
- **Commit del código:** se anota al ejecutar (`git rev-parse HEAD`).
- **Resultados crudos:** `datos/resultados/` (archivo JSON con fecha que genera el comando).
