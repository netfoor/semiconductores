---
titulo: "Mapa de oportunidades de proyecto (primera versión)"
tipo: analisis
estado: borrador
creado: 2026-10-02
actualizado: 2026-10-02
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-020, F-031, F-032, F-033, F-034, F-036, F-041, F-042, F-044, F-046, F-048, F-051, F-052, F-057, F-058, F-060, F-079]
tags: [femeci, ideas, oportunidades, matriz, fase-5]
aliases: ["Mapa de oportunidades", "Matriz de comparación"]
---

# Mapa de oportunidades de proyecto (primera versión)

Fase 5, letra H del documento maestro: "un primer mapa de oportunidades de proyecto, todavía sin comprometernos con ninguna". **Aquí no se elige nada.**

La decisión es del equipo en G1 (martes 6 oct), con la ruta de §5. Insumos:
- [[registro-de-problemas]] (P-001 a P-008);
- [[problemas-y-oportunidades]] (OP-01 a OP-06);
- [[sintesis-fase-2]] y [[sintesis-fase-3]];
- [[comparacion-nube-vs-edge]];
- [[informacion-faltante]].

> [!note] Preferencia del equipo
> `#idea-equipo` Fortino comentó el 2 oct: "yo creo que sí nos vamos con semiconductores". Por eso las ideas de esa familia están más detalladas. Aun así, el documento maestro pide no forzarla y señalar si otra opción tiene mejor evidencia; eso se hace en §4.

## 1. Ideas candidatas

| ID | Idea | Familia | Problema / oportunidad | Estado de la evidencia hoy |
|---|---|---|---|---|
| IC-01 | Inspección asistida de uniones soldadas through-hole o de soldadura manual | Electrónica: ensamble de tarjetas (Yankuilotl) | P-008, OP-01 | Problema documentado en la industria; **sin confirmar en Puebla** |
| IC-02 | Verificación automática de la primera tarjeta al cambiar de producto | Electrónica: ensamble de tarjetas (Yankuilotl) | P-005, OP-03 | Indicio local (programación por proyecto) y evidencia de proveedor; **sin confirmar** |
| IC-03 | Segunda opinión para reducir falsas alarmas de la inspección óptica automatizada (AOI) | Electrónica: ensamble de tarjetas (Yankuilotl) | P-008, OP-02 | Documentado en la industria; no se sabe si Yankuilotl tiene AOI |
| IC-04 | Registro de defectos y trazabilidad ligera | Electrónica: ensamble de tarjetas (Yankuilotl) | P-005, OP-04 | Sin confirmar; mejor como módulo de otra idea |
| IC-05 | Automatización de mediciones o análisis de datos de caracterización de chips | Semiconductores: diseño y validación (Kutsari/INAOE) | P-005, OP-05 | Necesidades desconocidas |
| IC-06 | Dataset propio con defectos controlados y clasificador de soldadura through-hole, para formación y control de calidad | Electrónica sin acceso a planta (plan B) | P-004, P-005, OP-06 | Brecha de talento documentada a nivel nacional; uso local sin confirmar |
| IC-07 | Detección de descargas intermitentes al río Atoyac con monitoreo continuo de bajo costo | Agua (comparador) | P-001 | Documentado con cifras de CONAGUA (vía prensa) |
| IC-08 | Alerta temprana de crecidas súbitas en la Sierra Norte | Riesgo (comparador) | P-002 | Documentado con cifras oficiales; **es el proyecto aparte de Fortino** |

## 2. Fichas

### IC-01 · Inspección asistida de uniones soldadas through-hole

- **Problema:**
  - `#hecho` En la mayoría de las tareas de inspección visual, los inspectores pasan por alto entre 20 y 30 % de los defectos [F-060].
  - `#hecho` Un proveedor de AOI estima ≈ 30 % de errores reales no detectados en la revisión manual [F-051].
  - `#hecho` El through-hole es difícil de inspeccionar: uniones del lado inferior, componentes altos, deformación por calor [F-057].
  - `#hecho` Yankuilotl ensambla through-hole (hasta 40 mil componentes por hora) [F-041].
  - `#hipotesis` En su línea, la inspección de esas uniones es manual y falla. Hay que confirmarlo (Q-034, Q-035).
