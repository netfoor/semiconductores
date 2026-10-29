---
titulo: "Spec: página del proyecto v2, el sistema en contexto"
tipo: especificacion
estado: en-curso
creado: 2026-10-29
actualizado: 2026-10-29
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-080]
tags: [femeci, landing, demo, d-015]
---

# Spec: página del proyecto v2, el sistema en contexto

Idea de Fortino (29 oct), en la línea de D-015: la página principal de femeci.foor.dev deja de repetir lo que explican la bitácora y el protocolo, y **muestra el sistema**. Cuenta primero cómo se fabrica una tarjeta electrónica, dónde está la inspección y por qué through-hole; luego cómo se usa la estación, con capturas reales, y los resultados.

## Principios

1. **Contexto antes que tecnología.** Alguien que nunca vio una línea de ensamble debe entender en un minuto dónde entra el sistema.
2. **Visual y por pasos.** Recorrido con desplazamiento: el texto avanza a la izquierda y la ilustración, fija a la derecha, cambia con cada paso (capas de la tarjeta que se separan, como en la referencia de agrocebada.foor.dev).
3. **Sin internet.** La estación local también sirve esta página, así que no se cargan bibliotecas externas: SVG, CSS 3D y JavaScript propio. Iconos dibujados para el proyecto.
4. **Accesible.** El texto se entiende sin la animación; con «reducir movimiento» no hay transiciones; funciona en celular.
5. **Honesto.** Las capturas son de la demostración (mosaico de fotos públicas) y se dice en la sección; los resultados conservan sus intervalos y la advertencia de M2.

## Secciones (en orden)

| # | Sección | Contenido | Estado |
|---|---|---|---|
| L1 | Portada | «Una segunda mirada para cada soldadura» y una captura del celular con la inspección | Pendiente (se conserva la actual) |
| L2 | **Del diseño a la tarjeta revisada** (recorrido) | Seis pasos con una tarjeta en 3D cuyas capas se separan: 1 tarjeta desnuda (sustrato, cobre, máscara); 2 montaje superficial (SMD): pasta, colocación automática y horno, lo inspeccionan máquinas (AOI); 3 montaje through-hole (THT): las patillas atraviesan la tarjeta; 4 soldadura por ola o a mano, del lado inferior; 5 **inspección, donde trabaja nuestra estación** (barrido y uniones marcadas); 6 prueba eléctrica y envío. Corte transversal THT frente a SMD en los pasos 2 y 3 | Hecho (v2-3) |
| L3 | El problema | Breve, con la cifra de See (2015) | Se conserva, se acorta |
| L4 | **La estación en uso** | Capturas del celular en secuencia: elegir perfil, tomar foto, analizando, inspección, inspección terminada | Pendiente |
| L5 | Resultados | Gráfica de EXP-006 con mejor presentación: cifras grandes y una vista de «en qué se equivoca» | Pendiente (se conserva la actual) |
| L6 | Hacia dónde va | Las tres fases de D-016 | Hecho |
| L7 | Equipo y fuentes | Se conserva | Hecho |

## Detalle de L2

- **Ilustración:** una tarjeta cuadrada en vista isométrica (CSS 3D: `rotateX` y `rotateZ`) con seis capas SVG: sustrato FR-4, pistas de cobre, máscara y serigrafía, componentes SMD, componentes THT y soldaduras del lado inferior. Cada paso cambia la separación y la opacidad de las capas.
- **Paso 5:** la capa de soldaduras baja y se agranda; una línea de barrido la recorre y aparecen marcos de colores en algunas uniones, con los mismos colores y estilos de línea que la estación.
- **Barra de proceso:** seis iconos propios (tarjeta, máquina, mano, ola, lupa, caja) con el paso activo resaltado; el de inspección siempre marcado como «aquí trabajamos».
- **Celular:** la ilustración queda fija arriba (aprox. 45 % de la pantalla) y el texto pasa debajo.
- **Técnica:** `IntersectionObserver` cambia `data-paso` en el escenario; las transiciones son CSS. Sin dependencias.

## Pendientes derivados

Se llevan en [[pendientes]] (sección «Página del proyecto v2»).
