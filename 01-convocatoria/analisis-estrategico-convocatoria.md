---
titulo: "Análisis estratégico de la convocatoria"
tipo: analisis
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-002, F-003, F-004, F-005]
tags: [femeci, estrategia, riesgos, fase-1]
aliases: ["Análisis estratégico", "Implicaciones de la convocatoria"]
---

# Análisis estratégico de la convocatoria

> [!summary] En una frase
> FEMECI-PUEBLA 2026 premia un **proceso de investigación o ingeniería riguroso, hecho y defendido por los estudiantes y documentado en el tiempo**, más que un producto vistoso; y lo hace con un calendario muy corto: **17 días para entregar el expediente y 29 para defenderlo** (al 2026-10-01).

## 1. Qué parece buscar FEMECI (inferencias desde el texto)

| # | `#inferencia` | Evidencia en la convocatoria |
|---|---|---|
| 1 | El rigor metodológico es el valor central | Propósito: "premiar la excelencia y rigurosidad metodológica" [§1.1]; 50 de 100 puntos en el criterio A [§6.1] |
| 2 | El trabajo debe ser de los estudiantes | Todos los integrantes exponen y responden; prohibida la intervención de asesores [§7.4]; el líder resguarda la bitácora [§3.3]; descalificación por suplantación de autoría [§9.1] |
| 3 | Alineación con estándares nacionales de tipo ISEF | "estándares de evaluación y normatividad de la fase nacional" [§1.1]; formatos FE equivalentes a los de ISEF [F-003, F-005] |
| 4 | Pertinencia para el desarrollo de Puebla | Preámbulo: juventud "como motor del desarrollo sostenible e inclusivo del Estado"; A2 pide "impacto social, ambiental o productivo" |
| 5 | Originalidad con manejo ético de la información | Criterio B (25 pts) incluye "manejo ético de la información"; F-04 obligatorio; sanciones [§9.1] |
| 6 | Sustancia sobre costo, prestigio o estética | No se evalúa costo ni prestigio; se prohíben valoraciones estéticas ajenas al método [§6.3] |
| 7 | Un proceso verificable en el tiempo | Bitácora obligatoria en el expediente [§5] y evaluada en C3 ("evidencia cronológica") |

## 2. Estructura de la competencia

- #hecho Premios por nivel educativo: tres premios para **todo** el nivel superior [§8.1].
- #hecho Acreditación nacional: hasta 3 proyectos de superior, los de mayor puntaje global, con ≥ 80 [§1.3, §8.2].
- #inferencia Competimos contra todos los proyectos de nivel superior del estado, de cualquier categoría y modalidad. Llegar a 80 es condición necesaria, no suficiente: hay que quedar en el top 3. Meta interna: ≥ 90 (`#supuesto`).
- #hecho Hay dos filtros: revisión técnica del expediente por el CRC (19–23 oct) y evaluación presencial de finalistas (30 oct) [§4, §7.1].
- #inferencia El protocolo es la pieza que decide si llegamos a la jornada.
- #pregunta ¿El puntaje del CRC cuenta en la calificación final? (Q-004) ¿"Categoría desierta" se refiere a categoría temática o a nivel? (Q-007)

## 3. Modalidad y categoría: opciones (sin decidir)

- **Modalidad (D-005):** #inferencia "Ingenierías" encaja con el perfil del equipo y con la intención de diseñar, construir y probar un prototipo [§2.1]; en ella, A3 se evalúa como "metas técnicas alcanzables" y la estructura nacional pide "ejecución y construcción" [F-003]. "Ciencias" convendría si el núcleo del proyecto fuera generar conocimiento (por ejemplo, caracterizar un fenómeno con datos). Se decide en G1, cuando conozcamos el problema.
- **Categoría (D-006):** las líneas exploratorias del documento maestro caen sobre todo en "Sistemas Informáticos y Computación" (aprendizaje automático, visión artificial, ciberseguridad, sistemas embebidos e IoT) o en "Ingenierías y Tecnologías" (procesos industriales, materiales). #inferencia En Puebla la categoría no cambia el número de premios, pero probablemente sí el perfil de la terna; en la fase nacional define contra quién se compite [F-003].

## 4. La restricción dominante: el tiempo

- #hecho Al 2026-10-01 faltan **17 días** para el cierre (domingo 18 oct) y **29** para la jornada (viernes 30 oct); hay **12 días hábiles** para conseguir firmas institucionales.
- #inferencia La investigación estratégica (Fases 2 a 5 del documento maestro) cabe en **≈ 5 días** si queremos decidir el problema el 6 oct y tener el protocolo v1 el 14 oct.
- #inferencia Si la plantilla incluye resultados, necesitamos un **piloto con datos reales antes del 14 oct**.
- #inferencia El proyecto tiene que ser **pequeño en alcance y profundo en rigor**: una pregunta o meta verificable, con datos propios y un análisis honesto, vale más que un sistema amplio sin validar.

> [!warning] Evidencia que contradice una suposición nuestra
> El documento maestro asume un proceso amplio de investigación antes de decidir. La convocatoria no deja ese tiempo. Propuesta: investigar con tiempo acotado, decidir con evidencia **suficiente** (no completa) el 6 oct y seguir recolectando evidencia del problema durante la construcción. Plan detallado: [[calendario-y-plazos]].

## 5. Riesgos de incumplimiento

