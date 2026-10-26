"""Huellas SHA-256 de los datos crudos (integridad, REQ-DER-02).

Los archivos crudos no se modifican nunca. El manifiesto permite demostrar,
en cualquier momento, que siguen siendo los mismos que se capturaron.
"""

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

EXTENSIONES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".dng"}
CAMPOS = ("archivo", "sha256", "bytes", "modificado_utc")


def sha256_archivo(ruta: Path, bloque: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        while trozo := f.read(bloque):
            h.update(trozo)
    return h.hexdigest()


def archivos_de_datos(carpeta: Path) -> list[Path]:
    return sorted(p for p in carpeta.rglob("*") if p.is_file() and p.suffix.lower() in EXTENSIONES)


def generar(carpeta: Path, salida: Path | None = None) -> Path:
    """Escribe <carpeta>/MANIFIESTO.csv con la huella de cada imagen."""
    carpeta = Path(carpeta)
    salida = Path(salida) if salida else carpeta / "MANIFIESTO.csv"
    with open(salida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for p in archivos_de_datos(carpeta):
            st = p.stat()
            w.writerow({
                "archivo": p.relative_to(carpeta).as_posix(),
                "sha256": sha256_archivo(p),
                "bytes": st.st_size,
                "modificado_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds"),
            })
    return salida


def agregar(carpeta: Path, archivo: Path, manifiesto: Path | None = None) -> None:
    """Añade una sola entrada (se usa al capturar, para no recalcular todo)."""
    carpeta = Path(carpeta)
    manifiesto = Path(manifiesto) if manifiesto else carpeta / "MANIFIESTO.csv"
    nuevo = not manifiesto.exists()
    st = Path(archivo).stat()
    with open(manifiesto, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if nuevo:
            w.writeheader()
        w.writerow({
            "archivo": Path(archivo).relative_to(carpeta).as_posix(),
            "sha256": sha256_archivo(Path(archivo)),
            "bytes": st.st_size,
            "modificado_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc).isoformat(timespec="seconds"),
        })


@dataclass
class Discrepancia:
    archivo: str
    problema: str  # "falta", "modificado" o "no_registrado"


def verificar(carpeta: Path, manifiesto: Path | None = None) -> list[Discrepancia]:
    """Compara los archivos actuales contra el manifiesto. Lista vacía = íntegro."""
    carpeta = Path(carpeta)
    manifiesto = Path(manifiesto) if manifiesto else carpeta / "MANIFIESTO.csv"
    with open(manifiesto, newline="", encoding="utf-8") as f:
        esperado = {fila["archivo"]: fila["sha256"] for fila in csv.DictReader(f)}
    actuales = {p.relative_to(carpeta).as_posix(): p for p in archivos_de_datos(carpeta)}
    problemas = []
    for nombre, huella in esperado.items():
        if nombre not in actuales:
            problemas.append(Discrepancia(nombre, "falta"))
        elif sha256_archivo(actuales[nombre]) != huella:
            problemas.append(Discrepancia(nombre, "modificado"))
    for nombre in sorted(set(actuales) - set(esperado)):
        problemas.append(Discrepancia(nombre, "no_registrado"))
    return problemas
