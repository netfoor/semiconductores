"""Partición por tarjeta y congelamiento del conjunto de prueba (protocolo, sección 6.3).

Se parte por tarjeta, no por imagen ni por unión, para que ninguna tarjeta del
conjunto de prueba se haya visto al entrenar. El conjunto de prueba se congela con
una huella; si alguien lo cambia después, la verificación falla.
"""

import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

CONJUNTOS = ("entrenamiento", "validacion", "prueba")


def particionar(
    tarjetas: list[str],
    proporciones: tuple[float, float, float] = (0.6, 0.2, 0.2),
    semilla: int = 20261026,
) -> dict[str, str]:
    """Asigna cada tarjeta a un conjunto. Determinista para una misma semilla."""
    unicas = sorted(set(tarjetas))
    if len(unicas) < 3:
        raise ValueError("Se necesitan al menos tres tarjetas para formar los tres conjuntos")
    if abs(sum(proporciones) - 1) > 1e-9 or min(proporciones) <= 0:
        raise ValueError("Las proporciones deben ser positivas y sumar 1")
    rng = random.Random(semilla)
    orden = unicas[:]
    rng.shuffle(orden)
    n = len(orden)
    n_prueba = max(1, round(n * proporciones[2]))
    n_val = max(1, round(n * proporciones[1]))
    n_ent = n - n_prueba - n_val
    if n_ent < 1:
        raise ValueError("No quedan tarjetas para entrenamiento con estas proporciones")
    asignacion = {}
    for i, t in enumerate(orden):
        asignacion[t] = "entrenamiento" if i < n_ent else ("validacion" if i < n_ent + n_val else "prueba")
    return asignacion


def huella_prueba(asignacion: dict[str, str]) -> str:
    prueba = sorted(t for t, c in asignacion.items() if c == "prueba")
    return hashlib.sha256("\n".join(prueba).encode()).hexdigest()


def guardar(asignacion: dict[str, str], ruta: Path, semilla: int, nota: str = "") -> dict:
    datos = {
        "creado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "semilla": semilla,
        "nota": nota,
        "conjuntos": {c: sorted(t for t, v in asignacion.items() if v == c) for c in CONJUNTOS},
        "huella_prueba_sha256": huella_prueba(asignacion),
    }
    Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    return datos


def cargar(ruta: Path) -> dict[str, str]:
    datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    asignacion = {t: c for c, ts in datos["conjuntos"].items() for t in ts}
    if huella_prueba(asignacion) != datos["huella_prueba_sha256"]:
        raise ValueError("El conjunto de prueba no coincide con su huella: se modificó después de congelarlo")
    return asignacion
