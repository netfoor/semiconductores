---
titulo: "Protocolo y Plan de Investigación v1 (Ingenierías)"
tipo: entregable
estado: borrador
creado: 2026-10-18
actualizado: 2026-10-18
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-014, F-043, F-046, F-048, F-051, F-052, F-057, F-060, F-061, F-073, F-079]
tags: [femeci, protocolo, entregable, ic-01]
aliases: ["Protocolo v1"]
---

<!-- CONSTRUCCIÓN: lo que sigue a esta línea es el texto del PDF. Compilar con 12-protocolo/herramientas/build.py -->

::: {custom-style="TitlePageTitle"}
Estación de inspección visual asistida con procesamiento local para uniones soldadas through-hole en el ensamble electrónico: diseño y validación experimental de un prototipo
:::

::: {custom-style="TitlePageText"}
Fortino Romero Mantilla e Israel Jesus Garcia Osorio
:::

::: {custom-style="TitlePageText"}
Universidad Tecnológica de Puebla
:::

::: {custom-style="TitlePageText"}
Asesor institucional: José Francisco Espinosa Garita
:::

::: {custom-style="TitlePageText"}
FEMECI-PUEBLA 2026 · Nivel Superior · Modalidad Ingenierías · Categoría Sistemas Informáticos y Computación (robótica y máquinas inteligentes: visión artificial)
:::

::: {custom-style="TitlePageText"}
18 de octubre de 2026
:::

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Resumen {-}

Las uniones soldadas de componentes through-hole se revisan en buena medida a ojo, y la literatura muestra que la inspección visual humana deja pasar entre 20 % y 30 % de los defectos en la mayoría de las tareas (See, 2015). En una conversación con personal técnico de una empresa de ensamble electrónico de Puebla, se nos informó que la validación de piezas conserva etapas manuales y que, cuando algo falla, se revisa con mayor resolución a ojo humano (comunicación personal, octubre de 2026). Planteamos el siguiente reto de ingeniería: ¿es posible construir una estación de bajo costo, con cámara de alta resolución e inferencia local, que señale las uniones through-hole sospechosas con una sensibilidad y una tasa de falsas alarmas conocidas, sin conexión a internet y en un tiempo compatible con una estación de revisión? Proponemos un prototipo con humano en el ciclo: el sistema marca, la persona decide. Lo evaluaremos con un conjunto de datos propio de al menos 30 tarjetas con defectos sembrados a propósito, partido por tarjeta, con criterios de aceptación fijados antes de medir, línea base humana y línea base de visión clásica. A la fecha de este documento no existen resultados experimentales; el protocolo define cómo se obtendrán y cómo se reportarán, incluidos los resultados desfavorables.

*Palabras clave:* inspección de soldadura, through-hole, visión artificial, cómputo en el borde, control de calidad, ensamble electrónico

# 1. Introducción

Puebla ha puesto en su agenda pública el desarrollo de capacidades en electrónica y semiconductores. El diagnóstico nacional de la OCDE describe a México como fuerte en ensamble, prueba y encapsulado y en diseño, y propone fortalecer el ecosistema (OECD, 2026); el plan maestro de la industria incluye entre sus metas 2030 relocalizar la manufactura de tarjetas de circuito impreso y el ensamble, y señala una formación insuficiente de talento en estas etapas (CANIETI, 2024). En el estado, el anuncio de manufactura de tarjetas electrónicas para 2027 se acompañó de la declaración de que la planta de ensamble ya estaba saturada por la demanda (El Universal Puebla, 2026). Cuando una línea de ensamble crece, la calidad depende cada vez más de qué tan bien se detectan los defectos, y no solo de qué tan rápido se produce.

Este proyecto parte de un problema, no de una tecnología: la verificación de soldaduras through-hole conserva pasos manuales que dependen de la agudeza visual del inspector. Nuestra propuesta es una estación de apoyo a esa verificación. En el resto del documento exponemos los antecedentes (sección 2), el reto de ingeniería (3), su justificación (4), las metas técnicas medibles (5), la metodología y el plan de pruebas (6), el diseño del prototipo (7), cómo se reportarán los resultados (8), el cronograma (9) y las conclusiones esperadas y los límites (10).

