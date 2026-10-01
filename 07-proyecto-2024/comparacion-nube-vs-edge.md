---
titulo: "Nube frente a procesamiento local (edge): comparación técnica"
tipo: analisis
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-054, F-059, F-061, F-062, F-063, F-064, F-065, F-066, F-067, F-068, F-069, F-070, F-071, F-072, F-073, F-074]
tags: [femeci, arquitectura, edge, nube, fase-4]
aliases: ["Nube vs edge", "Comparación nube edge"]
---

# Nube frente a procesamiento local (edge): comparación técnica

> [!important] Comparación sin decisión
> El documento maestro pide comparar **sin decidir todavía**. La decisión queda registrada como pendiente (D-009 en [[registro-de-decisiones]]). Se tomará con el experimento de §8, cuando haya un problema elegido y requisitos medibles: tiempo de ciclo, conectividad, política de datos.

Contexto: [[analisis-proyecto-2024]] y [[contenido-presentacion-2024]]. Índice: [[indice-proyecto-2024]].

## 1. Punto de partida: qué hacía el proyecto 2024

- `#hecho` La presentación promete "real-time cloud analytics" y una API conectada a la nube [F-059, diap. 2 y 5]. Su controlador central se comunica directamente con la banda y el brazo [F-059, diap. 6].
- `#inferencia` La captura, el procesamiento con OpenCV y el control de actuadores estaban junto al hardware. La nube (si la hubo, Q-041) guardaba y mostraba resultados. **Ya era un esquema híbrido.**
- Por eso la pregunta útil no es "¿nube o Raspberry Pi?", sino **dónde conviene poner cada función**.

## 2. Funciones a ubicar

| Función | Exigencia de tiempo | Dónde puede vivir | Comentario |
|---|---|---|---|
| Captura de imagen | Sincronizada con la pieza (milisegundos) | Solo local | La cámara está junto a la pieza |
| Preprocesamiento (recorte, corrección de iluminación) | Milisegundos | Local, o en la nube si se sube la imagen completa | Hacerlo local reduce lo que se transmite |
| **Inferencia** (detectar o clasificar) | Dentro del tiempo de ciclo | Local (CPU, acelerador o teléfono) o nube | **Es el punto en disputa** |
| Decisión y acción (avisar al operador, apartar la pieza, detener) | Determinista | Local | Si depende de la red, una caída de internet detiene la estación |
| Registro y trazabilidad | Segundos a minutos | Local con sincronización, servidor de planta o nube | Puede guardarse local y sincronizarse después |
| Tableros y reportes | Minutos | Cualquiera | — |
| Revisión humana y etiquetado | Minutos a horas | Cualquiera; local si las imágenes no pueden salir | Base del dataset propio |
| Entrenamiento del modelo | Horas | PC con GPU, servidor o nube | No se entrena en la Raspberry Pi |
| Distribución de modelos y monitoreo | Días | Servidor o nube | Importa cuando hay varias estaciones |

## 3. Opciones de arquitectura

| Opción | Descripción | Hardware de ejemplo |
|---|---|---|
| **A. Nube** | La estación sube cada imagen; la inferencia y el registro ocurren en un servicio en la nube y el resultado regresa | Cámara + computadora mínima + servicio en la nube |
| **B. Local en CPU** | Captura, inferencia y decisión en una computadora pequeña; registro local | Raspberry Pi 5 (el equipo ya tiene) |
| **C. Local con acelerador** | Como B, con acelerador de IA o inferencia dentro del sensor | AI HAT+ o AI HAT+ 2, AI Camera (IMX500), Jetson Orin Nano Super |
| **D. Híbrida** | Inferencia y decisión locales (B o C). Solo suben resultados, metadatos y una muestra de imágenes para auditar y reentrenar | B o C + nube o servidor |
| **E. Local completa** | Como D, pero el registro y los tableros viven dentro de la red de la planta, sin internet | B o C + servidor local (o la misma Raspberry) |
| **F. Teléfono** | Inferencia en un teléfono Android | Teléfonos del equipo |

Sobre la opción F (`#inferencia`): es útil para inspección asistida a mano, pero menos repetible para una estación fija, porque cambian el encuadre, la iluminación y la temperatura.