- **Usuario:** inspector u operador de la estación through-hole o de retrabajo.
- **Qué se construiría:** estación fija con cámara, iluminación controlada y Raspberry Pi. Señala las uniones sospechosas y el inspector decide (humano en el ciclo); cada decisión queda registrada como etiqueta.
- **Meta medible (`#hipotesis`, valores con el usuario):** sensibilidad ≥ X % por clase de defecto (por ejemplo, soldadura insuficiente, puente, unión fría, pin sin soldar; según IPC-A-610), con falsos rechazos ≤ Y % y ≤ Z s por tarjeta. Comparación contra la inspección humana sin asistencia.
- **Datos:** tarjetas reales de Yankuilotl (Q-046) o tarjetas propias con defectos inducidos (estrategia de IC-06).
- **Piloto antes del 14 oct:** 100–200 imágenes de uniones, clasificador base y primeras métricas.
- **Modalidad y categoría probables:** Ingenierías · Sistemas Informáticos y Computación (Robótica y Máquinas Inteligentes: visión artificial).
- **Formatos FE probables:**
  - FE-1C si se toman datos dentro de la planta (Q-009);
  - FE-04 si inspectores externos prueban el sistema (Q-008). Se evita si los inspectores de la prueba son los propios integrantes.
- **Riesgos:** acceso a Yankuilotl; pocos defectos reales disponibles.
- **Qué la haría subir:** confirmación del problema y acceso a tarjetas o fotos.

### IC-02 · Verificación automática de la primera tarjeta

- **Problema:**
  - `#hecho` Yankuilotl programa sus máquinas por proyecto y valida antes de producir en serie [F-041, F-042].
  - `#hecho` En producción de alta mezcla, verificar a mano la primera tarjeta tras cada cambio puede tomar ≈ 3 horas en tarjetas de 300–600 componentes, con la línea detenida. Las piezas mal cargadas por errores de preparación son la falla principal [F-079]. Es una fuente de proveedor de 2006; hay que verificar su vigencia.
  - `#hipotesis` Para Yankuilotl, los cambios de producto y la verificación inicial son un cuello de botella (Q-036, Q-044).
- **Usuario:** técnico de calidad o ingeniero de proceso al arrancar cada lote.
- **Qué se construiría:** compara la primera tarjeta contra una tarjeta de referencia aprobada (o contra la lista de componentes, si se permite usarla). Detecta componentes faltantes, desplazados, girados o con polaridad invertida y produce una lista de verificación asistida.
- **Meta medible (`#hipotesis`):** detectar ≥ X % de errores sembrados con ≤ Y falsas alarmas por tarjeta, en menos tiempo que la verificación manual medida.
- **Ventaja metodológica:** los errores se pueden **sembrar a propósito** (quitar, girar o cambiar un componente), lo que da una verdad de referencia perfecta (A4, A5).
- **Datos:** pocas tarjetas, más los errores sembrados. Puede empezar con tarjetas propias.
- **Hardware:** cámara de mayor resolución y lente o iluminación adecuadas para componentes SMD pequeños; puede requerir compra (`#inferencia`).
- **Modalidad, categoría y FE:** como IC-01.
- **Riesgos:**
  - diseños confidenciales (comparar contra una tarjeta de referencia evita usar archivos de diseño);
  - resolución suficiente para componentes diminutos.
- **Qué la haría subir:** que Yankuilotl confirme muchos cambios de producto y verificación manual lenta.

### IC-03 · Reducción de falsas alarmas de AOI

- **Problema:** `#hecho` Las máquinas AOI alarman en 5–70 % de lo que pasa por la línea, y hasta 95 % de esas alarmas son falsas [F-051]. `#pregunta` ¿Yankuilotl tiene AOI y guarda imágenes y decisiones del operador? (Q-034, Q-037)
- **Qué se construiría:** clasificador de segunda opinión entrenado con el historial de alarmas y decisiones, más un tablero de revisión.
- **Meta:** reducir ≥ X % las falsas alarmas sin dejar pasar defectos reales.
- **Riesgo dominante:** depende por completo de sus datos históricos y de permisos.

