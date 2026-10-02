---
titulo: "Problemas documentados y oportunidades preliminares en semiconductores y electrónica"
tipo: analisis
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-040, F-041, F-042, F-043, F-044, F-046, F-048, F-051, F-052, F-054]
tags: [femeci, semiconductores, problemas, oportunidades, fase-3]
aliases: ["Oportunidades semiconductores"]
---

# Problemas documentados y oportunidades preliminares en semiconductores y electrónica

> [!warning] Estado
> Nada de esto es una propuesta de proyecto. Las oportunidades (`OP-##`) son **hipótesis** que solo pasarán a ideas candidatas (`IC-##`, Fase 5) si una entrevista o un documento confirma el problema.

## 1. Problemas documentados

| # | Problema | Dónde | Evidencia | Nivel |
|---|---|---|---|---|
| 1 | Laboratorios Kutsari abiertos con 15 meses de retraso; en octubre de 2025 "les faltaba equipo, así como internet" | Diseño y prueba de chips (Puebla) | Director del INAOE citado en prensa [F-044] | Medio (local, de infraestructura; no es un problema que un proyecto estudiantil resuelva) |
| 2 | Planta con demanda saturada y programación específica de máquinas por cada proyecto | Ensamble de tarjetas, Yankuilotl | Gobernador y Director de Tecnología en comunicados y prensa [F-042, F-043] | Medio (local; describe el proceso, no un fallo) |
| 3 | Falsas alarmas masivas en AOI ("up to 95 percent" de las alarmas) y errores de la revisión manual (≈ 30 % de errores reales no detectados) | Ensamble electrónico en general | Documento de proveedor [F-051] | Medio en la industria; **no verificado en Puebla** |
| 4 | Generalización deficiente de la inspección automática entre modelos de tarjeta, escasez de datos y costo del hardware para pymes | Ensamble electrónico en general | Revisión académica 2025 [F-052] | Alto en la literatura; **no verificado en Puebla** |
| 5 | Talento insuficiente, sobre todo en ATP; falta de coordinación entre política, industria y universidades | México | OCDE, CANIETI y ASU [F-046, F-047, F-048] | Alto (nacional) |

## 2. Oportunidades preliminares (hipótesis)

| ID | Hipótesis de oportunidad | Problema que la sustentaría | Qué hay que confirmar | Datos | Hardware | Riesgos y cumplimiento |
|---|---|---|---|---|---|---|
| OP-01 | Inspección visual asistida en una etapa que hoy se revise a mano en Yankuilotl (por ejemplo, uniones through-hole o soldadura manual) | 3, 4 | Que exista esa etapa manual y que los defectos importen | Imágenes propias en planta | Cámara + cómputo local | Acceso; FE-1C si se toman datos en planta; confidencialidad |
| OP-02 | Clasificación de falsas alarmas de AOI para reducir la revisión manual | 3 | Que Yankuilotl tenga AOI y guarde imágenes y decisiones del operador | Registros de su AOI | Cómputo local | Depende por completo de sus datos |
| OP-03 | Verificación de la primera pieza al cambiar de producto (comparar la tarjeta ensamblada contra la lista de componentes y el diseño) | 2 | Que el cambio de producto y la verificación inicial sean cuellos de botella | Archivos de diseño + imágenes | Cámara + cómputo local | Confidencialidad de diseños |
| OP-04 | Registro de defectos y trazabilidad ligera para una planta nueva (captura, tablero de control estadístico) | 2 | Que hoy no tengan trazabilidad digital | Datos de producción | Software | Más software de gestión que investigación; difícil mostrar rigor experimental |
| OP-05 | Automatización de pruebas y análisis de datos de caracterización de chips en los laboratorios Kutsari | 1 | Que tengan necesidades de software o datos y acepten estudiantes | Mediciones de laboratorio | Equipo del laboratorio | Acceso y supervisión; riesgo alto en 29 días |
| OP-06 | Material de formación con visión por computadora para criterios de aceptación de ensambles | 5 | Que la formación de operadores sea un problema para Yankuilotl | Imágenes de referencia | Cámara / celular | Impacto difícil de medir en 29 días |

## 3. Lectura (`#inferencia`)

1. Las oportunidades OP-01 a OP-03 son las que mejor encajan con las capacidades del equipo y con la rúbrica (prototipo, experimento cuantitativo, demo en mesa), **pero las tres dependen de lo que diga Yankuilotl**.
2. La literatura muestra que la tecnología base ya existe [F-054]; el valor estaría en resolver un problema verificado de una planta poblana con datos propios y validación rigurosa.
3. Si Yankuilotl no da acceso antes del ≈ 9 de octubre, la familia de semiconductores pierde fuerza frente a problemas con mejor evidencia pública (ver [[sintesis-fase-2]] §4).

> [!info] Fase 5 (2 oct)
> Estas oportunidades pasaron al [[mapa-de-oportunidades]] como ideas candidatas: OP-01 → IC-01, OP-02 → IC-03, OP-03 → IC-02, OP-04 → IC-04, OP-05 → IC-05 y OP-06 → IC-06.
