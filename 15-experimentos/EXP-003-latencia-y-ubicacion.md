---
titulo: "EXP-003 Latencia y ubicación del procesamiento"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-28
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-060]
tags: [femeci, experimento, exp-003]
---

# EXP-003 · Latencia y ubicación del procesamiento

**Objetivo.** Medir el tiempo de captura a resultado en la Raspberry Pi 5 sin red y decidir dónde se procesa (D-009).

**Metas (protocolo §5).**
- **M4:** mediana ≤ 5 s y percentil 95 ≤ 8 s por tarjeta.
- **M5:** 100 % de las funciones de captura, inferencia y registro con la red desconectada.

**Procedimiento.**
1. Desconectar la red de la Raspberry Pi y verificarlo.
2. `uv run tht latencia --imagen <captura real> --diseno <diseño> --repeticiones 30` (registra equipo, mediana, p95 y tiempos crudos).
3. Repetir el flujo completo en la interfaz (capturar, inspeccionar, decidir) y anotar si algo falló sin red.
4. El mismo comando calcula el tiempo de subida de esa imagen a 5, 20 y 100 Mbit/s para comparar con la opción en la nube.

**Regla de decisión fijada de antemano.** Se elige la opción más simple que cumpla M4, M5 y la confidencialidad; la nube solo si lo local no cumple M4.

**Amenazas a la validez.** Temperatura y carga del equipo; tamaño de imagen distinto al de la cámara definitiva.

## Desviación propuesta (2026-10-28) — propuesta, pendiente de confirmación del equipo

> [!warning] No adoptada
> Esta sección es una **propuesta** redactada por Claude (IA). Los criterios fijados el 2026-10-26 siguen vigentes hasta que el equipo la confirme o la rechace, y la decisión se anota aquí con fecha antes de ejecutar.

**Qué cambiaría.** Si no se consigue una Raspberry Pi 5 antes de medir, EXP-003 se ejecutaría en la laptop con Ubuntu que se usará en la mesa, sin red, con el mismo comando (`make latencia IMAGEN=... DISENO=...` o `uv run tht latencia`) y las mismas metas M4 y M5.

**Razón.**
- `#hecho` (comunicado por Fortino, 27 oct) La estación de la jornada del 30 de octubre corre en una laptop con Ubuntu y usa un celular como cámara; la Raspberry Pi 5 podría no conseguirse a tiempo.
- `#inferencia` Medir en un equipo que no es el de la ficha deja EXP-003 sin ejecutar, o lo ejecuta en un hardware distinto sin decirlo. Declararlo antes de medir mantiene la regla de no cambiar criterios después de ver los datos.

**Cómo se reportaría.**
1. El JSON de resultados registra arquitectura, sistema operativo y nombre del equipo (`equipo`), pero no el procesador ni la memoria: se anotan con `--nota` (salida de `lscpu` y `free -h`). El reporte dice "laptop (modelo, CPU, RAM)" y no "Raspberry Pi 5".
2. M4 se reporta como cumplida o no **en la laptop**. `#inferencia` Una laptop suele ser más rápida que una Raspberry Pi 5, así que el resultado no demuestra M4 en la Pi: la afirmación "funciona en una Raspberry Pi" queda pendiente hasta medir en ella.
3. Con celular, el tiempo de captura a resultado incluye la subida de la foto por la red local. Se propone medir por separado: (a) la inspección (`tht latencia`, sin cambios) y (b) la subida desde el celular, tomada del registro del servidor o con cronómetro, al menos 30 veces. M4 se evaluaría con la suma, y se reporta cada parte.
4. El tamaño de imagen será el de la cámara del celular, no el de la cámara de 12 MP de la ficha; se anota la resolución.

**Lo que no cambia.** M5 (todo funciona con la red desconectada) se comprueba igual: la red local del hotspot no tiene internet. La regla de decisión de D-009 no cambia.

**Lo que no es.** Las mediciones hechas durante el desarrollo (por ejemplo, unos 0.1 s por tarjeta sintética en la laptop de Fortino, 27 oct) son pruebas de software y no se reportan como resultados de este experimento.

**Pendiente.** El protocolo entregado ([[protocolo-v1]] §5 y §6) menciona la Raspberry Pi 5 para M4 y una cámara de 12 MP; si el equipo adopta esta desviación, el cambio se declara en la presentación y en la bitácora, sin reescribir el protocolo entregado.

## Registro

- **Planeado:** 2026-10-26, a partir de [[protocolo-v1]] §6.5. Los criterios de aceptación quedan fijos desde esta fecha; cualquier cambio se anota aquí con fecha y razón antes de ejecutar.
- **Ejecutado:** pendiente.
- **Responsables:** por asignar.
- **Commit del código:** se anota al ejecutar (`git rev-parse HEAD`).
- **Resultados crudos:** `datos/resultados/` (archivo JSON con fecha que genera el comando).