### IC-04 · Registro de defectos y trazabilidad ligera

- **Idea:** captura de defectos por estación, tablero de control estadístico y reportes para una planta nueva de alta mezcla.
- **Lectura (`#inferencia`):** es útil, pero es sobre todo software de gestión. Es difícil demostrar una mejora con un experimento cuantitativo en 4 semanas (A3 a A5). Conviene más como módulo de IC-01 o IC-02.

### IC-05 · Datos de caracterización de chips (Kutsari/INAOE)

- **Problema:** `#hecho` Los laboratorios abrieron en mayo de 2026 tras 15 meses de retraso [F-044]. `#pregunta` No se conocen sus necesidades técnicas (Q-030).
- **Qué se construiría:** según lo que digan:
  - automatizar mediciones (control de instrumentos desde Python);
  - organizar y analizar resultados;
  - detectar curvas anómalas.
- **Riesgos:** acceso, equipo de laboratorio, conocimiento del dominio y tiempo. Es la opción más alineada con "semiconductores" en sentido estricto y la de mayor riesgo. Guía en [[guia-contacto-inaoe-kutsari]].

### IC-06 · Dataset propio con defectos controlados (plan B de la familia)

- **Problema:**
  - `#hecho` La brecha de talento en el ecosistema de semiconductores y electrónica está documentada a nivel nacional [F-046, F-048].
  - `#hecho` En Puebla, retener talento especializado es objetivo declarado de la estrategia [F-020].
  - `#hecho` La inspección humana es falible [F-060].
  - `#hipotesis` Instructores o técnicos en formación (UTP, Yankuilotl) necesitan retroalimentación objetiva sobre la calidad de sus soldaduras (Q-047).
- **Qué se construiría:**
  - tarjetas soldadas por el equipo con defectos inducidos según IPC-A-610;
  - un conjunto de datos propio y documentado;
  - un clasificador en Raspberry Pi que dé retroalimentación inmediata.
- **Fortalezas:** datos totalmente controlados, factible sin depender de nadie, demostrable en la mesa.
- **Debilidades:**
  - el problema local es el más débil (A1, A2);
  - la originalidad es moderada: ya hay trabajos y datasets de defectos de soldadura [F-052, F-058];
  - riesgo de "tecnología buscando problema".
- **Lectura (`#inferencia`):** sola es débil. Su estrategia de datos (defectos sembrados) puede **reforzar** IC-01 o IC-02 si Yankuilotl confirma el problema pero no da datos.

### IC-07 · Descargas intermitentes al Atoyac (comparador)

- **Problema:**
  - `#hecho` Según cifras de CONAGUA difundidas en prensa: 1,095 descargas irregulares y un aumento de 160 % entre marzo y diciembre de 2025.
  - `#hecho` Las empresas suspenden la descarga cuando detectan inspectores; CONAGUA está adquiriendo equipos de monitoreo [F-032].
- **Qué se construiría:** nodo de sensores (pH, conductividad, turbidez, temperatura) con detección de eventos anómalos. Se valida en laboratorio con descargas simuladas y luego con un despliegue corto en campo.
- **Riesgos:** campo (acceso, seguridad, permisos), calibración y tiempo. Categoría probable: Ciencias Ambientales o Sistemas Embebidos e IoT.

### IC-08 · Alerta de crecidas en la Sierra Norte (comparador)

- **Problema:** `#hecho` 22 fallecidos en octubre de 2025 y compromiso de gobierno de fortalecer el pronóstico y el alertamiento [F-033, F-034]. No se encontró un sistema de alerta local de crecidas súbitas en la Sierra Norte ([[indice-inundaciones-sierra-norte]]).
- **Condiciones especiales:**
  - es el **proyecto aparte de Fortino**, que él decidió mantener separado;
  - si se llevara a FEMECI, probablemente sí aplicaría FE-07 (continuidad de un proyecto propio previo);
  - habría que diferenciarse de los trabajos de El Colegio de Puebla y del IPN.
- Se incluye solo para comparar la fuerza de la evidencia.

