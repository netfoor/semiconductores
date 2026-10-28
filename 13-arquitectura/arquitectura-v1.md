---
titulo: "Arquitectura del prototipo v1"
tipo: especificacion
estado: borrador
creado: 2026-10-26
actualizado: 2026-10-28
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
| Captura | `captura.py` | Toma la foto (Picamera2, cámara USB, archivo o foto de celular), la guarda en PNG sin pérdida con nombre `T07_B_il1_<fecha>.png`, escribe sus metadatos y la agrega al manifiesto |
| Captura por celular | `app.py` (`/capturar`), `captura.CamaraMemoria` | Recibe una foto JPEG del celular por la red local de la mesa, conserva el original y lo pasa por la misma captura (§7) |
| Integridad | `manifiesto.py` | Huella SHA-256 de cada imagen cruda y verificación posterior |
| Alineación | `plantilla.py` | ECC (correlación de intensidades, transformación euclidiana) sobre versiones reducidas; si no converge, puntos ORB con RANSAC |
| Línea base | `linea_base.py` | Nueve características por recorte (brillo, áreas, componentes, circularidad, extensión, rugosidad) y clasificador de centroides |
| Datos | `anotaciones.py`, `particion.py`, `datos.py` | Etiquetas por persona, kappa y consenso; partición por tarjeta con huella del conjunto de prueba |
| Evaluación | `metricas.py` | Sensibilidad, falsas alarmas, Wilson, bootstrap por tarjeta, McNemar |
| Latencia | `latencia.py` | Mediana y percentil 95, y estimación de subida a un servicio remoto |
| Operación | `app.py`, `registro.py` | Interfaz local y registro de decisiones en SQLite |

## 4. Flujo de una inspección

1. El operador coloca la tarjeta en el soporte y captura (cámara de la estación o celular, §7).
2. La captura se alinea contra la referencia del diseño (`alineacion_s`).
3. Se recorta cada unión con un margen de 15 % y se calculan sus características (`caracteristicas_s`).
4. El clasificador sugiere una clase por unión y un puntaje de defecto (`clasificacion_s`).
5. La interfaz muestra solo las sospechosas, ordenadas por puntaje. El operador confirma o corrige cada una; cada decisión se guarda con su tiempo.

Medición inicial con datos **sintéticos** en el contenedor de desarrollo (no en la Raspberry Pi, no es resultado): unos 0.1 s por tarjeta de 40 uniones. La medición válida para M4 es EXP-003 en el hardware objetivo.

## 5. Dónde se procesa (D-009)

La arquitectura inicial es **local completa**: captura, inferencia, interfaz y registro en el mismo equipo, sin red (opción B o E de [[comparacion-nube-vs-edge]]). Es una hipótesis: EXP-003 la confirma o la descarta con la regla fijada en el protocolo (la opción más simple que cumpla latencia, operación sin internet y confidencialidad; la nube solo si lo local no cumple M4). La interfaz escucha en `127.0.0.1` por omisión, de modo que no queda expuesta a la red de la planta [F-074 §5]. La captura por celular (§7) agrega una red local **sin internet** entre el teléfono y la laptop; no cambia la opción: el procesamiento sigue en el mismo equipo.

## 6. Lo que falta

- ~~Clasificador ligero~~ Hecho el 26 oct: red convolucional pequeña (PyTorch para entrenar, ONNX Runtime para inferir en la Pi), cinco semillas, modelo elegido por validación. Falta entrenarlo y evaluarlo con DS-01.
- Soporte físico, iluminación difusa y cámara definitiva: resolución y distancia se fijan en la ficha del montaje.
- Calibrar un umbral de puntaje con el conjunto de validación, si hace falta equilibrar M1 y M2 (la función `inspeccionar` ya acepta `umbral`).
- Probar la captura por celular (§7) con teléfonos reales, Android e iPhone.

## 7. Captura desde un celular (agregado el 2026-10-27)

Componente para la jornada del 30 de octubre: un celular sirve de cámara sin instalar ninguna app. Bitácora: [[2026-10-27]]. Guía de operación: `prototipo/MESA.md`.

```
celular (navegador) ──HTTP, hotspot propio con contraseña, sin internet──▶ laptop Ubuntu
  /capturar: <input type="file" capture="environment">                      tht servir --host 0.0.0.0
                                                                            CamaraMemoria → captura.capturar
                                                                            crudos/ + MANIFIESTO.csv → inspección
```

| Aspecto | Diseño | Tipo |
|---|---|---|
| Sin app | La página usa el selector de archivos con `capture="environment"`, que abre la cámara del sistema a resolución completa. No usa `getUserMedia`, que exige HTTPS; por eso funciona sobre HTTP en la red local | `#inferencia` (comportamiento documentado de los navegadores; falta probar en teléfonos reales) |
| Una sola lógica de captura | `CamaraMemoria` decodifica el JPEG con `cv2.imdecode` y entra a `captura.capturar`: mismo nombre, mismo JSON, mismo manifiesto | `#hecho` (código y pruebas) |
| Integridad del original (RA-04) | El JPEG se guarda sin modificar junto al PNG, con el mismo nombre y su propia huella. La huella del JPEG prueba lo que generó la cámara; la del PNG, la copia que se procesa | `#hecho` (pruebas) |
| Orientación | OpenCV 5.0 aplica la orientación EXIF al decodificar; una prueba lo fija para detectar si una versión distinta lo cambia | `#hecho` (prueba del 27 oct) |
| Metadatos | `camara: "celular"`, marca y modelo del EXIF (lector propio, sin Pillow), orientación, `tiene_gps` y User-Agent | `#hecho` |
| Formatos | Solo JPEG, hasta 30 MB; HEIC se rechaza con instrucciones para el iPhone | `#hecho` |
| Ubicación (GPS) | No se borra del original, para no alterar su huella; se marca en el JSON, la página avisa y la guía pide desactivar la ubicación de la cámara | Elección aprobada por Fortino al aprobar el plan |
| Exposición en red (RA-02) | Solo en la estación local: con `en_linea=True` la ruta no existe y la demo pública no recibe fotos (D-011). `127.0.0.1` sigue siendo el valor por omisión; `0.0.0.0` solo con `make mesa` en un hotspot propio con contraseña [F-074 §5] | `#hecho` (pruebas) |
| Contenedor | `make docker-mesa` usa la imagen de Railway con el comando `tht servir` en modo local, sin cambiar `wsgi.py` | `#hecho` (probado en la laptop de Fortino) |

- `#inferencia` La subida por Wi-Fi agrega tiempo entre la captura y el resultado; EXP-003 tendría que medirlo aparte si se adopta la desviación propuesta en [[EXP-003-latencia-y-ubicacion]].
- `#supuesto` Chrome en Android conserva el EXIF al subir y Safari en iPhone entrega JPEG; se verifica con teléfonos reales antes del 30 de octubre.
