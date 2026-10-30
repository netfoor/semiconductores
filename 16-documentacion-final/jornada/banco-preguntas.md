---
titulo: "Banco de preguntas probables (jornada del 30 de octubre)"
tipo: guia
estado: borrador
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-080]
tags: [femeci, jornada, exposicion, preguntas]
---

Pendiente #16 de [[pendientes]]. Datos: protocolo entregado, [[adenda-2026-10-29]], EXP-006, D-011, D-015, D-016 y la bitácora del 29 de octubre.

<!-- CONSTRUCCIÓN: lo que sigue a esta línea es el texto del PDF. Compilar con 12-protocolo/herramientas/build.py -->

::: {custom-style="TitlePageTitle"}
Banco de preguntas probables
:::

::: {custom-style="TitlePageText"}
Estación de inspección visual asistida para uniones through-hole · FEMECI-PUEBLA 2026 · 30 de octubre
:::

# Cómo usarlo

- Las preguntas están agrupadas por tema; junto a cada una va quién responde primero: **MJ** (María José), **IG** (Israel) o **FR** (Fortino). Si falta Israel, sus preguntas las toma Fortino.
- Las respuestas son la idea central. Respondan con sus palabras, cortas, y miren al evaluador.
- Regla de oro: si algo no se ha medido, se dice. «Eso todavía no lo hemos medido; lo mediremos con…» es una respuesta correcta.

# 1. El problema

**1. ¿Cómo saben que el problema existe? (MJ)**
Por tres vías. La literatura: la inspección visual humana deja pasar entre 20 % y 30 % de los defectos en la mayoría de las tareas (See, 2015). La técnica: las uniones through-hole son difíciles de inspeccionar con máquinas porque la unión queda abajo y hay componentes altos que tapan zonas (GÖPEL electronic). Y una fuente local: personal técnico de una empresa de ensamble de Puebla nos dijo que la validación conserva pasos manuales y que, si algo falla, se revisa a ojo con más resolución. Es una sola fuente y lo decimos así; la visita técnica del 5 de noviembre es para confirmarlo.

**2. ¿Qué empresa es? (MJ)**
Preferimos no nombrarla por confidencialidad; así lo decidimos como equipo. Fue una conversación con personal técnico, no un acuerdo formal.

**3. ¿Por qué through-hole y no montaje superficial (SMD)? (MJ)**
Porque el SMD casi siempre se ensambla y se inspecciona con máquinas. En through-hole la unión queda del lado de abajo, muchas veces se suelda con ola o a mano y se revisa a ojo. Ahí es donde hace más falta apoyo.

**4. ¿El 20 % al 30 % es de soldadura? (MJ)**
No. Es de inspección visual en general, de piezas de precisión. Lo usamos solo como orden de magnitud. La línea base que sí vamos a comparar es la nuestra: la inspección sin apoyo de los integrantes, que es el experimento EXP-001.

**5. ¿Qué tiene que ver esto con semiconductores? (MJ)**
En Puebla no hay fabricación de chips en sentido estricto; lo que hay y está creciendo es ensamble de tarjetas electrónicas. Nuestro proyecto está en esa parte de la cadena: la calidad del ensamble.

# 2. Metas y método

**6. ¿Por qué esas metas: 0.90, 0.15, 5 s? (IG)**
Las fijamos antes de medir. La sensibilidad de 0.90 toma como referencia que inspectores humanos detectan cerca de 0.85 en el estudio de See; queremos estar al menos ahí. Las falsas alarmas de 0.15: si el sistema marca demasiadas uniones buenas, el inspector deja de confiar en él. Los 5 segundos son un requisito de diseño para una estación de revisión, que validaremos con el usuario.

**7. ¿Qué es sensibilidad y qué son falsas alarmas? (IG)**
Sensibilidad: de todos los defectos que hay, qué proporción detecta el sistema. Falsas alarmas: de todas las uniones buenas, qué proporción marca como sospechosas por error. Usamos esas dos y no solo la exactitud porque hay muchas más uniones buenas que malas, y la exactitud engaña en ese caso.

**8. ¿Por qué separan los datos por tarjeta? (IG)**
Porque las uniones de una misma tarjeta se parecen: misma soldadura, misma luz. Si una tarjeta aparece en entrenamiento y en prueba, el modelo «hace trampa» y el resultado se infla. Por eso separamos por tarjeta y el conjunto de prueba se usa una sola vez.

