"""Imágenes SINTÉTICAS para probar el software sin tarjetas reales.

Nada de lo que se genere aquí es un dato del proyecto: sirve solo para pruebas
automáticas, para revisar la interfaz y para medir la latencia del flujo.
Toda imagen sintética lleva la marca "SINTETICO" y no se mezcla con DS-01.
"""

import numpy as np
import cv2

from .clases import CLASES
from .plantilla import Plantilla, Union

FONDO = (60, 110, 150)     # tarjeta perforada color café (BGR)
COBRE = (70, 140, 200)
LADO_CELDA = 80


def _metal(img, centro, radio, brillo=210, ruido=8.0, rng=None):
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    d = np.sqrt((xx - centro[0]) ** 2 + (yy - centro[1]) ** 2)
    m = d <= radio
    grad = brillo - 60 * (d / max(radio, 1)) ** 2
    if rng is not None:
        grad = grad + rng.normal(0, ruido, grad.shape)
    for c in range(3):
        canal = img[..., c].astype(np.float32)
        canal[m] = np.clip(grad[m], 0, 255)
        img[..., c] = canal.astype(np.uint8)


def celda(clase: str, rng: np.random.Generator, lado: int = LADO_CELDA) -> np.ndarray:
    """Una unión sintética centrada en una celda de `lado` x `lado`."""
    if clase not in CLASES:
        raise ValueError(clase)
    img = np.full((lado, lado, 3), FONDO, np.uint8)
    c = (lado // 2 + int(rng.integers(-2, 3)), lado // 2 + int(rng.integers(-2, 3)))
    r_pad = lado // 4
    cv2.circle(img, c, r_pad, COBRE, -1)
    if clase == "aceptable":
        _metal(img, c, r_pad - 1, 215, rng=rng)
    elif clase == "exceso":
        _metal(img, c, int(r_pad * 1.55), 225, rng=rng)
    elif clase == "insuficiente":
        _metal(img, c, r_pad - 1, 205, rng=rng)
        cv2.circle(img, c, r_pad // 2, (25, 30, 35), -1)
    elif clase == "sin_soldar":
        cv2.circle(img, c, r_pad // 2, (20, 25, 30), -1)
        cv2.circle(img, c, max(2, r_pad // 5), (150, 150, 150), -1)
    elif clase == "puente":
        _metal(img, c, r_pad - 1, 215, rng=rng)
        y0 = c[1] - r_pad // 3
        cv2.rectangle(img, (c[0], y0), (lado - 1, y0 + 2 * r_pad // 3), (205, 205, 205), -1)
    elif clase == "fria":
        _metal(img, c, r_pad - 1, 150, ruido=30.0, rng=rng)
    ruido = rng.normal(0, 4, img.shape)
    return np.clip(img.astype(np.float32) + ruido, 0, 255).astype(np.uint8)


def tarjeta(filas: int, columnas: int, rng: np.random.Generator, prob_defecto: float = 0.3,
            diseno: str = "sintetica-01") -> tuple[np.ndarray, Plantilla, dict[str, str]]:
    """Tarjeta sintética, su plantilla y la verdad de referencia por unión."""
    margen = 40
    H, W = filas * LADO_CELDA + 2 * margen, columnas * LADO_CELDA + 2 * margen
    img = np.full((H, W, 3), FONDO, np.uint8)
    uniones, verdad = [], {}
    defectos = [c for c in CLASES if c != "aceptable"]
    for i in range(filas):
        for j in range(columnas):
            uid = f"U{i + 1:02d}{j + 1:02d}"
            clase = str(rng.choice(defectos)) if rng.random() < prob_defecto else "aceptable"
            x, y = margen + j * LADO_CELDA, margen + i * LADO_CELDA
            img[y:y + LADO_CELDA, x:x + LADO_CELDA] = celda(clase, rng)
            uniones.append(Union(uid, x, y, LADO_CELDA, LADO_CELDA))
            verdad[uid] = clase
    # Marcas de referencia para la alineación y marca de dato sintético.
    for (x, y) in [(12, 12), (W - 28, 12), (12, H - 28), (W - 28, H - 28)]:
        cv2.rectangle(img, (x, y), (x + 16, y + 16), (240, 240, 240), -1)
    cv2.putText(img, "SINTETICO", (margen, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return img, Plantilla(diseno, f"{diseno}.png", W, H, uniones), verdad


def desplazar(img: np.ndarray, dx: float, dy: float, angulo: float = 0.0) -> np.ndarray:
    """Simula una colocación imperfecta en el soporte (EXP-004)."""
    h, w = img.shape[:2]
    m = cv2.getRotationMatrix2D((w / 2, h / 2), angulo, 1.0)
    m[:, 2] += (dx, dy)
    return cv2.warpAffine(img, m, (w, h), borderMode=cv2.BORDER_REPLICATE)


def iluminar(img: np.ndarray, factor: float) -> np.ndarray:
    """Simula otra condición de iluminación (EXP-004)."""
    return np.clip(img.astype(np.float32) * factor, 0, 255).astype(np.uint8)
