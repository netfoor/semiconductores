---
titulo: "Spec: interfaz v2, centrada en el inspector"
tipo: especificacion
estado: en-curso
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: []
tags: [femeci, interfaz, demo, d-015]
---

# Spec: interfaz v2, centrada en el inspector

Decisión: D-015 (Fortino, 29 oct). Fuente de verdad: el repositorio; el protocolo y la bitácora se actualizan al final del día.

## Objetivo

Que la demostración muestre **el sistema como lo usaría un inspector en una planta**, no la tecnología ni las aclaraciones. Lo técnico, las declaraciones (uso de IA, origen de los datos, formatos, red local) y los detalles de evaluación viven en la bitácora, el protocolo y una página **Acerca de la demostración** (anexo), a un clic.

## Reglas (no negociables)

1. **Nada se oculta, se reubica.** Cada aviso que sale de la pantalla principal queda en «Acerca de la demostración», en la bitácora o en el protocolo.
2. **La demostración se identifica como tal** con una etiqueta discreta «Demostración» en el encabezado, que lleva al anexo. Nunca se presenta un dato sintético o público como dato propio.
3. **Crédito CC BY 4.0** de las fotos de PCBSPDefect: una línea pequeña donde aparecen las fotos (lo exige la licencia).
4. **Menos trabajo para el inspector:** lo que el sistema puede saber o generar no se pregunta.
5. **Tono:** profesional y directo, como se presentaría a un jefe de calidad. Sin frases de máquina («no sale a internet», «usted confirma o corrige cada una»), sin jerga técnica en la pantalla.

## Prioridades

### P1, antes de las 14:20 (lo que se ve en la mesa)

| # | Cambio | Estado |
|---|---|---|
| 1 | **Menú:** la barra de enlaces se vuelve un botón de menú (hamburguesa) con panel lateral | Hecho en v2-1 |
| 2 | **Avisos:** el banner naranja «Datos sintéticos» / «Tarjeta-mosaico» se sustituye por la etiqueta «Demostración» y la página **Acerca de la demostración** (`/acerca`) con: origen de los datos, crédito de PCBSPDefect, uso de IA, detalles técnicos y enlace a experimentos | Hecho en v2-1 |
| 3 | **Nueva inspección** (antes «Capturar desde el celular»): sesión de inspector (se elige una vez de una lista, con turno y estación), número de tarjeta automático, lado e iluminación por omisión, modelo de tarjeta automático si solo hay uno, **un solo botón «Tomar foto»** que envía en cuanto se toma, sin textos de ayuda | Hecho en v2-1 |
| 4 | **Inspección:** encabezado con tarjeta, inspector y resumen («3 uniones por revisar»); textos de operador; quitar el nombre de archivo de la vista principal | Pendiente |
| 5 | **Textos** de Proyecto, Fotos reales, Reto y Experimentos con tono de presentación (por ejemplo, el Reto: «¿Puedes ver lo que ve la red?») | Pendiente |

### P2, si hay tiempo

| # | Cambio |
|---|---|
| 6 | Perfil del inspector: inspecciones de hoy, uniones revisadas y tiempo promedio (de `decisiones.sqlite`) |
| 7 | Historial de inspecciones de la estación |
| 8 | Pantalla de la laptop como «tablero de la estación» mientras el celular captura |

### P3, en la bitácora como próximos pasos

- Datos propios: colaboración con una planta para un piloto (DS-01), que es lo que convierte el prototipo en sistema real.
- Detección: la red solo vio fotos de PCBSPDefect; se reentrena con DS-01 (EXP-002).
- Velocidad: medida en la Raspberry Pi 4 el 30 de octubre (prueba de software).

## Detalle de «Nueva inspección» (P1-3)

- **Inspector:** la primera vez se elige de una lista (`datos/operadores.json`; si no existe, la lista del equipo). Se recuerda en el teléfono y aparece arriba: nombre, turno y estación, con «Cambiar».
- **Tarjeta:** el servidor asigna la siguiente (`T01`, `T02`…) si no se indica. Lado B (soldadura) e iluminación 1 por omisión.
- **Modelo de tarjeta:** si hay uno solo, se usa sin preguntar; si hay varios, se elige de una lista.
- **Foto:** un botón grande «Tomar foto» (en la laptop abre el selector de archivos). Al elegir la foto se envía sola y aparece «Analizando la tarjeta…»; al terminar se abre la inspección.
- **Se quita:** «Elegir de la galería», la nota, el campo de iluminación visible y los textos de ayuda (formatos, HEIC, ubicación). Esa información pasa al anexo y a `MESA.md`.
- **Sin cambios por dentro:** el JPEG original, su huella SHA-256, el manifiesto y los metadatos se guardan igual.
