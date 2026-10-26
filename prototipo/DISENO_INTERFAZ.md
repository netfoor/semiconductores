# Diseño de la interfaz local

Interfaz de la estación de inspección (etiquetado, plantillas e inspección asistida). Corre en la Raspberry Pi o en una laptop, **sin internet**, en `http://127.0.0.1:8000`.

## Origen de la identidad

Sale del cartel oficial de FEMECI Capítulo Puebla 2026 para que el prototipo se reconozca como parte de esa convocatoria:

- **Marca:** magenta de FEMECI.
- **Acento:** morado del texto "Capítulo Puebla 2026".
- **Motivo:** la barra corta de cuatro colores que acompaña a "Ciencia, Ingeniería, Tecnología, Innovación" en el cartel. Se usa una sola vez, bajo el encabezado.
- **Tipografía:** el cartel usa una sans pesada y condensada en los títulos. Como la estación no debe descargar nada, se usa la pila del sistema con peso 800 e interletrado cerrado en los títulos, que da un efecto parecido. Si el equipo consigue la fuente del cartel con licencia libre, se agrega primero en la pila.

## Tokens (`static/estilo.css`)

| Token | Valor | Uso |
|---|---|---|
| `--tinta` | `#2b1d30` | Texto principal |
| `--tinta-2` | `#57485b` | Texto secundario |
| `--gris` | `#766c7a` | Notas |
| `--linea` | `#e4dce5` | Bordes de 1 px |
| `--banda` | `#f7f3f7` | Fondo alterno |
| `--marca` | `#d4006f` | Botón primario, enlaces, selección |
| `--marca-profunda` | `#9c0051` | Hover y texto de marca sobre blanco |
| `--acento` | `#6c2a7c` | Títulos de sección, foco |
| `--seleccion` | `#fbe4f0` | Fila o unión elegida |
| `--cian`, `--amarillo`, `--naranja`, `--verde` | `#0098d4`, `#f1b400`, `#ef8a00`, `#2e8b45` | Solo en el motivo y en las clases |

## Clases de condición

Cada clase tiene color **y** forma de borde y nombre escrito, para que nada dependa solo del color:

| Clase | Color | Borde |
|---|---|---|
| Aceptable | verde `#2e8b45` | delgado, punteado |
| Insuficiente | naranja `#c26a00` | grueso, continuo |
| Puente | magenta `#d4006f` | grueso, continuo |
| Sin soldar | cian `#0076a8` | grueso, discontinuo |
| Exceso | amarillo oscuro `#9a7200` | grueso, doble |
| Fría | morado `#6c2a7c` | grueso, punteado |

## Reglas

- Paneles con borde de 1 px, sin sombra ni esquinas redondeadas (radio de 0 a 2 px).
- Botón primario magenta con texto blanco, alto mínimo de 44 px.
- Atajos de teclado del 1 al 6 para las clases, en el orden de la tabla.
- Cuando la carpeta de datos es sintética, toda página lo dice arriba.
- En el teléfono el panel lateral pasa debajo de la imagen y los botones ocupan el ancho completo.
