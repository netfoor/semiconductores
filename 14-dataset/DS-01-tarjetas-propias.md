---
titulo: "DS-01 Tarjetas propias con defectos sembrados"
tipo: especificacion
estado: planeado
creado: 2026-10-26
actualizado: 2026-10-26
autor: "Claude (IA)"
revisado_por: []
fuentes: [F-001]
tags: [femeci, dataset, ds-01]
---

# DS-01 · Tarjetas propias con defectos sembrados

Ficha según la plantilla de [[indice-dataset]]. Estado: **planeado**; no hay imágenes todavía.

| Campo | Contenido |
|---|---|
| Propósito | Entrenar y evaluar la estación de inspección asistida (EXP-001 a EXP-005) |
| Origen | Tarjetas de práctica through-hole soldadas por los integrantes |
| Licencia o permiso | Datos propios del equipo; sin información de terceros |
| Meta de tamaño | Al menos 30 tarjetas con al menos 60 uniones cada una; unos 150 defectos en prueba (protocolo §6.3) |
| Clases | Aceptable, insuficiente, puente, sin soldar, exceso, fría ([[protocolo-v1]] §6.2) |
| Siembra | Cada defecto se siembra a propósito y se anota en la hoja de siembra **antes** de capturar (tarjeta, unión, clase, fecha, quién) |
| Instrumento | Cámara de al menos 12 MP en soporte fijo, iluminación difusa; configuración exacta en la ficha del montaje |
| Captura | `uv run tht capturar`: PNG sin pérdida, ambos lados, dos condiciones de iluminación; metadatos JSON por imagen |
| Integridad | `crudos/MANIFIESTO.csv` con SHA-256; se verifica con `tht manifiesto verificar` antes de cada experimento |
| Etiquetado | Dos personas por separado y a ciegas en la interfaz; acuerdo con kappa de Cohen (`tht acuerdo`); discrepancias resueltas juntas y registradas; resultado `consenso` |
| Partición | Por tarjeta, 60/20/20, semilla fija; prueba congelada con huella (`particion.json`) |
| Datos sintéticos | Los de `tht demo` no forman parte de DS-01 y nunca se mezclan con él |
| Ubicación | Fuera del repositorio (las imágenes pesan); se registran aquí la ruta y la huella del manifiesto |
| Limitaciones conocidas | Defectos sembrados por estudiantes; un solo diseño o pocos; la clase fría es difícil de sembrar de forma reproducible |

## DS-02 (opcional)

Tarjetas aportadas por un productor local bajo acuerdo escrito, solo para validación externa. La visita técnica del 5 de noviembre de 2026 servirá para explorarlo. No se usan para entrenar y no se publican imágenes sin autorización escrita (D-011).
