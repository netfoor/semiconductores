# Guía de la mesa (jornada del 30 de octubre de 2026)

Cómo montar la estación para que un celular sirva de cámara **sin instalar ninguna app** y **sin internet**. El celular abre una página que sirve la laptop en la red local, toma la foto con su cámara y la sube; todo el procesamiento ocurre en la laptop (Ubuntu).

```
celular ──Wi-Fi (hotspot propio, con contraseña, sin internet)──▶ laptop: tht servir --host 0.0.0.0
  /capturar: foto JPEG                                             crudos/ + MANIFIESTO.csv + inspección
```

## 1. Seguridad: lo que no se negocia

- `tht servir` escucha en `127.0.0.1` por omisión: solo la propia laptop puede abrir la interfaz. Eso no cambia.
- `0.0.0.0` (abrir a la red) **solo** con `make mesa` o `make docker-mesa`, y **solo** en un hotspot propio con contraseña WPA2. Nunca en el Wi-Fi abierto del recinto: la interfaz no pide usuario y cualquiera en la misma red podría subir fotos o registrar decisiones.
- La contraseña del hotspot no se escribe en el repositorio ni en el cartel.
- Las fotos de la mesa no salen de la laptop. La demostración en línea (femeci.foor.dev) no tiene `/capturar`.

## 2. Red local

Elija una opción y pruébela antes del día.

### Opción A: hotspot desde la laptop (recomendada)

1. Verifique que la tarjeta Wi-Fi admite modo punto de acceso:
   ```bash
   nmcli -t -f DEVICE,TYPE device | grep wifi          # nombre de la interfaz, p. ej. wlp2s0
   nmcli -f WIFI-PROPERTIES.AP device show wlp2s0      # debe decir: yes
   ```
   Si dice `no`, use la opción B.
2. Desconecte el cable de red: si la laptop tiene otra salida a internet, NetworkManager la comparte con el hotspot.
3. Cree el hotspot (la laptop deja la red Wi-Fi a la que estaba conectada):
   ```bash
   nmcli device wifi hotspot ifname wlp2s0 con-name mesa-tht ssid MESA-THT password 'una-clave-larga-de-12+'
   ```
   La laptop suele quedar en `10.42.0.1`. `make url` muestra la dirección exacta.
4. En el celular: conéctese a `MESA-THT`. Si avisa «Esta red no tiene acceso a internet», elija **mantener la conexión**, y apague los datos móviles para que el teléfono no cambie de red.
5. Al terminar: `nmcli connection down mesa-tht`.

### Opción B: hotspot del celular

1. Active el punto de acceso del celular con contraseña y conecte la laptop a él.
2. Apague los datos móviles del celular, para que la red quede sin internet. `#supuesto` En Android el punto de acceso sigue funcionando sin datos; en iPhone puede pedir datos celulares activos. Probarlo antes del día.
3. `make url` muestra la IP que el hotspot le dio a la laptop (en Android suele ser `192.168.x.x`; en iPhone, `172.20.10.x`).

## 3. Firewall (ufw)

```bash
sudo ufw status
```

- Si dice `inactive`, no haga nada.
- Si está activo, abra el puerto 8000 **solo en la interfaz del hotspot**:
  ```bash
  sudo ufw allow in on wlp2s0 to any port 8000 proto tcp comment 'mesa THT'
  ```
  Con la opción A, si el celular no obtiene IP, ufw está bloqueando el DHCP y el DNS del hotspot:
  `sudo ufw allow in on wlp2s0 to any port 67 proto udp` y `sudo ufw allow in on wlp2s0 to any port 53`.
- Al terminar, borre las reglas: `sudo ufw delete allow in on wlp2s0 to any port 8000 proto tcp` (y las de 67 y 53 si las agregó).
- `make docker-mesa` no pasa por ufw (Docker escribe sus propias reglas). Por eso publica el puerto solo en la IP del hotspot.

## 4. Arrancar la estación

```bash
cd prototipo
make mesa DATOS=datos          # o DATOS=datos-demo para practicar con datos sintéticos
```

`make mesa` imprime la URL que debe abrir el celular (`http://<IP>:8000/capturar`) y, si `qrencode` está instalado, un código QR. En el celular se puede guardar la página en la pantalla de inicio.

Alternativa con contenedor (la misma imagen que la demostración en línea, pero en modo local; la imagen se construye **antes** del día porque necesita internet):