## 4. Datos de referencia

| Dato | Valor | Fuente |
|---|---|---|
| Inferencia en Raspberry Pi 5 (CPU), YOLO26n, 640 px, FP32 | **≈ 67 ms por imagen** en formato NCNN (≈ 15 imágenes/s). Otros formatos: OpenVINO 105 ms, ONNX 126 ms, PyTorch 299 ms. mAP50-95 ≈ 0.48 en el benchmark estándar del fabricante, no en tarjetas | F-061 |
| YOLO26 frente a YOLO11 | Sin supresión de no máximos (NMS); hasta 43 % más rápido en CPU (YOLO26n frente a YOLO11n); licencia AGPL-3.0 o empresarial | F-062 |
| Caso publicado: Raspberry Pi 5 + YOLOv11 para tarjetas | 5–10 FPS, ≈ 3 s por tarjeta; sin métricas de exactitud | F-054 |
| AI HAT+ (oct 2024) | 13 TOPS (Hailo-8L) por 70 USD o 26 TOPS (Hailo-8) por 110 USD; PCIe Gen3 | F-064 |
| AI HAT+ 2 (ene 2026) | 130 USD; 40 TOPS (INT4) y 8 GB de RAM; en visión rinde "broadly equivalent" al de 26 TOPS | F-063 |
| AI Camera (sep 2024) | 70 USD; sensor IMX500 de 12.3 MP con inferencia dentro del sensor; 4056×3040 a 10 fps o 2028×1520 a 40 fps | F-065 |
| Jetson Orin Nano Super (dic 2024) | 249 USD; 67 TOPS (dispersos) o 33 TOPS (densos); 7–25 W | F-066 |
| Precio de la Raspberry Pi 5 (USD, lista) | 16 GB: **305** (página oficial, consulta del 2026-10-01). Aumentos del 1 abr 2026: +25 (4 GB), +50 (8 GB), +100 (16 GB), por el precio de la memoria LPDDR4. Precios de feb 2026: 85, 125 y 205. Precios estimados actuales (`#inferencia`): 4 GB ≈ 110 y 8 GB ≈ 175. En México varían por distribuidor e impuestos | F-067, F-068, F-069 |
| Nube en México | Azure México Central (may 2024), Google Cloud Querétaro (dic 2024) y AWS México Central con 3 zonas de disponibilidad (ene 2025), todas en Querétaro | F-070, F-071, F-072 |
| Revisión académica edge/nube (2024) | Edge: menor latencia, menos carga de red, más privacidad; pero cómputo limitado, escalado más difícil y mayor inversión inicial. Nube: escala y potencia, pero más latencia y riesgos de privacidad. Los esquemas híbridos atienden las limitaciones de ambos | F-073 |
| Seguridad en tecnología operacional (NIST, 2023) | La sección 5 trata la seguridad en arquitecturas de red de planta, con énfasis en segmentar y separar la red de producción de las redes corporativas e internet (zonas desmilitarizadas, cortafuegos, compuertas unidireccionales) | F-074 §5 |

## 5. Cálculos ilustrativos

Cálculos propios. Los tamaños de imagen y los volúmenes son **supuestos para dimensionar**, no datos de una planta.

**Tiempo de subida de una imagen a la nube** (segundos = MB × 8 / Mbit/s). No incluye ida y vuelta de red, protocolo, cola ni inferencia en el servidor:

| Tamaño de imagen (`#supuesto`) | 5 Mbit/s de subida | 20 Mbit/s | 100 Mbit/s |
|---|---|---|---|
| 0.5 MB (≈ 1080p comprimida) | 0.80 s | 0.20 s | 0.04 s |
| 2 MB | 3.20 s | 0.80 s | 0.16 s |
| 4 MB (≈ 12 MP de alta calidad) | 6.40 s | 1.60 s | 0.32 s |

**Inferencia local en Raspberry Pi 5 (CPU) según la resolución de entrada.** Se extrapola desde 67 ms a 640 px [F-061], suponiendo que el tiempo crece con el número de píxeles (`#inferencia`; hay que medirlo):