**Delimitación.** El proyecto no pretende reemplazar al inspector, certificar tarjetas, ni cubrir todos los tipos de defecto o de tecnología de montaje. Se limita a uniones through-hole, a cinco clases de defecto y una de unión aceptable (sección 6.2) y a una estación fija de revisión, no a inspección a velocidad de línea.

# 2. Antecedentes

## 2.1 Inspección visual humana

En una revisión de la confiabilidad de la inspección visual en piezas de precisión, See (2015) reporta que en la mayoría de las tareas de inspección los defectos no detectados oscilan entre 20 % y 30 %. En el estudio que presenta, los inspectores rechazaron correctamente 85 % de las piezas defectuosas y rechazaron por error 35 % de las aceptables. Estas cifras no son de soldadura ni de nuestra población de inspectores, por lo que las usamos solo como referencia de orden de magnitud; la línea base que sí comparamos es la que medimos nosotros (experimento EXP-001, sección 6.5). Un proveedor de inspección óptica automatizada (AOI) estima que alrededor de 30 % de los errores reales no se detectan en la revisión manual, y que entre las alarmas de los sistemas automáticos hasta 95 % pueden ser falsas (Siemens Digital Industries Software, 2023). Esta última fuente es de un proveedor, por lo que la tratamos como indicio y no como medición independiente.

## 2.2 El caso through-hole

Las uniones through-hole son difíciles de inspeccionar automáticamente porque parte de la unión está en el lado inferior de la tarjeta, hay componentes altos que ocultan zonas y el calor deforma materiales (GÖPEL electronic, s. f.). Además, al cambiar de producto, la verificación de la primera tarjeta puede ser lenta: una ponencia técnica de proveedor reporta cerca de tres horas de inspección manual por cambio de producto en tarjetas de 300 a 600 componentes, frente a cerca de 0.6 horas con automatización (Ross, 2006). Es un dato antiguo y de proveedor; lo usamos para ilustrar la magnitud posible del problema y no como cifra para el contexto local.

## 2.3 Estado del arte técnico

Ong et al. (2025) revisan la inspección visual de uniones soldadas para aplicaciones industriales y señalan retos abiertos, entre ellos la dependencia de la iluminación y de los datos disponibles. Existen conjuntos de datos públicos de defectos en tarjetas y trabajos de detección con modelos ligeros en computadoras de placa única; revisamos estas opciones y sus licencias en el registro de búsquedas (Anexo A). Con esa revisión concluimos que detectar defectos en tarjetas con una red convolucional pequeña en una Raspberry Pi **no es en sí una novedad**. Lo que buscamos aportar es otra cosa (sección 4): una evaluación honesta y reproducible de un sistema de apoyo con humano en el ciclo, en la tecnología through-hole, con datos propios etiquetados de forma controlada, criterios de aceptación definidos antes de medir y una comparación explícita con la inspección humana y con una línea base de visión clásica.

## 2.4 Dónde procesar: nube, local o híbrido

Las revisiones sobre cómputo en el borde y en la nube señalan que el borde reduce la latencia y la carga de red y favorece la privacidad, pero limita el cómputo; la nube escala mejor, pero añade latencia y riesgos de privacidad; los esquemas híbridos atienden las limitaciones de ambos (Andriulo et al., 2024). Como las imágenes de tarjetas de una planta pueden ser confidenciales, no asumimos la nube: la ubicación del procesamiento es una decisión de ingeniería que se toma con un experimento (EXP-003) y una regla definida de antemano.

# 3. Planteamiento del problema y reto de ingeniería

**Quién.** Inspectores, técnicos de calidad y personal de retrabajo en estaciones de ensamble through-hole y de soldadura manual de una línea de manufactura electrónica en Puebla.

**Qué ocurre.** Personal técnico de una empresa de ensamble electrónico del estado nos informó que la validación de piezas todavía tiene partes manuales y que, cuando algo falla, se revisa con mayor resolución a ojo humano (comunicación personal, octubre de 2026). Esta es una fuente primaria pero única, de una sola organización, cuyo nombre se reserva por confidencialidad; la tratamos como un indicio local que motiva el problema y no como una cifra del sector.

**Cómo se resuelve hoy.** Inspección visual humana, con apoyo de mayor resolución cuando se sospecha una falla.

**Por qué no basta.** La inspección visual humana es falible y variable (See, 2015), y la revisión con más resolución depende de que alguien ya sospeche. No contamos con una cifra de la tasa de error de la empresa consultada y no la inventamos; si la obtenemos, la usaremos como línea base y se registrará con permiso.

