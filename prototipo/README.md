# Estación de inspección asistida de uniones through-hole

Prototipo del proyecto FEMECI-PUEBLA 2026 (modalidad Ingenierías). El sistema alinea la foto de una tarjeta contra una referencia, recorta cada unión soldada, la clasifica y marca las sospechosas; **la persona decide**. Todo corre en local, en una Raspberry Pi 5 o en una laptop, sin internet.

El diseño experimental está en el protocolo (`12-protocolo/protocolo-v1.md`), la arquitectura en `13-arquitectura/arquitectura-v1.md` y las fichas de los experimentos en `15-experimentos/`.

## Instalación

Requiere [uv](https://docs.astral.sh/uv/) y Python 3.12 o superior.

```bash
cd prototipo
uv sync
uv run pytest          # pruebas automáticas
uv run tht --help      # comandos disponibles
make                   # objetivos de operación de la mesa (ver MESA.md)
```

En la Raspberry Pi, la cámara se usa con Picamera2, que viene con Raspberry Pi OS (`sudo apt install python3-picamera2`). Para que el entorno de uv la vea, cree el entorno con `uv venv --system-site-packages`. Sin Picamera2 se usa cualquier cámara USB vía OpenCV.

## Flujo de trabajo

| Paso | Comando | Experimento |
|---|---|---|
| 1. Crear carpetas | `uv run tht iniciar --datos datos` | |
| 2. Capturar cada tarjeta por ambos lados | `uv run tht capturar --tarjeta T01 --lado B --iluminacion 1 --responsable fortino`, o desde un celular en `/capturar` (ver abajo) | DS-01 |
| 3. Verificar que los crudos no cambiaron | `uv run tht manifiesto verificar datos/crudos` | |
| 4. Crear el diseño de tarjeta y marcar sus uniones | `uv run tht servir --datos datos` y luego "Crear diseño" | |
| 5. Etiquetar por separado (dos personas, a ciegas) | En la interfaz: "Etiquetar" | DS-01 |
| 6. Medir el acuerdo entre etiquetadores | `uv run tht acuerdo --a fortino --b israel` | DS-01 |
| 7. Congelar la partición por tarjeta | `uv run tht particion` | |
| 8. Entrenar la línea base | `uv run tht entrenar` | EXP-002 |
| 8b. Entrenar el clasificador ligero (5 semillas) | `uv run --group cnn tht entrenar-red` | EXP-002 |
| 9. Evaluar en el conjunto de prueba | `uv run tht evaluar --modelo linea_base` y `uv run --group cnn tht evaluar --modelo red` | EXP-002 |
| 10. Medir la latencia | `uv run tht latencia --imagen ... --diseno ...` | EXP-003 |
| 11. Inspección asistida | En la interfaz: "Inspeccionar" | EXP-005 |

Las etiquetas finales (`consenso`) se forman con las de dos personas; donde no coinciden, deciden juntas y lo registran.

## Captura desde un celular

Un celular Android o iPhone sirve como cámara **sin instalar ninguna app**: abre `http://<IP de la laptop>:8000/capturar` en la red local de la mesa, toma la foto con la cámara del sistema (o la elige de la galería, para fotos en modo manual) y la sube. Todo el procesamiento ocurre en la laptop, sin internet.

```bash
make mesa DATOS=datos     # tht servir --host 0.0.0.0; imprime la URL del celular
make url                  # solo la URL (y un QR si está instalado qrencode)
```

- La página existe solo en la estación local; la demostración en línea no recibe fotos.
- Se guarda el JPEG **original sin modificar** (`T07_B_il1_<fecha>.jpg`) junto a la copia PNG que se procesa, cada uno con su huella en `MANIFIESTO.csv`: la huella del JPEG prueba lo que generó la cámara y la del PNG, la copia que usa el sistema. El JSON registra `camara: "celular"`, el modelo del teléfono si el EXIF lo trae, la orientación, si la foto trae ubicación (GPS) y el User-Agent.
- Solo JPEG, hasta 30 MB. HEIC (iPhone) se rechaza con instrucciones: Ajustes > Cámara > Formatos > «Más compatible».
- `cv2.imdecode` aplica la orientación EXIF: una foto vertical se guarda derecha (hay una prueba que lo verifica).
- Si al capturar se elige el diseño de tarjeta, o si solo existe uno, la página lleva directo a inspeccionar.
- **Seguridad:** `tht servir` sigue escuchando en `127.0.0.1` por omisión. Abrirlo a la red (`0.0.0.0`) solo con `make mesa` y en un hotspot propio con contraseña: la interfaz no pide usuario. Guía completa del día de la feria: [`MESA.md`](MESA.md).

`make fotos-prueba` genera en `fotos-prueba/` tarjetas **sintéticas** en JPEG del mismo diseño que `datos-demo` (una vertical con EXIF), un PNG que debe rechazarse y una foto pública por clase de PCBSPDefect, para probar la captura sin tarjetas.

## Probar sin tarjetas

```bash
make demo                        # tht demo, manifiesto, partición y línea base en datos-demo
uv run tht servir --datos datos-demo
```

`tht demo` genera tarjetas **sintéticas** marcadas como tales. Sirven para probar el software y la interfaz; no son datos del proyecto y sus métricas no se reportan como resultados.

## Estructura

| Módulo | Qué hace |
|---|---|
| `captura.py` | Cámara (Picamera2, USB, archivo o foto de celular en memoria), nombre de archivo, metadatos, EXIF y huella |
| `manifiesto.py` | Huellas SHA-256 de los datos crudos y su verificación |
| `plantilla.py` | Uniones por diseño de tarjeta y alineación de la captura (ECC, con ORB como respaldo) |
| `linea_base.py` | Características por umbral y morfología, y clasificador de centroides |
| `anotaciones.py` | Etiquetas por persona, acuerdo (kappa de Cohen) y consenso |
| `particion.py` | Partición por tarjeta y congelamiento del conjunto de prueba |
| `metricas.py` | Sensibilidad, falsas alarmas, Wilson, bootstrap por tarjeta y McNemar |
| `latencia.py` | Medición de latencia y estimación de subida a la nube |
| `flujo.py` | Flujo completo de inspección |
| `registro.py` | Decisiones del operador en SQLite |
| `datos.py` | Organización de la carpeta de datos y construcción de ejemplos |
| `app.py`, `templates/`, `static/` | Interfaz local; diseño en `DISENO_INTERFAZ.md` |
| `clasificador.py` | Interfaz común de modelos e inferencia ONNX |
| `entrenamiento_red.py` | Entrenamiento de la red, aumento de datos y exportación a ONNX |
| `wsgi.py` | Arranque de la demostración en la nube |
| `Makefile`, `MESA.md` | Operación de la mesa: servir a la red local, URL del celular, latencia y contenedor en modo local |
| `externos.py` | Descarga y lectura de PCBSPDefect (EXP-006) |
| `sintetico.py` | Tarjetas sintéticas para pruebas (con variabilidad de tamaño, brillo, reflejos y desenfoque) |

## Clasificador ligero

- Se entrena con PyTorch (`uv sync --group cnn`), en la laptop o en otra computadora; la Raspberry Pi no necesita PyTorch.
- Se exporta a ONNX y se ejecuta con ONNX Runtime, que es ligero (`red.onnx` y su `red.json` con clases, semilla, épocas e historial).
- `tht entrenar-red` entrena cinco semillas y elige la de mejor exactitud balanceada **en validación**; el conjunto de prueba solo se usa en `tht evaluar`, que reporta cada semilla y su media.
- Arquitecturas: `pequena` (unos 52 mil parámetros, desde cero) y `mobilenet` (MobileNetV3-Small con pesos de ImageNet; necesita `uv add --group cnn torchvision` e internet la primera vez).
- La interfaz usa la red con `uv run tht servir --modelo red`.

## Demostración en la nube

`Dockerfile` y `railway.json` levantan la interfaz con datos **sintéticos** que se generan al arrancar (variable `THT_DATOS`, un volumen persistente). Con `THT_USUARIO` y `THT_CLAVE` pide usuario y contraseña. Nunca se suben imágenes de empresas (D-011): la estación real corre en local. `make docker-mesa` usa la misma imagen en modo local (sin `/capturar` en línea ni datos sintéticos automáticos), montando `DATOS` en `/data/tht`. Las páginas Fotos reales, Reto y Experimentos usan solo datos públicos con licencia abierta (PCBSPDefect, CC BY 4.0, con atribución; D-014), que `uv run --group cnn tht publicar` copia a `src/inspeccion_tht/publico/` (ver su `LEEME.md`).

## Pendiente

- Probar la captura con la cámara definitiva en la Raspberry Pi y fijar resolución e iluminación.
- Probar `/capturar` con teléfonos reales: que Android conserve el EXIF al subir y que Safari en iPhone entregue JPEG.
- `tht capturar --archivo` guarda solo el PNG; decidir si también debe conservar el JPEG original.
- Entrenar y evaluar con DS-01 cuando haya tarjetas reales.
