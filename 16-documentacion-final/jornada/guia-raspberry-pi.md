---
titulo: "Guía de la jornada: estación en la Raspberry Pi 4"
tipo: guia
estado: vigente
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, jornada, raspberry-pi, demostracion]
---

# Guía de la jornada: estación en la Raspberry Pi 4

**Viernes 30 de octubre de 2026.** Registro y montaje a las 7:30; todo listo para la revisión de las 8:45. La mesa tiene dos contactos de 110 V.

Esta guía sirve para llegar, recibir la Raspberry Pi y tener la estación funcionando **sin internet** en unos 20 minutos. La laptop es el respaldo.

## Compatibilidad: qué está probado y qué no

| Punto | Estado |
|---|---|
| Bibliotecas para la Raspberry Pi de 64 bits (numpy, OpenCV, ONNX Runtime) | Verificado: todas tienen versión para ARM de 64 bits y Python 3.11 a 3.13 |
| El programa con Python 3.11 (el de Raspberry Pi OS Bookworm) | Verificado: 70 pruebas pasan |
| Instalación sin internet con los scripts del paquete | Verificada en una PC con Python 3.11 |
| Tiempo de inspección | 0.3 a 0.4 s por tarjeta en el contenedor de desarrollo; en la Pi 4 será mayor, se mide con `probar.sh` |
| Correr en una Raspberry Pi real | **No probado**: no tuvimos una Pi. Por eso existe el plan B |
| Raspberry Pi OS de 32 bits | **No funciona** (no hay ONNX Runtime para 32 bits). Usar la laptop |

## 1. Hoy en la noche, en la laptop (con internet)

```bash
cd semiconductores && git pull
cd prototipo
make probar          # deben pasar todas las pruebas
make paquete-pi      # crea paquete-pi/ (unos 150 MB)
make mosaico         # crea datos-mosaico/ y la hoja para imprimir
```

1. Copie la carpeta **`paquete-pi/` completa** a una memoria USB.
2. Imprima `datos-mosaico/mosaico-imprimir.png` **en color**, hoja carta horizontal, «ajustar a la página». Péguela a un cartón.
3. Ensaye el plan B en la laptop, con el celular: `make mesa DATOS=datos-mosaico MODELO=red` y abra en el celular la dirección que aparece.
4. Guarde en la laptop y en la USB el video de respaldo de la demostración.

**Llevar:** memoria USB, laptop y su cargador, celular y su cargador, extensión y multicontacto, hoja del mosaico en cartón, tríptico, bitácora impresa, protocolo y la ficha con el QR del folio. Si la Pi viene sin accesorios: fuente oficial USB-C de 5 V / 3 A, cable micro-HDMI, teclado y ratón.

## 2. Al recibir la Raspberry Pi: cinco preguntas (2 minutos)

| Pregunta | Cómo saberlo | Si la respuesta es mala |
|---|---|---|
| ¿Cómo la vemos? | Monitor por micro-HDMI con teclado, o SSH desde la laptop | Pedir monitor o usuario y contraseña con SSH activo |
| ¿Usuario y contraseña? | Preguntar a quien la entrega | Sin acceso no se puede instalar: plan B |
| ¿Es de 64 bits? | `uname -m` debe decir `aarch64` | Si dice `armv7l`: plan B (laptop) |
| ¿Qué Python trae? | `python3 --version`: 3.11, 3.12 o 3.13 | Otra versión: plan B |
| ¿Hay espacio? | `df -h ~`: al menos 1 GB libre | Borrar archivos o plan B |

## 3. Instalar sin internet (10 minutos)

Conecte la USB a la Pi. En una terminal:

```bash
cp -r /media/$USER/*/paquete-pi ~/
cd ~/paquete-pi
bash instalar.sh
bash probar.sh
```

- `instalar.sh` revisa la arquitectura y la versión de Python, crea el entorno en `~/tht` e instala todo desde la USB. Termina con «Instalado».
- `probar.sh` crea la tarjeta-mosaico en `~/datos-mosaico`, mide el tiempo de inspección cinco veces e imprime la dirección para el celular y el comando para arrancar.
- **Anote el tiempo mediano que imprime `probar.sh`.** Es la respuesta honesta a «¿cuánto tarda en la Raspberry?».

## 4. Red local y celular (5 minutos)

1. En el celular: active el **punto de acceso** con contraseña y **apague los datos móviles** (la convocatoria prohíbe conexiones activas a internet para operar el proyecto).
2. Conecte la Pi a ese punto de acceso (icono de Wi-Fi del escritorio, o `nmcli device wifi connect "NOMBRE" password "CLAVE"`).
3. Arranque la estación con el comando que imprimió `probar.sh`:
   ```bash
   ~/tht/bin/tht servir --datos ~/datos-mosaico --modelo red --host 0.0.0.0 --puerto 8000
   ```
4. Vuelva a ver la dirección con `hostname -I` y abra en el celular `http://ESA-IP:8000/capturar`.

## 5. Prueba completa antes de las 8:45

1. En `/capturar`: tarjeta **T90**, lado B, diseño **mosaico-01**, su nombre como responsable.
2. «Tomar foto»: la hoja completa, con las **cuatro marcas blancas de las esquinas** dentro de la foto y sin reflejos de lámparas.
3. Se abre la inspección: el sistema marca las uniones sospechosas. Compare con las respuestas de `~/datos-mosaico/LEEME_MOSAICO.txt`.
4. Al pie de la inspección aparece el tiempo de procesamiento local.
5. Haga dos o tres fotos de práctica. Deje la Pi encendida y la página abierta en el celular.

## 6. Si algo falla

| Problema | Qué hacer |
|---|---|
| `uname -m` no dice `aarch64` | Plan B: laptop con `make mesa DATOS=datos-mosaico MODELO=red` |
| `instalar.sh` dice que falta `python3-venv` | El script instala solo para el usuario; si también falla, plan B |
| El celular no abre la página | ¿Están en la misma red? ¿La IP es la de `hostname -I`? Revise `sudo ufw status`; si está activo: `sudo ufw allow 8000/tcp` |
| «No se pudo alinear» | Repita la foto con las cuatro marcas de las esquinas, de frente y sin reflejos |
| La foto es HEIC (iPhone) | Ajustes > Cámara > Formatos > «Más compatible» |
| Tarda más de 5 s | Dígalo tal cual: es la medición de hoy en la Pi 4. La laptop es el respaldo |
| Nada funciona | Video de respaldo y la página «Fotos reales» en la laptop, que corre en local |

## 7. Qué decir al jurado

- La estación corre en una **Raspberry Pi 4, sin internet**; el celular solo toma la foto y la envía por una red local.
- La tarjeta de la demostración es un **mosaico de fotos reales de un conjunto público** (PCBSPDefect, CC BY 4.0). No es una tarjeta física ni datos propios: la hoja y la pantalla lo dicen.
- El protocolo menciona una Raspberry Pi 5; hoy usamos una Pi 4, que es más lenta. Los tiempos de hoy son una **prueba de software**, no el experimento EXP-003.
- Si el sistema se equivoca en alguna unión, es parte de la demostración: por eso la persona decide.