| Lado de entrada | Factor de píxeles | Tiempo estimado | Imágenes/s |
|---|---|---|---|
| 640 px | 1.0 | 67 ms | ≈ 15 |
| 960 px | 2.25 | ≈ 151 ms | ≈ 6.6 |
| 1280 px | 4.0 | ≈ 268 ms | ≈ 3.7 |

Los defectos de tarjeta suelen ser pequeños, así que podría hacer falta más resolución o recortar por regiones (`#inferencia`).

**Volumen hacia la nube con una imagen por tarjeta y 30 días al mes** (`#supuesto`):

| Tarjetas por día | 0.5 MB | 2 MB | 4 MB |
|---|---|---|---|
| 500 | 7.5 GB/mes | 30 GB/mes | 60 GB/mes |
| 2,000 | 30 GB/mes | 120 GB/mes | 240 GB/mes |

**Lectura** (`#inferencia`):
- Con ciclos de varios segundos por tarjeta, cualquier opción podría alcanzar en latencia. Con ciclos de ≈ 1 s o menos y conexiones modestas, subir imágenes completas consume casi todo el presupuesto de tiempo.
- La inferencia local en CPU alcanza para inspección de estación, no para inspección a velocidad de línea.

## 6. Comparación preliminar

Toda la tabla es `#inferencia`, con base en §4 y §5. ✓ favorable · ~ depende o intermedio · ✗ desfavorable.

| Criterio | A. Nube | B. Local CPU | C. Local + acelerador | D. Híbrida | E. Local sin internet | F. Teléfono |
|---|---|---|---|---|---|---|
| Latencia de extremo a extremo | ~ depende de la red y del tamaño de imagen | ✓ en ciclos de segundos | ✓ | ✓ | ✓ | ✓ |
| Variabilidad (determinismo) | ✗ variación de la red | ✓ | ✓ | ✓ | ✓ | ~ sistema operativo y temperatura |
| Funciona sin internet | ✗ | ✓ | ✓ | ✓ (solo se pierden los tableros remotos) | ✓ | ✓ |
| Ancho de banda | ✗ alto | ✓ | ✓ | ✓ bajo (metadatos y muestras) | ✓ nulo hacia fuera | ✓ |
| Confidencialidad de imágenes | ✗ salen de la planta; requiere permiso | ✓ | ✓ | ~ solo muestras con permiso | ✓ | ✓ |
| Seguridad de la red de planta | ✗ conecta la estación a internet [F-074 §5] | ✓ | ✓ | ~ solo tráfico de salida, controlado | ✓ | ~ teléfono personal en planta |
| Capacidad de cómputo y tamaño del modelo | ✓ GPU, modelos grandes | ✗ modelos pequeños | ✓ | igual que B o C | igual que B o C | ~ |
| Exactitud | ✓ sin cuantizar | ~ posible pérdida al optimizar; hay que medirla | ~ requiere convertir a INT8; hay que medirla | igual que B o C | igual que B o C | ~ |
| Costo inicial | ✓ bajo | ~ la Raspberry se encareció, pero ya la tenemos | ✗ mayor | ~ | ~ | ✓ teléfono existente |
| Costo recurrente | ✗ cómputo, almacenamiento y transferencia | ✓ | ✓ | ~ bajo | ✓ | ✓ |
| Varias estaciones y actualizar modelos | ✓ modelo central | ✗ flota de equipos | ✗ flota de equipos | ✓ distribución central | ~ | ~ |
| Riesgo en la mesa de la FEMECI (internet no confirmado, Q-014) | ✗ | ✓ | ✓ | ✓ con datos en caché | ✓ | ✓ |
| Esfuerzo para el equipo en 4 semanas | ✓ el equipo domina la nube | ✓ | ~ convertir modelos al acelerador | ~ más piezas | ✓ | ~ aplicación móvil |

`#inferencia` Ninguna opción gana en todos los criterios. Lo que inclina la balanza son datos del problema que **todavía no tenemos** (§7).

## 7. Lo que decide y aún no sabemos

