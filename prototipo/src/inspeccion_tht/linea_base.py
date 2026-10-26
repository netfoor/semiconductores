"""Línea base de visión clásica (protocolo, sección 6.4).

Umbral y morfología sobre cada recorte de unión para obtener características
de forma y brillo, y un clasificador de centroides más cercano. Sirve como
referencia contra la cual se compara el clasificador ligero de aprendizaje
profundo: si este no supera a la línea base, no se justifica.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from .clases import ACEPTABLE, validar

NOMBRES_CARACTERISTICAS = (
    "frac_brillante",
    "frac_oscura",
    "n_componentes",
    "area_mayor",
    "circularidad",
    "extension_h",
    "extension_v",
    "brillo_medio",
    "rugosidad",
)

LADO = 64  # todos los recortes se normalizan a este tamaño


def caracteristicas(recorte: np.ndarray) -> np.ndarray:
    g = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY) if recorte.ndim == 3 else recorte
    g = cv2.resize(g, (LADO, LADO), interpolation=cv2.INTER_AREA)
    g = cv2.GaussianBlur(g, (3, 3), 0)
    total = float(LADO * LADO)
    _, brillante = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    brillante = cv2.morphologyEx(brillante, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    oscura = (g < 0.45 * max(1.0, float(np.median(g)))).astype(np.uint8)
    n, etiquetas, stats, _ = cv2.connectedComponentsWithStats(brillante, 8)
    areas = stats[1:, cv2.CC_STAT_AREA] if n > 1 else np.array([0])
    grandes = int((areas > 0.02 * total).sum())
    if n > 1:
        k = 1 + int(np.argmax(areas))
        mascara = (etiquetas == k).astype(np.uint8)
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        per = max(1.0, cv2.arcLength(contornos[0], True))
        area = float(areas.max())
        circ = 4 * np.pi * area / (per * per)
        ext_h = stats[k, cv2.CC_STAT_WIDTH] / LADO
        ext_v = stats[k, cv2.CC_STAT_HEIGHT] / LADO
        dentro = g[mascara > 0].astype(np.float32)
        brillo, rug = float(dentro.mean()) / 255, float(dentro.std()) / 255
    else:
        area, circ, ext_h, ext_v, brillo, rug = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    return np.array([
        brillante.sum() / 255 / total,
        oscura.sum() / total,
        grandes,
        area / total,
        circ,
        ext_h,
        ext_v,
        brillo,
        rug,
    ], dtype=np.float64)


@dataclass
class ClasificadorCentroide:
    clases: list[str]
    centroides: np.ndarray  # (n_clases, n_caract) en espacio estandarizado
    media: np.ndarray
    escala: np.ndarray

    @classmethod
    def entrenar(cls, X: np.ndarray, y: list[str]) -> "ClasificadorCentroide":
        X = np.asarray(X, dtype=np.float64)
        for c in y:
            validar(c)
        media = X.mean(axis=0)
        escala = X.std(axis=0)
        escala[escala < 1e-9] = 1.0
        Z = (X - media) / escala
        clases = sorted(set(y))
        y_arr = np.array(y)
        centroides = np.stack([Z[y_arr == c].mean(axis=0) for c in clases])
        return cls(clases, centroides, media, escala)

    def _distancias(self, X: np.ndarray) -> np.ndarray:
        Z = (np.atleast_2d(X) - self.media) / self.escala
        return np.linalg.norm(Z[:, None, :] - self.centroides[None, :, :], axis=2)

    def probabilidades(self, X: np.ndarray) -> np.ndarray:
        d = self._distancias(X)
        e = np.exp(-(d - d.min(axis=1, keepdims=True)))
        return e / e.sum(axis=1, keepdims=True)

    def predecir(self, X: np.ndarray) -> list[str]:
        return [self.clases[i] for i in self._distancias(X).argmin(axis=1)]

    def puntaje_defecto(self, X: np.ndarray) -> np.ndarray:
        """Probabilidad de que la unión no sea aceptable (sirve para ordenar o fijar umbral)."""
        p = self.probabilidades(X)
        if ACEPTABLE not in self.clases:
            return np.ones(len(p))
        return 1 - p[:, self.clases.index(ACEPTABLE)]

    def guardar(self, ruta: Path) -> None:
        Path(ruta).write_text(json.dumps({
            "tipo": "linea_base_centroide",
            "caracteristicas": list(NOMBRES_CARACTERISTICAS),
            "clases": self.clases,
            "centroides": self.centroides.tolist(),
            "media": self.media.tolist(),
            "escala": self.escala.tolist(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def cargar(cls, ruta: Path) -> "ClasificadorCentroide":
        d = json.loads(Path(ruta).read_text(encoding="utf-8"))
        return cls(d["clases"], np.array(d["centroides"]), np.array(d["media"]), np.array(d["escala"]))
