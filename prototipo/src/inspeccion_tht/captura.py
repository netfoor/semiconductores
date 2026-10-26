"""Captura de imágenes con nombre, metadatos y huella (protocolo de captura, DS-01).

Cámaras soportadas, en orden de preferencia:
- Picamera2 (Raspberry Pi con módulo de cámara), si está instalada en el sistema;
- cualquier cámara USB vía OpenCV;
- una carpeta de archivos (para pruebas y para repetir capturas ya hechas).
"""

import json
import platform
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

from . import manifiesto

PATRON_TARJETA = re.compile(r"^T\d{2,3}$")


class Camara:
    nombre = "generica"

    def capturar(self) -> np.ndarray:
        raise NotImplementedError

    def cerrar(self) -> None:
        pass


class CamaraPicamera2(Camara):
    nombre = "picamera2"

    def __init__(self, resolucion: tuple[int, int] = (4056, 3040)):
        from picamera2 import Picamera2  # solo existe en Raspberry Pi OS
        self._cam = Picamera2()
        self._cam.configure(self._cam.create_still_configuration(main={"size": resolucion, "format": "RGB888"}))
        self._cam.start()
        self.resolucion = resolucion

    def capturar(self) -> np.ndarray:
        # Picamera2 entrega RGB888 que en memoria ya está en orden BGR para OpenCV.
        return self._cam.capture_array()

    def cerrar(self) -> None:
        self._cam.stop()


class CamaraOpenCV(Camara):
    nombre = "opencv"

    def __init__(self, indice: int = 0, resolucion: tuple[int, int] | None = None):
        self._cap = cv2.VideoCapture(indice)
        if not self._cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara {indice}")
        if resolucion:
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolucion[0])
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucion[1])

    def capturar(self) -> np.ndarray:
        for _ in range(3):  # descartar cuadros viejos del búfer
            self._cap.read()
        ok, img = self._cap.read()
        if not ok:
            raise RuntimeError("La cámara no devolvió imagen")
        return img

    def cerrar(self) -> None:
        self._cap.release()


class CamaraArchivo(Camara):
    nombre = "archivo"

    def __init__(self, rutas: list[Path]):
        self._rutas = list(rutas)
        self._i = 0

    def capturar(self) -> np.ndarray:
        if self._i >= len(self._rutas):
            raise RuntimeError("No quedan archivos por leer")
        img = cv2.imread(str(self._rutas[self._i]), cv2.IMREAD_COLOR)
        self._i += 1
        if img is None:
            raise RuntimeError(f"No se pudo leer {self._rutas[self._i - 1]}")
        return img


def abrir(preferencia: str = "auto", **kw) -> Camara:
    if preferencia in ("auto", "picamera2"):
        try:
            return CamaraPicamera2(**kw)
        except Exception:
            if preferencia == "picamera2":
                raise
    return CamaraOpenCV(**kw)


@dataclass
class Metadatos:
    archivo: str
    tarjeta: str
    lado: str
    iluminacion: str
    camara: str
    ancho: int
    alto: int
    capturado_utc: str
    equipo: str
    responsable: str
    nota: str = ""


def nombre_archivo(tarjeta: str, lado: str, iluminacion: str, cuando: datetime) -> str:
    if not PATRON_TARJETA.match(tarjeta):
        raise ValueError("La tarjeta se nombra T seguido de 2 o 3 dígitos, por ejemplo T07")
    if lado not in ("A", "B"):
        raise ValueError("El lado es A (componentes) o B (soldadura)")
    return f"{tarjeta}_{lado}_il{iluminacion}_{cuando.strftime('%Y%m%dT%H%M%S')}.png"


def capturar(camara: Camara, carpeta: Path, tarjeta: str, lado: str, iluminacion: str,
             responsable: str, nota: str = "") -> Path:
    """Guarda la imagen sin pérdida (PNG), su JSON de metadatos y la añade al manifiesto."""
    carpeta = Path(carpeta)
    cuando = datetime.now(timezone.utc)
    destino = carpeta / tarjeta / nombre_archivo(tarjeta, lado, iluminacion, cuando)
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        raise FileExistsError(destino)
    img = camara.capturar()
    if not cv2.imwrite(str(destino), img):
        raise RuntimeError(f"No se pudo escribir {destino}")
    meta = Metadatos(destino.name, tarjeta, lado, iluminacion, camara.nombre, img.shape[1], img.shape[0],
                     cuando.isoformat(timespec="seconds"), platform.node(), responsable, nota)
    destino.with_suffix(".json").write_text(json.dumps(asdict(meta), ensure_ascii=False, indent=2), encoding="utf-8")
    manifiesto.agregar(carpeta, destino)
    return destino