## 3. Matriz de comparación

Escala por criterio: **3** alto o favorable · **2** medio · **1** bajo o desfavorable. En "Riesgo y dependencias", 3 = bajo riesgo. Todo es `#inferencia` de Claude con la evidencia al 2 oct; el equipo debe revisarlo y ajustarlo.

| # | Criterio del documento maestro | IC-01 | IC-02 | IC-03 | IC-04 | IC-05 | IC-06 | IC-07 | IC-08 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Problema real demostrado (en Puebla) | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 3 |
| 2 | Relevancia para Puebla | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 |
| 3 | Evidencia disponible hoy | 2 | 1 | 2 | 1 | 1 | 2 | 2 | 3 |
| 4 | Alineación con FEMECI (rúbrica y organizador) | 3 | 3 | 3 | 2 | 3 | 2 | 3 | 3 |
| 5 | Rigor metodológico demostrable | 3 | 3 | 3 | 1 | 2 | 3 | 2 | 2 |
| 6 | Originalidad | 2 | 2 | 2 | 1 | 2 | 1 | 2 | 1 |
| 7 | Impacto potencial | 2 | 2 | 3 | 2 | 2 | 2 | 3 | 3 |
| 8 | Viabilidad en el tiempo | 2 | 2 | 1 | 2 | 1 | 3 | 1 | 2 |
| 9 | Hardware disponible | 3 | 2 | 3 | 3 | 1 | 2 | 2 | 2 |
| 10 | Datos disponibles o creables | 1 | 2 | 1 | 1 | 1 | 3 | 2 | 2 |
| 11 | Prototipo funcional | 3 | 3 | 2 | 3 | 2 | 3 | 3 | 3 |
| 12 | Experimentos cuantitativos | 3 | 3 | 3 | 1 | 2 | 3 | 2 | 3 |
| 13 | Facilidad para demostrar ante evaluadores | 3 | 3 | 2 | 2 | 1 | 3 | 2 | 2 |
| 14 | Riesgo y dependencias externas | 1 | 2 | 1 | 1 | 1 | 3 | 1 | 2 |
| | **Suma (orientativa)** | **32** | **32** | **30** | **24** | **23** | **33** | **30** | **34** |

**Si Yankuilotl confirma el problema y da acceso a tarjetas o fotos** (`#inferencia`):

| Idea | Cambios | Suma |
|---|---|---|
| IC-01 | Problema 1 → 3, evidencia 2 → 3, datos 1 → 3, riesgo 1 → 2 | 38 |
| IC-02 | Problema 1 → 3, evidencia 1 → 2, datos 2 → 3, riesgo 2 → 3 | 37 |
| IC-03 (si tiene AOI con historial) | Problema 1 → 3, evidencia 2 → 3, viabilidad 1 → 2, datos 1 → 3, riesgo 1 → 2 | 37 |

**Por qué la suma no basta.** Una idea muy factible con un problema débil (IC-06) suma casi lo mismo que una con un problema demostrado (IC-08). El documento maestro exige "problema antes que tecnología", y la rúbrica dedica A1 y A2 (≈ 20 puntos) al problema y su pertinencia. Por eso se aplican dos filtros antes de comparar sumas:
- **Filtro 1 — problema:** criterio 1 ≥ 2. El problema debe estar demostrado, o haber indicios locales fuertes confirmados por el usuario.
- **Filtro 2 — tiempo:** criterio 8 ≥ 2, o una forma concreta de acotar la idea para que quepa en el calendario.

## 4. Lectura

1. `#inferencia` **Hoy ninguna idea de la familia de semiconductores pasa el filtro del problema.** Todas dependen de una conversación con Yankuilotl o con el INAOE. Esto confirma lo que se vio en la Fase 3; no es una novedad.
2. `#inferencia` **Si Yankuilotl confirma, la familia pasa a ser la mejor opción** (IC-01 o IC-02, con 37–38). Junta alta alineación con el organizador, rigor experimental y una demostración clara en la mesa. La preferencia del equipo tiene sustento, **condicionada a esa confirmación**.
3. `#inferencia` **Con la evidencia de hoy, las opciones con mejor problema demostrado están fuera de semiconductores:**
   - IC-08 (inundaciones) es la más fuerte, pero es el proyecto aparte de Fortino y probablemente sería de continuidad;
   - IC-07 (Atoyac) tiene un problema real, pero su trabajo de campo es arriesgado para el calendario.

   Se señala por instrucción del documento maestro; no es una recomendación de cambiar de tema.
