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


PARECIDO_SUFICIENTE = 0.6  # correlación con la referencia a partir de la cual no se prueba ECC


class ErrorAlineacion(RuntimeError):
    pass


def _gris(img: np.ndarray) -> np.ndarray:
    return img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def alinear(imagen: np.ndarray, referencia: np.ndarray, lado_max: int = 900) -> np.ndarray:
    """Matriz 3x3 que lleva `imagen` al marco de `referencia`.

    - Primero, homografía con puntos SIFT y RANSAC, que corrige escala y perspectiva (foto tomada
      a mano con un celular). Si reproduce bien la referencia, se usa directamente.
    - Si no, también ECC (correlación de intensidades, giro y desplazamiento) sobre versiones
      reducidas, que tolera el patrón repetitivo de una tarjeta perforada en un soporte fijo
      (si no converge, puntos ORB con RANSAC), y se elige la que mejor reproduce la referencia.
    """
    candidatos = []
    h = _alinear_homografia(imagen, referencia)
    if h is not None:
        if _parecido(imagen, referencia, h) >= PARECIDO_SUFICIENTE:
            return h
        candidatos.append(h)
    try:
        candidatos.append(_a_3x3(_alinear_ecc(imagen, referencia, lado_max)))
    except ErrorAlineacion:
        pass
    if not candidatos:
        raise ErrorAlineacion("No se pudo alinear la captura con la referencia")
    if len(candidatos) == 1:
        return candidatos[0]
    return max(candidatos, key=lambda m: _parecido(imagen, referencia, m))


def _a_3x3(m: np.ndarray) -> np.ndarray:
    return np.vstack([m, [0, 0, 1]]).astype(np.float32) if m.shape == (2, 3) else m.astype(np.float32)


def _parecido(imagen: np.ndarray, referencia: np.ndarray, m: np.ndarray, lado: int = 400) -> float:
    """Correlación normalizada entre la referencia y la captura llevada a su marco (versiones reducidas)."""
    g_ref = _gris(referencia)
    f = min(1.0, lado / max(g_ref.shape))
    s = np.array([[f, 0, 0], [0, f, 0], [0, 0, 1]], np.float32)
    tam = (max(1, int(g_ref.shape[1] * f)), max(1, int(g_ref.shape[0] * f)))
    a = cv2.warpPerspective(_gris(imagen), s @ m, tam, flags=cv2.INTER_AREA).astype(np.float32)
    r = cv2.resize(g_ref, tam, interpolation=cv2.INTER_AREA).astype(np.float32)
    a, r = a - a.mean(), r - r.mean()
    return float((a * r).sum() / (np.sqrt((a * a).sum() * (r * r).sum()) + 1e-6))


def _alinear_ecc(imagen: np.ndarray, referencia: np.ndarray, lado_max: int) -> np.ndarray:
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


def _alinear_homografia(imagen: np.ndarray, referencia: np.ndarray, lado_max: int = 1000,
                        min_inliers: int = 25) -> np.ndarray | None:
    """Homografía imagen -> referencia con SIFT y RANSAC, o None si no es confiable."""
    g_img, g_ref = _gris(imagen), _gris(referencia)
    fi, fr = min(1.0, lado_max / max(g_img.shape)), min(1.0, lado_max / max(g_ref.shape))
    a = cv2.resize(g_img, None, fx=fi, fy=fi, interpolation=cv2.INTER_AREA)
    r = cv2.resize(g_ref, None, fx=fr, fy=fr, interpolation=cv2.INTER_AREA)
    sift = cv2.SIFT_create(2000)
    k1, d1 = sift.detectAndCompute(a, None)
    k2, d2 = sift.detectAndCompute(r, None)
    if d1 is None or d2 is None or len(k1) < min_inliers or len(k2) < min_inliers:
        return None
    pares = cv2.BFMatcher(cv2.NORM_L2).knnMatch(d1, d2, k=2)
    buenos = [p[0] for p in pares if len(p) == 2 and p[0].distance < 0.75 * p[1].distance]
    if len(buenos) < min_inliers:
        return None
    src = np.float32([k1[m.queryIdx].pt for m in buenos]) / fi
    dst = np.float32([k2[m.trainIdx].pt for m in buenos]) / fr
    h, mascara = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    if h is None or int(mascara.sum()) < min_inliers:
        return None
    if not 0.05 < abs(np.linalg.det(h[:2, :2])) < 20:  # descarta transformaciones degeneradas
        return None
    return h.astype(np.float32)


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
    """Lleva la captura al marco de la referencia con una matriz afín (2x3) o una homografía (3x3)."""
    tam = (plantilla.ancho, plantilla.alto)
    if warp.shape == (3, 3):
        return cv2.warpPerspective(imagen, warp, tam, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return cv2.warpAffine(imagen, warp, tam, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def normalizar_color(alineada: np.ndarray, referencia: np.ndarray) -> np.ndarray:
    """Iguala la media y la desviación de cada canal de la captura alineada a las de la referencia.

    Compensa el brillo, el contraste y el nivel de negro de otra cámara o de otra luz, que el
    clasificador no tolera bien (un corrimiento de ±20 niveles bajó la exactitud de la red de
    EXP-006 en una tarjeta de prueba). Ambas imágenes están en el mismo marco.
    """
    mu_a, sd_a = (v.ravel() for v in cv2.meanStdDev(alineada))
    mu_r, sd_r = (v.ravel() for v in cv2.meanStdDev(referencia))
    escala = sd_r / np.maximum(sd_a, 1e-6)
    niveles = np.arange(256, dtype=np.float32)[:, None]
    tabla = np.clip((niveles - mu_a) * escala + mu_r, 0, 255).astype(np.uint8)  # 256 x 3, una columna por canal
    return cv2.LUT(alineada, tabla.reshape(1, 256, 3))


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
