---
titulo: "Experimentos — índice"
tipo: indice
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, experimentos]
---

# Experimentos — índice

**Estado:** pendiente; primer piloto antes de G2 (14 oct). **Alimenta:** A3, A4 y A5 → EV-06, EV-11, EV-13, EV-14.

## Reglas

- **Planear antes de correr:** pregunta o meta, hipótesis, métricas y criterio de aceptación se registran **antes** de ejecutar; si cambian, se documenta por qué.
- **Registrar todo:** incluidas las corridas fallidas; ningún dato se excluye sin justificación escrita.
- **Reproducibilidad:** entorno de Python gestionado con uv (con archivo de bloqueo), semillas, commit del código y ubicación de datos y resultados crudos.
- **Comparación:** cada experimento tiene línea base o referencia.
- **Bitácora:** cada experimento tiene entrada en la bitácora del día en que se planeó y del día en que se corrió.

## Ficha de experimento (plantilla)

`EXP-###-nombre.md`: objetivo · meta o hipótesis (A3) · variables (independiente, dependiente, controladas) · montaje y equipo · datos (DS-##) · procedimiento · métricas y criterio de aceptación · resultados crudos (ubicación) · análisis (incertidumbre, errores) · conclusión · amenazas a la validez · fecha, responsables y commit.
