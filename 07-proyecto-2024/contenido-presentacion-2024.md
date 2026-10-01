---
titulo: "Presentación 2024: registro de contenido"
tipo: registro
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-059]
tags: [femeci, proyecto-2024, fase-4]
aliases: ["Contenido presentación 2024"]
---

# Presentación 2024: registro de contenido

Registro fiel de **lo que contiene** la presentación del proyecto de referencia 2024 [F-059], diapositiva por diapositiva, incluidos los videos. El análisis está en [[analisis-proyecto-2024]] y la comparación nube/edge en [[comparacion-nube-vs-edge]]. Índice: [[indice-proyecto-2024]].

> [!warning] Material marcado como confidencial
> Todas las diapositivas llevan la leyenda "Confidential" y la presentación no nombra a sus autores. Esta nota **parafrasea** el contenido para analizarlo; solo cita textualmente las afirmaciones que hay que verificar. No copiar texto, figuras, diagramas ni capturas de la presentación a ningún entregable (ver [[analisis-proyecto-2024]] §12). Si el repositorio de la bóveda se publica algún día, revisar antes esta nota.

## 1. Ficha

| Campo | Valor |
|---|---|
| Título en Canva | "Semiconductores" |
| Título de portada | *Industrial Semiconductor Inspection System with cloud-Based Inventory Control* |
| Organización y año en portada | "MIRAI INOVATION" (así, con una sola N), 2024 |
| Autores | No aparecen en ninguna diapositiva |
| Extensión | 11 diapositivas, en inglés; las interfaces que aparecen en los videos están en español e inglés |
| Videos | 4 grabaciones de pantalla en la diapositiva 7 (detalle en §3) |
| Otros elementos animados | Un GIF decorativo de banco de imágenes (brazo robótico) en las primeras diapositivas |
| Enlace | https://canva.link/lbqz7r56ctu1vdz (redirige al modo de vista de Canva) |
| Consulta | 2026-10-01, ≈ 14:40–15:00, en el navegador integrado, en modo de vista, **sin iniciar sesión, sin descargar archivos y sin aceptar cookies** (el aviso de cookies se ocultó en la página, no se aceptó) |

## 2. Cómo se leyó

- **Texto:** extraído de la estructura de la página de cada diapositiva y cotejado con una captura de pantalla.
- **Imágenes y diagramas:** revisión visual de cada diapositiva.
- **Videos:** se revisaron cuadro por cuadro dentro del navegador, con cortes cada ≈ 10–12 segundos (unos 5 a 8 cuadros por video). El reproductor los muestra **sin sonido**; no se sabe si tenían audio. Pudieron escaparse eventos breves entre un cuadro y otro.
- **No accesible:** notas del orador. No hace falta el PDF: los videos sí se pudieron revisar.

## 3. Diapositiva por diapositiva

