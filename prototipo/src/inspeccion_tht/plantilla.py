"""Plantilla de uniones por diseño de tarjeta y alineación de imagen.

Cada diseño de tarjeta tiene una imagen de referencia y la lista de rectángulos
donde están sus uniones. Una captura nueva se alinea contra la referencia
(el soporte fijo limita el desplazamiento a unos milímetros) y de ahí se
recorta cada unión. Así no hace falta un detector para encontrar las uniones.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import cv2
import numpy as np


@dataclass
class Union:
    id: str
    x: int
    y: int
    w: int
    h: int


@dataclass
class Plantilla:
    diseno: str
    referencia: str  # nombre del archivo de la imagen de referencia
    ancho: int
    alto: int
    uniones: list[Union] = field(default_factory=list)

    def guardar(self, ruta: Path) -> None:
        Path(ruta).write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def cargar(cls, ruta: Path) -> "Plantilla":
        d = json.loads(Path(ruta).read_text(encoding="utf-8"))
        d["uniones"] = [Union(**u) for u in d.get("uniones", [])]
        return cls(**d)

    def union(self, id_: str) -> Union:
        for u in self.uniones:
            if u.id == id_:
                return u
        raise KeyError(id_)


class ErrorAlineacion(RuntimeError):
    pass


def _gris(img: np.ndarray) -> np.ndarray:
    return img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def alinear(imagen: np.ndarray, referencia: np.ndarray, lado_max: int = 900) -> np.ndarray:
    """Matriz afín 2x3 que lleva `imagen` al marco de `referencia`.

    Usa ECC (correlación de intensidades) sobre versiones reducidas, que tolera
    el patrón repetitivo de una tarjeta perforada mejor que los puntos clave.
    Si ECC no converge, intenta con puntos ORB y RANSAC.
    """
    g_img, g_ref = _gris(imagen), _gris(referencia)
    if g_img.shape != g_ref.shape:
        g_img = cv2.resize(g_img, (g_ref.shape[1], g_ref.shape[0]))
        escala_ini = np.array([[g_ref.shape[1] / imagen.shape[1], 0, 0],
                               [0, g_ref.shape[0] / imagen.shape[0], 0]], dtype=np.float32)
    else:
        escala_ini = None
    f = min(1.0, lado_max / max(g_ref.shape))
    peq = lambda g: cv2.GaussianBlur(cv2.resize(g, None, fx=f, fy=f, interpolation=cv2.INTER_AREA), (5, 5), 0)
    a, r = peq(g_img).astype(np.float32), peq(g_ref).astype(np.float32)
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        _, warp = cv2.findTransformECC(r, a, warp, cv2.MOTION_EUCLIDEAN,
                                       (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
        # ECC devuelve la transformación referencia -> imagen; se invierte.
        warp = cv2.invertAffineTransform(warp)
        warp[:, 2] /= f
    except cv2.error:
        warp = _alinear_orb(g_img, g_ref)
    if escala_ini is not None:
        warp = _componer(warp, escala_ini)
    return warp.astype(np.float32)


def _alinear_orb(g_img: np.ndarray, g_ref: np.ndarray) -> np.ndarray:
    orb = cv2.ORB_create(3000)
    k1, d1 = orb.detectAndCompute(g_img, None)
    k2, d2 = orb.detectAndCompute(g_ref, None)
    if d1 is None or d2 is None:
        raise ErrorAlineacion("Sin puntos característicos suficientes")
    pares = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(d1, d2)
    if len(pares) < 10:
        raise ErrorAlineacion(f"Solo {len(pares)} correspondencias")
    src = np.float32([k1[m.queryIdx].pt for m in pares])
    dst = np.float32([k2[m.trainIdx].pt for m in pares])
    m, _ = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    if m is None:
        raise ErrorAlineacion("RANSAC no encontró una transformación")
    return m


def _componer(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """a ∘ b para matrices afines 2x3 (primero b, luego a)."""
    A = np.vstack([a, [0, 0, 1]])
    B = np.vstack([b, [0, 0, 1]])
    return (A @ B)[:2]


def al_marco_de_referencia(imagen: np.ndarray, warp: np.ndarray, plantilla: Plantilla) -> np.ndarray:
    return cv2.warpAffine(imagen, warp, (plantilla.ancho, plantilla.alto),
                          flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def recortes(alineada: np.ndarray, plantilla: Plantilla, margen: float = 0.15) -> dict[str, np.ndarray]:
    """Recorte de cada unión (con un margen proporcional) desde la imagen ya alineada."""
    out = {}
    H, W = alineada.shape[:2]
    for u in plantilla.uniones:
        mx, my = int(u.w * margen), int(u.h * margen)
        x0, y0 = max(0, u.x - mx), max(0, u.y - my)
        x1, y1 = min(W, u.x + u.w + mx), min(H, u.y + u.h + my)
        out[u.id] = alineada[y0:y1, x0:x1].copy()
    return out
