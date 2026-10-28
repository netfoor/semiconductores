"""Captura de imágenes con nombre, metadatos y huella (protocolo de captura, DS-01).

Cámaras soportadas, en orden de preferencia:
- Picamera2 (Raspberry Pi con módulo de cámara), si está instalada en el sistema;
- cualquier cámara USB vía OpenCV;
- una carpeta de archivos (para pruebas y para repetir capturas ya hechas);
- una foto en memoria subida desde un celular (página /capturar de la interfaz local).
"""

import json
import platform
import re
import struct
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np

from . import manifiesto

PATRON_TARJETA = re.compile(r"^T\d{2,3}$")
PATRON_ILUMINACION = re.compile(r"^[0-9A-Za-z]{1,10}$")


class Camara:
    nombre = "generica"

    def capturar(self) -> np.ndarray:
        raise NotImplementedError

    def cerrar(self) -> None:
        pass

    def original(self) -> tuple[bytes, str] | None:
        """Bytes del archivo tal como lo generó la cámara y su extensión, si la cámara los entrega."""
        return None

    def extra(self) -> dict:
        """Metadatos propios de esta cámara (ver los campos opcionales de Metadatos)."""
        return {}


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


class FormatoNoSoportado(ValueError):
    pass


MENSAJE_HEIC = ("La foto está en formato HEIC (iPhone), que OpenCV no lee. En el iPhone, vaya a Ajustes > Cámara > "
                "Formatos y elija «Más compatible»; luego tome la foto otra vez desde esta página.")


