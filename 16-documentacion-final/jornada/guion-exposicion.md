---
titulo: "Guion de la exposición (jornada del 30 de octubre)"
tipo: guia
estado: borrador
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-080]
tags: [femeci, jornada, exposicion, guion]
---

Fuentes de cada dato: [[triptico-v2]], [[adenda-2026-10-29]], EXP-006, D-015, D-016 y la bitácora del 29 de octubre. Pendiente #15 de [[pendientes]].

<!-- CONSTRUCCIÓN: lo que sigue a esta línea es el texto del PDF. Compilar con 12-protocolo/herramientas/build.py -->

::: {custom-style="TitlePageTitle"}
Guion de la exposición
:::

::: {custom-style="TitlePageText"}
Estación de inspección visual asistida para uniones through-hole · FEMECI-PUEBLA 2026 · 30 de octubre
:::

# Cómo usar este guion

- **Tiempo:** de 8 a 10 minutos de exposición y de 5 a 7 de preguntas, ante cada evaluador (convocatoria, §7.3; la carta da un máximo de 15 minutos en total).
- **No se lee.** La carta pide evitar leer, las muletillas, hablar rápido y dar la espalda al evaluador. Cada bloque trae las **ideas que no pueden faltar** y una frase de ejemplo; díganlo con sus palabras.
- **Siempre inicia Majo.** Cada quien señala en el tríptico la sección de la que habla.
- **Antes de que llegue el evaluador:** la Pi encendida, un celular ya conectado a la red Estacion-THT y una inspección de calentamiento hecha (la primera tarda más), la hoja del mosaico en la mesa y la tarjeta de QR a la vista.
- **Honestidad ante todo:** la tarjeta de la demostración es un mosaico de fotos públicas, no una tarjeta nuestra; los resultados son con datos públicos; los datos propios empiezan después de la jornada.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Versión para tres personas

## 1. María José: presentación y problema (2 minutos)

**Señala:** título, Introducción, Figura 1 y Antecedentes.

- Saludo; presenta al equipo y el nombre del proyecto.
- Cómo surgió: buscábamos un problema real del ensamble electrónico en Puebla, un sector que el estado y el país quieren hacer crecer.
- Qué es una unión through-hole (Figura 1): la patilla atraviesa la tarjeta y la unión queda abajo, donde muchas veces se revisa a ojo.
- Por qué importa: la inspección visual humana deja pasar del 20 % al 30 % de los defectos en la mayoría de las tareas (See, 2015), y personal técnico de una empresa de ensamble de Puebla nos dijo que cuando algo falla se revisa a ojo con más resolución.
- (Opcional, como anécdota y no como evidencia) Una persona que trabajó en soldadura de metales me contó que cada soldadura se revisaba a ojo y se marcaba con plumón.

> *Ejemplo:* «Buenos días, somos Fortino, Israel y María José. Nuestro proyecto es una estación que ayuda a revisar soldaduras de tarjetas electrónicas. En estas uniones la patilla atraviesa la tarjeta y la soldadura queda abajo, y todavía se revisan a ojo… »

**Pasa a Israel:** «¿Y qué nos propusimos construir? Israel les explica.»

## 2. Israel: meta, objetivo y método (2.5 minutos)

**Señala:** Meta de ingeniería, Justificación, Objetivo, Metodología y Creatividad e innovación.

- Meta: una estación de bajo costo que, sin internet, señale las uniones sospechosas. Las metas se fijaron antes de medir: sensibilidad de al menos 0.90, falsas alarmas de 0.15 como máximo, hasta 5 s por tarjeta y funcionar sin internet.
- Los cinco pasos: capturar con el celular, alinear con la plantilla, recortar cada unión, clasificar con una red pequeña en el mismo equipo y **la persona decide**, una unión a la vez.
- Lo que tiene de nuevo: la plantilla por diseño (las uniones se marcan una sola vez, sin entrenar un detector), la confidencialidad (las fotos de la planta no salen del equipo) y que el sistema señala, no rechaza.
- El plan con datos propios: al menos 30 tarjetas con defectos sembrados, etiquetadas por dos personas y separadas por tarjeta para que el modelo no se evalúe con lo que ya vio.

> *Ejemplo:* «El sistema no decide por el inspector: le dice dónde mirar primero. Y todo pasa en esa Raspberry Pi, sin internet, porque las fotos de una planta son confidenciales.»

**Pasa a Fortino:** «Mejor se los mostramos. Fortino.»

## 3. Fortino: demostración y resultados (3 minutos)

**Señala:** la Pi, la hoja del mosaico, Figuras 3 y 5 y Resultados preliminares.

