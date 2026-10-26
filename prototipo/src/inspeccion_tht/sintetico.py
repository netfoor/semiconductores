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


def celda(clase: str, rng: np.random.Generator, lado: int = LADO_CELDA, variabilidad: float = 1.0) -> np.ndarray:
    """Una unión sintética centrada en una celda de `lado` x `lado`.

    `variabilidad` (0 a 1) controla cuánto cambian tamaño, brillo, desenfoque,
    reflejos y orientación. Con 0 salen casi idénticas; con 1 se parecen más al
    desorden de una foto real, aunque siguen siendo sintéticas.
    """
    if clase not in CLASES:
        raise ValueError(clase)
    v = float(np.clip(variabilidad, 0, 1))
    fondo = np.clip(np.array(FONDO) + rng.normal(0, 12 * v, 3), 0, 255)
    img = np.full((lado, lado, 3), fondo, np.uint8)
    d = int(2 + 3 * v)
    c = (lado // 2 + int(rng.integers(-d, d + 1)), lado // 2 + int(rng.integers(-d, d + 1)))
    r_pad = int(round(lado / 4 * (1 + rng.uniform(-0.12, 0.12) * v)))
    brillo = 215 + rng.uniform(-25, 15) * v
    cv2.circle(img, c, r_pad, COBRE, -1)
    if clase == "aceptable":
        _metal(img, c, r_pad - 1, brillo, rng=rng)
    elif clase == "exceso":
        _metal(img, c, int(r_pad * rng.uniform(1.4, 1.7)), brillo + 8, rng=rng)
    elif clase == "insuficiente":
        _metal(img, c, r_pad - 1, brillo - 10, rng=rng)
        hueco = int(r_pad * rng.uniform(0.35, 0.6))
        cv2.circle(img, (c[0] + int(rng.integers(-2, 3)), c[1] + int(rng.integers(-2, 3))), hueco, (25, 30, 35), -1)
    elif clase == "sin_soldar":
        cv2.circle(img, c, r_pad // 2, (20, 25, 30), -1)
        cv2.circle(img, c, max(2, r_pad // 5), (150, 150, 150), -1)
    elif clase == "puente":
        _metal(img, c, r_pad - 1, brillo, rng=rng)
        grosor = int(r_pad * rng.uniform(0.5, 0.8))
        gris = int(brillo - 10)
        if rng.random() < 0.5 * v:
            x0 = c[0] - grosor // 2
            cv2.rectangle(img, (x0, c[1]), (x0 + grosor, lado - 1), (gris, gris, gris), -1)
        else:
            y0 = c[1] - grosor // 2
            cv2.rectangle(img, (c[0], y0), (lado - 1, y0 + grosor), (gris, gris, gris), -1)
    elif clase == "fria":
        _metal(img, c, r_pad - 1, brillo - rng.uniform(55, 80), ruido=30.0, rng=rng)
    if v and clase not in ("sin_soldar",) and rng.random() < 0.6 * v:
        # Reflejo especular de la lámpara sobre el metal.
        ang = rng.uniform(0, 2 * np.pi)
        p = (int(c[0] + 0.35 * r_pad * np.cos(ang)), int(c[1] + 0.35 * r_pad * np.sin(ang)))
        cv2.circle(img, p, max(2, r_pad // 5), (250, 250, 250), -1)
    if v:
        k = int(rng.choice([1, 1, 3, 3, 5]))
        if k > 1:
            img = cv2.GaussianBlur(img, (k, k), 0)
    ruido = rng.normal(0, 4 + 4 * v, img.shape)
    return np.clip(img.astype(np.float32) + ruido, 0, 255).astype(np.uint8)


def tarjeta(filas: int, columnas: int, rng: np.random.Generator, prob_defecto: float = 0.3,
            diseno: str = "sintetica-01", variabilidad: float = 1.0) -> tuple[np.ndarray, Plantilla, dict[str, str]]:
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
            img[y:y + LADO_CELDA, x:x + LADO_CELDA] = celda(clase, rng, variabilidad=variabilidad)
            uniones.append(Union(uid, x, y, LADO_CELDA, LADO_CELDA))
            verdad[uid] = clase
    # Marcas de referencia para la alineación y marca de dato sintético.
    for (x, y) in [(12, 12), (W - 28, 12), (12, H - 28), (W - 28, H - 28)]:
        cv2.rectangle(img, (x, y), (x + 16, y + 16), (240, 240, 240), -1)
    if variabilidad:
        # Iluminación no uniforme sobre toda la tarjeta.
        gx = np.linspace(1 - 0.12 * variabilidad, 1 + 0.12 * variabilidad, W)[None, :, None]
        if rng.random() < 0.5:
            gx = gx[:, ::-1]
        img = np.clip(img.astype(np.float32) * gx, 0, 255).astype(np.uint8)
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
