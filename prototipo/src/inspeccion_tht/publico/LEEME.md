# Datos públicos de la plataforma

Los genera `uv run tht publicar` (ver `prototipo/README.md`). No se editan a mano.

- `resultados.json`: resumen de EXP-006 con la huella SHA-256 del archivo fuente.
- `experimentos.json`: estado de las fichas EXP-*.md.
- `fotos/` y `fotos.json`: 60 fotos del conjunto de prueba oficial de PCBSPDefect (b_dip), copiadas sin modificar.
  Tsang, S.-H., Suo, Z., Chan, T. T.-L., Nguyen, H.-T., & Lun, D. P.-K. (2023). PCB soldering defect inspection using multitask learning under low data regimes. *Advanced Intelligent Systems, 5*, 2300364. https://doi.org/10.1002/aisy.202300364. Conjunto en https://zenodo.org/records/23307359, licencia CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
- `red_pcbspdefect.onnx`: red de EXP-006 (partición oficial, semilla 2, elegida por validación).