**9. ¿Cómo van a etiquetar sus datos? (IG)**
Dos personas etiquetan cada unión por separado, sin ver la hoja donde registramos qué defecto sembramos. Medimos qué tanto coinciden con la kappa de Cohen, y las diferencias se resuelven por consenso.

**10. ¿Tienen la norma IPC-A-610? (IG)**
No tenemos el texto completo: es una norma de pago. Definimos las clases tomando como referencia lo que se puede verificar con material de acceso disponible, y no afirmamos certificar nada según la norma.

**11. ¿Qué es la «plantilla por diseño»? (IG)**
Para cada modelo de tarjeta se marcan una sola vez dónde están las uniones. Después, cualquier foto de esa tarjeta se alinea a la plantilla y cada unión se recorta sola. Así no hay que entrenar un detector que encuentre las uniones, que necesitaría muchas más etiquetas.

**12. ¿Por qué no usan YOLO u otro detector? (FR)**
Porque en una línea de ensamble se inspecciona muchas veces el mismo diseño de tarjeta. Si ya sabemos dónde está cada unión, basta con clasificarla, y eso necesita menos datos y menos cómputo. Detectar defectos en tarjetas con YOLO en una Raspberry Pi ya está publicado; no decimos que esa sea nuestra novedad.

# 3. La demostración

**13. ¿Esa hoja es una tarjeta suya? (FR)**
No. Es un mosaico de 30 fotos reales de uniones de un conjunto público, PCBSPDefect, con licencia abierta CC BY 4.0. Lo armamos porque no tuvimos material para soldar tarjetas propias antes de la jornada. La hoja y la pantalla lo dicen.

**14. ¿Por qué no hicieron sus tarjetas? (FR o MJ)**
No conseguimos el material a tiempo. Preferimos decirlo y demostrar el sistema completo con fotos reales públicas, en lugar de presentar datos que no tenemos. Las tarjetas propias empiezan después de la jornada, junto con la visita técnica.

**15. ¿Realmente funciona sin internet? (FR)**
Sí. La Raspberry Pi crea su propia red Wi-Fi, que no tiene salida a internet; el celular se conecta a ella, toma la foto y la Pi hace todo el procesamiento. Pueden comprobarlo: la red no tiene internet.

**16. ¿Por qué una Raspberry Pi 4 si el protocolo dice Pi 5? (FR)**
No conseguimos una Pi 5 a tiempo. La Pi 4 es más lenta, así que si cumple la meta de tiempo es probable que la Pi 5 también, pero no lo demuestra. Usar la Pi 4 para el experimento de tiempo es un cambio que el equipo todavía no adopta formalmente; por eso no reportamos todavía la meta de tiempo como cumplida.

**17. ¿Cuánto tarda? (FR)**
En la Raspberry Pi 4, con la imagen digital del mosaico, la mediana fue de 1.27 segundos en 5 repeticiones. Es una prueba de software, no el experimento formal: el protocolo pide al menos 30 repeticiones con fotos de la cámara. La primera foto del celular tardó bastante más; creemos que es la carga inicial, pero no lo hemos analizado.

**18. ¿Por qué un celular como cámara? (FR)**
Porque cualquier planta tiene uno y no hay que instalar ninguna aplicación: se abre una página de la estación. Para la estación definitiva el protocolo contempla una cámara fija con iluminación controlada, porque la posición y la luz afectan el resultado.

# 4. Resultados

**19. ¿De dónde salen el 0.94 y el 0.12? (FR)**
Del experimento EXP-006, con 622 uniones reales de 121 tarjetas del conjunto PCBSPDefect, fotografiadas con tres iluminaciones. Entrenamos con cinco semillas, elegimos la red con los datos de validación y usamos el conjunto de prueba una sola vez. Los intervalos se calcularon con bootstrap agrupado por tarjeta.

**20. Entonces, ¿ya cumplen sus metas? (FR)**
Con datos públicos, la red cumple la de sensibilidad. La de falsas alarmas cumple en el valor medido, 0.12, pero el intervalo llega a 0.22, así que no podemos afirmarla. Con nuestras tarjetas todavía no hay resultados, y eso es lo que de verdad dirá si la estación funciona.

**21. ¿Qué es la línea base clásica y por qué compararla? (FR)**
Es una técnica de visión por computadora sin aprendizaje: umbrales, forma y color de cada unión. Sirve para saber si de verdad hace falta una red neuronal. Con 0.74 de sensibilidad y 0.28 de falsas alarmas no cumple ninguna meta, así que sí hace falta.