| Dato que falta | Qué decide | Pregunta |
|---|---|---|
| Tiempo de ciclo por tarjeta en la etapa donde ayudaríamos | Presupuesto de latencia | Q-044 |
| Si la estación tiene red o internet, y si las imágenes pueden salir de la planta | Si la opción A es viable | Q-043, Q-037 |
| Tamaño del defecto frente al campo de visión | Resolución, tiempo de inferencia y tamaño de imagen | Q-035 y medición propia |
| Número de estaciones y de modelos de tarjeta | Necesidad de gestión central (D) | Q-044, Q-036 |
| Frecuencia de reentrenamiento | Dónde entrenar y cómo distribuir modelos | Por definir con el usuario |
| Internet y contacto eléctrico en la mesa de exhibición | Si la demostración puede depender de la red | Q-014 (DME) |

## 8. Experimento para decidir

Borrador: se registrará como EXP-### en `15-experimentos/` cuando se elija el problema.

- **Pregunta:** ¿qué ubicación del procesamiento cumple los requisitos del usuario con la menor complejidad?
- **Variables independientes:**
  - ubicación: B (Raspberry Pi 5, CPU); C (con acelerador, si se consigue); A (servicio en la región de nube más cercana); una laptop como referencia;
  - resolución de entrada: 640 y 1280 px;
  - condición de red: cableada, Wi-Fi o datos móviles, más degradación simulada de retardo y pérdida con `tc netem` de Linux.
- **Variables dependientes:**
  - latencia de extremo a extremo, de la captura a la decisión (p50, p95 y p99);
  - imágenes por segundo;
  - exactitud del **mismo** modelo en cada destino (precisión, sensibilidad, F1; FP32 frente a INT8);
  - disponibilidad: porcentaje de inspecciones completadas con la red caída;
  - energía por inspección (medidor USB);
  - costo por 1,000 inspecciones, calculado con precios del día.
- **Control:**
  - mismo conjunto de prueba (≥ 300 imágenes o la partición de prueba completa), en el mismo orden aleatorio;
  - se descartan las primeras corridas de calentamiento;
  - tres repeticiones;
  - registro con marca de tiempo;
  - código en Python con uv;
  - resultados en `15-experimentos/`.
- **Regla de decisión, fijada antes de medir:** elegir la opción más simple que cumpla:
  1. p95 de latencia ≤ la fracción acordada del tiempo de ciclo;
  2. pérdida de F1 frente a la referencia ≤ el umbral acordado;
  3. si la estación no tiene internet confiable o las imágenes no pueden salir, solo cuentan B, C y E;
  4. costo dentro del presupuesto.

  Los umbrales se fijan con el usuario después de la entrevista y se escriben como requisitos (REQ).
- **Ética y permisos:**
  - no subir imágenes de terceros a la nube sin permiso escrito (REQ-ETI-05, Q-037);
  - si se toman datos en planta, revisar el formato FE-1C (Q-009).

## 9. Conclusión provisional (condicional, sin decidir)

- `#inferencia` **Gana lo local o lo híbrido** (B, C, D o E) en una estación de planta con ciclos de segundos, sin internet garantizado o con imágenes confidenciales.
- `#inferencia` **Gana terreno la nube o lo híbrido** (A o D) si el problema exige modelos grandes, muchas estaciones o análisis central con datos de varias líneas, y si la red y la política de datos lo permiten.
- `#inferencia` En cualquier opción, el entrenamiento ocurre fuera del dispositivo. Para la exhibición del 30 de octubre, el prototipo debería funcionar sin internet o tener un respaldo local (Q-014).
- `#idea-equipo` La hipótesis del documento maestro ("puede tener más sentido ejecutar inferencia localmente") es razonable para una estación de planta, pero **se confirma o descarta con el experimento**.

## 10. Preguntas nuevas

| ID | Pregunta | A quién |
|---|---|---|
| Q-043 | ¿Las estaciones tienen red o internet? ¿Pueden salir imágenes o datos de la planta hacia servicios en la nube, o todo debe quedarse en su red? ¿Qué equipos se permite conectar en la línea? | Yankuilotl (o la planta o laboratorio que se elija) |
| Q-044 | En la etapa donde podríamos ayudar, ¿cuánto tiempo hay por tarjeta? ¿Cuántos modelos de tarjeta pasan por día o por semana? | Yankuilotl (o la planta o laboratorio que se elija) |

Registradas en [[preguntas-pendientes]] y añadidas al bloque 2 de [[guia-contacto-yankuilotl]].
