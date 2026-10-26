---
titulo: "EXP-001 Línea base humana"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-060]
tags: [femeci, experimento, exp-001]
---

# EXP-001 · Línea base humana

**Objetivo.** Medir qué tan bien detectan defectos los propios integrantes sin ayuda, en las mismas tarjetas y condiciones que el sistema. Es la referencia real de M1 y M2; las cifras de See (2015) solo dan orden de magnitud [F-060].

**Hipótesis o meta.** No es una meta: es la medición contra la que se comparan EXP-002 y EXP-005.

**Variables.** Independiente: inspector. Dependientes: sensibilidad, tasa de falsas alarmas y tiempo por tarjeta. Controladas: tarjetas del conjunto de prueba, iluminación, distancia, lupa o pantalla usada.

**Datos.** Conjunto de prueba de [[DS-01-tarjetas-propias]] (las tarjetas congeladas en `particion.json`).

**Procedimiento.**
1. Cada integrante inspecciona tarjetas que soldó otro integrante, para reducir el recuerdo de dónde sembró defectos.
2. Sin ver la hoja de siembra ni las etiquetas, marca cada unión como aceptable o con su clase de defecto.
3. Se registra el tiempo por tarjeta.
4. Se compara contra las etiquetas de consenso.

**Métricas y criterio.** Sensibilidad y falsas alarmas con IC de Wilson y bootstrap por tarjeta (`metricas.resumen`). No hay criterio de aprobación: se reporta tal cual.

**Amenazas a la validez.** Los inspectores no son técnicos con experiencia industrial; conocen el proyecto; pocas personas (tres).

## Registro

- **Planeado:** 2026-10-26, a partir de [[protocolo-v1]] §6.5. Los criterios de aceptación quedan fijos desde esta fecha; cualquier cambio se anota aquí con fecha y razón antes de ejecutar.
- **Ejecutado:** pendiente.
- **Responsables:** por asignar.
- **Commit del código:** se anota al ejecutar (`git rev-parse HEAD`).
- **Resultados crudos:** `datos/resultados/` (archivo JSON con fecha que genera el comando).
