Quiero que a partir de este momento actúes como copiloto principal de investigación, ingeniería y documentación de este proyecto para FEMECI-PUEBLA 2026. No quiero que simplemente me des ideas aisladas: quiero que construyamos el proyecto de manera sistemática dentro de la bóveda de Obsidian a la que tienes acceso, dejando documentada nuestra investigación, decisiones, fuentes, hipótesis, experimentos y avances.

1. Contexto del equipo

Somos un equipo formado por dos estudiantes de Ingeniería de Software, Israel y yo, y un profesor como asesor.
Israel y yo participamos previamente en una experiencia en Japón mediante MIRAI y tenemos experiencia desarrollando proyectos tecnológicos. Nuestro asesor tiene experiencia especialmente en datos.
Como equipo tenemos experiencia en áreas como:

- Python y desarrollo de software.
- Open source.
- Cloud computing.
- Sistemas distribuidos.
- Docker y Kubernetes.
- IoT y sistemas embebidos.
- Datos.
- Desarrollo de prototipos tecnológicos.
Podemos trabajar con Raspberry Pi, Arduino/microcontroladores, teléfonos Android con cámara y otros componentes que ya tenemos disponibles.
No quiero que elijamos tecnologías porque nos gustan o porque ya las conocemos. Elegiremos cada tecnología únicamente cuando sea adecuada para resolver el problema. Podemos adaptarnos al stack que resulte necesario.
Cuando trabajemos con Python, mantendremos nuestras prácticas habituales, incluyendo uv para gestión del proyecto y dependencias.
1. Objetivo principal
Nuestro objetivo es desarrollar un proyecto sólido para participar en FEMECI-PUEBLA 2026, organizado por la Secretaría de Ciencia, Humanidades, Tecnología e Innovación del Estado de Puebla.
No quiero empezar programando ni decidir prematuramente qué producto construir.
Primero necesitamos entender:
1. qué exige exactamente la convocatoria;
1. cómo se evalúan los proyectos;
1. qué problemas tecnológicos reales y actuales existen en Puebla;
1. cuáles son las prioridades científicas, tecnológicas, industriales y económicas actuales del estado;
1. dónde existe una oportunidad concreta en la que nuestras capacidades permitan desarrollar y validar una solución convincente.
El proyecto final debe nacer de esa intersección:
problema real de Puebla + evidencia verificable + necesidad actual + solución técnicamente viable + innovación + metodología rigurosa + prototipo demostrable.
1. Primera tarea: estudiar completamente la convocatoria
Antes de investigar ideas o comenzar a desarrollar, lee íntegramente la convocatoria FEMECI-PUEBLA 2026 que dejé en el contexto de este chat.
No hagas solamente un resumen superficial.
Extrae y documenta:

- objetivos del certamen;
- modalidades;
- categorías;
- requisitos;
- restricciones;
- documentación necesaria;
- fechas;
- criterios de evaluación;
- ponderaciones de la rúbrica;
- requisitos metodológicos;
- requisitos de prototipo y presentación;
- reglas de originalidad;
- cualquier aspecto que pueda afectar nuestra estrategia de proyecto.
Convierte la convocatoria en una especie de especificación del proyecto: qué características tendría que demostrar una propuesta excelente para cumplir de manera verificable con cada criterio de evaluación.
Guarda esta información de manera organizada en la bóveda de Obsidian para utilizarla durante todo el proyecto.
Si tu sistema de memoria permite guardar contexto relevante del proyecto, conserva también los elementos esenciales de la convocatoria, pero la bóveda debe ser nuestra fuente persistente principal, de modo que las decisiones importantes no dependan únicamente de tu memoria.
1. Segunda tarea: investigación estratégica sobre Puebla
Después realiza una investigación profunda en Internet. Puedes utilizar Chrome sin problema.
Prioriza fuentes oficiales y primarias: Gobierno del Estado de Puebla, SECIHTI Puebla, Secretaría de Economía, universidades, centros de investigación, organismos públicos, publicaciones científicas, documentos gubernamentales, empresas directamente involucradas y otras fuentes institucionales.
Investiga, entre otras cosas:

