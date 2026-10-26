---
titulo: "EXP-006 Validación con datos públicos reales (PCBSPDefect)"
tipo: especificacion
estado: planeado
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
- **Ejecutado:** pendiente.
- **Resultados crudos:** `15-experimentos/resultados/EXP-006_*.json`.