| # | Título | Contenido (paráfrasis) | Observaciones |
|---|---|---|---|
| 1 | Portada | Título del proyecto, "MIRAI INOVATION", 2024 | Sin autores ni institución mexicana |
| 2 | Specific Objectives | Cuatro objetivos: (1) sistema de visión por computadora que capture imágenes para procesarlas; (2) API conectada a la nube que guarde resultados de inspección en tiempo real; (3) aplicación web para ver inspecciones y administrar inventarios de circuitos aceptados y rechazados; (4) integrar robots para automatizar la inspección y clasificación de circuitos | Ningún objetivo es medible (sin métricas ni metas) |
| 3 | General Objective · Client/User Profile | Objetivo general: sistema automatizado de inspección de semiconductores con visión por computadora y conectividad a la nube, para mejorar la eficiencia y reducir errores al clasificar circuitos defectuosos. Usuario: fabricantes de semiconductores que necesitan mejor control de calidad; beneficios declarados: menor costo, inspección más rápida y resultados consistentes | Usuario genérico; ninguna empresa o planta concreta |
| 4 | State of the Art: camera-based inspection systems | Cámaras de barrido lineal (obleas y componentes; alta resolución a velocidad; escalables) y cámaras SWIR (obleas de silicio; defectos invisibles con luz normal). Limitaciones: sincronizar cámara e iluminación; la complejidad y el costo crecen con el número de inspecciones | Sin referencias; describe inspección de obleas, no de tarjetas |
| 5 | State of the Art: computer vision and our differentiation | Los sistemas con IA "show potential" pero les cuesta integrar robótica y procesamiento en la nube en tiempo real; su diferencia sería combinar visión, automatización robótica y analítica en la nube en tiempo real, con "high precision, speed, and scalability" | Diferenciación por integración; sin datos que la respalden |
| 6 | Metodology [*sic*] | Tres capas: **Frontend** (Vite, React, Ant Design: resultados en tiempo real, inventarios); **Backend** (Node.js, Express, MongoDB, autenticación con JWT: intermediario entre frontend y controlador, reglas de negocio y rutas de la API); **Central Controller** (Flask, OpenCV: coordina banda transportadora y brazo robótico mediante endpoints REST, comunicación directa con el hardware, sincroniza actuadores con la inspección). Diagrama: cámara y banda → controlador central ↔ brazo; controlador → backend ↔ MongoDB; backend ↔ frontend (computadoras, celular y un control de videojuego) | No menciona modelo de IA, dataset ni entrenamiento: solo OpenCV. El diagrama dibuja los tres componentes como nubes |
| 7 | Test the Complete System | Cuatro grabaciones de pantalla del sistema funcionando (§4) | Única evidencia de funcionamiento |
| 8 | Justification | Por qué es necesario: "20-30% of electronic circuits fail during manual inspections". Por qué es mejor: automatiza con robots y visión, con más precisión, velocidad y conectividad en la nube. Impacto: la inspección manual en la industria de semiconductores causaría "annual losses of up to $2 billion" | Ninguna cifra tiene fuente (verificación en [[analisis-proyecto-2024]] §7) |
| 9 | Next Steps | Adaptabilidad a otros tipos de inspección e industrias; modelos de IA más avanzados para más exactitud y rapidez; analítica y reportes en tiempo real. Incluye un "procedimiento" de 6 pasos de fabricación de obleas: preparación de material, fabricación de oblea, litografía, depósito y grabado, dopado y oxidación, inspección | El procedimiento es de fabricación de chips, no corresponde al prototipo |
| 10 | Business Plan | Inversión inicial de **12,630 USD**: software 47.5 %, infraestructura en la nube 23.8 %, hardware 20.8 %, contingencia 7.9 %. Precios: venta directa 19,000 USD; suscripción anual 8,000 USD; 3 años 21,600 USD; 5 años 32,000 USD. Estrategia: campañas dirigidas, demostraciones y modelos flexibles | Sin tamaño de mercado, clientes validados ni costos de operación |
| 11 | References | Ocho referencias, **todas sobre prótesis de miembro superior** (abandono y uso de prótesis, rehabilitación, mercado de prótesis y órtesis, guía de entrenamiento mioeléctrico de Ottobock, entrenamiento de prótesis controladas con aprendizaje automático) | Ninguna referencia trata de inspección, visión, semiconductores ni tarjetas. Parece reutilizada de otra presentación (`#inferencia`) |

## 4. Videos de la diapositiva 7

Los nombres de archivo de los videos (visibles en la página) son grabaciones de pantalla de macOS en español; de ahí salen las fechas.

