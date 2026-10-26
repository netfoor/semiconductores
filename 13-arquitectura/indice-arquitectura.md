---
titulo: "Arquitectura — índice"
tipo: indice
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, arquitectura]
---

# Arquitectura — índice

**Estado:** pendiente; se trabaja después de definir el problema y los requisitos (G1). Orden de trabajo del documento maestro: problema → evidencia → requisitos → hipótesis → experimento → **arquitectura** → tecnologías.

## Restricciones que ya impone la convocatoria

- Prototipo exhibible en una mesa y no peligroso [F-001 §7.2] (REQ-EXP-02).
- Demo sin depender de electricidad o internet del recinto, con video de respaldo (REQ-DER-01, `#inferencia`; Q-014).
- Explicable en 8–10 minutos por ambos integrantes [§7.3–7.4].
- Cada decisión de diseño se registra con alternativas y razones en [[registro-de-decisiones]] (B2, EV-09).

## Pendiente explícito del documento maestro

Comparar técnicamente procesamiento en la nube frente a inferencia local (edge) **cuando** existan requisitos y datos para hacerlo; la decisión no se toma antes.

## Notas

- [[arquitectura-v1]]: plantilla por diseño con alineación, línea base clásica, procesamiento local y registro de decisiones. Código en `prototipo/`; diseño de la interfaz en `prototipo/DISENO_INTERFAZ.md`.
