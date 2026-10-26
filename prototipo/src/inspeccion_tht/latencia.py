"""Medición de latencia y comparación local / nube (EXP-003)."""

import json
import os
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


def medir(funcion: Callable[[], object], repeticiones: int = 30, calentamiento: int = 3) -> dict:
    """Mediana, percentil 95, media y extremos en segundos."""
    if repeticiones < 1:
        raise ValueError("repeticiones debe ser al menos 1")
    for _ in range(calentamiento):
        funcion()
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - t0)
    ordenados = sorted(tiempos)
    p95 = ordenados[min(len(ordenados) - 1, max(0, int(round(0.95 * len(ordenados))) - 1))]
    return {
        "n": len(tiempos),
        "mediana_s": statistics.median(tiempos),
        "p95_s": p95,
        "media_s": statistics.fmean(tiempos),
        "min_s": ordenados[0],
        "max_s": ordenados[-1],
        "tiempos_s": tiempos,
    }


def subida_estimada(bytes_imagen: int, mbps: float) -> float:
    """Segundos para subir una imagen (sin contar ida y vuelta de red ni inferencia remota)."""
    if mbps <= 0:
        raise ValueError("mbps debe ser positivo")
    return bytes_imagen * 8 / (mbps * 1e6)


def equipo() -> dict:
    return {
        "maquina": platform.machine(),
        "sistema": platform.platform(),
        "python": platform.python_version(),
        "nucleos": os.cpu_count(),
        "nodo": platform.node(),
    }


def guardar(resultado: dict, ruta: Path, nota: str = "") -> Path:
    datos = {"fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "equipo": equipo(), "nota": nota, **resultado}
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    return Path(ruta)
