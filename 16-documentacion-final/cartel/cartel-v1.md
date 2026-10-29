---
titulo: "Cartel v1 para la jornada (90 x 120 cm)"
tipo: entregable
estado: sustituido
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-080]
tags: [femeci, cartel, jornada]
---

# Cartel v1 para la jornada

> Sustituido por [[triptico-v1]] (150 x 120 cm), según las recomendaciones de la SECIHTI Puebla del 26 de octubre.

- **Archivo para imprimir:** `cartel-v1.pdf`, una página de 900 x 1200 mm (vertical, convocatoria §7.2), con fuentes incrustadas. Vista previa: `cartel-v1-vista.png`.
- **Cómo se genera:** `uv run --no-project --with segno --with pillow python 16-documentacion-final/cartel/build_cartel.py`. Las cifras salen de `resultados.json` de EXP-006, no se escriben a mano, así que el cartel coincide con el protocolo (§8.1) y con femeci.foor.dev.
- **Fuente tipográfica:** Inter, licencia SIL OFL 1.1 (`fuentes/OFL.txt`).
- **Fotos:** cinco uniones del conjunto de prueba de PCBSPDefect, CC BY 4.0, sin modificar, con su atribución en el cartel. Miden 280 px, así que impresas a unos 16 cm se ven algo suaves; vistas a 1 o 2 m no se nota.
- **QR:** lleva a https://femeci.foor.dev. Verificado leyendo el PDF.

## Estructura (narrativa de C1)

Problema → reto y metas → propuesta (5 pasos y las clases) → resultado preliminar (EXP-006, con IC y la advertencia sobre M2) → lo que sigue → pruébelo (QR) → declaración de IA → referencias.

## Pendiente del equipo antes de imprimir

1. `#pregunta` La convocatoria descalifica por suplantación de autoría (§9.1) y REQ-DER-05 pide que el equipo redacte los entregables. Este borrador lo armó Claude (IA): el equipo debe revisar y reescribir los textos con sus palabras y poder explicar cada cifra.
2. Decidir si se agregan logotipos (UTP, FEMECI o SECIHTI) y conseguir los archivos oficiales; no se inventaron.
3. Si hay foto del soporte o de la estación armada, sustituir o complementar las fotos de ejemplo.
4. Confirmar con la imprenta el formato (PDF a tamaño real) y si el cartel se cuelga o necesita soporte (Q-014).