def formato(datos: bytes) -> str:
    """Formato de imagen según sus primeros bytes: jpeg, png, heic, webp o desconocido."""
    if datos[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if datos[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if datos[4:8] == b"ftyp" and datos[8:12] in {b"heic", b"heix", b"hevc", b"heim", b"heis", b"mif1", b"msf1"}:
        return "heic"
    if datos[:4] == b"RIFF" and datos[8:12] == b"WEBP":
        return "webp"
    return "desconocido"


def leer_exif(datos: bytes) -> dict:
    """Marca, modelo, orientación y presencia de un bloque GPS en el EXIF de un JPEG.

    Lee solo la IFD0, con la biblioteca estándar, para no depender de Pillow.
    Si el EXIF falta o está dañado devuelve lo que haya podido leer.
    """
    i = 2
    while i + 4 <= len(datos) and datos[i] == 0xFF:
        marcador, largo = datos[i + 1], int.from_bytes(datos[i + 2:i + 4], "big")
        if marcador == 0xE1 and datos[i + 4:i + 10] == b"Exif\x00\x00":
            return _ifd0(datos[i + 10:i + 2 + largo])
        if marcador == 0xDA:  # empieza la imagen comprimida: ya no hay EXIF
            break
        i += 2 + largo
    return {}


def _ifd0(t: bytes) -> dict:
    out: dict = {}
    try:
        orden = {b"II": "<", b"MM": ">"}[t[:2]]
        inicio = struct.unpack(orden + "I", t[4:8])[0]
        for k in range(struct.unpack(orden + "H", t[inicio:inicio + 2])[0]):
            e = inicio + 2 + 12 * k
            etiqueta, tipo, cuenta = struct.unpack(orden + "HHI", t[e:e + 8])
            valor = t[e + 8:e + 12]
            if etiqueta in (0x010F, 0x0110) and tipo == 2:  # marca y modelo (ASCII)
                if cuenta > 4:
                    desde = struct.unpack(orden + "I", valor)[0]
                    valor = t[desde:desde + cuenta]
                texto = valor[:cuenta].split(b"\x00")[0].decode("ascii", "replace").strip()
                out["marca" if etiqueta == 0x010F else "modelo"] = texto
            elif etiqueta == 0x0112 and tipo == 3:
                out["orientacion"] = struct.unpack(orden + "H", valor[:2])[0]
            elif etiqueta == 0x8825:
                out["gps"] = True
    except (KeyError, IndexError, struct.error):
        pass
    return out


class CamaraMemoria(Camara):
    """Una foto JPEG ya tomada (por ejemplo, subida desde un celular).

    La imagen se decodifica con cv2.imdecode, que aplica la orientación EXIF; los bytes
    originales se conservan para guardarlos junto al PNG con su propia huella.
    """
    nombre = "celular"

    def __init__(self, datos: bytes, user_agent: str = ""):
        tipo = formato(datos)
        if tipo == "heic":
            raise FormatoNoSoportado(MENSAJE_HEIC)
        if tipo != "jpeg":
            raise FormatoNoSoportado(f"Solo se aceptan fotos JPEG tal como las entrega la cámara (se recibió: {tipo}).")
        self._img = cv2.imdecode(np.frombuffer(datos, np.uint8), cv2.IMREAD_COLOR)
        if self._img is None:
            raise FormatoNoSoportado("No se pudo leer la foto: el archivo está dañado o incompleto. Tómela otra vez.")
        self._datos = datos
        self._exif = leer_exif(datos)
        self._user_agent = user_agent

    def capturar(self) -> np.ndarray:
        return self._img

    def original(self) -> tuple[bytes, str]:
        return self._datos, ".jpg"

    def extra(self) -> dict:
        e = self._exif
        modelo = e.get("modelo", "")
        if e.get("marca") and not modelo.lower().startswith(e["marca"].lower()):
            modelo = f"{e['marca']} {modelo}".strip()
        return {"modelo_camara": modelo, "orientacion_exif": e.get("orientacion"),
                "tiene_gps": bool(e.get("gps")), "user_agent": self._user_agent}


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
    # Opcionales: solo se escriben si tienen valor (las capturas con Picamera2 o USB no cambian).
    original: str = ""              # archivo tal como lo generó la cámara (JPEG del celular)
    original_sha256: str = ""
    modelo_camara: str = ""         # del EXIF del original
    orientacion_exif: int | None = None
    tiene_gps: bool | None = None   # el EXIF del original trae un bloque de ubicación
    user_agent: str = ""
    diseno: str = ""                # diseño de tarjeta, si se conoce al capturar

    def como_dict(self) -> dict:
        nombres = [f.name for f in fields(self)]
        opcionales = set(nombres[nombres.index("nota") + 1:])
        return {k: v for k, v in asdict(self).items() if k not in opcionales or v not in ("", None)}


def nombre_archivo(tarjeta: str, lado: str, iluminacion: str, cuando: datetime) -> str:
    if not PATRON_TARJETA.match(tarjeta):
        raise ValueError("La tarjeta se nombra T seguido de 2 o 3 dígitos, por ejemplo T07")
    if lado not in ("A", "B"):
        raise ValueError("El lado es A (componentes) o B (soldadura)")
    if not PATRON_ILUMINACION.match(iluminacion):
        raise ValueError("La iluminación se indica con letras o números, sin espacios, por ejemplo 1")
    return f"{tarjeta}_{lado}_il{iluminacion}_{cuando.strftime('%Y%m%dT%H%M%S')}.png"


def capturar(camara: Camara, carpeta: Path, tarjeta: str, lado: str, iluminacion: str,
             responsable: str, nota: str = "", diseno: str = "") -> Path:
    """Guarda la imagen sin pérdida (PNG), su JSON de metadatos y la añade al manifiesto.

    Si la cámara entrega el archivo original (por ejemplo, el JPEG de un celular), se guarda
    sin modificar junto al PNG, con el mismo nombre y su extensión, y también entra al manifiesto:
    su huella prueba lo que generó la cámara; la del PNG, la copia que se procesa.
    """
    carpeta = Path(carpeta)
    cuando = datetime.now(timezone.utc)
    destino = carpeta / tarjeta / nombre_archivo(tarjeta, lado, iluminacion, cuando)
    original = camara.original()
    copia = destino.with_suffix(original[1]) if original else None
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists() or (copia and copia.exists()):
        raise FileExistsError(destino)
    img = camara.capturar()
    if copia:
        with open(copia, "xb") as f:  # "x": nunca sobrescribe
            f.write(original[0])
    if not cv2.imwrite(str(destino), img):
        raise RuntimeError(f"No se pudo escribir {destino}")
    meta = Metadatos(destino.name, tarjeta, lado, iluminacion, camara.nombre, img.shape[1], img.shape[0],
                     cuando.isoformat(timespec="seconds"), platform.node(), responsable, nota,
                     diseno=diseno, **camara.extra())
    if copia:
        meta.original, meta.original_sha256 = copia.name, manifiesto.sha256_archivo(copia)
    destino.with_suffix(".json").write_text(json.dumps(meta.como_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    if copia:
        manifiesto.agregar(carpeta, copia)
    manifiesto.agregar(carpeta, destino)
    return destino
