"""Datos públicos externos para EXP-006 (nunca se mezclan con DS-01).

PCBSPDefect (Tsang et al., 2023; Zenodo 23307359; CC BY 4.0): fotos reales de uniones
de componentes DIP del lado de soldadura (subconjunto b_dip).
"""

import hashlib
import re
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

URL_PCBSPDEFECT = "https://zenodo.org/records/23307359/files/PCBSPDefect.zip?download=1"
SHA256_PCBSPDEFECT = "1e135795835f04deccb0bc5fc1dd071c7fc944963e2cd5b76c6deff399c0de98"
CITA_PCBSPDEFECT = ("Tsang, S.-H., Suo, Z., Chan, T. T.-L., Nguyen, H.-T., & Lun, D. P.-K. (2023). PCB soldering "
                    "defect inspection using multitask learning under low data regimes. Advanced Intelligent "
                    "Systems, 5, 2300364. https://doi.org/10.1002/aisy.202300364")

MAPA_CLASES = {"good": "aceptable", "insuff": "insuficiente", "bridge": "puente", "no": "sin_soldar", "excess": "exceso"}
PARTES_OFICIALES = {"entrenamiento": "train_20_percent/b_dip/train", "validacion": "val_test/b_dip/val",
                    "prueba": "val_test/b_dip/test"}
_PATRON = re.compile(r"^b_(light\d)_(b\d+)_dip_([a-z]+)_(b\d+)_a0_y0_x0\.jpg$")


@dataclass(frozen=True)
class Muestra:
    ruta: Path
    tarjeta: str
    union: str      # tarjeta + clase original + índice; las tres luces comparten unión
    luz: str
    clase: str      # en nuestras clases
    conjunto_oficial: str


def descargar(destino: Path) -> Path:
    """Descarga el ZIP de Zenodo y verifica su huella."""
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    zip_ = destino / "PCBSPDefect.zip"
    if not zip_.exists():
        urllib.request.urlretrieve(URL_PCBSPDEFECT, zip_)
    h = hashlib.sha256(zip_.read_bytes()).hexdigest()
    if h != SHA256_PCBSPDEFECT:
        raise ValueError(f"La huella del ZIP no coincide ({h}); el archivo cambió o se descargó incompleto")
    return zip_


def extraer(zip_: Path, destino: Path) -> Path:
    with zipfile.ZipFile(zip_) as z:
        for n in z.namelist():
            if "b_dip" in n and n.endswith(".jpg") and (n.startswith("train_20_percent") or n.startswith("val_test")):
                z.extract(n, destino)
    return Path(destino)


def leer_pcbspdefect(carpeta: Path) -> list[Muestra]:
    carpeta = Path(carpeta)
    out = []
    for conjunto, parte in PARTES_OFICIALES.items():
        for f in sorted((carpeta / parte).glob("*/*.jpg")):
            m = _PATRON.match(f.name)
            if not m or m.group(3) not in MAPA_CLASES:
                continue
            luz, tarjeta, original, indice = m.groups()
            out.append(Muestra(f, tarjeta, f"{tarjeta}_{original}_{indice}", luz, MAPA_CLASES[original], conjunto))
    if not out:
        raise FileNotFoundError(f"No se encontraron imágenes b_dip en {carpeta}")
    return out


def asignar(muestras: list[Muestra], particion: str, semilla: int = 20261026) -> list[str]:
    """Conjunto de cada muestra según la partición 'oficial' o 'tarjeta' (protocolo)."""
    if particion == "oficial":
        return [m.conjunto_oficial for m in muestras]
    if particion == "tarjeta":
        from .particion import particionar
        a = particionar([m.tarjeta for m in muestras], semilla=semilla)
        return [a[m.tarjeta] for m in muestras]
    raise ValueError("La partición es 'oficial' o 'tarjeta'")


def cargar_imagenes(muestras: list[Muestra]) -> list[np.ndarray]:
    imgs = []
    for m in muestras:
        im = cv2.imread(str(m.ruta), cv2.IMREAD_COLOR)
        if im is None:
            raise FileNotFoundError(m.ruta)
        imgs.append(im)
    return imgs
