---
titulo: "Dataset — índice"
tipo: indice
estado: borrador
creado: 2026-10-01
actualizado: 2026-10-01
autor: "Claude (IA)"
revisado_por: []
tags: [femeci, dataset]
---

# Dataset — índice

**Estado:** pendiente. **Alimenta:** A4, A5 y B3 → EV-10, EV-13, EV-18.

## Reglas de manejo de datos derivadas de la convocatoria

- **Integridad:** la falsificación o alteración de datos causa descalificación [F-001 §9.1]. Los datos crudos se conservan sin cambios, con hash (SHA-256); toda transformación queda en scripts versionados (REQ-DER-02).
- **Datos sintéticos o aumentados:** se etiquetan y declaran como tales; nunca se mezclan sin marca con datos reales.
- **Derechos:** cada fuente de datos tiene licencia o permiso escrito registrado; los datos de una empresa requieren autorización explícita de uso **y** de publicación (REQ-ETI-05, R-07).
- **Personas:** evitar datos personales (por ejemplo, rostros en imágenes); si aparecen, anonimizarlos.
- **Partición:** datos de prueba independientes de los de desarrollo, definidos antes de entrenar o ajustar (A4).

## Ficha de dataset (plantilla)

`DS-##-nombre.md`: propósito · origen y procedencia · licencia o permiso · fecha y condiciones de captura · instrumento (cámara, sensor) y configuración · tamaño y clases · protocolo de etiquetado y quién etiquetó · acuerdo entre etiquetadores · partición · hash de los archivos crudos · limitaciones y sesgos conocidos · ubicación de los archivos.

## Fichas

- [[DS-01-tarjetas-propias]] (planeado; incluye la nota sobre DS-02 opcional).
