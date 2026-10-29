---
titulo: "Estado del proyecto y cómo continuar (29 oct, noche)"
tipo: seguimiento
estado: vigente
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, estado, continuidad]
---

# Estado del proyecto y cómo continuar

Nota de traspaso, escrita al cerrar la sesión en la nube del 29 de octubre. El trabajo sigue en local (Claude Desktop o Claude Code). Lo que no esté aquí, en [[pendientes]], en la bitácora o en el código **no existe**: la memoria del agente no se conserva entre sesiones.

## Para una sesión nueva: leer en este orden

1. `CLAUDE.md` (raíz): reglas de la bóveda y el orden de lectura completo.
2. Esta nota y [[pendientes]], que es la lista viva con responsables.
3. Última entrada de la bitácora, [[2026-10-29]] (sesiones 1 a 4), y [[bitacora-indice]].
4. Decisiones recientes en [[registro-de-decisiones]]: **D-015** (interfaz centrada en el inspector) y **D-016** (el inspector se queda; automatización gradual).
5. Las especificaciones en curso: [[spec-interfaz-v2]] y [[spec-landing-v2]]. Primero se escribe la especificación y después se implementa (indicación de Fortino).

## Dónde estamos

- `#hecho` **Jornada:** viernes 30 de octubre de 2026, de 9:30 a 18:00, en el Centro de Vinculación UPAEP. El montaje es a las 7:30 y la revisión, de 8:45 a 9:00. La Raspberry Pi 4 se recoge el 29 de octubre a las 14:20.
- `#hecho` **Rama `main`:** contiene todo lo hecho hasta esta nota (PR del 29 de octubre). No quedan ramas con trabajo sin fusionar.
- `#hecho` **Pruebas:** 77 pasan (`cd prototipo && uv run pytest -q`).
- **Prototipo (`prototipo/`):**
  - Estación Flask `inspeccion_tht`.
  - Red de EXP-006 en ONNX.
  - Alineación por homografía y normalización de color.
  - Tarjeta-mosaico (`make mosaico`).
  - Paquete para la Pi sin internet (`make paquete-pi`).
  - La inspección tarda de 0.3 a 0.4 s en el contenedor. En la Pi falta medirla.
- **Interfaz v2 (D-015):** la prioridad P1 está completa (puntos 1 a 5 de [[spec-interfaz-v2]]):
  - menú lateral;
  - etiqueta «Demostración» con el anexo `/acerca`;
  - perfiles de inspector;
  - número de tarjeta automático;
  - un solo botón «Tomar foto»;
  - inspección con cifras y cierre.
- **Página del proyecto v2:**
  - Hechas:
    - L2, el recorrido «Del diseño a la tarjeta revisada», con la tarjeta en capas 3D, THT frente a SMD y la barra de proceso.
    - L4, «La estación en uso», con seis capturas del celular en un marco de teléfono dibujado en CSS. El inspector del ejemplo es María José de la Rosa.
    - L6, «Hacia dónde va» (D-016).
  - Pendientes: L1, L3 y L5.
- **Documentos para la jornada:**
  - Tríptico v1 (`16-documentacion-final/cartel/build_triptico.py`). María José lo reescribe con sus palabras y lo imprime.
  - Guía de la Raspberry Pi (`16-documentacion-final/jornada/guia-raspberry-pi.pdf`).
- `#supuesto` La Raspberry Pi entregada tiene sistema de 64 bits y Python 3.11 a 3.13; se revisa al recibirla (guía §2).

## Lo siguiente, en orden

Detalle y responsables en [[pendientes]].

1. **Pi y mesa:** seguir [[guia-raspberry-pi]]:
   - `make paquete-pi` y copiar el paquete a la USB;
   - revisar `aarch64` y Python en la Pi;
   - `bash instalar.sh` y `bash probar.sh`, y anotar el tiempo medido;
   - imprimir el mosaico en color y probar con el celular.
2. **Protocolo y bitácora finales (esta noche):** incorporar la interfaz v2, D-015, D-016, la Pi 4, el paquete sin internet, el mosaico y la página v2. Los PDF del expediente están en `16-documentacion-final/expediente/` y se regeneran desde la bóveda.
3. **Exposición:** guion de 8 a 10 minutos con la defensa de D-016, banco de preguntas y video de respaldo.
4. **Página v2:**
   - L5: resultados con cifras grandes y «en qué se equivoca» (#22). Aplicar la skill `dataviz` y la skill `ui-minimal`.
   - L1: portada con el celular (#21).
   - L3: acortar «El problema» (#23).
5. **Despliegue:** comprobar femeci.foor.dev tras el merge (#14).

## Cómo trabajar en local

- **Prototipo:** `cd prototipo && make ayuda` lista las tareas. Python siempre con `uv`.
- **Ver la estación con el mosaico:** `make mosaico` y `uv run tht servir --datos datos-mosaico --modelo red --puerto 8000`. Después abrir `http://127.0.0.1:8000/` (la página del proyecto) y `/capturar`.
- **Capturas de «La estación en uso»:** `prototipo/herramientas/capturas_uso.js` (Playwright; instrucciones en su encabezado).
- **Protocolo y bitácora en PDF:** los generadores están en `12-protocolo/herramientas/` (los PDF van a `16-documentacion-final/expediente/`):
  - Protocolo: `uv run --with python-docx python build.py ENTRADA.md SALIDA.pdf`.
  - Bitácora: `python exportar_bitacora.py SALIDA.md`, que junta las entradas en un solo Markdown para convertirlo a PDF.
- **Guía de la Raspberry Pi en PDF:** `16-documentacion-final/jornada/guia_pdf.js` (instrucciones en su encabezado).
- **Tríptico:** `uv run python 16-documentacion-final/cartel/build_triptico.py`. En Canva quedó una copia del PDF en «Cargas»; hay que abrirla para que Canva la convierta.
- **Skill de diseño:** la skill `ui-minimal` se actualizó con dos secciones nuevas: «Interfaces de producto y demostraciones» y «Recorridos con scroll». Falta subirla a claude.ai (#24).

## Reglas que siguen vigentes

- No nombrar a empresas concretas.
- No subir imágenes de empresas a la nube (D-011).
- Los datos sintéticos o públicos se identifican como tales.
- La etiqueta «Demostración», el anexo `/acerca` y el crédito CC BY 4.0 de PCBSPDefect se conservan (reglas de D-015).
- No se reportan resultados que no se midieron. La prueba con el mosaico es de software, no un experimento.
- Las entradas de la bitácora llevan la fecha real; no se fechan hacia atrás.
- Los commits van a nombre de Fortino (D-013).
- No se reescribe el historial (sin rebase ni force-push).
- El tríptico no lleva QR, logotipos ni páginas web de los participantes (inciso e de las recomendaciones de SECIHTI).
- Las respuestas del Reto no se guardan en el servidor.
