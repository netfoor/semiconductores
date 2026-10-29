---
titulo: "Registro de decisiones"
tipo: registro
estado: vigente
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, decisiones]
aliases: ["Decisiones", "Registro de decisiones"]
---

# Registro de decisiones

Cada decisión registra contexto, opciones, decisión, razones, consecuencias y quién decidió. Estados: **propuesta** (espera aprobación del equipo) · **adoptada** · **reemplazada por D-###** · **descartada**. Las decisiones no se borran; si cambian, se registra una nueva que reemplaza a la anterior.

## Resumen

| ID | Decisión | Estado | Fecha | Decide |
|---|---|---|---|---|
| D-001 | Estructura y convenciones de la bóveda | Adoptada (revisable) | 2026-10-01 | Claude (IA), por encargo del documento maestro |
| D-002 | Formato de la bitácora | **Adoptada: bitácora digital en la bóveda como fuente de verdad**; manuscrita solo si la DME la exige | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-003 | Política de uso de IA | **Adoptada: el equipo usará IA** (salvaguardas en la ficha) | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-004 | Versionado de la bóveda con git | **Adoptada** | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-005 | Modalidad (Ciencias o Ingenierías) | **Adoptada: Ingenierías** | 2026-10-18 | Equipo (comunicado por Fortino) |
| D-006 | Categoría temática | **Adoptada: Sistemas Informáticos y Computación** (robótica y máquinas inteligentes: visión artificial); confirmar contra el menú de la plataforma | 2026-10-18 | Equipo (comunicado por Fortino) |
| D-007 | Líder de Proyecto | **Adoptada: Fortino Romero Mantilla** | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-008 | Asesor institucional y posible asesor científico externo | **Adoptada (asesor institucional): Prof. José Francisco Espinosa Garita**; asesor externo pendiente | 2026-10-01 | Equipo (comunicado por Fortino) |
| D-009 | Ubicación del procesamiento (nube, local o híbrido) | Pendiente: se decide con un experimento después de elegir el problema | — | Equipo, con datos del experimento |
| D-010 | Tratamiento del proyecto 2024 de Mirai: ¿continuidad o antecedente? | **Adoptada: desarrollo desde cero, sin continuidad.** El proyecto 2024 queda solo como referencia del análisis | 2026-10-02 | Equipo (comunicado por Fortino) |
| D-011 | Problema elegido (G1): IC-01, inspección asistida de uniones through-hole, con procesamiento local; y política de confidencialidad: los entregables no nombran empresas específicas | **Adoptada** | 2026-10-18 | Equipo (comunicado por Fortino) |
| D-012 | Integración de una tercera integrante: María José de la Rosa Hernández | **Adoptada** | 2026-10-26 | Equipo (comunicado por Fortino) |
| D-013 | Autoría de los commits del prototipo | **Adoptada** | 2026-10-26 | Fortino |
| D-014 | Usar PCBSPDefect (público, CC BY 4.0) como validación externa preliminar (EXP-006) y dejar abierta la demo en línea | **Adoptada** | 2026-10-26 | Fortino (demo abierta); Claude (IA) propone el conjunto |
| D-015 | Interfaz centrada en el inspector: lo técnico y las declaraciones pasan a un anexo | **Adoptada** | 2026-10-29 | Fortino |
| D-016 | El inspector sigue en el ciclo; ruta hacia la automatización gradual por planta (fuera del alcance de esta investigación) | **Adoptada** | 2026-10-29 | Fortino; Claude (IA) ordena la idea |

## D-001 · Estructura y convenciones de la bóveda

- **Contexto:** el documento maestro pide una estructura lógica para convocatoria, rúbrica, investigación, actores, fuentes, proyecto 2024, problemas, entrevistas, ideas, decisiones, arquitectura, experimentos, dataset, bitácora, protocolo y documentación final, y distinguir hechos, inferencias, hipótesis e ideas del equipo.
- **Opciones:** (a) estructura plana con etiquetas; (b) carpetas numeradas en el orden del flujo de trabajo, con una nota índice por carpeta; (c) una nota por fuente desde el inicio.
- **Decisión:** (b), con un registro único de fuentes (que puede dividirse después), IDs estables y etiquetas de tipo de afirmación. Detalle en [[convenciones]] y mapa en [[inicio]].
- **Razones:** trazabilidad para el criterio C3; el orden de carpetas refleja el principio "problema antes que tecnología"; nombres sin acentos ni espacios funcionan bien con git y en cualquier sistema operativo; cada carpeta tiene contenido, así que se conserva aunque se versione.
- **Consecuencias:** las notas nuevas siguen las convenciones; el equipo puede cambiarlas registrando una nueva decisión.