- quién organiza FEMECI-PUEBLA y cuáles son sus objetivos;
- ediciones anteriores de FEMECI o certámenes relacionados;
- proyectos seleccionados o reconocidos anteriormente, si existe información;
- prioridades actuales de SECIHTI Puebla;
- planes estatales relacionados con ciencia, tecnología e innovación;
- sectores estratégicos para Puebla;
- problemas tecnológicos concretos que el estado o su industria estén intentando resolver;
- programas, inversiones, laboratorios, empresas y universidades relacionadas con esos sectores.
No quiero que busques simplemente “una idea que suene innovadora”. Quiero identificar problemas verificables y actuales.
Para cada hallazgo importante, registra la fuente, URL, fecha y qué implicación podría tener para nuestro proyecto.
1. Hipótesis inicial: semiconductores
Tenemos una hipótesis inicial que quiero investigar seriamente, pero no quiero que la aceptes de antemano.
Hemos observado que Puebla parece estar impulsando actualmente iniciativas relacionadas con semiconductores y desarrollo tecnológico asociado.
Quiero comprobar qué tan cierto y relevante es esto actualmente.
Investiga:

- estrategia de Puebla relacionada con semiconductores;
- inversiones y programas actuales;
- empresas involucradas;
- universidades y laboratorios;
- formación de talento;
- cadena de suministro;
- manufactura, diseño, encapsulado, pruebas, inspección y control de calidad;
- problemas técnicos documentados;
- necesidades actuales de la industria;
- oportunidades donde software, IA, visión por computadora, IoT, edge computing, ciberseguridad o sistemas distribuidos puedan aportar algo concreto.
Investiga también a Yankuilot y otras organizaciones o empresas relevantes que operen en Puebla en este ecosistema.
Tenemos posibilidad de contactar personas relacionadas con el sector, por lo que identifica también qué información sería especialmente valiosa obtener mediante entrevistas con especialistas y qué preguntas deberíamos hacerles.
1. Proyecto previo que puede servir como referencia
Existe un proyecto de aproximadamente 2024 relacionado con este tema que puede servirnos como punto de partida conceptual.
Te voy a proporcionar esta presentación:
<https://canva.link/lbqz7r56ctu1vdz>
Ábrela y analízala completamente. Si tienes problemas para acceder a ella, dímelo y te proporcionaré el PDF, aunque algunos videos cortos de la presentación se perderían.
No asumas que tenemos que reconstruir ese proyecto.
Úsalo para entender:

- qué problema intentaba resolver;
- arquitectura propuesta;
- tecnologías;
- supuestos;
- limitaciones;
- qué sigue siendo vigente en 2026;
- qué ha cambiado desde 2024;
- qué partes podríamos reutilizar conceptualmente;
- qué haríamos diferente actualmente.
En aquel proyecto parte del procesamiento se planteaba en cloud. Nosotros podríamos descubrir que para un prototipo industrial tiene más sentido ejecutar inferencia localmente mediante Raspberry Pi/edge computing, por ejemplo. Pero no tomes esa decisión todavía: compárala técnicamente.
1. Líneas que quiero explorar
Algunas posibilidades que hemos mencionado son:

- visión por computadora;
- inspección o verificación mediante cámara;
- aplicación móvil;
- Raspberry Pi + cámara;
- inferencia en edge;
- control de calidad;
- detección de defectos;
- apoyo a toma de decisiones;
- trazabilidad;
- ciberseguridad aplicada a sistemas industriales;
- verificación automática;
- IoT;
- creación de datasets propios;
- combinación de datasets públicos con datos reales;
- modelos existentes y transfer learning;
- YOLO;
- Hugging Face;
- herramientas y modelos open source.
Estas son hipótesis de exploración, no requisitos del proyecto.
Si la investigación demuestra que existe otro problema más importante, viable y defendible, quiero que lo señales.
Una posibilidad particularmente interesante sería conseguir físicamente alguna pieza o componente relacionado con la industria, generar nuestro propio pequeño dataset y construir un prototipo real que funcione con Raspberry Pi/cámara u otro hardware accesible.
Sin embargo, primero debemos saber si eso responde a un problema real.
1. Principio fundamental: problema antes que tecnología
Evita esta secuencia:
“tenemos YOLO + Raspberry Pi + cloud → busquemos dónde utilizarlos”.
Quiero que trabajemos al contrario:
problema documentado → usuario/sector afectado → evidencia → requisitos → hipótesis → experimento → arquitectura → tecnologías.
No quiero tecnología por tecnología.
Si proponemos visión por computadora, por ejemplo, debemos poder justificar:

