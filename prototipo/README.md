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
```

En la Raspberry Pi, la cámara se usa con Picamera2, que viene con Raspberry Pi OS (`sudo apt install python3-picamera2`). Para que el entorno de uv la vea, cree el entorno con `uv venv --system-site-packages`. Sin Picamera2 se usa cualquier cámara USB vía OpenCV.

## Flujo de trabajo

| Paso | Comando | Experimento |
|---|---|---|
| 1. Crear carpetas | `uv run tht iniciar --datos datos` | |
| 2. Capturar cada tarjeta por ambos lados | `uv run tht capturar --tarjeta T01 --lado B --iluminacion 1 --responsable fortino` | DS-01 |
| 3. Verificar que los crudos no cambiaron | `uv run tht manifiesto verificar datos/crudos` | |
| 4. Crear el diseño de tarjeta y marcar sus uniones | `uv run tht servir --datos datos` y luego "Crear diseño" | |
| 5. Etiquetar por separado (dos personas, a ciegas) | En la interfaz: "Etiquetar" | DS-01 |
| 6. Medir el acuerdo entre etiquetadores | `uv run tht acuerdo --a fortino --b israel` | DS-01 |
| 7. Congelar la partición por tarjeta | `uv run tht particion` | |
| 8. Entrenar la línea base | `uv run tht entrenar` | EXP-002 |
| 9. Evaluar en el conjunto de prueba | `uv run tht evaluar` | EXP-002 |
| 10. Medir la latencia | `uv run tht latencia --imagen ... --diseno ...` | EXP-003 |
| 11. Inspección asistida | En la interfaz: "Inspeccionar" | EXP-005 |

Las etiquetas finales (`consenso`) se forman con las de dos personas; donde no coinciden, deciden juntas y lo registran.

## Probar sin tarjetas

```bash
uv run tht demo --salida datos-demo
uv run tht particion --datos datos-demo
uv run tht entrenar --datos datos-demo
uv run tht servir --datos datos-demo
```

`tht demo` genera tarjetas **sintéticas** marcadas como tales. Sirven para probar el software y la interfaz; no son datos del proyecto y sus métricas no se reportan como resultados.

## Estructura

| Módulo | Qué hace |
|---|---|
| `captura.py` | Cámara (Picamera2, USB o archivo), nombre de archivo, metadatos y huella |
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
| `sintetico.py` | Tarjetas sintéticas para pruebas |

## Pendiente

- Clasificador ligero de aprendizaje profundo (protocolo, sección 6.4). Se agrega cuando haya datos reales, para compararlo contra la línea base con el mismo conjunto de prueba.
- Probar la captura con la cámara definitiva en la Raspberry Pi y fijar resolución e iluminación.