## D-002 · Formato de la bitácora (adoptada)

- **Contexto:** Puebla exige una "Bitácora de Investigación: registro cronológico de actividades" en PDF [F-001 §5] y evalúa su "coherencia y evidencia cronológica" (C3). Otro capítulo estatal exige bitácora manuscrita presente en el stand [F-004]. Puebla no especifica el formato (Q-006).
- **Opciones consideradas:** (a) solo digital en la bóveda, exportada a PDF; (b) manuscrita oficial + digital detallada; (c) solo manuscrita.
- **Decisión (2026-10-01, ≈ 09:50):** (a). La bitácora digital de la bóveda ([[bitacora-indice]]) es la **fuente de verdad**; el historial de git aporta sellos de tiempo verificables. Se exportará a PDF para el expediente.
- **Condición:** si la DME responde que la bitácora debe ser manuscrita (Q-006), se reconsidera; en ese caso la manuscrita se derivaría de la digital.

## D-003 · Política de uso de IA (adoptada)

- **Decisión (2026-10-01, ≈ 09:50):** el equipo usará herramientas de IA en el proyecto.
- **Salvaguardas que se mantienen como práctica recomendada** mientras la DME no publique lineamientos (Q-010), porque la convocatoria descalifica por "suplantación de autoría" [§9.1], solo los estudiantes exponen y responden [§7.4] y otro capítulo estatal ya restringe la IA generativa en secciones clave [F-004]:
  1. Declarar el uso de IA en la metodología del protocolo y en la bitácora (qué se hizo con IA y qué verificó el equipo).
  2. Verificar contra la fuente original toda afirmación aportada por la IA antes de usarla.
  3. Que Fortino e Israel dominen todo el contenido y redacten con sus palabras los textos que se entregan (protocolo, resumen, cartel, guion).
  4. Las notas de la bóveda indican su autor (`autor:` en las propiedades).

> [!note] Versión anterior
> La propuesta original de D-003 (1 oct, sesión 1) planteaba que la IA no redactara secciones de los entregables. El equipo aprobó usar IA; las salvaguardas anteriores conservan ese espíritu sin prohibirlo, y se ajustarán a lo que responda la DME.

## D-004 · Versionado de la bóveda con git (adoptada)

- **Contexto:** C3 evalúa la evidencia cronológica; un historial de versiones da sellos de tiempo verificables y respaldo.
- **Decisión (2026-10-01, ≈ 09:08):** el equipo decide versionar la bóveda con git.
- **Implementación (2026-10-01, ≈ 09:10):** repositorio local en la carpeta `semiconductores/` (la carpeta padre `ObsidianVault/` no es un repositorio), rama `main`, `.gitignore` para archivos locales de Obsidian y del sistema. Primer commit: estado al cierre de la Fase 1. Autor de los commits: Fortino Romero Mantilla; los commits preparados con apoyo de IA llevan la línea `Co-Authored-By: Claude`.
- **Nota técnica:** para que git pueda borrar sus archivos temporales y de bloqueo desde la sesión de trabajo de Claude se habilitó el borrado en esta carpeta durante la sesión; solo se usa para archivos internos de `.git`.
- **Pendiente:** remoto privado (por ejemplo, GitHub) y si el código del prototipo irá en un repositorio aparte.

## D-005 · Modalidad (pendiente, G1)

Opciones y criterios en [[analisis-estrategico-convocatoria]] §3. Se decide al elegir el problema.

## D-006 · Categoría temática (pendiente, G1)

Opciones y criterios en [[analisis-estrategico-convocatoria]] §3. Considerar la fase nacional, donde se compite por categoría [F-003].

