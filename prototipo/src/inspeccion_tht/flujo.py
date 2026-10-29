"""Flujo completo de inspección: alinear, recortar, clasificar y marcar."""

import time
from dataclasses import dataclass

import cv2
import numpy as np

from .clases import es_defecto
from .plantilla import Plantilla, al_marco_de_referencia, alinear, normalizar_color, recortes


@dataclass
class Resultado:
    union_id: str
    x: int
    y: int
    w: int
    h: int
    sugerencia: str
    puntaje_defecto: float
    sospechosa: bool


def inspeccionar(imagen: np.ndarray, referencia: np.ndarray, plantilla: Plantilla,
                 modelo, umbral: float | None = None
                 ) -> tuple[list[Resultado], dict[str, float], np.ndarray]:
    """Devuelve resultados por unión, tiempos por etapa (s) y la imagen alineada.

    `modelo` es cualquier clasificador con `evaluar_recortes` (línea base o red ONNX).

    Una unión es sospechosa si la clase sugerida es un defecto o, cuando se da
    `umbral`, si su puntaje de defecto lo supera.
    """
    tiempos = {}
    t = time.perf_counter()
    warp = alinear(imagen, referencia)
    alineada = normalizar_color(al_marco_de_referencia(imagen, warp, plantilla), referencia)
    tiempos["alineacion_s"] = time.perf_counter() - t

    t = time.perf_counter()
    rec = recortes(alineada, plantilla)
    ids = [u.id for u in plantilla.uniones]
    tiempos["recortes_s"] = time.perf_counter() - t

    t = time.perf_counter()
    sugerencias, puntajes = modelo.evaluar_recortes([rec[i] for i in ids])
    tiempos["clasificacion_s"] = time.perf_counter() - t
    tiempos["total_s"] = sum(tiempos.values())

    resultados = []
    for u, s, p in zip(plantilla.uniones, sugerencias, puntajes):
        sospechosa = es_defecto(s) if umbral is None else bool(p >= umbral)
        resultados.append(Resultado(u.id, u.x, u.y, u.w, u.h, s, float(p), sospechosa))
    return resultados, tiempos, alineada


def leer(ruta) -> np.ndarray:
    img = cv2.imread(str(ruta), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(ruta)
    return img