| ID | Riesgo | Consecuencia | Mitigación |
|---|---|---|---|
| R-01 | Expediente incompleto o tardío (firmas solo en días hábiles; cierre en domingo) | Quedamos fuera | Trámite de carta esta semana; envío el viernes 16 |
| R-02 | Plagio parcial: reutilizar texto, figuras o ideas del proyecto 2024 u otras fuentes sin citar | Descalificación inapelable [§9.1] | Registro de fuentes; citar todo; aclarar autoría del proyecto 2024 (Q-023); FE-07 si es continuidad |
| R-03 | Uso de IA interpretado como suplantación de autoría | Descalificación posible [§9.1]; precedente explícito en otro estado [F-004] | Política D-003: los estudiantes redactan todo lo entregable; IA declarada; bitácora registra el apoyo |
| R-04 | Datos alterados o percibidos como tales (sintéticos no declarados, exclusiones sin justificar, métricas cambiadas a posteriori) | Descalificación [§9.1] | Datos crudos inmutables con hash; plan de análisis registrado antes de probar; declarar datos sintéticos o aumentados |
| R-05 | Pruebas o encuestas con personas sin FE-04 ni consentimiento | Incumplimiento bioético [§9.1] | Diseñar pruebas sin participantes externos o tramitar FE-04 + consentimiento (Q-008) |
| R-06 | Trabajo en instalaciones industriales o laboratorios sin FE-1C | Incumplimiento de formatos [§5.1] | Confirmar con la DME (Q-009) |
| R-07 | Datos o piezas de una empresa que no podemos mostrar por confidencialidad | Resultados no exhibibles | Permiso escrito previo que diga qué se puede publicar; respetar la propiedad intelectual [§9.2] |
| R-08 | Un integrante no disponible el 30 oct o en marzo 2027 | No se puede sustituir [§3.3] | Confirmar disponibilidad y permisos ahora (Q-022) |
| R-09 | Asesor no adscrito a la UTP o con perfil poco congruente con el tema | Incumple §3.5 | Confirmar asesor; justificar congruencia; considerar asesor científico externo (§3.6) |
| R-10 | La demo falla en la jornada (sin red o sin energía) | Pérdida en A4 y C1 | Demo autónoma y video de respaldo (REQ-DER-01) |
| R-11 | Un integrante no domina parte del proyecto | Pérdida en C1 y C2; el asesor no puede ayudar [§7.4] | Entrenamiento cruzado; simulacros |
| R-12 | Alcance demasiado amplio para 29 días | Resultados débiles en A5 | Acotar; piloto antes de G2 |

## 6. Implicaciones para nuestra forma de trabajar

1. **Autoría.** La bóveda es material de trabajo. Lo que se entrega (protocolo, F-01, cartel, bitácora oficial) lo redactan Fortino e Israel; la IA apoya en búsqueda, organización y revisión, y eso se declara (D-003).
2. **Bitácora desde hoy.** Ya inició en [[bitacora-indice]]. Conviene una bitácora manuscrita en paralelo hasta que la DME aclare el formato (D-002) y un historial de versiones con sellos de tiempo (D-004).
3. **Evidencia antes que afirmaciones.** Cada afirmación del protocolo deberá rastrearse a una fuente (F-###) o a un dato propio (EXP-###, DS-##).
4. **Diseño de pruebas consciente de la ética.** Antes de diseñar validaciones con personas, considerar el costo de FE-04 y el consentimiento.
5. **Industria con reglas claras.** Si una empresa aporta datos, piezas o acceso, acordar por escrito qué se puede mostrar y cómo se citará.

## 7. Criterios de selección de proyecto que impone la convocatoria

Se suman a los criterios del documento maestro (§ "Cómo quiero que evalúes posibles proyectos") para comparar hipótesis de proyecto en `10-ideas-candidatas/`.

| Criterio | Pregunta de filtro |
|---|---|
| Evidencia del problema a tiempo | ¿Podemos documentar el problema con fuentes y validarlo con especialistas antes del ≈ 9 oct? |
| Medible en 29 días | ¿Podemos producir datos reales y un análisis cuantitativo antes del 28 oct? |
| Piloto factible | ¿Hay un experimento mínimo realizable antes del 14 oct? |
| Cumplimiento ético sencillo | ¿Evita participantes externos, agentes regulados e instalaciones reguladas, o podemos tramitar los FE a tiempo? |
| Demo segura y autónoma | ¿Se puede demostrar en una mesa, sin riesgo y sin depender de la red del recinto? |
| Explicable en 8–10 min | ¿La historia problema → método → resultado cabe en una exposición clara? |
| Datos con derechos claros | ¿Podemos usar y mostrar los datos (licencias, permisos)? |
| Defendible por ambos | ¿Ambos pueden dominar la teoría necesaria en el tiempo disponible? |
| Coherente con el asesor | ¿El perfil del asesor de la UTP es congruente con el tema, o necesitamos asesor científico externo? |

## 8. Conclusiones clave de la Fase 1

1. El calendario es la restricción dominante: 17 días al expediente, 29 a la jornada, 12 días hábiles para firmas.
2. El protocolo es el centro de gravedad: pesa la mitad del puntaje y es el filtro para ser finalista.
3. Para ganar hay que quedar en el top 3 de todo el nivel superior con ≥ 80; ningún subcriterio es opcional.
4. La rúbrica premia la cadena problema → metas → método → datos → conclusiones, defendida por los estudiantes y respaldada por la bitácora; coincide con el principio "problema antes que tecnología" del documento maestro.
5. Las causas de descalificación (plagio parcial, datos alterados, suplantación de autoría, bioética) obligan a cuidar desde hoy la autoría, el uso de IA, los datos crudos y las pruebas con personas.
6. La evidencia del problema debe obtenerse rápido: entrevistas con el sector en la semana del 5 de octubre.
7. Faltan datos clave que solo la DME puede dar (plantilla del protocolo, formato de la bitácora, hora de cierre, reglas de IA y de participantes humanos): conviene preguntar de inmediato.
8. "Ingenierías" + "Sistemas Informáticos y Computación" parece la combinación natural, pero se decide después de elegir el problema.