## D-007 · Líder de Proyecto (adoptada)

- **Decisión (2026-10-01):** **Fortino Romero Mantilla** es el Líder de Proyecto: responsable del registro formal, del canal oficial de comunicación y del resguardo de la bitácora [§3.3].
- **Equipo registrado:** Fortino Romero Mantilla (líder) e Israel Jesus Garcia Osorio. Los integrantes registrados son irremplazables [§3.3].
- **Avance:** el líder creó la cuenta en la plataforma de registro el 2026-10-01.

## D-008 · Asesor institucional y asesor científico externo (adoptada en parte)

- **Decisión (2026-10-01):** asesor institucional: **Prof. José Francisco Espinosa Garita** (UTP) [§3.5].
- **Pendiente:** justificar la congruencia de su perfil con la temática cuando se defina el problema; confirmar su disponibilidad para revisar el protocolo (14 oct) y firmar F-02 (15–16 oct) (Q-019).
- **Asesor científico externo** (universidad, centro de investigación o industria, opcional y recomendado para temas especializados [§3.6]): pendiente; se evaluará con los contactos del sector (Q-024).

## D-009 · Ubicación del procesamiento: nube, local o híbrido (pendiente)

- **Contexto:** el proyecto de referencia 2024 planteaba parte del procesamiento en la nube. El documento maestro pide compararlo técnicamente con la inferencia local (por ejemplo, en Raspberry Pi) **sin decidir todavía**.
- **Opciones:** A nube · B local en CPU · C local con acelerador · D híbrida · E local sin internet · F teléfono. Detalle en [[comparacion-nube-vs-edge]] §3.
- **Cómo se decidirá:** con el experimento de [[comparacion-nube-vs-edge]] §8. La regla de decisión se fija antes de medir: la opción más simple que cumpla latencia, exactitud, operación sin internet o confidencialidad si aplican, y costo.
- **Depende de:** el problema elegido (G1), el tiempo de ciclo (Q-044), la conectividad y la política de datos del usuario (Q-043, Q-037) y el internet en la mesa de exhibición (Q-014).
- **Registro:** 2026-10-01, Fase 4, por Claude (IA). Queda pendiente por instrucción del documento maestro.

## D-010 · Tratamiento del proyecto 2024 de Mirai (adoptada)

> [!success] Decisión del equipo (2026-10-02, ≈ 01:16, comunicada por Fortino)
> "Desarrollamos nosotros desde 0, no hay continuidad." El proyecto 2024 queda **solo como referencia del análisis** de Claude, porque es distinto de lo que se haría en Puebla.
> - **Consecuencias:** no se llena FE-07 ni se le pregunta a la DME (Q-011 cerrada); no se reutiliza código, textos, figuras ni datos de Mirai; el proyecto 2026 no se construye sobre el de 2024.
> - **Nota de transparencia:** si un evaluador pregunta por experiencia previa, se responde con la verdad (participaron en 2024 en un proyecto de Mirai), sin presentarlo como base de este (C2).
>
> Abajo queda la propuesta original del 1 oct, que consideraba mencionar el antecedente en el protocolo; el equipo eligió la variante sin continuidad.

- **Contexto:** Fortino e Israel participaron en 2024, durante su estancia en Mirai Innovation, en el proyecto *Industrial Semiconductor Inspection System with cloud-Based Inventory Control*. El autor principal fue Mirai (Q-023, respondida por Fortino el 1 oct, 16:07). Fortino pregunta si conviene o es obligatorio presentar el proyecto 2026 como continuidad.
- **Lo que dicen las reglas:**
  - FE-07 es un formulario "aplicable", que solo se entrega si hay continuidad [F-001 §5.1];
  - la rúbrica no da puntos por continuidad [F-001 §6.1];
  - el plagio parcial y la suplantación de autoría descalifican [F-001 §9.1];
  - los derechos son de autores e instituciones participantes [F-001 §9.2];
  - en el reglamento del que derivan los formatos, la continuidad se refiere a un proyecto previo del estudiante en el mismo campo, exige anexar el resumen y el plan anteriores, y solo se juzga el trabajo nuevo [F-077, F-078].
