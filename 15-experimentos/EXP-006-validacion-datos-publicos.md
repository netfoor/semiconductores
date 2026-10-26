---
titulo: "EXP-006 Validación con datos públicos reales (PCBSPDefect)"
tipo: especificacion
estado: ejecutado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-080]
tags: [femeci, experimento, exp-006, datos-externos]
---

# EXP-006 · Validación con datos públicos reales (PCBSPDefect)

**Por qué se agrega.** Mientras no haya tarjetas de DS-01, este experimento prueba los dos modelos con **fotos reales** de uniones through-hole tomadas por otro grupo de investigación. No sustituye a EXP-002: otra cámara, otras tarjetas y otra planta. Sirve para saber si el método aprende defectos reales y no solo los sintéticos.

**Datos.** PCBSPDefect, subconjunto `b_dip` (componentes DIP vistos del lado de soldadura) [F-080]. Licencia CC BY 4.0. Archivo `PCBSPDefect.zip`, SHA-256 `1e135795835f04deccb0bc5fc1dd071c7fc944963e2cd5b76c6deff399c0de98`. Revisión del 26 oct: 622 uniones distintas de 121 tarjetas, cada una fotografiada con tres iluminaciones (1866 imágenes de 280 x 280 px). Las imágenes no se suben al repositorio; se descargan de Zenodo con el script.

**Correspondencia de clases.** good = aceptable, insuff = insuficiente, bridge = puente, no = sin soldar, excess = exceso. No hay clase "fría".

**Particiones (fijadas antes de entrenar).**
- **Oficial:** `train_20_percent` para entrenar, `val` para elegir el modelo y `test` para evaluar. Separa por unión (las tres iluminaciones de una unión van juntas), pero comparte tarjetas entre conjuntos.
- **Por tarjeta (la del protocolo):** todas las imágenes de una tarjeta en un solo conjunto, 60/20/20, semilla 20261026, con `particion.particionar`.

**Modelos.** Línea base clásica y red pequeña (lado de 64 px, cinco semillas: 1 a 5, 40 épocas, elección por exactitud balanceada en validación), con el mismo código de `prototipo/`.

**Métricas y criterios (los de M1 y M2).**
- **Sensibilidad para cualquier defecto:** ≥ 0.90 con límite inferior de Wilson ≥ 0.85.
- **Falsas alarmas:** ≤ 0.15.
- Se reportan también la exactitud por clase, la matriz de confusión, los IC por bootstrap agrupando por tarjeta y la media y desviación entre semillas.

La unidad de conteo es la imagen. Como cada unión tiene tres imágenes, el bootstrap agrupa por tarjeta para no sobrestimar la precisión.

**Amenazas a la validez.**
- Cámara, iluminación y tarjetas distintas a las de la estación.
- Los defectos son de producción de otra planta.
- En la partición oficial las tarjetas se comparten entre conjuntos, lo que puede inflar el resultado; por eso se reporta también la partición por tarjeta.

## Registro

- **Planeado:** 2026-10-26, antes de entrenar o evaluar cualquier modelo con estos datos.
- **Ejecutado:** 2026-10-26, por Claude (IA), con `uv run --group cnn tht externo evaluar` (12 minutos en el contenedor de desarrollo, CPU). Sin cambios respecto de lo planeado.
- **Resultados crudos:** `15-experimentos/resultados/EXP-006_2026-10-26.json` (cada semilla, por clase y matrices de confusión).

## Resultados

Unidad: imagen (tres por unión). IC 95 %: Wilson y bootstrap agrupado por tarjeta (2000 repeticiones).

| Partición | Prueba | Modelo | Sensibilidad | Falsas alarmas |
|---|---|---|---|---|
| Oficial | 1116 imágenes, 372 uniones, 120 tarjetas | Línea base | 0.739 (bootstrap 0.679 a 0.794) | 0.282 (bootstrap 0.171 a 0.407) |
| Oficial | Igual | Red, semilla 2 (elegida por validación) | 0.941 (Wilson 0.924 a 0.955; bootstrap 0.913 a 0.967) | 0.116 (Wilson 0.080 a 0.165; bootstrap 0.030 a 0.216) |
| Oficial | Igual | Red, media de 5 semillas | 0.938 (DE 0.014) | 0.130 (DE 0.020) |
| Por tarjeta | 360 imágenes, 120 uniones, 24 tarjetas | Línea base | 0.684 (bootstrap 0.514 a 0.826) | 0.333 (bootstrap 0.278 a 0.444) |
| Por tarjeta | Igual | Red, semilla 2 (elegida por validación) | 0.983 (Wilson 0.960 a 0.993; bootstrap 0.959 a 1.000) | 0.083 (Wilson 0.039 a 0.170; bootstrap 0.000 a 0.194) |
| Por tarjeta | Igual | Red, media de 5 semillas | 0.974 (DE 0.010) | 0.100 (DE 0.090) |

Sensibilidad por clase de la red elegida (oficial / por tarjeta): aceptable 0.88 / 0.92, insuficiente 0.91 / 1.00, puente 0.94 / 0.98, sin soldar 0.83 / 1.00, exceso 0.81 / 0.93.

## Lectura

- `#hecho` Con fotos reales de uniones through-hole, la red cumple M1 en las dos particiones (sensibilidad ≥ 0.90 y límite inferior de Wilson ≥ 0.85) y su falsa alarma puntual cumple M2 (≤ 0.15). La línea base clásica no cumple ninguna de las dos.
- `#inferencia` El límite superior del IC de falsas alarmas (0.17 a 0.22) rebasa 0.15: con estos datos no se puede afirmar con seguridad que M2 se cumple. Hay que reportarlo así.
- `#inferencia` Las falsas alarmas varían mucho entre semillas en la partición por tarjeta (la semilla 4 llegó a 0.278): elegir por validación importa, y conviene reportar la media y la dispersión, no solo la mejor semilla.
- `#inferencia` La partición por tarjeta dio números más altos que la oficial, probablemente porque entrena con el triple de imágenes (1119 contra 375); no se probó por separado. Su conjunto de prueba es más chico (24 tarjetas), y por eso sus IC son más anchos.
- Advertencia: las tres fotos de una unión no son independientes, así que el IC de Wilson queda demasiado estrecho. El IC que vale es el bootstrap por tarjeta.
- Esto **no** es el resultado de EXP-002: falta repetirlo con DS-01, con la cámara y la iluminación de la estación.
