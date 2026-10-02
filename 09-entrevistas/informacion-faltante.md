---
titulo: "Información faltante y qué obtener de los contactos"
tipo: analisis
estado: borrador
creado: 2026-10-02
actualizado: 2026-10-02
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-002, F-041, F-042, F-051, F-057, F-060, F-079]
tags: [femeci, entrevistas, informacion-faltante, fase-5]
aliases: ["Información faltante", "Qué nos falta saber"]
---

# Información faltante y qué obtener de los contactos

Fase 5, letra G del documento maestro: "identifica qué información nos falta y qué podríamos obtener directamente de contactos de la industria".

Todo está ordenado por lo que necesita la **decisión del martes 6 de octubre (G1)**. Las preguntas completas están en [[preguntas-pendientes]] (contactos externos) y [[preguntas-abiertas-convocatoria]] (DME y equipo). Las guías de conversación están en §5.

## 1. Lo mínimo que decide G1

| # | Qué falta saber | Por qué decide | Quién lo responde | Cómo y cuándo | Preguntas |
|---|---|---|---|---|---|
| 1 | Si Yankuilotl tiene un **problema técnico concreto** que quiera trabajar con estudiantes: inspección, verificación de primera pieza o falsas alarmas | Sin esto, ninguna idea de la familia de semiconductores pasa el filtro de "problema demostrado" ([[mapa-de-oportunidades]] §3) | Contactos de Fortino en el área de software, que pueden llevar al laboratorio o a la dirección de tecnología | Plática hoy, 2 oct; llamada de 20–30 min la semana del 5 | Q-034, Q-035, Q-036 |
| 2 | **Acceso**: visita, fotos o tarjetas físicas, incluidas de desecho, y qué se puede mostrar | Define si habrá datos reales y con qué permisos | Yankuilotl | Misma conversación | Q-037, Q-046 |
| 3 | Vínculo formal **UTP–Yankuilotl** | Abre una vía institucional y reduce el riesgo de no tener respuesta | Directora de división | Reunión de hoy, 2 oct ([[guia-reunion-directora-utp]]) | Q-028 |
| 4 | **Plan B dentro de la familia**: laboratorio de electrónica de la UTP con prácticas de soldadura | Permite crear tarjetas y defectos controlados si no hay acceso a planta (IC-06) | Directora; docentes de electrónica o mecatrónica | Reunión de hoy | Q-047 |
| 5 | Opciones de **categoría y área** en la plataforma, y si se pueden editar después de inscribirse | Define D-006 y cuándo confirmar la inscripción | Fortino (abrir los dos menús sin confirmar); DME | Hoy; correo | Q-045 |
| 6 | Interés de **INAOE/Kutsari** (semiconductores en sentido estricto) | Segunda puerta de la familia si Yankuilotl no responde | Contacto del INAOE, por identificar ([[guia-contacto-inaoe-kutsari]]) | Correo; probablemente después de G1 | Q-030 |

## 2. Lo que necesita el protocolo (antes del 14 de octubre)

| Tema | Pregunta | Quién |
|---|---|---|
| Plantilla, formato de cuartilla, resultados preliminares | Q-001 | DME (pregunta 1 del correo) |
| Formatos F-01 a F-05 y FE; firmas; edición de la inscripción | Q-002, Q-045 | DME (pregunta 2 del correo) |
| Bitácora digital o manuscrita | Q-006 | DME |
| Reglas de uso de IA | Q-010 | DME |
| Participantes humanos (si personas externas prueban el prototipo) y FE-1C (datos en una empresa) | Q-008, Q-009 | DME |
| Criterios de aceptación de ensambles (IPC-A-610) y acceso a la norma | Q-039 | Yankuilotl; biblioteca de la UTP |
| Defectos más frecuentes y costosos: definen las clases y las métricas | Q-035 | Yankuilotl |
| Tiempo por tarjeta y conectividad de la estación: definen latencia y arquitectura (D-009) | Q-043, Q-044 | Yankuilotl |
| Asesor científico externo y su registro | Q-024, Q-013 | Contactos de industria o academia; DME |

## 3. Qué podemos obtener directamente de contactos de la industria

