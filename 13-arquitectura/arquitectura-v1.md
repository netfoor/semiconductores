---
titulo: "Arquitectura del prototipo v1"
tipo: especificacion
estado: borrador
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-061, F-073, F-074]
tags: [femeci, arquitectura, prototipo, ic-01]
aliases: ["Arquitectura v1"]
---

# Arquitectura del prototipo v1

Diseño técnico de la estación de inspección asistida (IC-01, D-011). Responde a las metas M1 a M6 de [[protocolo-v1]] §5. El código está en `prototipo/` y su manual en `prototipo/README.md`.

## 1. Requisitos que manda el problema

| ID | Requisito | De dónde sale |
|---|---|---|
| RA-01 | La persona decide; el sistema solo marca | Humano en el ciclo, protocolo §3 |
| RA-02 | Funciona sin internet | M5; confidencialidad de imágenes de planta (D-011); internet del recinto no garantizado (Q-014) |
| RA-03 | Latencia por tarjeta con mediana ≤ 5 s en Raspberry Pi 5 | M4 |
| RA-04 | Datos crudos inmutables y verificables | REQ-DER-02; F-001 §9.1 |
| RA-05 | Conjunto de prueba independiente, fijado antes de entrenar | A4; protocolo §6.3 |
| RA-06 | Cada decisión del operador queda registrada | EXP-005; trazabilidad |
| RA-07 | Tolera el desplazamiento de la tarjeta en el soporte (±3 mm) | M6, EXP-004 |

## 2. Decisión principal: plantilla por diseño en lugar de un detector

- `#inferencia` En una estación de revisión se inspecciona siempre el mismo diseño de tarjeta durante un lote. Las uniones están en posiciones fijas del diseño.
- **Opción elegida:** marcar una vez las uniones sobre una imagen de referencia del diseño, alinear cada captura contra esa referencia y recortar cada unión.
- **Alternativa descartada por ahora:** un detector de objetos (por ejemplo, YOLO) que busque las uniones en cada imagen. Pide muchas más etiquetas (cajas en cada imagen), es más lento en CPU [F-061] y su licencia (AGPL) obliga a publicar el código bajo la misma licencia.
- **Consecuencia:** el problema se reduce a clasificar recortes, que necesita menos datos y se puede medir unión por unión. Si un diseño cambia, se crea una plantilla nueva en minutos desde la interfaz.

## 3. Componentes

| Componente | Módulo | Qué hace |
|---|---|---|
| Captura | `captura.py` | Toma la foto (Picamera2, cámara USB o archivo), la guarda en PNG sin pérdida con nombre `T07_B_il1_<fecha>.png`, escribe sus metadatos y la agrega al manifiesto |
| Integridad | `manifiesto.py` | Huella SHA-256 de cada imagen cruda y verificación posterior |
| Alineación | `plantilla.py` | ECC (correlación de intensidades, transformación euclidiana) sobre versiones reducidas; si no converge, puntos ORB con RANSAC |
| Línea base | `linea_base.py` | Nueve características por recorte (brillo, áreas, componentes, circularidad, extensión, rugosidad) y clasificador de centroides |
| Datos | `anotaciones.py`, `particion.py`, `datos.py` | Etiquetas por persona, kappa y consenso; partición por tarjeta con huella del conjunto de prueba |
| Evaluación | `metricas.py` | Sensibilidad, falsas alarmas, Wilson, bootstrap por tarjeta, McNemar |
| Latencia | `latencia.py` | Mediana y percentil 95, y estimación de subida a un servicio remoto |
| Operación | `app.py`, `registro.py` | Interfaz local y registro de decisiones en SQLite |

## 4. Flujo de una inspección

1. El operador coloca la tarjeta en el soporte y captura.
2. La captura se alinea contra la referencia del diseño (`alineacion_s`).
3. Se recorta cada unión con un margen de 15 % y se calculan sus características (`caracteristicas_s`).
4. El clasificador sugiere una clase por unión y un puntaje de defecto (`clasificacion_s`).
5. La interfaz muestra solo las sospechosas, ordenadas por puntaje. El operador confirma o corrige cada una; cada decisión se guarda con su tiempo.

Medición inicial con datos **sintéticos** en el contenedor de desarrollo (no en la Raspberry Pi, no es resultado): unos 0.1 s por tarjeta de 40 uniones. La medición válida para M4 es EXP-003 en el hardware objetivo.

## 5. Dónde se procesa (D-009)

La arquitectura inicial es **local completa**: captura, inferencia, interfaz y registro en el mismo equipo, sin red (opción B o E de [[comparacion-nube-vs-edge]]). Es una hipótesis: EXP-003 la confirma o la descarta con la regla fijada en el protocolo (la opción más simple que cumpla latencia, operación sin internet y confidencialidad; la nube solo si lo local no cumple M4). La interfaz escucha en `127.0.0.1` por omisión, de modo que no queda expuesta a la red de la planta [F-074 §5].

## 6. Lo que falta

- ~~Clasificador ligero~~ Hecho el 26 oct: red convolucional pequeña (PyTorch para entrenar, ONNX Runtime para inferir en la Pi), cinco semillas, modelo elegido por validación. Falta entrenarlo y evaluarlo con DS-01.
- Soporte físico, iluminación difusa y cámara definitiva: resolución y distancia se fijan en la ficha del montaje.
- Calibrar un umbral de puntaje con el conjunto de validación, si hace falta equilibrar M1 y M2 (la función `inspeccionar` ya acepta `umbral`).