- **Opciones:**
  - (a) presentarlo como continuidad o "evolución" (FE-07);
  - (b) proyecto propio, declarando el antecedente de 2024 en el protocolo y la bitácora;
  - (c) proyecto propio sin mencionar el antecedente.
- **Propuesta:** (b).
- **Razones:**
  - la continuidad no suma puntos y obligaría a documentar un trabajo ajeno marcado como confidencial;
  - (c) arriesga preguntas de autoría y de originalidad;
  - (b) es transparente y convierte el antecedente en argumento de experiencia.
- **Condiciones:**
  - el proyecto 2026 debe ser realmente nuevo: problema, datos, código y método propios;
  - no reutilizar material de Mirai;
  - citar cualquier idea que se tome de él.

  Si el proyecto 2026 terminara reutilizando el prototipo de 2024, se reconsidera (a).
- **Confirmación pendiente (1 oct):** pregunta 11 del correo a la DME (Q-011). Detalle en [[analisis-proyecto-2024]] §12. *Superado el 2 oct por la decisión del equipo; la pregunta se retiró del correo.*

## D-011 · Problema elegido (G1) y confidencialidad (adoptada)

- **Decisión (2026-10-18, ≈ 19:15):** el equipo formaliza **IC-01**, inspección visual asistida de uniones soldadas through-hole, con humano en el ciclo y procesamiento local. Modalidad Ingenierías (D-005) y categoría Sistemas Informáticos y Computación (D-006).
- **Evidencia que la sostiene:** conversación con personal de una empresa de ensamble electrónico de Puebla (comunicada por Fortino): la validación de piezas conserva partes manuales y las fallas se revisan con mayor resolución a ojo humano. Es una sola fuente y sin cifras; el protocolo la declara así. Literatura: [[mapa-de-oportunidades]] IC-01.
- **Datos:** hoy no hay tarjetas ni imágenes. Se propone colaborar con un productor local para tarjetas (DS-02, opcional); el plan base es DS-01, tarjetas propias con defectos sembrados.
- **Confidencialidad:** la información de la empresa es privada; **ningún entregable nombra empresas específicas** y no se publican imágenes ni datos sin autorización escrita. En la bóveda y en el historial git sí consta el nombre; la bitácora que se entrega usa una versión con el nombre reservado y lo declara.
- **D-009** (nube, local o híbrido) sigue pendiente: se decide con EXP-003 y la regla fijada en el protocolo.
- **Riesgo aceptado:** sin resultados al momento de entregar; el criterio A5 queda expuesto y el protocolo lo declara.

## D-012 · Tercera integrante (adoptada)

- **Decisión (comunicada por Fortino el 2026-10-26):** el equipo queda integrado por Fortino Romero Mantilla (líder), Israel Jesús García Osorio y María José de la Rosa Hernández. La convocatoria permite equipos de 2 a 3 estudiantes y los integrantes registrados son irremplazables [F-001 §3.2, §3.3].
- **Consecuencias:** María José aparece en el protocolo, F-01, F-04, la carta de postulación, la carta del asesor y la bitácora, y firma su propio F-03 y F-05. Debe participar en la exposición y la defensa [§7.4] y no estar inscrita en otro proyecto [§3.4].
- **Pendiente:** confirmar la fecha real en que se integró, para registrarla en la bitácora sin inventarla, y la escritura exacta de los tres nombres según la INE.

## D-013 · Autoría de los commits del prototipo (adoptada)

- **Decisión (2026-10-26, comunicada por Fortino):** los commits del desarrollo del prototipo hechos por Claude (IA) quedan con autor Fortino Romero Mantilla y sin la línea `Co-Authored-By: Claude`. Reemplaza en ese punto la práctica descrita en D-004.
- **Lo que se mantiene para no perder transparencia (D-003):** cada sesión de desarrollo hecha por la IA se registra en la bitácora con responsable "Claude (IA)", qué se hizo y qué falta verificar; el protocolo declara el uso de IA.
- **Lo que no se hizo:** Fortino propuso también commits a nombre de María José. Claude (IA) no los firmó con su nombre porque ella no escribió ese código, y la convocatoria descalifica por suplantación de autoría [F-001 §9.1]. María José entra como revisora del repositorio, y su trabajo propio va con su nombre.