**Reto de ingeniería.** Diseñar, construir y evaluar una estación de inspección asistida que, con cámara de alta resolución e inferencia local, señale uniones through-hole sospechosas y cumpla las metas técnicas de la sección 5.

**Pregunta de ingeniería.** ¿Puede una estación de bajo costo con inferencia local alcanzar una sensibilidad y una tasa de falsas alarmas medidas y aceptables, en un tiempo por tarjeta compatible con una estación de revisión y sin conexión a internet, y cómo se compara con la inspección humana sin asistencia en las mismas condiciones?

**Alcance.** *Sí:* uniones through-hole en tarjetas de práctica; cinco clases; estación fija; operación sin red; evaluación con datos propios y, si se concreta, validación externa con tarjetas aportadas por un productor local. *No:* certificación según IPC-A-610; inspección en línea a alta velocidad; tecnologías SMD; decisiones automáticas de rechazo sin humano.

# 4. Justificación

**Pertinencia local.** La electrónica y los semiconductores son una prioridad en la agenda pública de Puebla (El Universal Puebla, 2026) y de la política industrial nacional (CANIETI, 2024; OECD, 2026). Una línea de ensamble en crecimiento necesita herramientas de calidad, y un componente de verificación asistida es aplicable en cualquier productor de tarjetas del estado sin depender de un proveedor específico.

**Beneficiarios.** Inspectores y técnicos de calidad (menos carga visual y menos omisiones), responsables de proceso (datos objetivos de defectos por estación) y centros de formación de técnicos (retroalimentación inmediata sobre la calidad de una soldadura).

**Impacto plausible.** Nuestro objetivo no es afirmar un ahorro, sino medir tres cantidades con incertidumbre: sensibilidad, falsas alarmas y tiempo. Si las metas se cumplen, el prototipo demuestra que una solución local y de bajo costo es técnicamente posible para esta tarea. Si no se cumplen, el análisis de errores indicará qué condiciones lo impiden. En ambos casos el resultado es útil.

**Contribución.** (1) Un conjunto de datos propio, documentado, con defectos sembrados y partición por tarjeta. (2) Una evaluación con criterios fijados antes de medir, con intervalos de confianza y comparación contra línea base humana y de visión clásica. (3) Una decisión de arquitectura (nube, local o híbrida) justificada con mediciones y no con preferencia.

# 5. Objetivos y metas técnicas

**Objetivo general.** Diseñar, construir y evaluar experimentalmente una estación de inspección visual asistida de uniones soldadas through-hole con procesamiento local.

**Objetivos específicos.**

1. Definir las clases de condición de soldadura y el criterio de etiquetado, tomando como referencia la norma de aceptabilidad de ensambles electrónicos IPC-A-610 (IPC, s. f.), consultada a través de material de acceso disponible.
2. Construir un conjunto de datos propio con protocolo de captura, etiquetado por dos personas y partición por tarjeta.
3. Implementar una línea base de visión clásica y al menos un clasificador basado en aprendizaje profundo ligero.
4. Medir el desempeño, la latencia y la robustez del sistema en el hardware objetivo, sin conexión.
5. Comparar el sistema con la inspección humana sin asistencia.
6. Decidir la ubicación del procesamiento con base en las mediciones.

**Metas técnicas.** Los umbrales son valores iniciales y se fijan antes de observar los datos de prueba. Si se modifican con base en información del usuario, el cambio y su razón se registran en la bitácora antes de ejecutar EXP-002.

| ID | Meta | Umbral inicial | Origen del umbral | Prueba |
|:--|:--------------------|:------------|:--------------------|:-----|
| M1 | Sensibilidad para cualquier defecto, con el límite inferior del intervalo de confianza de 95 % (Wilson) | ≥ 0.90; límite inferior ≥ 0.85 | Referencia de orden de magnitud: 0.85 de inspectores en See (2015); la línea base real es EXP-001 | EXP-002 |
| M2 | Tasa de falsas alarmas (uniones buenas señaladas) | ≤ 0.15 | Referencia: 0.35 en See (2015); una tasa alta anula el beneficio del apoyo | EXP-002 |
| M3 | Sensibilidad asistida frente a no asistida, mismas tarjetas | Asistida ≥ no asistida (exploratoria) | Objetivo de utilidad del apoyo | EXP-005 |
| M4 | Latencia de captura a resultado por tarjeta, en Raspberry Pi 5 sin red | Mediana ≤ 5 s; percentil 95 ≤ 8 s | Requisito de diseño para una estación de revisión; se validará con el usuario | EXP-003 |
| M5 | Funcionalidad principal con la red desconectada | 100 % de las funciones de captura, inferencia y registro | Confidencialidad y no depender del recinto | EXP-003 |
| M6 | Pérdida de sensibilidad ante variaciones controladas de iluminación y posición | Caída absoluta ≤ 0.05 | Requisito de robustez para uso en una estación real | EXP-004 |

