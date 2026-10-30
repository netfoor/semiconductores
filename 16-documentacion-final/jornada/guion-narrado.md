---
titulo: "Guion narrado para estudiar (13 minutos)"
tipo: guia
estado: borrador
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-080]
tags: [femeci, jornada, exposicion, guion]
---

Versión completa para estudiar, pedida por Fortino. La versión de ideas clave para el día está en [[guion-exposicion]]. Datos: [[triptico-v2]], [[adenda-2026-10-29]], EXP-006, D-015, D-016 y la bitácora del 29 de octubre.

<!-- CONSTRUCCIÓN: lo que sigue a esta línea es el texto del PDF. Compilar con 12-protocolo/herramientas/build.py -->

::: {custom-style="TitlePageTitle"}
Guion narrado para estudiar
:::

::: {custom-style="TitlePageText"}
Estación de inspección visual asistida para uniones through-hole · FEMECI-PUEBLA 2026 · 30 de octubre
:::

# Antes de empezar

- **Duración:** unos 13 minutos leído en voz alta, a un ritmo tranquilo. Es para estudiar. Ante el evaluador, la convocatoria da de 8 a 10 minutos de exposición y de 5 a 7 de preguntas. Omitir los párrafos marcados con **[se puede omitir]** lo baja a unos 11.5 minutos; para quedar en 8 a 10, usen las ideas clave del guion corto (`guion-exposicion.pdf`).
- **No se lee el día de la jornada.** Apréndanse las ideas y díganlas con sus palabras; la carta pide evitar leer.
- Entre corchetes van las acciones: qué señalar en el tríptico o qué hacer en la demostración.
- **Siempre inicia María José.**

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Guion para tres personas

## María José: presentación y problema (unos 3 minutos)

[De frente al evaluador, señala el título del tríptico.]

Buenos días. Somos Fortino Romero, Israel García y María José de la Rosa, y nuestro proyecto se llama «Estación de inspección visual asistida con procesamiento local para uniones soldadas through-hole en el ensamble electrónico». Dicho de forma sencilla: construimos una estación que ayuda a una persona a revisar las soldaduras de una tarjeta electrónica y le señala dónde mirar primero.

La idea surgió de buscar un problema real en Puebla. El estado y el país quieren hacer crecer la industria electrónica y de semiconductores: el plan maestro de la industria para 2024 a 2030 y un diagnóstico de la OCDE de este año lo ponen como prioridad. Cuando una línea de ensamble crece, la calidad ya no depende solo de qué tan rápido se produce, sino de qué tan bien se detectan los defectos.

[Señala la Figura 1.]

En una tarjeta electrónica hay dos formas de montar componentes. En el montaje superficial, o SMD, el componente se suelda encima de la tarjeta, casi siempre con máquinas, y casi siempre lo revisa otra máquina. En el montaje through-hole, o THT, la patilla del componente atraviesa la tarjeta y se suelda por el lado de abajo. Se usa en conectores y componentes grandes que necesitan una unión más resistente. Esa unión de abajo es la que nos interesa, porque es difícil de revisar con máquinas: hay componentes altos que tapan zonas, y en muchos lugares todavía se revisa a ojo.

[Señala Antecedentes.]

¿Por qué es un problema revisar a ojo? Una revisión publicada en la revista Human Factors encontró que la inspección visual humana deja pasar entre el 20 y el 30 por ciento de los defectos en la mayoría de las tareas. No es un dato de soldadura, pero da una idea del tamaño del problema. Además, personal técnico de una empresa de ensamble electrónico de Puebla nos contó que la validación de piezas todavía tiene pasos manuales y que, cuando algo falla, se revisa con más resolución, pero a ojo. Por confidencialidad no damos el nombre de la empresa. Y el 5 de noviembre haremos una visita técnica a una planta de ensamble para observar el proceso de cerca.

**[se puede omitir]** Yo también platiqué con una persona que trabajó en soldadura de metales. Me contó que ahí cada soldadura se revisaba a ojo y se marcaba con un plumón para llevar el registro. No es soldadura electrónica, pero muestra lo mismo: la revisión depende de la vista y de la atención de una persona.

[Señala la Meta de ingeniería.]

Por eso nos planteamos este reto: una estación de bajo costo que, sin conexión a internet, señale las uniones sospechosas. Israel les explica cómo lo planteamos.

## Israel: meta, objetivo y método (unos 4 minutos)

[Señala la Meta de ingeniería.]

