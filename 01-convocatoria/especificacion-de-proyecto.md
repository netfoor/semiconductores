---
titulo: "Especificación de proyecto derivada de la convocatoria"
tipo: especificacion
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-003, F-004, F-005]
tags: [femeci, convocatoria, requisitos, fase-1]
aliases: ["Especificación FEMECI", "Requisitos de la convocatoria"]
---

# Especificación de proyecto derivada de la convocatoria

> [!abstract] Para qué sirve
> Convierte la convocatoria ([[convocatoria-femeci-puebla-2026]]) en una lista de requisitos verificables, como si fuera la especificación de un sistema. Cada requisito tiene un ID, su origen y cómo comprobaremos que lo cumplimos. Los requisitos de calidad (sección 9) traducen la rúbrica en atributos que una propuesta excelente debe demostrar; el detalle por criterio está en [[rubrica-y-evidencias]].
>
> **Tipos:** `Obligatorio` (texto expreso de la convocatoria) · `Condicional` (solo si se activa un supuesto) · `Recomendado` (la convocatoria lo sugiere) · `Derivado` (#inferencia nuestra a partir del texto; se indica la base).
> **Estados:** Pendiente · Por confirmar · Cumple (preliminar) · Cumple (verificado) · No aplica.

## 1. Elegibilidad y equipo (REQ-ELG)

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-ELG-01 | Cada integrante tiene matrícula oficial vigente en el ciclo 2026-2027 en una institución de educación superior con sede en Puebla | §3.1 | Obligatorio | Credencial vigente / constancia de estudios de cada integrante (Q-015, Q-021) | Por confirmar |
| REQ-ELG-02 | Equipo de 2 a 3 estudiantes | §3.2 | Obligatorio | Fortino Romero Mantilla e Israel Jesus Garcia Osorio (2 integrantes) | Cumple (preliminar) |
| REQ-ELG-03 | Designar Líder de Proyecto: registro formal, comunicación oficial y resguardo de la bitácora | §3.3 | Obligatorio | D-007: Fortino Romero Mantilla | Cumple |
| REQ-ELG-04 | Los integrantes registrados son irremplazables: ambos deben estar disponibles para la jornada (30 oct) y, si se acredita, para la fase nacional (marzo 2027) | §3.3, §8.2 | Obligatorio | Confirmación de disponibilidad (Q-022) | Por confirmar |
| REQ-ELG-05 | Cada estudiante participa en un solo proyecto de esta convocatoria | §3.4 | Obligatorio | Confirmación de ambos integrantes | Por confirmar |
| REQ-ELG-06 | Asesor(a) institucional obligatorio: docente o investigador(a) de la UTP, con perfil congruente con la temática | §3.5 | Obligatorio | D-008: Prof. José Francisco Espinosa Garita (UTP); falta justificar congruencia con el tema elegido (Q-019) | Cumple (preliminar) |
| REQ-ELG-07 | Asesoría científica externa para temas especializados (universidad, centro de investigación o industria) | §3.6 | Recomendado | Evaluar al definir el problema; posible FE-02 (Q-009, Q-013, Q-024) | Pendiente |
| REQ-ELG-08 | Participar en el nivel educativo "Superior" | Preámbulo, §1.3, §8.1 | Obligatorio | Registro en el nivel correcto | Cumple (preliminar) |

## 2. Proceso y plazos (REQ-PRC)

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-PRC-01 | Registrar proyecto y expediente en https://secihti-pue-dme.org/ entre el 17 sep y el 18 oct 2026 (gratuito) | §4, §5 (3.7) | Obligatorio | Comprobante/captura de envío en la plataforma | En curso (cuenta creada el 1 oct) |
| REQ-PRC-02 | Inscribir el proyecto en una modalidad (Ciencias o Ingenierías) | §2.1 | Obligatorio | Decisión D-005 | Pendiente |
| REQ-PRC-03 | Enmarcar el proyecto en una de las 8 categorías temáticas | §2.2 | Obligatorio | Decisión D-006 | Pendiente |
| REQ-PRC-04 | Superar la revisión técnica del CRC (19–23 oct) y aparecer como finalista (26 oct) | §4, §7.1 | Obligatorio | Correo de notificación / lista publicada | Pendiente |
| REQ-PRC-05 | Asistir presencialmente a la jornada del 30 oct 2026, Centro de Vinculación UPAEP | §4, §7.1 | Obligatorio | Logística confirmada (G4 en [[calendario-y-plazos]]) | Pendiente |

## 3. Expediente digital (REQ-DOC)

Seguimiento operativo de cada documento: [[checklist-expediente]].

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-DOC-01 | Todos los documentos en PDF legible | §5 (3.8) | Obligatorio | Revisión de legibilidad antes de cargar | Pendiente |
| REQ-DOC-02 | Identificación oficial por ambos lados (INE o pasaporte) de cada integrante | §5 (3.8) | Obligatorio | PDF por integrante | Pendiente |
| REQ-DOC-03 | Carta de Postulación y Respaldo Institucional con membrete y firma/sello de autoridad de la UTP | §5 (3.8) | Obligatorio | Carta firmada (trámite con lead time: Q-012, Q-020) | Pendiente |
| REQ-DOC-04 | Protocolo y Plan de Investigación con la estructura estandarizada de la modalidad, máximo 20 cuartillas | §5 (3.8) | Obligatorio | Plantilla oficial (Q-001) + conteo de páginas | Pendiente |
| REQ-DOC-05 | F-01 Ficha de inscripción y resumen ejecutivo | §5 (3.8) | Obligatorio | Formato lleno, consistente con el protocolo | Pendiente |
| REQ-DOC-06 | F-02 Revisión y validación del asesor | §5 (3.8) | Obligatorio | Firmado por el asesor | Pendiente |
| REQ-DOC-07 | F-03 Declaratoria y aprobación del estudiante | §5 (3.8) | Obligatorio | Firmado (probablemente uno por integrante) | Pendiente |
| REQ-DOC-08 | F-04 Declaración de originalidad y no plagio | §5 (3.8) | Obligatorio | Firmado; respaldado por registro de fuentes y licencias | Pendiente |
| REQ-DOC-09 | F-05 Autorización de uso de imagen y tratamiento de datos personales | §5 (3.8) | Obligatorio | Firmado por cada integrante | Pendiente |
| REQ-DOC-10 | Bitácora de investigación: registro cronológico de actividades | §5 (3.8), §3.3 | Obligatorio | PDF de la bitácora (formato: D-002, Q-006) | En curso (inicia 2026-10-01) |
| REQ-DOC-11 | Formatos FE que apliquen (FE-1C, FE-02, FE-03, FE-04, FE-05A/5B, FE-06A/6B, FE-07) | §5.1 | Condicional | Análisis de aplicabilidad en [[checklist-expediente]] tras definir el proyecto | Pendiente |

## 4. Jornada de exhibición (REQ-EXP)

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-EXP-01 | Cartel de 90 cm de ancho × 120 cm de alto (vertical) | §7.2 | Obligatorio | Archivo final a escala + impresión | Pendiente |
| REQ-EXP-02 | Prototipo exhibible en mesa, no peligroso | §7.2 | Obligatorio | Revisión de seguridad del prototipo (posible FE-03) | Pendiente |
| REQ-EXP-03 | Exposición oral de 8–10 min + 5–7 min de preguntas técnicas (15 min en total) | §7.3 | Obligatorio | Ensayos cronometrados | Pendiente |
| REQ-EXP-04 | Todos los integrantes participan activamente en exposición y defensa | §7.4 | Obligatorio | Guion con roles equilibrados; ambos responden cualquier tema | Pendiente |
| REQ-EXP-05 | Ninguna intervención del asesor, tutores o directivos durante la evaluación | §7.4 | Obligatorio | Preparación autónoma de los estudiantes | Pendiente |

## 5. Evaluación (REQ-EVA)

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-EVA-01 | Obtener ≥ 80.0/100 para ser elegible a premio y acreditación | §6.2, §8.2 | Obligatorio | Autoevaluación con [[rubrica-y-evidencias]] en G2 y G4 | Pendiente |
| REQ-EVA-02 | Estar entre los 3 mayores puntajes globales de nivel superior para la acreditación nacional | §1.3, §8.2 | Obligatorio | — (meta interna: ≥ 90) | Pendiente |
| REQ-EVA-03 | Cubrir los 11 subcriterios de la rúbrica (A1–A5, B1–B3, C1–C3) con evidencia | §6.1 | Obligatorio | Matriz criterio × evidencia | Pendiente |

## 6. Ética e integridad (REQ-ETI)

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-ETI-01 | Cero plagio, total o parcial: todo texto, figura, dato o código ajeno se cita | §9.1, F-04 | Obligatorio | [[registro-de-fuentes]]; revisión de originalidad antes de enviar | Pendiente |
| REQ-ETI-02 | Cero falsificación o alteración de datos | §9.1 | Obligatorio | Datos crudos inmutables con hash; transformaciones documentadas | Pendiente |
| REQ-ETI-03 | Cero suplantación de autoría: el trabajo y su redacción son de los estudiantes | §9.1, §7.4 | Obligatorio | Política de IA (D-003); bitácora con responsables | Pendiente |
| REQ-ETI-04 | Cumplir normativas de bioseguridad y bioética (participantes humanos, agentes regulados) | §9.1, §5.1 | Obligatorio | Análisis FE; consentimiento si hay personas (F-004, F-005) | Pendiente |
| REQ-ETI-05 | Respetar la propiedad intelectual: derechos de autores e instituciones | §9.2 | Obligatorio | Acuerdos escritos con terceros que aporten datos, piezas o instalaciones | Pendiente |

## 7. Después de ganar (REQ-PRE)

| ID | Requisito | Origen | Tipo | Verificación / evidencia | Estado |
|---|---|---|---|---|---|
| REQ-PRE-01 | Integrar documentos fiscales para cobrar el premio: INE/pasaporte, CSF del SAT (≤ 3 meses), kárdex, comprobante de domicilio, cartas libres | §8.3 | Condicional | Carpeta lista si somos premiados (Q-017) | No aplica aún |

## 8. Requisitos derivados (REQ-DER)

Son `#inferencia`: no están escritos literalmente, pero se desprenden del texto. Cada uno indica su base.

| ID | Requisito derivado | Base |
|---|---|---|
| REQ-DER-01 | La demo debe funcionar en una mesa, sin riesgo y sin depender de electricidad o internet del recinto (no garantizados); se prepara un video de respaldo | §7.2 solo garantiza cartel y mesa; Q-014 |
| REQ-DER-02 | Datos crudos preservados sin cambios (con hash), transformaciones documentadas y datos sintéticos o aumentados declarados como tales | §9.1 (falsificación o alteración de datos) |
| REQ-DER-03 | Cada resultado del protocolo y del cartel debe poder rastrearse a una entrada de bitácora y a un archivo de datos o experimento | C3 "coherencia y evidencia cronológica"; §9.1 |
| REQ-DER-04 | Registro de licencias y permisos de toda fuente, dataset, modelo y código de terceros | B3 "manejo ético de la información"; §9.1–9.2 |
| REQ-DER-05 | Los documentos entregables (protocolo, F-01, cartel, bitácora oficial) los redactan los estudiantes; el apoyo de IA se declara | §9.1 (suplantación de autoría); precedente de reglas de IA en otro capítulo estatal (F-004) |
| REQ-DER-06 | Ambos integrantes deben poder exponer y responder cualquier parte del proyecto | §7.4; C1 "todos los miembros"; C2 |
| REQ-DER-07 | Las firmas institucionales deben obtenerse a más tardar el viernes 16 oct (el cierre, 18 oct, es domingo) | §4; calendario |
| REQ-DER-08 | Si alguna prueba involucra a personas ajenas al equipo (encuestas, pruebas de usuario), tramitar FE-04 y consentimiento; si se trabaja en instalaciones industriales, evaluar FE-1C; si hay equipos o materiales peligrosos, FE-03 | §5.1; reglas ISEF (F-005) y formatos nacionales (F-003) |
| REQ-DER-09 | El protocolo debe caber en 20 cuartillas sin perder ninguna sección evaluada | §5 (3.8); §6.1 A1–A5 |
| REQ-DER-10 | Si el proyecto se basa en trabajo previo (p. ej., el proyecto de referencia 2024), declararlo y citarlo; si fue de los mismos autores, evaluar FE-07 | §5.1 (FE-07), §9.1; Q-011, Q-023 |

## 9. Atributos de calidad: cómo luce una propuesta excelente, de forma verificable

| ID | Atributo | Subcriterios | Cómo se verifica |
|---|---|---|---|
| AC-01 | Problema real, acotado y relevante, con evidencia triangulada (meta interna: ≥ 3 fuentes independientes, ≥ 1 primaria: entrevista o documento del sector) | A1, A2 | Ficha del problema en `08-problemas/`; cada afirmación tiene fuente |
| AC-02 | Pertinencia para Puebla demostrada con documentos oficiales o actores del sector, no con afirmaciones genéricas | A2 | Matriz de alineación (Fase 2) |
| AC-03 | Hipótesis o metas técnicas medibles, con umbral justificado y método de prueba definido de antemano | A3 | Tabla meta → métrica → umbral → origen del umbral → prueba |
| AC-04 | Diseño experimental con línea base o comparación, variables controladas, repeticiones y datos de prueba independientes | A4 | Plan de pruebas por experimento en `15-experimentos/` |
| AC-05 | Resultados reproducibles por un tercero a partir de datos crudos | A5, B3 | Instrucciones de reproducción (entorno con uv y archivo de bloqueo, scripts, commit) |
| AC-06 | Análisis con métricas adecuadas, incertidumbre, análisis de errores y conclusiones que responden a cada meta | A5 | Tabla meta → resultado → cumple / no cumple → discusión |
| AC-07 | Contribución original explícita frente al estado del arte (literatura, soluciones existentes, patentes, repositorios) | B1, A5 | Tabla de estado del arte + registro de búsquedas |
| AC-08 | Decisiones técnicas justificadas con alternativas evaluadas | B2, A4 | [[registro-de-decisiones]] |
| AC-09 | Integridad de la información: citas, licencias, permisos, consentimientos y uso de IA declarados | B3, §9 | Registro de fuentes y licencias; F-04 |
| AC-10 | Prototipo demostrable, seguro y autónomo durante la jornada | A4, C1 | Prueba de la demo en condiciones de jornada + video de respaldo |
| AC-11 | Exposición de 8–10 min con participación equilibrada y respuestas sólidas | C1, C2 | ≥ 3 simulacros cronometrados con jurado simulado |
| AC-12 | Bitácora continua y trazable a los resultados | C3 | Muestreo: cada resultado del cartel → entrada de bitácora |
| AC-13 | Consistencia total entre protocolo, F-01, cartel, exposición, demo y bitácora | Todos | Revisión cruzada antes de enviar (G3) y antes de la jornada (G4) |

Las metas numéricas internas (≥ 3 fuentes, ≥ 3 simulacros, ≥ 90 puntos) son `#supuesto` nuestro, no requisitos de la convocatoria.