Una meta no cumplida se reporta como no cumplida, con su análisis de errores.

# 6. Metodología

## 6.1 Proceso de diseño

Seguimos la secuencia requisitos, alternativas, selección con criterios, construcción, pruebas e iteración. Cada decisión de diseño con alternativas se registra en el registro de decisiones de la bóveda del proyecto (D-###) y cada actividad en la bitácora (Anexo B). La bóveda está versionada con git, de modo que las fechas de cada cambio son verificables.

## 6.2 Clases de condición

Cinco clases de defecto y una de unión aceptable, definidas en el protocolo de etiquetado y alineadas con IPC-A-610 en lo que la norma permite verificar sin acceso a su texto completo:

1. Unión aceptable.
2. Soldadura insuficiente (llenado incompleto del barril).
3. Puente de soldadura entre pines.
4. Pin sin soldar u omitido.
5. Exceso de soldadura.
6. Unión fría o deslustrada.

La unión fría es la clase más difícil de sembrar de forma reproducible; si no se logran ejemplos suficientes, se reporta y se excluye de las metas con justificación, no en silencio.

## 6.3 Datos (DS-01)

*Material.* Al menos 30 tarjetas de práctica through-hole con al menos 60 uniones cada una, soldadas por los integrantes, con defectos sembrados de manera intencional y registrados en una hoja de control antes de la captura.

*Captura.* Soporte fijo, cámara de al menos 12 megapíxeles a distancia constante, iluminación difusa tipo anillo y dos condiciones de iluminación. Cada tarjeta se fotografía por ambos lados. Los archivos crudos se conservan sin cambios con huella SHA-256; toda transformación se hace con scripts versionados.

*Etiquetado.* Dos personas etiquetan cada unión de forma independiente sin consultar la hoja de siembra; los desacuerdos se resuelven por consenso y se reporta el acuerdo entre etiquetadores (kappa de Cohen). Las etiquetas se contrastan con la hoja de siembra y las discrepancias se analizan como ruido de etiqueta.

*Partición.* Por tarjeta (no por imagen ni por unión) para evitar fuga de información: aproximadamente 60 % entrenamiento, 20 % validación y 20 % prueba. El conjunto de prueba se define antes de entrenar, se congela con huella y solo se usa para la evaluación final.

*Tamaño y justificación.* Con unos 150 defectos en prueba, el intervalo de confianza de 95 % de una sensibilidad cercana a 0.90 tiene una semiamplitud aproximada de ±0.05 (1.96 × raíz de 0.90 × 0.10 / 150 ≈ 0.048). Por clase, los intervalos serán más amplios y así se reportarán. Si las tarjetas logradas son menos de las planeadas, se reporta el tamaño real y se ajusta la interpretación.

*Datos externos (DS-02, opcional).* Proponemos colaborar con un productor local que aporte tarjetas bajo acuerdo escrito, para una validación externa independiente; esta colaboración aún no está acordada, no es necesaria para el proyecto y las tarjetas externas no se usan en el entrenamiento principal. No se incluirán diseños, marcas ni datos de clientes, y ninguna imagen se publicará sin autorización escrita. Si el acuerdo no se concreta, el proyecto se evalúa solo con DS-01 y se declara así.

## 6.4 Modelos y líneas base

- **Línea base clásica.** Segmentación por umbral y morfología con características de color y forma por unión.
- **Clasificador ligero.** Clasificación por recorte de unión con una red convolucional pequeña preentrenada y ajustada (transferencia de aprendizaje). Se elegirá con criterios (exactitud, latencia, licencia) y se justificará en el registro de decisiones. Daremos prioridad a modelos con licencia permisiva; si se usa software con licencia AGPL, el código se publicará bajo una licencia compatible (Ultralytics, 2026).
- **Referencia de hardware.** En una Raspberry Pi 5 se han publicado 67 ms por imagen con un detector pequeño a 640 píxeles en CPU (Ultralytics, 2026), cifra de un banco de pruebas estándar y no de tarjetas. Como las uniones son pequeñas, probablemente se requiera mayor resolución o procesamiento por recortes; lo medimos en EXP-003.

## 6.5 Experimentos

Cada experimento se registra antes de ejecutarlo (objetivo, hipótesis, métricas y criterio de aceptación) y también se registran las corridas fallidas.

- **EXP-001. Línea base humana.** Los dos integrantes inspeccionan, sin asistencia y a ciegas respecto de la hoja de siembra, las tarjetas del conjunto de prueba; cada uno revisa tarjetas soldadas por el otro para reducir el conocimiento previo. Se mide sensibilidad, falsas alarmas y tiempo por tarjeta. Limitación: los inspectores no son técnicos con experiencia industrial.
- **EXP-002. Desempeño del sistema.** Línea base clásica y clasificador ligero sobre el conjunto de prueba. Se reportan matriz de confusión, sensibilidad y precisión por clase, curva precisión-sensibilidad e intervalos de confianza por *bootstrap* por tarjeta, con cinco semillas de entrenamiento.
- **EXP-003. Latencia y ubicación del procesamiento.** Medición de captura a resultado en Raspberry Pi 5 sin red (al menos 30 repeticiones, mediana y percentil 95), y estimación del tiempo de subida a un servicio remoto con la medición de la red disponible, para comparar nube, local e híbrido. *Regla de decisión fijada de antemano:* se elige la opción más simple que cumpla las metas de latencia, la operación sin internet y la confidencialidad; la nube solo se elige si el local no cumple M4.
- **EXP-004. Robustez.** Variaciones controladas de iluminación (dos niveles y un ángulo adicional) y desplazamiento de la tarjeta (±3 mm), midiendo la caída de sensibilidad.
- **EXP-005. Asistido frente a no asistido (exploratorio).** Los integrantes inspeccionan las tarjetas de prueba con las marcas del sistema y se compara con EXP-001 mediante la prueba de McNemar. Con dos personas, el resultado se reporta como exploratorio.

## 6.6 Análisis de datos

Métricas adecuadas a clases desbalanceadas (sensibilidad, precisión, falsas alarmas), no solo exactitud; intervalos de Wilson para proporciones y *bootstrap* agrupado por tarjeta, porque las uniones de una misma tarjeta no son independientes; análisis de errores con ejemplos de falsos positivos y falsos negativos; y conclusiones meta por meta.

## 6.7 Seguridad, ética y uso de herramientas

*Seguridad.* La soldadura involucra herramientas calientes y humos; se trabajará con ventilación y protección y se evaluará la aplicabilidad del formato de evaluación de riesgo (FE-03). El prototipo exhibido no incluye herramientas calientes ni alta tensión.

*Participantes humanos.* La línea base y la prueba asistida se realizan con los propios integrantes, sin personas externas; si en el futuro un técnico externo prueba el sistema, se tramitará el formato correspondiente (FE-04).

*Confidencialidad y propiedad intelectual.* No se usan datos de terceros sin autorización escrita de uso y de publicación; no se menciona a empresas específicas; las fuentes, licencias y permisos se registran. El proyecto se desarrolló desde cero y no reutiliza código, datos ni textos de proyectos anteriores.

*Uso de inteligencia artificial.* Declaramos el uso de un asistente de IA (Claude; Anthropic, 2026) como apoyo en búsqueda de información, organización del repositorio, revisión de estructura y borradores de trabajo. Los integrantes verifican cada afirmación con la fuente original, redactan y defienden el contenido entregado y registran en la bitácora qué se hizo con IA y qué verificó el equipo.

*Reproducibilidad.* Entorno de Python gestionado con uv y archivo de bloqueo, semillas fijas, versión del código por *commit* y ubicación de datos crudos y resultados en el repositorio del proyecto.

# 7. Diseño y construcción del prototipo

**Función.** La estación captura la imagen de la tarjeta, localiza cada unión, la clasifica y muestra al operador las uniones sospechosas con su clase y nivel de confianza. El operador acepta o corrige, y cada decisión se registra con fecha, tarjeta, unión y resultado. La decisión final es siempre de la persona.

**Arquitectura inicial.** Captura, preprocesamiento, inferencia, interfaz y registro en una sola computadora de placa única, sin dependencia de red. La carga de datos a un servicio remoto es opcional y no necesaria para la función principal. Esta arquitectura es una hipótesis de partida y se confirmará o se descartará con EXP-003; la nube, la opción local con acelerador y la híbrida se consideran como alternativas (Andriulo et al., 2024).

**Hardware.** Raspberry Pi 5, cámara de al menos 12 megapíxeles, iluminación difusa y soporte con altura fija; entrenamiento en una computadora con GPU. Las características exactas se documentan en la ficha del montaje con fotografías fechadas, y cada iteración del prototipo queda con su versión en el repositorio.

**Demostración.** El prototipo funciona sin internet ni conexión del recinto y cuenta con un video de respaldo.

# 8. Resultados

**Estado al 18 de octubre de 2026: no hay resultados experimentales.** Este documento presenta el diseño y el plan de pruebas. No presentamos cifras de desempeño, y no hay datos de validación en este momento. Los resultados se obtendrán siguiendo la sección 6 y se reportarán, completos y sin selección, en el cartel y en la exposición del 30 de octubre, con su entrada de bitácora y su archivo de datos.

La tabla siguiente es la estructura en la que se reportarán, junto con los criterios ya fijados.

| Meta | Resultado medido | Intervalo de confianza | Cumple |
|:----|:------------|:-------------|:-----|
| M1 sensibilidad | Por obtener (EXP-002) | Por obtener | Por determinar |
| M2 falsas alarmas | Por obtener (EXP-002) | Por obtener | Por determinar |
| M3 asistido vs no asistido | Por obtener (EXP-005) | Por obtener | Por determinar |
| M4 latencia | Por obtener (EXP-003) | Mediana y percentil 95 | Por determinar |
| M5 operación sin red | Por obtener (EXP-003) | No aplica | Por determinar |
| M6 robustez | Por obtener (EXP-004) | Por obtener | Por determinar |

# 9. Cronograma

| Fechas | Actividad | Entregable |
|:------|:-----------------------|:-----------------|
| 19–23 oct | Montaje de la estación, protocolo de captura, soldadura de tarjetas con defectos sembrados | Ficha de montaje; hoja de siembra |
| 24–26 oct | Captura y etiquetado; partición y congelamiento del conjunto de prueba | DS-01 con huellas |
| 26–28 oct | EXP-001 y EXP-002; EXP-003 y EXP-004 | Resultados crudos y scripts |
| 28–29 oct | EXP-005; análisis; cartel; ensayos | Cartel 90 × 120 cm; guion |
| 30 oct | Jornada estatal | Exposición y demostración |
| Nov 2026 – mar 2027 | Validación externa (DS-02), si se concreta; mejoras; preparación para la fase nacional | Informe ampliado |

El calendario es ajustado y lo sabemos. Si el tiempo no alcanza, priorizaremos EXP-001, EXP-002 y EXP-003 y reportaremos con claridad lo que no se hizo.

# 10. Conclusiones y límites esperados

Este protocolo no contiene conclusiones sobre el desempeño de la estación porque aún no hay datos; contiene las condiciones bajo las cuales cada conclusión será válida o no. Si se cumplen las metas, concluiremos únicamente que una estación local de bajo costo logra, con datos propios y en las condiciones probadas, la sensibilidad, las falsas alarmas y la latencia reportadas, y que la inspección asistida mejora o no mejora la revisión de los integrantes. No concluiremos nada sobre el desempeño en una línea industrial real, con inspectores expertos o con otros tipos de tarjeta, y así lo declararemos.

**Limitaciones conocidas.** Datos de tarjetas de práctica y defectos sembrados que pueden diferir de los defectos reales de producción; dos inspectores sin experiencia industrial; un solo tipo de montaje; una sola configuración de cámara e iluminación; la evidencia local del problema proviene de una conversación con una organización. **Trabajo futuro.** Validación externa con tarjetas de producción y con técnicos de calidad, ampliación a otras clases y evaluación de aceleradores de inferencia.

# Referencias {-}

::: {custom-style="Bibliography"}
Andriulo, F. C., Fiore, M., Mongiello, M., Traversa, E., & Zizzo, V. (2024). Edge computing and cloud computing for Internet of Things: A review. *Informatics, 11*(4), Artículo 71. https://doi.org/10.3390/informatics11040071
:::

::: {custom-style="Bibliography"}
Anthropic. (2026). *Claude* [Modelo de lenguaje de gran tamaño]. https://claude.ai
:::

::: {custom-style="Bibliography"}
Cámara Nacional de la Industria Electrónica, de Telecomunicaciones y Tecnologías de la Información. (2024). *Plan maestro para el desarrollo de la industria de semiconductores 2024–2030* [Documento en PDF]. CANIETI. https://canieti.org/storage/PageBuilderFiles/Mdbs9xohDrXx8BFTwgQPVUFsgSa1qz-metaUExBTiBNQUVTVFJPLUVTUEHDkU9MLnBkZg==-.pdf
:::

::: {custom-style="Bibliography"}
El Universal Puebla. (2026, 28 de septiembre). *Puebla también fabricará tarjetas electrónicas PCB, anuncia Armenta*. https://www.eluniversalpuebla.com.mx/estado/puebla-tambien-fabricara-tarjetas-electronicas-pcb-anuncia-armenta/
:::

::: {custom-style="Bibliography"}
GÖPEL electronic. (s. f.). *Optimal inspection of THT assemblies* [Documento técnico]. https://www.goepel.com/fileadmin/fachartikel/aoi/en/Optimal_Inspection_of_THT_Assemblies.pdf
:::

::: {custom-style="Bibliography"}
IPC. (s. f.). *IPC-A-610: Acceptability of electronic assemblies* [Norma]. https://www.ipc.org
:::

::: {custom-style="Bibliography"}
Ong, Tan, Teoh, & Haron. (2025). Review of solder joint vision inspection for industrial applications. *The International Journal of Advanced Manufacturing Technology, 137*(7), 3257–3272. https://doi.org/10.1007/s00170-025-15383-4
:::

::: {custom-style="Bibliography"}
Organisation for Economic Co-operation and Development. (2026). *Promoting the development of the semiconductor ecosystem in Mexico: Assessment and recommendations*. OECD Publishing. https://www.oecd.org/en/publications/promoting-the-development-of-the-semiconductor-ecosystem-in-mexico_02c81dec-en/full-report/assessment-and-recommendations_a54f7797.html
:::

::: {custom-style="Bibliography"}
Ross, G. (2006). *First article inspection strategies* [Ponencia]. IPC Printed Circuits Expo, APEX and the Designers Summit. https://www.electronics.org/system/files/technical_resource/E16&S35-01.pdf
:::

::: {custom-style="Bibliography"}
See, J. E. (2015). Visual inspection reliability for precision manufactured parts. *Human Factors, 57*(8), 1427–1442. https://doi.org/10.1177/0018720815602389
:::

::: {custom-style="Bibliography"}
Siemens Digital Industries Software. (2023). *Smarter false call reduction for electronics* [Libro blanco]. https://static.sw.cdn.siemens.com/siemens-disw-assets/public/1Ms1MRN5y1CWR4Q5aWqUCU/en-US/Siemens-SW-AOI-FCR-White-Paper.pdf
:::

::: {custom-style="Bibliography"}
Ultralytics. (2026). *Raspberry Pi* [Guía de documentación]. https://docs.ultralytics.com/guides/raspberry-pi/
:::

# Anexo A. Registro de búsquedas del estado del arte {-}

Búsquedas realizadas entre el 1 y el 2 de octubre de 2026 sobre inspección de soldadura through-hole, falsas alarmas de inspección óptica automatizada, detección de defectos en tarjetas con aprendizaje profundo en computadoras de placa única y conjuntos de datos públicos de defectos en tarjetas. Los detalles de cada fuente (fecha de consulta, tipo y qué aporta) están en el registro de fuentes de la bóveda del proyecto. Los conjuntos de datos públicos encontrados se usarán, en todo caso, solo después de verificar su licencia, y se declararán como externos.

# Anexo B. Bitácora de investigación {-}

La bitácora cronológica se entrega como documento independiente (PDF) y es la fuente de verdad de las fechas del proceso. Está resguardada por el líder del proyecto y versionada con git.