- Demostración en vivo (1.5 minutos): con el celular ya conectado, «Tomar foto» a la hoja del mosaico. El sistema la alinea y marca las sospechosas. Revisar dos o tres uniones: confirmar una y corregir otra. Ofrecer al evaluador hacerlo él mismo (QR 1 y 2) o probar el Reto (QR 3).
- Aclarar qué es la hoja: un mosaico de fotos reales de un conjunto público (PCBSPDefect, CC BY 4.0), no una tarjeta nuestra.
- Resultados con 622 uniones reales de 121 tarjetas del conjunto público: la red detectó 0.94 de los defectos, frente a 0.74 de la visión clásica, con 0.12 de falsas alarmas, frente a 0.28.
- Lo que todavía no podemos afirmar: M2, porque el intervalo de las falsas alarmas llega a 0.22. Y con la foto de una tarjeta de otra cámara, la red falló: el desempeño en nuestra estación solo lo dirán nuestros datos.

> *Ejemplo:* «Con fotos reales la red cumple la meta de sensibilidad. Pero no vamos a decir que ya funciona en una planta: con otra cámara falló, y por eso el siguiente paso son nuestras propias tarjetas.»

**Si la demostración falla:** decirlo con calma y abrir en la laptop la página «Fotos reales», o el video de respaldo si ya lo grabaron.

**Pasa a María José:** «¿Y hacia dónde va esto? Majo.»

## 4. María José: hacia dónde va y cierre (1.5 minutos)

**Señala:** Conclusiones y Hacia dónde va.

- Por qué el inspector se queda (D-016): hoy garantiza la calidad mientras el modelo no demuestre ser confiable en una planta, y cada vez que confirma o corrige produce los ejemplos con los que el modelo de esa planta mejora.
- La ruta: (1) apoyo, este proyecto; (2) piloto por planta, con un modelo para cada empresa entrenado con sus tarjetas; (3) automatización gradual, en la que solo las uniones dudosas llegan a la persona.
- Lo siguiente: la visita técnica a una planta de ensamble el 5 de noviembre y las tarjetas propias.
- Cierre: agradecer e invitar a preguntas.

> *Ejemplo:* «No queremos sustituir al inspector: queremos que revise primero lo que importa y que, con su trabajo, el sistema aprenda en cada planta. Gracias, ¿tienen alguna pregunta?»

## Preguntas: quién responde

| Tema | Responde primero |
|---|---|
| El problema, la industria en Puebla, la visita técnica | María José |
| Metas, método, datos propios, etiquetado | Israel |
| La red, los resultados, la Raspberry Pi, el código | Fortino |
| ¿Para qué sirve si el inspector sigue revisando? | María José (D-016) |

Si alguien no sabe una respuesta, otro la completa. Nunca inventar una cifra: «eso todavía no lo hemos medido» es una buena respuesta.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Versión para dos personas (si Israel no llega)

María José toma la meta y el objetivo; Fortino toma el método junto con la demostración. Si el evaluador pregunta por Israel, decir la verdad con brevedad.

## 1. María José: presentación, problema y meta (3 minutos)

**Señala:** título, Introducción, Figura 1, Antecedentes, Meta de ingeniería y Justificación.

- Todo el bloque 1 de la versión para tres personas.
- La meta: una estación de bajo costo que, sin internet, señale las uniones sospechosas, con metas fijadas antes de medir (sensibilidad de al menos 0.90, falsas alarmas de 0.15 como máximo, hasta 5 s por tarjeta, sin internet).
- La justificación: menos defectos que pasan, apoyo y no sustitución, bajo costo frente a una máquina de inspección automática.

**Pasa a Fortino:** «¿Cómo funciona? Fortino les muestra.»

## 2. Fortino: método, demostración y resultados (4.5 minutos)

**Señala:** Metodología, Creatividad e innovación, la Pi, la hoja del mosaico y Resultados preliminares.

- Los cinco pasos y lo que tiene de nuevo (bloque 2 de la versión para tres personas), en 1.5 minutos.
- La demostración y los resultados (bloque 3), en 3 minutos.

**Pasa a María José:** «¿Y hacia dónde va esto? Majo.»

## 3. María José: hacia dónde va y cierre (1.5 minutos)

- Igual que el bloque 4 de la versión para tres personas.

## Preguntas

María José responde problema, industria y D-016; Fortino responde metas, método, datos, red y Raspberry Pi.

# Ensayo antes de mañana

1. Cronometrar una vuelta completa: debe quedar entre 8 y 10 minutos.
2. Ensayar los relevos en voz alta, para que se oigan naturales.
3. Practicar la demostración con la hoja impresa y la Pi, incluido qué hacer si falla.
