---
titulo: "Estudios existentes: informes, literatura, datasets y normas"
tipo: referencia
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-046, F-047, F-048, F-051, F-052, F-053, F-054, F-055, F-056, F-057, F-058, F-060, F-076]
tags: [femeci, semiconductores, estado-del-arte, fase-3]
aliases: ["Estado del arte", "Estudios existentes"]
---

# Estudios existentes: informes, literatura, datasets y normas

Primera revisión del estado del arte (alimenta EV-07 y el criterio B1 de la rúbrica). Lectura automatizada de resúmenes y páginas públicas: **antes de citar en el protocolo, leer el texto completo**. Lo que no se pudo leer está al final.

## 1. Informes sobre el ecosistema en México

| Estudio | Qué dice (lo relevante para nosotros) | Fuente |
|---|---|---|
| OCDE (feb 2026), *Promoting the Development of the Semiconductor Ecosystem in Mexico* | México se enfoca en "assembly, testing and packaging as well as semiconductor design"; fortalezas: apertura comercial, fuerza laboral grande y con experiencia, centros de investigación; cinco temas de mejora: coordinación institucional, **talento**, investigación local, infraestructura (electricidad y agua) e integración a cadenas globales | F-046 |
| CANIETI (2024), *Plan Maestro para el Desarrollo de la Industria de Semiconductores 2024–2030* | Metas: duplicar exportaciones y empleo, duplicar el diseño, relocalizar ATP por más de 10 mil millones de dólares, **relocalizar PCB y sustratos**, duplicar proveeduría local. Formación en ATP "deficitaria". **No menciona a Puebla** | F-048 |
| ASU sobre el informe de la OCDE (feb 2026) | México tiene talento pero necesita "faster coordination and deeper integration between public policy, industry, and higher education" | F-047 |

## 2. Inspección y control de calidad en ensamble electrónico

| Estudio | Hallazgo clave | Fuente |
|---|---|---|
| Ong, Tan, Teoh y Haron (2025), revisión de inspección visual de uniones de soldadura (*Int J Adv Manuf Technol*) | Retos abiertos: escasez y desbalance de datos, **generalización entre tarjetas distintas**, interpretabilidad, tiempo real, **hardware de bajo costo para pymes**, reflejos especulares e iluminación | F-052 |
| Siemens (2023), libro blanco sobre reducción de falsas alarmas en AOI (documento de proveedor) | Las máquinas AOI alarman en "5 to 70 percent of the passing throughput" y "up to 95 percent of those are false calls"; la revisión manual tiene "30 percent chance of an operator missing a real error"; el problema crece cuando una línea produce muchos modelos de tarjeta | F-051 |
| Klco et al. (2023), *Scientific Reports* (Semikron-Danfoss) | Detección de salpicaduras de soldadura en producción real: 198 imágenes de 15 MP → 24,000 recortes; YOLOv8n con mAP de 96.6 % y 90 ms por imagen; limitación: supone las mismas condiciones de iluminación en entrenamiento y prueba | F-053 |
| Jaswanth et al. (2026), *EPJ Web of Conferences* | **Raspberry Pi 5 + YOLOv11 (NCNN)** con banda transportadora para detectar componentes faltantes en tarjetas de fuentes conmutadas; ≈ 500 imágenes; 5–10 FPS, ≈ 3 s por tarjeta; **no reporta precisión ni sensibilidad** | F-054 |
| GÖPEL (s. f.), inspección de ensambles through-hole (documento de proveedor) | Dificultades del through-hole: tarjetas pesadas, componentes de hasta 80 mm, uniones del lado inferior, deformación por calor; sin datos de defectos | F-057 |
| See (2015), confiabilidad de la inspección visual humana (*Human Factors*; agregado en la Fase 4) | "For most inspection tasks, missed defects typically range from 20% to 30%"; en su estudio, los inspectores detectaron 85 % de los defectuosos pero rechazaron 35 % de piezas aceptables | F-060 |

## 3. Datasets públicos

