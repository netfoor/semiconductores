---
titulo: "Convenciones de la bóveda"
tipo: convenciones
estado: vigente
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, metodo]
aliases: ["Convenciones"]
---

# Convenciones de la bóveda

Estas reglas existen para que cualquier persona (el equipo, el asesor o un evaluador) pueda reconstruir **cómo** llegamos a cada conclusión, y para cumplir con la exigencia de evidencia cronológica de la convocatoria (criterio C3, ver [[rubrica-y-evidencias]]). Adoptadas en D-001 ([[registro-de-decisiones]]).

## 1. Tipos de afirmación

Toda afirmación relevante lleva una etiqueta al inicio:

| Etiqueta | Significa | Requisito |
|---|---|---|
| `#hecho` | Hecho verificado | Cita a una fuente del registro, p. ej. `[F-001 §6.1]` |
| `#inferencia` | Conclusión razonada a partir de hechos | Indicar en qué hechos se apoya |
| `#supuesto` | Supuesto de trabajo aún no verificado | Indicar cómo y cuándo se verificará |
| `#hipotesis` | Proposición que se puede comprobar con un experimento o con evidencia | Indicar cómo se probaría |
| `#idea-equipo` | Idea u opinión del equipo | No presentarla como necesidad del sector sin evidencia |
| `#pregunta` | Hueco de información | Registrarla como Q-### (preguntas abiertas o guía de entrevista) |

En tablas, la etiqueta puede ir en una columna "Tipo" o en el encabezado de la columna.

## 2. Identificadores

| Prefijo | Uso | Dónde vive |
|---|---|---|
| `F-###` | Fuente | [[registro-de-fuentes]] |
| `D-###` | Decisión | [[registro-de-decisiones]] |
| `REQ-XXX-##` | Requisito derivado de la convocatoria | [[especificacion-de-proyecto]] |
| `AC-##` | Atributo de calidad de una propuesta excelente | [[especificacion-de-proyecto]] |
| `EV-##` | Evidencia que debemos producir | [[rubrica-y-evidencias]] |
| `Q-###` | Pregunta abierta | [[preguntas-abiertas-convocatoria]] y guías en `09-entrevistas/` |
| `R-##` | Riesgo | [[analisis-estrategico-convocatoria]], [[calendario-y-plazos]] |
| `P-###` | Problema identificado | `08-problemas/` |
| `IC-##` | Hipótesis de proyecto candidata | `10-ideas-candidatas/` |
| `EXP-###` | Experimento | `15-experimentos/` |
| `DS-##` | Conjunto de datos | `14-dataset/` |
| `G0…G5` | Compuertas del calendario | [[calendario-y-plazos]] |

Los IDs no se reutilizan. Lo descartado se marca como `descartado` con su razón; no se borra.

Las carpetas temáticas dedicadas pueden llevar su propio registro de fuentes con prefijo propio (por ejemplo, `SN-##` para inundaciones de la Sierra Norte); el registro general las enlaza.

## 3. Citas

- En el texto: `[F-001 §6.1]` (fuente + sección o página). Para la convocatoria basta `[§6.1]`.
- Cada fuente registrada incluye: título, emisor, URL, fecha de publicación, fecha de consulta, tipo (primaria/secundaria), cómo se leyó (directa o automatizada), qué aporta y qué implica.
- En el protocolo final se usará un estilo bibliográfico único (APA 7, salvo que la plantilla oficial indique otro).

## 4. Propiedades de cada nota (frontmatter)

```yaml
titulo:        # título legible
tipo:          # indice | referencia | especificacion | analisis | registro | checklist | bitacora | convenciones
estado:        # borrador | vigente | revisado | obsoleto
creado:        # AAAA-MM-DD
actualizado:   # AAAA-MM-DD
autor:         # Fortino | Israel | Asesor | "Claude (IA)"
revisado_por:  # lista de quienes revisaron
fuentes:       # lista de F-###
tags:          # lista
```

## 5. Autoría y uso de IA

- El equipo decidió usar IA en el proyecto (D-003, adoptada el 1 oct). Salvaguardas:
  - Toda nota indica su autor. Las notas elaboradas por Claude (IA) son **material de trabajo**: el equipo las revisa y se anota en `revisado_por`.
  - Los textos que se entregan (protocolo, F-01, cartel, guion) los redactan Fortino e Israel con sus palabras y dominan todo su contenido.
  - Cuando la IA ayude en una tarea, la bitácora lo dice: qué hizo y qué verificó el equipo; el protocolo declara el uso de IA en la metodología.
  - Toda afirmación aportada por la IA se verifica contra la fuente original antes de usarse en un entregable.

## 6. Bitácora

- La bitácora digital de esta bóveda es la **fuente de verdad** del proyecto (D-002); se exporta a PDF para el expediente.
- Una nota por día en `02-bitacora/` llamada `AAAA-MM-DD.md`; índice en [[bitacora-indice]].
- Cada entrada: hora aproximada, responsable (incluida la IA cuando aplique), actividad, resultado o evidencia, decisiones y pendientes.
- Las entradas pasadas no se reescriben: las correcciones se agregan como nueva entrada o como bloque "Corrección (fecha)".

## 7. Archivos y carpetas

- Nombres de archivo en minúsculas, sin acentos, con guiones (`rubrica-y-evidencias.md`); el título legible va en el H1 y en `titulo`.
- Carpetas numeradas en el orden del flujo de trabajo (ver [[inicio]]).
- Documentos oficiales (PDF) se guardan sin modificar en `01-convocatoria/documentos-oficiales/`.

## 8. Fechas y horas

Formato ISO 8601 (`2026-10-01`); hora del centro de México (UTC−6).
