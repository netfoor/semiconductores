---
titulo: "Pendientes del equipo"
tipo: seguimiento
estado: vigente
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, pendientes]
---

# Pendientes del equipo

Lista viva: se actualiza en cada sesión. Lo terminado se marca con la fecha y se deja una semana antes de borrarlo. Estado general y cómo retomar en local: [[estado-y-continuacion]].

## Hoy, 29 de octubre

| # | Pendiente | Responsable | Estado |
|---|---|---|---|
| 1 | Revisar en local la interfaz v2 y fusionar a main | Fortino | Hecho 29 oct (PR #13) |
| 2 | Recibir la Raspberry Pi (14:20): revisar `uname -m` = `aarch64` y Python 3.11–3.13 (guía §2) | Fortino | Hecho 29 oct (bitácora, sesión 7) |
| 3 | `make paquete-pi` en la laptop y copiar `paquete-pi/` a la USB | Fortino | Hecho 29 oct |
| 4 | Instalar y probar en la Pi: `bash instalar.sh` y `bash probar.sh`; anotar el tiempo medido | Fortino, Israel | Hecho 29 oct: mediana 1.27 s con la imagen digital |
| 5 | Imprimir la hoja del mosaico en color, carta horizontal, y pegarla en cartón | Equipo | Pendiente |
| 6 | Tríptico: reescribir textos con sus palabras, decidir nombres, imprimir 150 x 120 cm en material rígido | María José | En curso |
| 7 | Protocolo y bitácora finales (la fuente de verdad es el repositorio): interfaz v2, D-015, D-016, Pi 4, paquete sin internet, mosaico | Equipo + Claude (IA), en la noche | Hecho 29 oct: bitácora regenerada (sesiones 7 y 8) y adenda al protocolo aparte; el protocolo entregado no cambia |
| 8 | Fecha de la conversación sobre soldadura de metales | María José | Pendiente |
| 9 | FE-03: confirmar si se usa alcohol isopropílico para limpiar fundente | Equipo | Pendiente |

## Interfaz y sistema (spec-interfaz-v2)

| # | Pendiente | Prioridad | Estado |
|---|---|---|---|
| 10 | Perfil del inspector: inspecciones de hoy, uniones revisadas, tiempo promedio | P2 | Pendiente |
| 11 | Historial de inspecciones de la estación | P2 | Pendiente |
| 12 | Pantalla de la laptop como tablero de la estación mientras el celular captura | P2 | Pendiente |
| 24 | Actualizar la skill ui-minimal en claude.ai con el archivo enviado (la copia local ya está actualizada) | P2 | Fortino |
| 13 | Revisar textos de Experimentos con el mismo tono (la página es para evaluadores; se deja técnica por ahora) | P2 | Pendiente |
| 14 | Fusionar a main y comprobar femeci.foor.dev | P1 | Todo fusionado el 29 oct; falta comprobar el despliegue |

## Página del proyecto v2 (spec-landing-v2)

| # | Pendiente | Prioridad | Estado |
|---|---|---|---|
| 18 | L2: recorrido «Del diseño a la tarjeta revisada» con la tarjeta en capas 3D y la barra de proceso | P1 | Hecho 29 oct (PR #14) |
| 19 | L2: corte transversal THT frente a SMD | P1 | Hecho 29 oct (PR #14) |
| 20 | L4: «La estación en uso» con capturas reales del celular, marco de teléfono en CSS y María José de la Rosa como inspectora | P1 | Hecho 29 oct (fusionado a main) |
| 21 | L1: portada con captura del celular (se puede reusar el marco `.telefono` y `static/capturas/uso-4.jpg`) | P2 | Pendiente |
| 22 | L5: mejor presentación de resultados: cifras grandes con sus intervalos y «en qué se equivoca» cada modelo, conservando la advertencia de M2 (usar las skills dataviz y ui-minimal) | P2 | Siguiente |
| 23 | L3: acortar «El problema» | P2 | Pendiente |

## Para la exposición (30 de octubre)

| # | Pendiente | Responsable | Estado |
|---|---|---|---|
| 15 | Guion de 8 a 10 minutos para los tres, con la respuesta de D-016 (por qué sigue el inspector) | Equipo + Claude (IA) | Hecho 29 oct: `16-documentacion-final/jornada/guion-exposicion.pdf` (tres y dos personas) |
| 16 | Banco de preguntas probables | Equipo + Claude (IA) | Pendiente |
| 17 | Video de respaldo de la demostración | Equipo | Pendiente |

## Próximos pasos de la investigación (después de la jornada)

- Visita técnica a una planta de ensamble (5 de noviembre); buscar colaboración para un piloto con datos propios (D-016, fase 2).
- DS-01 y experimentos EXP-001 a EXP-005; decidir la desviación propuesta de EXP-003 (Pi 4 o laptop en lugar de Pi 5).