| Dataset | Contenido | Tamaño | Licencia | Fuente |
|---|---|---|---|---|
| DsPCBSD+ (2024) | Defectos de **tarjeta desnuda** (9 clases: corto, abierto, mordida de ratón, etc.) captados por AOI industrial | 10,259 imágenes, 20,276 anotaciones | CC BY 4.0 | F-055 |
| DeepPCB (2019) | Pares plantilla/imagen de **tarjeta desnuda**, 6 clases | 1,500 pares | Por verificar | F-056 |
| SolDef_AI (2024) | Defectos de soldadura en **tarjetas ensambladas** | Por verificar | Por verificar | F-058 |
| HRIPCB, FICS-PCB, PCB-METAL, solder-joint-dataset | Identificados en búsqueda (ver pendientes) | — | — | — |
| MVTec AD 2 (2025; agregado en la Fase 4) | Detección de anomalías **sin ejemplos de defectos** en 8 escenarios industriales difíciles; los mejores métodos quedan por debajo de 60 % de AU-PRO | Más de 8,000 imágenes | Por verificar | F-076 |

`#inferencia` Casi todos los datasets abiertos y maduros son de **tarjeta desnuda**; los de **tarjeta ensamblada y uniones de soldadura** son más escasos y pequeños. Esto coincide con el reto de "escasez de datos" de la revisión de 2025 [F-052] y significa que un dataset propio de tarjetas ensambladas tendría valor real.

## 4. Normas a consultar

- **IPC-A-610**, *Acceptability of Electronic Assemblies*: criterios de aceptación visual de ensambles.
- **IPC J-STD-001**, *Requirements for Soldered Electrical and Electronic Assemblies*: requisitos de soldadura.
- Son normas de pago: preguntar si Yankuilotl o la biblioteca de la UTP tienen acceso. Si un proyecto clasifica defectos, sus clases deberían alinearse con estas normas.

## 5. Qué significa para la originalidad (`#inferencia`)

1. **"Raspberry Pi + cámara + YOLO para inspeccionar tarjetas" ya está publicado** [F-054]. La tecnología por sí sola no es original; la originalidad tendría que venir del **problema concreto** (por ejemplo, un defecto o una etapa de una planta poblana real), de **datos propios** y del **rigor de la validación** (métricas, línea base, condiciones reales), que es justo lo que le falta al trabajo de 2026.
2. La literatura documenta problemas generales del sector (falsas alarmas, inspección manual que pasa por alto errores, generalización entre muchos modelos de tarjeta); hay que verificar si alguno ocurre en Yankuilotl.
3. Si no se consigue acceso a una planta, los datasets de tarjeta desnuda permiten experimentar, pero se alejarían del problema local y harían más difícil justificar la pertinencia (A2).

## 6. Identificados, no leídos

| Estudio | URL | Motivo |
|---|---|---|
| "Surface Mounting Production Line AOI False Call Classification with Machine Learning Algorithms" (Springer) | https://link.springer.com/chapter/10.1007/978-3-031-74482-2_2 | Límite de solicitudes del servicio de lectura |
| "PCB Defects: A Unified Survey of Trends, Detection Techniques, and Limitations through Systematic Literature Review" (*J Electron Test*, 2025) | https://link.springer.com/article/10.1007/s10836-025-06198-y | Pendiente |
| "Automated detection and classification of soldering defects in PCBs using deep learning and optical and thermal imaging" (*J Intell Manuf*, 2025) | https://link.springer.com/article/10.1007/s10845-025-02691-5 | Pendiente |
| "Solder Joint Inspection on Printed Circuit Boards: A Survey and a Dataset" (IEEE, 2023) | https://ieeexplore.ieee.org/document/10129988/ | Pendiente |
| SolderNet (*AI Magazine*, 2023) | https://onlinelibrary.wiley.com/doi/full/10.1002/aaai.12129 | Error 403 |
| "Implementation of an AOI System for Solder Quality Classification of THT Solder Joints" (IEEE, 2018) | https://ieeexplore.ieee.org/document/8432492/ | Pendiente |
| "Deep Learning Driven Real-Time PCB Inspection Using an Optimized YOLO v9 Architecture" (2026) | https://www.sciencedirect.com/org/science/article/pii/S1546221826004832 | Pendiente |
| HRIPCB (2019) | https://digital-library.theiet.org/doi/full/10.1049/joe.2019.1183 | Pendiente |
| FICS-PCB (2020), dataset multimodal para aseguramiento de hardware | https://eprint.iacr.org/2020/366.pdf | Pendiente |
| solder-joint-dataset (GitHub) | https://github.com/furkanulger/solder-joint-dataset | Pendiente |
| Informe completo de la OCDE (PDF) | https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/02/promoting-the-development-of-the-semiconductor-ecosystem-in-mexico_ab1c92e8/02c81dec-en.pdf | Bloqueado para la herramienta; leerlo en el navegador |