Gracias, Majo. Lo primero que hicimos fue fijar metas medibles, antes de ver cualquier resultado, para no acomodar las metas a lo que saliera. Son cuatro. Una sensibilidad de al menos 0.90, es decir, que el sistema detecte al menos 9 de cada 10 defectos. Una tasa de falsas alarmas de 0.15 como máximo, es decir, que de cada 100 uniones buenas no marque como sospechosas más de 15; si marca demasiadas, el inspector deja de confiar en él. Un tiempo de hasta 5 segundos por tarjeta. Y que funcione al cien por ciento sin internet.

[Señala Justificación.]

¿Por qué vale la pena? Primero, porque la atención del inspector va primero a las uniones sospechosas, y así deberían pasar menos defectos. Esa es una hipótesis que vamos a medir. Segundo, porque es apoyo y no sustitución: la persona sigue decidiendo. Y tercero, por el costo: es una computadora pequeña y una cámara, en lugar de una máquina de inspección automática.

[Señala el Objetivo y la Metodología.]

Nuestro objetivo es diseñar, construir y evaluar esta estación con datos propios, y compararla con la inspección humana sin apoyo y con una técnica clásica de visión por computadora. El sistema trabaja en cinco pasos. Uno, capturar: un celular toma la foto desde una página de la estación, sin instalar ninguna aplicación. Dos, alinear: la foto se ajusta a la plantilla del modelo de tarjeta, aunque esté girada o en perspectiva. Tres, recortar cada unión según esa plantilla. Cuatro, clasificar cada unión con una red neuronal pequeña, de unos 52 mil parámetros, en el mismo equipo. Y cinco, lo más importante: la persona revisa una unión a la vez y confirma o corrige lo que sugiere el sistema. Cada decisión queda registrada.

El sistema distingue cinco tipos de defecto y la unión aceptable: soldadura insuficiente, puente entre pines, pin sin soldar, exceso de soldadura y unión fría. Las definimos tomando como referencia la norma IPC-A-610, que es la de aceptabilidad de ensambles electrónicos.

[Señala Creatividad e innovación.]

¿Qué tiene de nuevo? Detectar defectos con una red pequeña en una Raspberry Pi ya existe; no decimos que eso sea la novedad. Lo nuevo está en tres cosas. La plantilla por diseño: las uniones de cada modelo de tarjeta se marcan una sola vez, y no hay que entrenar un detector. La confidencialidad: las fotos de la planta se procesan en el mismo equipo y nunca salen de él, algo que para muchas empresas es indispensable. Y que el sistema señala, no rechaza: cada decisión del inspector se vuelve un ejemplo con el que el modelo de esa planta puede mejorar.

**[se puede omitir]** El plan con datos propios es construir al menos 30 tarjetas de práctica con defectos sembrados a propósito y registrados antes de fotografiarlas. Dos personas etiquetan cada unión por separado, y medimos qué tanto coinciden. Separamos los datos por tarjeta, no por foto, para que el modelo nunca se evalúe con una tarjeta que ya vio. Y el conjunto de prueba se congela antes de entrenar y se usa una sola vez, al final.

Pero mejor se los mostramos. Fortino.

## Fortino: demostración y resultados (unos 4.5 minutos)

[Toma el celular, ya conectado a la red de la estación.]

Gracias, Israel. Esta es la estación funcionando. Todo corre en esta Raspberry Pi 4, que crea su propia red Wi-Fi sin internet. El celular solo toma la foto y la manda por esa red local.

[Muestra la hoja del mosaico.]

Antes, una aclaración importante: esta hoja no es una tarjeta nuestra. Todavía no tenemos tarjetas propias soldadas; ese es el siguiente paso. Es un mosaico de 30 fotos reales de uniones de un conjunto público, que se llama PCBSPDefect y tiene licencia abierta. Lo armamos para poder demostrar el sistema completo hoy.

[Toca «Tomar foto» y fotografía la hoja.]

Tomo la foto. La estación la alinea con la plantilla, recorta cada unión y la clasifica. Aquí arriba aparece cuántas uniones hay que revisar y cuántas no tienen observaciones.

[Revisa dos o tres uniones.]

Ahora reviso una unión a la vez. El sistema me sugiere, por ejemplo, «soldadura insuficiente». Si estoy de acuerdo, confirmo. Si no, elijo la clase correcta, y esa corrección queda registrada. Esto es lo que significa que la persona decide. [Si el evaluador quiere, ofrécele el celular o el código QR de la mesa para que lo intente él, o el Reto, donde se pone a prueba como inspector.]

