---
titulo: "Tríptico v1 para la jornada (150 x 120 cm)"
tipo: entregable
estado: borrador
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001, F-080]
tags: [femeci, cartel, triptico, jornada]
---

# Tríptico v1 para la jornada

Sustituye al [[cartel-v1]] de 90 x 120 cm. Las recomendaciones de la SECIHTI Puebla del 26 de octubre piden un **tríptico de 150 cm de ancho por 120 cm de alto**, impreso en material resistente que se sostenga solo sobre la mesa.

- **Archivo para imprimir:** `triptico-v1.pdf`, una página de 1500 x 1200 mm. Los dobleces van a 50 y 100 cm (líneas punteadas). Vista previa: `triptico-v1-vista.png`.
- **Cómo se genera:** `uv run --no-project --with segno --with pillow python 16-documentacion-final/cartel/build_triptico.py`. Las cifras salen de `resultados.json` de EXP-006.

## Cómo cumple las recomendaciones

| Recomendación | En el tríptico |
|---|---|
| Título del proyecto arriba | El título registrado en el F-01 |
| Estructura sugerida para Ingenierías | Izquierda: introducción, antecedentes, meta de ingeniería y justificación. Centro: objetivos, metodología, y creatividad e innovación. Derecha: resultados, conclusiones y referencias |
| Arial, Calibri, Tahoma o Times New Roman | Arial; en Linux se incrusta Liberation Sans, de métricas idénticas |
| Legible a 2 m, fondo claro y letra oscura | Texto de unos 50 pt, títulos de unos 65 pt, fondo blanco; sin grises claros en la letra |
| Imágenes numeradas con su crédito | Figuras 1 a 3, cada una con su origen |
| Breve: síntesis con las ideas principales | Frases cortas (texto reducido a la mitad tras la revisión de Fortino) |
| Destacar resultados con números | 0.94 y 0.12, con la gráfica y sus intervalos |
| Sin logotipos ni referencias a la institución o al asesor | No los lleva |
| Sin páginas web, códigos (QR) ni datos de contacto de los participantes (inciso e) | No los lleva; solo los enlaces de las referencias |
| Sin conexión a internet para operar el proyecto (inciso f) | La demostración corre en local |

## Pendiente del equipo antes de imprimir

1. `#pregunta` Revisar y reescribir los textos con sus palabras (REQ-DER-05), y poder explicar cada cifra y cada figura.
2. `#pregunta` Nombres de los integrantes: la guía no los prohíbe, pero el ejemplo no los muestra. Decidir si se agregan bajo el título.
3. `#pregunta` La declaración de IA cita a Anthropic (Claude). Es una cita por honestidad, no un logotipo ni un patrocinio; si el comité lo objeta, basta «un asistente de IA».
4. Si mañana la foto real de la hoja impresa funciona, sustituir la Figura 2 por esa captura y quitar «foto simulada» del crédito.
5. Confirmar con la imprenta el tamaño (150 x 120 cm) y el material rígido o con soporte.