| Recurso | Para qué sirve en el proyecto | De quién | Cuidado |
|---|---|---|---|
| Descripción del proceso y de cómo inspeccionan hoy | Problema (A1), pertinencia (A2) y línea base para comparar | Yankuilotl | Registrar como entrevista; preguntar si se puede citar a la persona o a la organización |
| Defectos frecuentes, con tiempos o costos aproximados | Hipótesis y metas medibles (A3) | Yankuilotl | Pueden ser datos internos: acordar qué es público |
| Criterio de aceptación que usan (por ejemplo, IPC-A-610 clase 2 o 3) | Clases del dataset alineadas con una norma (A4) | Yankuilotl | La norma es de pago |
| **Tarjetas físicas** de desecho, de prueba o con retrabajo | Dataset propio con piezas reales, lo que el documento maestro considera "particularmente interesante" (B1) | Yankuilotl | Carta que diga qué se puede mostrar; FE-1C si se toman datos dentro de la planta (Q-009) |
| Fotos en planta, o imágenes de su AOI con la decisión del operador | Datos para entrenar y evaluar (A5) | Yankuilotl | Los diseños pueden ser de clientes: no subirlos a servicios en la nube sin permiso (D-009) |
| Tiempo por tarjeta, conectividad y equipos permitidos en la línea | Requisitos de latencia y arquitectura | Yankuilotl | — |
| Un técnico que pruebe el prototipo y dé su opinión | Evidencia de utilidad (A2, C2) | Yankuilotl | Si personas externas prueban el prototipo podría aplicar FE-04 (Q-008) |
| Asesoría científica externa | Respaldo especializado (§3.6) | Yankuilotl, INAOE o BUAP | Registro del asesor (Q-013) y, si supervisa trabajo, FE-02 |
| Carta o constancia de colaboración | Respaldo del problema y de los permisos | Yankuilotl | Pedirla por escrito |
| Datos de caracterización de chips | Solo para IC-05 | INAOE/Kutsari | Uso académico; confidencialidad |

## 4. Ya no hace falta

- **Q-011 y Q-042:** cerradas el 2 oct por D-010 (desarrollo desde cero, sin continuidad).
- **Q-040 y Q-041:** opcionales.

## 5. Guías y mensajes listos

| Para quién | Nota | Cuándo |
|---|---|---|
| Directora de división (carta, vínculo con Yankuilotl, laboratorio de electrónica) | [[guia-reunion-directora-utp]] | Hoy, 2 oct |
| Contactos y personal técnico de Yankuilotl | [[guia-contacto-yankuilotl]] (con versión corta de 5 minutos) | Hoy y la semana del 5 |
| DME (plantilla, formatos, inscripción, IA, bitácora, vinculación) | Correo en [[preguntas-abiertas-convocatoria]] §3 | Enviar hoy |
| INAOE/Kutsari | [[guia-contacto-inaoe-kutsari]] | Si Yankuilotl no responde, o en paralelo |
| Comparadores (Atoyac, inundaciones, automotriz) | Preguntas Q-031, Q-032 y Q-033 en [[preguntas-pendientes]] | Solo si el equipo decide explorarlos |

## 6. Calendario de obtención hasta G1

| Fecha | Qué |
|---|---|
| Vie 2 oct | Reunión con la directora (carta, Q-028, Q-047). Plática con los contactos de Yankuilotl. Enviar el correo a la DME. Abrir los menús de categoría y área sin confirmar la inscripción |
| Lun 5 oct | Llamada con personal técnico de Yankuilotl, si se consigue. Revisar si respondió la DME |
| Mar 6 oct (G1) | Aplicar la ruta de decisión de [[mapa-de-oportunidades]] §5 con la información que haya |
| Jue 8 oct | Fecha límite para confirmar con Yankuilotl si se eligió semiconductores en forma condicionada |

## 7. Huecos que internet no resolvió

Las fuentes que no se pudieron leer siguen en la tabla final de [[registro-de-fuentes]]. Destacan:
- el PDF completo del informe de la OCDE;
- el capítulo sobre falsas alarmas de AOI;
- la revisión de Sandia sobre inspección visual;
- el decreto de creación de Yankuilotl.

Ninguno bloquea G1. Sí conviene leerlos antes de redactar el estado del arte del protocolo.