| Video | Fecha y hora de grabación (por el nombre) | Duración | Qué muestra |
|---|---|---|---|
| V1 | 2024-11-28, 17:05 | 94.8 s | Página de inicio de la aplicación web: dos vistas de cámara en vivo, una del **brazo robótico de 6 ejes** junto a una **banda transportadora** con charolas rojas al frente, y otra **cenital** del área de inspección; botones "Bien", "Defectuoso" y "Modo automático"; botón grande de "Parada de emergencia"; lista de circuitos con conteos; resumen de inspección con botones "Actualizar" y "Generar PDF". En el área de inspección aparece una **tarjeta PCB redonda, azul y sin componentes, con el logotipo de MIRAI**; a partir de ≈ 24 s, una tarjeta con un **papel pegado marcado con una X roja**; desde ≈ 60 s el área queda vacía y el brazo cambia de posición |
| V2 | 2024-11-28, 17:17 | 59.4 s | Página "Control del brazo": cámara del brazo y panel "Control de movimiento" con las articulaciones J1–J6; se mueven con botones +/− y luego con deslizadores en grados (por ejemplo, J1 = 20°, J5 = −45°). El efector parece de succión (se ve una manguera) y el brazo parece tener piezas impresas en 3D (`#inferencia`) |
| V3 | 2024-12-02, 14:26 | 30.1 s | Página "Analytics": gráfica de pastel buenos/defectuosos, barras de "Inventario: Cantidad Total" por tipo de circuito y barras de distribución de buenos y defectuosos; botón "Actualizar Gráficas" |
| V4 | 2024-12-02, 14:37 | 43.4 s | Página "Inventory": una tarjeta por tipo de circuito con cantidad total, buenos, defectuosos y última actualización; botones "Editar" y "Borrar"; se renombra un tipo de circuito ("PCB_test" → "PCB_5") y se guarda |

Otros detalles visibles en los videos:
- La aplicación se abre por HTTP sin cifrar (el navegador la marca "No seguro"), en una dirección IP con puerto, sin dominio. No se puede saber si el servidor estaba en la red local o en la nube.
- En V1 y V2 el navegador muestra los menús traducidos al español ("Hogar", "Analítica", "Control del brazo"); en V3 y V4 aparecen en inglés ("Home", "Inventary", "Analitics", "Arm Controll"). Parece traducción automática del navegador (`#inferencia`).

## 5. Datos que aparecen en los videos

| Tipo de circuito | Total | Buenos | Defectuosos | % defectuosos (cálculo propio) | Última actualización |
|---|---|---|---|---|---|
| PCB1 | 19 | 8 | 11 | 57.9 % | 2024-10-23, 11:47 |
| PCB2 | 42 | 21 | 21 | 50.0 % | 2024-10-23, 11:47 |
| PCB3 | 26 | 14 | 12 | 46.2 % | 2024-10-23, 11:56 |
| PCB_test | 103 | 78 | 25 | 24.3 % | 2024-11-17, 19:14 |
| **Suma** | **190** | **121** | **69** | **36.3 %** | — |

Resumen de inspección visible en V1: informe del 2024-10-29, 15:59; 113 inspecciones, 62 buenas y 51 defectuosas (45.1 %). No coincide con la suma del inventario, posiblemente porque son de fechas distintas (`#inferencia`).

## 6. Cronología que se puede reconstruir

| Fecha | Evento | Tipo |
|---|---|---|
| 2024-10-23 | Primeras actualizaciones de inventario visibles (PCB1 a PCB3) | `#hecho` (dato en pantalla) |
| 2024-10-29 | Informe de inspección con 113 inspecciones | `#hecho` (dato en pantalla) |
| 2024-11-17 | Última actualización de "PCB_test" | `#hecho` (dato en pantalla) |
| 2024-11-28 | Grabación de V1 y V2 | `#hecho` (nombre del archivo) |
| 2024-12-02 | Grabación de V3 y V4 | `#hecho` (nombre del archivo) |
| ≈ dic 2024 | Presentación final del proyecto | `#inferencia` (fecha de los videos más recientes) |

`#inferencia` El prototipo funcionó al menos entre el 23 de octubre y el 2 de diciembre de 2024. La tarjeta inspeccionada lleva el logotipo de MIRAI, lo que sugiere que se desarrolló en Mirai Innovation (Osaka, Japón), que ofrece estancias de investigación de 4 a 12 semanas con presentación final [F-075]. Falta confirmarlo con el equipo (Q-023).
