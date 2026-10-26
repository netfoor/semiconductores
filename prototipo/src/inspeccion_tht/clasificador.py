"""Modelos de clasificación de uniones con una interfaz común.

- "linea_base": características clásicas + centroides (`linea_base.py`).
- "red": red convolucional pequeña exportada a ONNX y ejecutada con ONNX Runtime,
  que es ligero y corre en la Raspberry Pi sin PyTorch.

Ambos exponen `evaluar_recortes(recortes) -> (clases_sugeridas, puntajes_defecto)`.
"""

import json
from pathlib import Path

import cv2
import numpy as np

from .clases import ACEPTABLE

LADO_RED = 64
MEDIA, ESCALA = 0.5, 0.25
MODELOS = ("linea_base", "red")


def preparar(recortes: list[np.ndarray], lado: int = LADO_RED) -> np.ndarray:
    """Recortes BGR -> tensor NCHW float32 normalizado (mismo preprocesamiento al entrenar)."""
    lote = np.empty((len(recortes), 3, lado, lado), np.float32)
    for i, r in enumerate(recortes):
        x = cv2.resize(r, (lado, lado), interpolation=cv2.INTER_AREA)
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        lote[i] = ((x - MEDIA) / ESCALA).transpose(2, 0, 1)
    return lote


def _softmax(z: np.ndarray) -> np.ndarray:
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


class ClasificadorONNX:
    def __init__(self, ruta_onnx: Path):
        import onnxruntime as ort
        self.ruta = Path(ruta_onnx)
        self.meta = json.loads(self.ruta.with_suffix(".json").read_text(encoding="utf-8"))
        self.clases: list[str] = self.meta["clases"]
        self.lado = int(self.meta.get("lado", LADO_RED))
        opciones = ort.SessionOptions()
        opciones.intra_op_num_threads = 0
        self._sesion = ort.InferenceSession(str(self.ruta), opciones, providers=["CPUExecutionProvider"])
        self._entrada = self._sesion.get_inputs()[0].name

    def probabilidades(self, recortes: list[np.ndarray]) -> np.ndarray:
        if not recortes:
            return np.empty((0, len(self.clases)), np.float32)
        logits = self._sesion.run(None, {self._entrada: preparar(recortes, self.lado)})[0]
        return _softmax(logits)

    def evaluar_recortes(self, recortes: list[np.ndarray]) -> tuple[list[str], np.ndarray]:
        p = self.probabilidades(recortes)
        if not len(p):
            return [], np.array([])
        sugerencias = [self.clases[i] for i in p.argmax(axis=1)]
        puntaje = 1 - p[:, self.clases.index(ACEPTABLE)] if ACEPTABLE in self.clases else np.ones(len(p))
        return sugerencias, puntaje


def cargar(carpeta_modelos: Path, nombre: str = "linea_base", archivo: Path | None = None):
    """Carga el modelo `nombre` desde la carpeta de modelos (o un archivo concreto)."""
    from .linea_base import ClasificadorCentroide
    carpeta_modelos = Path(carpeta_modelos)
    if nombre == "linea_base":
        return ClasificadorCentroide.cargar(archivo or carpeta_modelos / "linea_base.json")
    if nombre == "red":
        return ClasificadorONNX(archivo or carpeta_modelos / "red.onnx")
    raise ValueError(f"Modelo desconocido: {nombre!r}. Válidos: {', '.join(MODELOS)}")


def ruta_principal(carpeta_modelos: Path, nombre: str) -> Path:
    return Path(carpeta_modelos) / ("linea_base.json" if nombre == "linea_base" else "red.onnx")