```bash
make docker-construir
make docker-mesa DATOS=datos
```

Con `MODELO=red` se usa el clasificador ONNX en lugar de la línea base.

### Tarjeta-mosaico (uniones reales sin tarjeta física)

Sin tarjetas soldadas propias, la demostración usa una **tarjeta-mosaico**: 30 fotos reales de uniones del conjunto de prueba de PCBSPDefect (CC BY 4.0), acomodadas como una tarjeta e impresas en papel. La red de EXP-006 no vio esas fotos al entrenar.

```bash
make mosaico                               # crea datos-mosaico/ (diseño, una captura, la red y las respuestas)
make mesa DATOS=datos-mosaico MODELO=red
```

1. Imprima `datos-mosaico/mosaico-imprimir.png` **en color**, hoja carta horizontal, «ajustar a la página». Llévela pegada a un cartón para que no se doble.
2. En `/capturar`: tarjeta `T90`, diseño `mosaico-01`. Fotografíe la hoja completa (las cuatro marcas blancas de las esquinas deben salir en la foto), sin reflejos de lámparas.
3. La inspección marca las sospechosas; compare con `datos-mosaico/LEEME_MOSAICO.txt`, que trae la clase real de cada unión.
4. Dígalo así: «son fotos reales de uniones de un conjunto público, acomodadas como tarjeta; no es una tarjeta física ni datos propios». La propia hoja y la interfaz lo dicen.

Prueba de software del 29 oct (simulación, no experimento): con una foto simulada de 12 MP de la hoja (perspectiva, tinte y desenfoque), el sistema acertó la clase de 26 de 30 uniones. Con una foto real de la hoja impresa puede ser distinto: pruébelo antes de abrir la mesa.

## 5. Lista de verificación antes de abrir la mesa

- [ ] `make probar` pasa.
- [ ] `uv run tht manifiesto verificar datos/crudos` dice `Íntegro`.
- [ ] La página Estación indica la partición congelada y el modelo entrenado.
- [ ] La laptop **no** tiene internet: `ping -c1 -W2 1.1.1.1` falla. El celular tiene los datos móviles apagados.
- [ ] El hotspot es propio y tiene contraseña (no el Wi-Fi del recinto).
- [ ] La hoja del mosaico está impresa en color y una foto suya desde el celular se inspecciona bien.
- [ ] Una captura de prueba desde el celular llega, y se inspecciona. Practique en `datos-demo` con las fotos de `make fotos-prueba`, no en la carpeta real.
- [ ] La ubicación de la cámara está desactivada. En iPhone: Ajustes > Cámara > Formatos > «Más compatible» (JPEG).
- [ ] La fecha y la hora de la laptop son correctas: entran en el nombre de cada foto.
- [ ] Laptop y celular con batería completa; cargadores y extensión.
- [ ] Video de respaldo de la demostración guardado en la laptop y en una memoria USB, reproducible sin internet.
- [ ] Cable USB del celular a la mano, por si falla la red (§6).

## 6. Si falla la red local

1. Tome las fotos con la app de cámara del celular, como siempre.
2. Páselas a la laptop por cable USB (transferencia de archivos) a una carpeta, por ejemplo `entrada-celular/`. No las envíe por mensajería: recomprime la foto y quita el EXIF.
3. Registre las huellas de los originales antes de tocarlos:
   ```bash
   uv run tht manifiesto generar entrada-celular
   ```
4. Capture cada una desde el archivo:
   ```bash
   uv run tht capturar --datos datos --archivo entrada-celular/IMG_0001.jpg \
     --tarjeta T07 --lado B --iluminacion 1 --responsable fortino --nota "plan B: USB"
   ```
   Limitación actual: por esta vía se guarda solo el PNG (`camara: "archivo"`); el JPEG original queda en `entrada-celular/` con su propio manifiesto, no junto al PNG.
5. Si tampoco hay celular, use una cámara USB: `uv run tht capturar --camara opencv ...`.

## 7. Al terminar

1. `uv run tht manifiesto verificar datos/crudos`.
2. Respalde la carpeta `datos/` en una memoria USB. No se sube al repositorio (D-011).
3. Baje el hotspot y borre las reglas de ufw (§2 y §3).
4. Registre en la bitácora qué se capturó, con qué teléfono y qué falló.