4. `#inferencia` **IC-01, IC-02 e IC-06 comparten la mayor parte del método:** estación con cámara, conjunto de datos, métricas y medición de latencia local. Se puede avanzar en esa base común desde el 6 oct sin saber todavía cuál de las tres será (§5).
5. `#inferencia` **El problema que nombre Yankuilotl debe decidir entre IC-01, IC-02 e IC-03, no la tecnología.** Si dicen "se nos escapan defectos de soldadura", es IC-01. Si dicen "perdemos horas al arrancar cada lote", es IC-02. Si dicen "la máquina AOI marca demasiado", es IC-03.
6. `#inferencia` **IC-04 e IC-05 quedan como secundarias:** IC-04 por rigor, IC-05 por acceso y tiempo.

## 5. Ruta de decisión para G1 (martes 6 oct)

| Escenario al lunes 5 o martes 6 | Qué hacer | Idea |
|---|---|---|
| **E1.** Yankuilotl confirma un problema concreto y da acceso a tarjetas o fotos | Elegir la idea que corresponda al problema que nombren y escribir el protocolo con datos reales | IC-01, IC-02 o IC-03 |
| **E2.** Yankuilotl confirma el problema en entrevista, pero sin datos o con pocos | La misma idea, con un dataset propio de defectos sembrados (estrategia de IC-06) y validación con las tarjetas reales que se consigan. La entrevista sostiene A1 y A2 | IC-01 o IC-02, con datos de IC-06 |
| **E3.** Hay interés, pero la conversación técnica será entre el 6 y el 8 | Decisión **condicionada** el 6: familia de semiconductores, con fecha límite el jueves 8 para confirmar; mientras tanto, avanzar en la base común | IC-01, IC-02 o IC-06 |
| **E4.** No hay respuesta técnica al jueves 8 | El equipo elige entre (a) IC-06, sabiendo que A1 y A2 quedan débiles, o (b) cambiar a una familia con problema demostrado (IC-07 acotado a laboratorio, o IC-08 si Fortino decide traer su proyecto, con FE-07) | Decisión del equipo |

**Trabajo que sirve en cualquier escenario de la familia (desde el 6 oct):**
- armar la estación con Raspberry Pi, cámara e iluminación;
- herramientas de etiquetado y versionado de datos;
- scripts de métricas con intervalos de confianza;
- medir la latencia local, según el experimento de [[comparacion-nube-vs-edge]] §8;
- redactar contexto y estado del arte del protocolo (inspección en ensamble electrónico).

## 6. Descartadas por ahora

| Familia o idea | Razón | Fuente |
|---|---|---|
| Automotriz (calidad y manufactura 4.0) | El problema documentado es de talento; no hay proveedor dispuesto a compartir datos (Q-033) | P-004, F-031 |
| Electromovilidad (Olinia, Zacua) | Sin problema técnico documentado | [[sintesis-fase-2]] |
| Cenizas del Popocatépetl | Ya hay un proyecto estudiantil de alto perfil (Gxiba-1); originalidad difícil | P-003, F-036 |
| Digitalización de MIPyMES | Problema muy amplio; difícil medir en 4 semanas | P-006 |
| Residuos agroindustriales | Requiere competencias de química o biología ajenas al equipo | P-007 |

## 7. Siguientes pasos

1. Hoy, 2 oct: reunión con la directora, plática con contactos de Yankuilotl y correo a la DME ([[informacion-faltante]] §6).
2. Lunes 5: actualizar esta matriz con lo que digan Yankuilotl y la DME.
3. Martes 6 (G1): el equipo decide con la ruta de §5. La idea elegida pasa a su propia ficha (`IC-##-nombre.md`) y se definen modalidad y categoría (D-005, D-006).