[Señala Resultados preliminares y la Figura 5.]

¿Y qué tan bien funciona? Con nuestras tarjetas todavía no lo sabemos, y no lo vamos a inventar. Lo que sí hicimos fue validar el método con datos reales: 622 uniones de 121 tarjetas del conjunto público, cada una fotografiada con tres iluminaciones. Entrenamos con una parte y evaluamos con otra que el modelo nunca vio, y que usamos una sola vez. La red detectó el 94 por ciento de los defectos, contra 74 de la técnica clásica. Y tuvo 12 por ciento de falsas alarmas, contra 28 de la clásica.

En la gráfica, el punto es el valor medido y la línea es el intervalo de confianza de 95 por ciento. Con eso podemos decir que la red cumple la meta de sensibilidad. Pero en falsas alarmas el intervalo llega hasta 0.22, más que nuestra meta de 0.15. Por eso todavía no podemos afirmar que se cumple. Y la técnica clásica no cumple ninguna de las dos: para este problema hace falta aprendizaje automático.

**[se puede omitir]** Hay algo más que queremos decir con honestidad. Probamos la red con la foto de una tarjeta through-hole de otra fuente, con otra cámara y otra luz, y falló: llamó «sin soldar» a uniones que se ven soldadas. Eso nos confirma lo que plantea el protocolo: un modelo entrenado con otras cámaras no sirve tal cual en una estación nueva. El desempeño en nuestra estación solo lo van a decir nuestros propios datos.

[Señala Conclusiones.]

En resumen: la red cumple la meta de sensibilidad con fotos reales, la meta de falsas alarmas aún no se puede afirmar, la visión clásica no basta, y el prototipo ya corre en una Raspberry Pi 4, en local y sin internet. Falta medir con tarjetas propias y comparar contra la inspección sin apoyo.

[Si la demostración falla: «Como ven, es un prototipo», y mostrar en la laptop la página «Fotos reales» o el video de respaldo.]

Y ahora, ¿hacia dónde va esto? Majo.

## María José: hacia dónde va y cierre (unos 1.5 minutos)

[Señala Hacia dónde va.]

Gracias, Fortino. Una pregunta que nos hicimos fue: si el inspector sigue revisando, ¿para qué sirve el sistema? La respuesta es que hoy el inspector cumple dos funciones que el sistema no puede cubrir. Garantiza la calidad mientras el modelo no demuestre ser confiable en esa planta. Y cada vez que confirma o corrige una unión, produce los ejemplos con los que el modelo de esa planta mejora.

Por eso vemos una ruta en tres fases. Primero, el apoyo, que es este proyecto: el inspector revisa primero lo marcado. Segundo, un piloto por planta, con un modelo para cada empresa entrenado con sus tarjetas, porque los defectos, la luz y los diseños cambian de una planta a otra. Y tercero, una automatización gradual, que ya está fuera de este proyecto: cuando los datos lo respalden, solo las uniones dudosas llegarían a la persona.

Lo siguiente para nosotros es la visita técnica del 5 de noviembre y construir nuestras propias tarjetas para medir todo esto. No queremos sustituir al inspector: queremos que revise primero lo que importa y que, con su trabajo, el sistema aprenda en cada planta. Muchas gracias. ¿Tienen alguna pregunta?

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Si Israel no llega: guion para dos personas

Se usa el mismo texto; solo cambia quién dice cada parte. Si el evaluador pregunta por Israel, digan la verdad con brevedad.

| Parte | Quién | Ajuste |
|:------------------|:--------|:----------------------------|
| Presentación y problema | María José | Igual. Al presentar: «Somos Fortino Romero y María José de la Rosa; nuestro compañero Israel García no pudo acompañarnos hoy». |
| Metas y justificación (primeros dos párrafos de Israel) | María José | Sigue de corrido después del problema. Cambia el relevo por: «¿Cómo funciona? Fortino les explica». |
| Objetivo, cinco pasos, clases, creatividad y plan de datos | Fortino | Empieza con «Gracias, Majo». Termina con «Y ahora se los muestro» y pasa directo a la demostración. |
| Demostración y resultados | Fortino | Igual. |
| Hacia dónde va y cierre | María José | Igual. |

Con dos personas, María José habla unos 6 minutos y Fortino unos 7. Los párrafos marcados se pueden omitir igual que en la versión para tres.
