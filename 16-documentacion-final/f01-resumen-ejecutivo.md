---
titulo: "Borrador de contenido para F-01 (resumen ejecutivo)"
tipo: entregable
estado: borrador
creado: 2026-10-18
actualizado: 2026-10-18
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, f-01, entregable]
aliases: ["F-01 resumen"]
---

# Borrador de contenido para F-01 (resumen ejecutivo)

> [!warning] Es un borrador de IA
> Fortino e Israel deben reescribirlo con sus palabras y pasarlo a la plantilla oficial de F-01 cuando se tenga. Debe coincidir con [[protocolo-v1]]. No nombra empresas (D-011).

**Título:** Estación de inspección visual asistida con procesamiento local para uniones soldadas through-hole en el ensamble electrónico: diseño y validación experimental de un prototipo

**Modalidad / categoría / nivel:** Ingenierías · Sistemas Informáticos y Computación (robótica y máquinas inteligentes: visión artificial) · Superior

**Integrantes:** Fortino Romero Mantilla (líder), Israel Jesús García Osorio y María José de la Rosa Hernández · **Asesor institucional:** José Francisco Espinosa Garita (UTP)

**Resumen ejecutivo (≈ 250 palabras):**

La inspección visual de uniones soldadas through-hole conserva etapas manuales, y la literatura indica que la inspección humana deja pasar entre 20 % y 30 % de los defectos en la mayoría de las tareas. Personal técnico de una empresa de ensamble electrónico de Puebla nos informó que la validación de piezas todavía tiene partes manuales y que, cuando algo falla, se revisa con mayor resolución a ojo humano. Nuestro reto de ingeniería es diseñar y evaluar una estación de bajo costo, con cámara y procesamiento local en una Raspberry Pi 5, que señale uniones sospechosas para que la persona decida (humano en el ciclo), sin depender de internet. Evaluaremos el prototipo con un conjunto de datos propio de al menos 30 tarjetas con defectos sembrados de forma controlada, partido por tarjeta, con criterios de aceptación fijados antes de medir: sensibilidad ≥ 0.90, falsas alarmas ≤ 0.15 y latencia mediana ≤ 5 s por tarjeta. Compararemos contra la inspección humana sin asistencia y contra una línea base de visión clásica, y reportaremos intervalos de confianza y análisis de errores. Decidiremos con un experimento si el procesamiento debe ser local, en la nube o híbrido. Aún no hay resultados con nuestras tarjetas; en una validación preliminar con fotos públicas reales de uniones through-hole, la red alcanzó una sensibilidad de 0.94 con 0.12 de falsas alarmas, frente a 0.74 y 0.28 de la línea base. Aportamos un conjunto de datos documentado, una evaluación reproducible y una decisión de arquitectura basada en mediciones.

**Palabras clave:** inspección de soldadura, through-hole, visión artificial, cómputo en el borde, control de calidad.