- qué se necesita detectar;
- quién necesita detectarlo;
- cómo se hace actualmente;
- qué problema existe con el método actual;
- qué datos necesitamos;
- qué métrica demostraría que nuestra solución funciona;
- qué hardware sería suficiente;
- qué limitaciones tendría;
- por qué nuestra propuesta aporta algo relevante.
1. Investigación y evidencia
Diferencia siempre claramente entre:
hechos verificados, inferencias, hipótesis e ideas del equipo.
No presentes una idea nuestra como si fuera una necesidad de la industria hasta encontrar evidencia.
Para afirmaciones importantes utiliza fuentes y registra las referencias.
Si encontramos huecos que Internet no puede resolver, conviértelos en preguntas de investigación o entrevistas. Podemos intentar conseguir información directamente de empresas, desarrolladores, investigadores o personas del sector.
2. Documentación en Obsidian
Quiero que todo este proceso quede documentado progresivamente en la bóveda a la que tienes acceso.
Crea una estructura lógica para:

- convocatoria y requisitos;
- rúbrica;
- investigación sobre Puebla;
- investigación sobre semiconductores;
- empresas y actores;
- fuentes;
- proyecto 2024;
- problemas identificados;
- entrevistas/preguntas pendientes;
- ideas candidatas;
- decisiones;
- arquitectura;
- experimentos;
- dataset;
- bitácora;
- protocolo de investigación;
- documentación final.
No borres ni sobrescribas información importante sin necesidad.
Mantén una bitácora cronológica desde ahora. La convocatoria exige evidencia del proceso de trabajo, así que nuestra documentación debe permitir reconstruir cómo pasamos desde investigación inicial hasta la solución final.
 1. Cómo quiero que evalúes posibles proyectos
Cuando tengamos suficiente investigación, no selecciones inmediatamente una idea.
Primero construye varias hipótesis de proyecto y compáralas en términos de:

- problema real demostrado;
- relevancia para Puebla;
- evidencia disponible;
- alineación con FEMECI;
- rigor metodológico que permite demostrar;
- originalidad;
- impacto potencial;
- viabilidad en el tiempo disponible;
- disponibilidad de hardware;
- disponibilidad o posibilidad de crear datos;
- posibilidad de construir un prototipo funcional;
- posibilidad de realizar experimentos cuantitativos;
- facilidad para demostrar resultados ante evaluadores;
- riesgos y dependencias externas.
No quiero que fuerces la opción de semiconductores a ser la elegida. Si la evidencia muestra una oportunidad mucho mejor, quiero saberlo.
1. Resultado que buscamos
Queremos terminar con algo mucho más fuerte que una presentación conceptual.
Idealmente debemos llegar a:
problema real documentado → investigación → hipótesis/reto de ingeniería → prototipo funcional → dataset/evidencia → experimentos → métricas → resultados reproducibles → conclusiones → demostración física → defensa técnica.
Queremos construir un proyecto competitivo y plenamente alineado con la convocatoria, pero sin inventar resultados, exagerar impacto ni diseñarlo únicamente para impresionar al jurado. La estrategia debe ser que un buen proyecto científico/de ingeniería produzca por sí mismo una candidatura sólida.
2. Tu primera ejecución
Por ahora NO empieces a programar.
En esta primera etapa:
A. Lee íntegramente la convocatoria.
B. Organiza sus requisitos y rúbrica dentro de Obsidian.
C. Investiga a la SECIHTI Puebla y el contexto actual de ciencia/tecnología en Puebla.
D. Investiga profundamente el ecosistema actual de semiconductores en Puebla.
E. Identifica empresas, universidades, laboratorios, iniciativas y problemas documentados.
F. Analiza el proyecto/presentación de 2024 que te proporcioné.
G. Identifica qué información nos falta y qué podríamos obtener directamente de contactos de la industria.
H. Genera un primer mapa de oportunidades de proyecto, todavía sin comprometernos con ninguna.
Documenta todo en la bóveda.
Al terminar esta primera fase, entrégame un brief de investigación explicando:
3. qué aprendiste de la convocatoria;
4. qué parece buscar realmente FEMECI;
5. cuáles son las prioridades tecnológicas actuales de Puebla que encontraste;
6. qué está ocurriendo actualmente con semiconductores en Puebla;
7. qué problemas concretos encontraste;
8. qué oportunidades ves para nuestro equipo;
9. qué información todavía necesitamos;
10. qué deberíamos preguntar a contactos de industria;
11. cuáles serían las siguientes acciones de investigación.
No necesito todavía que elijas el proyecto ganador. Primero quiero que construyamos evidencia suficiente para tomar esa decisión.
Trabaja con autonomía: abre las fuentes necesarias, sigue referencias relevantes y profundiza cuando encuentres algo importante. Si encuentras evidencia que contradice alguna de nuestras suposiciones, señálala claramente en lugar de intentar hacer que encaje con nuestra idea inicial.
