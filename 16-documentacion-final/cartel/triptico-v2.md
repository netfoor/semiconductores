---
titulo: "Tríptico v2 para la jornada (150 x 120 cm)"
tipo: entregable
estado: borrador
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-080]
tags: [femeci, cartel, triptico, jornada]
---

# Tríptico v2 para la jornada

Actualiza el [[triptico-v1]] con lo hecho el 29 de octubre. Mismo tamaño (1500 x 1200 mm, dobleces a 50 y 100 cm), misma estructura sugerida para Ingenierías y las mismas reglas de la carta de SECIHTI Puebla del 26 de octubre.

- **Archivo para imprimir:** `triptico-v2.pdf`. Vista previa: `triptico-v2-vista.png`.
- **Cómo se genera:** `uv run --no-project --with segno --with pillow python 16-documentacion-final/cartel/build_triptico.py` (escala del texto 0.99; ningún panel se desborda).

## Cambios frente a v1

| Sección | Cambio | Origen |
|---|---|---|
| Título | Nombres de los tres integrantes, porque cupieron | Indicación de Fortino |
| Introducción | Figura 1: corte SMD frente a THT (ilustración de elaboración propia) | Página del proyecto v2, diseño de María José |
| Metodología | Paso 5: revisión de una unión a la vez; Figura 3 con la pantalla del celular | PR #17; captura de elaboración propia con la tarjeta-mosaico |
| Resultados | Sin cambios (EXP-006). Las figuras se renumeran (1 a 5) | — |
| Conclusiones | «Ya corre en una Raspberry Pi 4, en local y sin internet» sustituye a «falta medir en la Raspberry Pi 4» | Instalación del 29 oct |
| Hacia dónde va | Nueva: apoyo, piloto por planta y automatización gradual | D-016 |
| Creatividad e innovación | Enfocada en el proyecto, no en la demo: plantilla por diseño, confidencialidad y el inspector que enseña al modelo (D-016). «Metas fijadas antes de medir» pasa a Metodología | Indicación de Fortino |
| Justificación | Enfocada en el proyecto: menos defectos que pasan, apoyo y no sustitución, bajo costo frente a una máquina de inspección automática. Se quita la repetición de la confidencialidad | Indicación de Fortino |
| Referencias y nota final | Se quitan la referencia a Anthropic (Claude) y la nota de apoyo de IA; la declaración de uso de IA queda en la bitácora y el protocolo | Indicación de Fortino |

## No incluido, a propósito

- `#hecho` Ningún QR ni página web: la carta prohíbe páginas web y «codificaciones» de los participantes (inciso e) y conexiones a internet (inciso f).
- `#pregunta` El tiempo en la Pi 4 no se reporta: la mediana con la imagen digital fue de 1.27 s, pero la primera foto del iPhone marcó 47.5 s. Falta aclarar la diferencia.
- La tarjeta en capas 3D de la página: compite con la gráfica de resultados en un cartel fijo.

## Pendiente del equipo antes de imprimir

1. Revisar ortografía y reescribir con sus palabras lo que haga falta (punto 6 de la carta).
2. Confirmar con la imprenta el tamaño y el material rígido.
3. La Figura 4 sigue con «foto simulada»; sustituirla si la foto real de la hoja impresa alinea bien.