**22. ¿Qué red usan? (FR)**
Una red convolucional pequeña, de unos 52 mil parámetros, entrenada desde cero con PyTorch en una computadora y ejecutada en la Pi con ONNX Runtime. El protocolo planteaba ajustar una red preentrenada; para EXP-006 usamos la pequeña desde cero, y la preentrenada (MobileNet) queda como alternativa para comparar con nuestros datos.

**23. ¿Qué pasa si la red se equivoca? (FR o MJ)**
Por eso la persona decide. El sistema solo señala dónde mirar; el inspector confirma o corrige, y esa corrección se registra y sirve para mejorar el modelo. En la demostración pueden ver cómo se corrige una unión.

**24. ¿Funcionaría con otras tarjetas o cámaras? (FR)**
No lo sabemos, y tenemos una señal de que no sin datos nuevos: probamos la red con la foto de una tarjeta de otra fuente y falló. Por eso el plan es un modelo por planta, entrenado con sus propias tarjetas.

# 5. Para qué sirve y originalidad

**25. Si el inspector sigue revisando, ¿para qué sirve el sistema? (MJ)**
El inspector deja de revisar todas las uniones con la misma atención y revisa primero las marcadas. Mientras el modelo no demuestre ser confiable en una planta, él garantiza la calidad, y cada confirmación o corrección enseña al modelo. Nuestra hipótesis es que así se detectan más defectos; la mediremos con el experimento EXP-005, inspección con apoyo frente a sin apoyo.

**26. ¿Algún día reemplazará al inspector? (MJ)**
No es nuestro objetivo. La ruta que vemos es: apoyo, que es este proyecto; un piloto con el modelo de cada planta; y una automatización gradual, fuera de este proyecto, en la que solo las uniones dudosas lleguen a la persona y se haga auditoría por muestreo.

**27. ¿Qué tiene de original? (IG)**
No es usar una red en una Raspberry Pi, eso ya existe. Es la combinación: plantilla por diseño, procesamiento local por confidencialidad, humano en el ciclo que enseña al modelo, y una evaluación honesta con metas fijadas antes de medir y comparación contra la inspección humana.

**28. ¿Cuánto cuesta? (FR)**
La convocatoria no evalúa el costo. El equipo es una computadora de placa única y una cámara o un celular, muy por debajo de una máquina de inspección automática. No damos una cifra exacta porque no la hemos documentado.

**29. ¿Por qué no usar la nube? (FR)**
Por confidencialidad: las fotos de las tarjetas de una planta pueden ser secretas. Y para no depender de la red del lugar. Aun así, el protocolo plantea decidirlo con un experimento (EXP-003): se elige la opción más simple que cumpla tiempo, operación sin internet y confidencialidad.

# 6. Proceso y ética

**30. ¿Usaron inteligencia artificial para hacer el proyecto? (FR)**
Sí, y está declarado en el protocolo y en la bitácora: usamos un asistente de IA, Claude, como apoyo en búsqueda de información, programación y documentos. Cada actividad hecha con IA está marcada en la bitácora, y el equipo revisa y defiende el contenido.

**31. ¿Cómo se repartieron el trabajo? (MJ)**
Respondan con lo que hizo cada quien. La bitácora registra cada actividad con su responsable y su fecha, y el repositorio guarda cada cambio con su fecha.

**32. ¿Qué harían diferente? (cualquiera)**
Empezar antes las tarjetas propias. Todo lo demás —el método, las metas y la estación— está listo para medir con ellas.

**33. ¿Cuál es el siguiente paso? (MJ)**
La visita técnica a una planta de ensamble el 5 de noviembre, construir y etiquetar las tarjetas propias, y hacer los experimentos de inspección humana, desempeño y tiempo en noviembre.

# Preguntas incómodas: cómo responder

- **Si señalan algo que no se ha hecho:** reconocerlo y decir cuándo y cómo se hará. No justificarse de más.
- **Si piden una cifra que no tienen:** «No la hemos medido». Nunca estimarla en el momento.
- **Si preguntan algo que no saben:** «Buena pregunta; no lo sabemos, pero lo revisaríamos así…».
- **Si la demostración falla:** «Es un prototipo; por eso lo medimos», y mostrar la página «Fotos reales» o el video de respaldo.