## D-014 · Validación externa con datos públicos y demo abierta (adoptada)

- **Datos:** sin tarjetas propias todavía, se usa el subconjunto b_dip de PCBSPDefect [F-080] para una validación preliminar (EXP-006). Se descartó SolDef_AI porque es de componentes SMD y los conjuntos de Hugging Face porque no declaran licencia. Las imágenes no se suben al repositorio: se descargan de Zenodo y se verifica su huella.
- **Demo:** femeci.foor.dev queda sin contraseña porque solo tiene datos sintéticos y solo el jurado tendrá la liga (decisión de Fortino, 26 oct). No se suben ahí datos de terceros (D-011). Actualización (26 oct, sesión 6): las páginas Fotos reales, Reto y Experimentos muestran 60 fotos públicas de PCBSPDefect (CC BY 4.0, con atribución) y el modelo de EXP-006; siguen sin subirse imágenes de empresas.

## D-015 · Interfaz centrada en el inspector (adoptada)

- **Decisión (2026-10-29, Fortino):** la plataforma y la demostración muestran el sistema como lo usaría un inspector. Las aclaraciones técnicas, el uso de IA y el origen de los datos dejan las pantallas principales y pasan a una página «Acerca de la demostración», a la bitácora y al protocolo. Se reducen los pasos manuales (sesión de inspector, número de tarjeta automático, un solo botón para tomar la foto) y se cambia el tono de los textos a uno de presentación. Spec: [[spec-interfaz-v2]].
- **Razón:** en una presentación pesa más la idea y su uso que la tecnología; los avisos grandes distraen de lo que el sistema hace. Los evaluadores tienen la bitácora y el protocolo.
- **Salvaguardas que se mantienen (D-003, D-014):** la demostración se identifica con una etiqueta «Demostración» que lleva al anexo; nunca se presenta un dato sintético o público como propio; el crédito CC BY 4.0 de PCBSPDefect queda junto a sus fotos; el uso de IA sigue declarado en el protocolo y la bitácora.

## D-016 · Humano en el ciclo y ruta hacia la automatización (adoptada)

- **Pregunta que responde:** si el inspector sigue revisando, ¿de qué sirve el sistema? ¿No es la inspección manual con una capa más?
- **Decisión (2026-10-29, idea de Fortino ordenada por Claude (IA)):** el inspector se mantiene en el ciclo porque hoy cumple dos funciones que el sistema no puede cubrir: garantizar la calidad mientras el modelo no ha demostrado ser confiable en esa planta, y producir, con cada confirmación o corrección, los ejemplos con los que el modelo de esa planta mejora. La ruta tiene tres fases:
  1. **Apoyo (este proyecto).** El inspector deja de revisar el 100 % de las uniones con la misma atención y revisa primero las marcadas; cada decisión queda registrada. `#hipotesis` Así detecta más defectos y en menos tiempo que sin apoyo; se mide con M3 (EXP-005).
  2. **Piloto por empresa (siguiente paso, con una planta colaboradora).** Cada empresa tiene su propio modelo, entrenado con sus tarjetas, porque los defectos, la iluminación y los diseños cambian de planta a planta. Las decisiones del inspector se vuelven etiquetas, sin un etiquetado aparte.
  3. **Automatización gradual (fuera del alcance de esta investigación).** Cuando los datos de esa planta muestren un desempeño suficiente, con un umbral calibrado, las uniones con confianza muy alta pasan sin revisión y solo las dudosas llegan a la persona, con auditorías por muestreo. El inspector pasa de filtrar todo a supervisar los casos difíciles.
- **Lo que no se afirma:** que el sistema ya sirve para desplegarse ni que ahorra tiempo; eso se mide. La observación exploratoria del 29 oct (la red de EXP-006 falla con una tarjeta de otra fuente) respalda que cada planta necesita su propio modelo.
- **Dónde aparece:** sección «Hacia dónde va» de la página del proyecto; protocolo (trabajo futuro) y exposición, al actualizarlos.
