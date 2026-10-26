"""Métricas e incertidumbre (protocolo, sección 6.6).

- Sensibilidad y tasa de falsas alarmas sobre la tarea binaria defecto / aceptable.
- Intervalo de Wilson para proporciones.
- Bootstrap agrupado por tarjeta: las uniones de una misma tarjeta no son independientes.
- Prueba exacta de McNemar para comparar inspección asistida y no asistida (EXP-005).
- Kappa de Cohen para el acuerdo entre etiquetadores.
"""

import math
import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence

from .clases import CLASES, es_defecto

Z95 = 1.959963984540054


def wilson(exitos: int, n: int, z: float = Z95) -> tuple[float, float]:
    """Intervalo de confianza de Wilson para una proporción exitos/n."""
    if n <= 0:
        raise ValueError("n debe ser positivo")
    if not 0 <= exitos <= n:
        raise ValueError("exitos debe estar entre 0 y n")
    p = exitos / n
    z2 = z * z
    centro = (p + z2 / (2 * n)) / (1 + z2 / n)
    semi = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    return max(0.0, centro - semi), min(1.0, centro + semi)


@dataclass(frozen=True)
class Caso:
    """Una unión evaluada: verdad de referencia y lo que dijo el sistema o la persona."""
    tarjeta: str
    union: str
    verdad: str
    prediccion: str


@dataclass
class Binaria:
    vp: int = 0  # defecto marcado como defecto
    fn: int = 0  # defecto que se escapó
    fp: int = 0  # unión buena marcada como defecto (falsa alarma)
    vn: int = 0

    @property
    def sensibilidad(self) -> float:
        return self.vp / (self.vp + self.fn) if (self.vp + self.fn) else float("nan")

    @property
    def falsas_alarmas(self) -> float:
        return self.fp / (self.fp + self.vn) if (self.fp + self.vn) else float("nan")

    @property
    def precision(self) -> float:
        return self.vp / (self.vp + self.fp) if (self.vp + self.fp) else float("nan")


def binaria(casos: Iterable[Caso]) -> Binaria:
    b = Binaria()
    for c in casos:
        d_real, d_pred = es_defecto(c.verdad), es_defecto(c.prediccion)
        if d_real and d_pred:
            b.vp += 1
        elif d_real:
            b.fn += 1
        elif d_pred:
            b.fp += 1
        else:
            b.vn += 1
    return b


def matriz_confusion(casos: Iterable[Caso], clases: Sequence[str] = CLASES) -> list[list[int]]:
    """Filas = verdad, columnas = predicción, en el orden de `clases`."""
    idx = {c: i for i, c in enumerate(clases)}
    m = [[0] * len(clases) for _ in clases]
    for c in casos:
        m[idx[c.verdad]][idx[c.prediccion]] += 1
    return m


def por_clase(casos: Sequence[Caso], clases: Sequence[str] = CLASES) -> dict[str, dict[str, float]]:
    """Sensibilidad (recall) y precisión de cada clase, con su n."""
    res = {}
    for k in clases:
        vp = sum(1 for c in casos if c.verdad == k and c.prediccion == k)
        n_real = sum(1 for c in casos if c.verdad == k)
        n_pred = sum(1 for c in casos if c.prediccion == k)
        res[k] = {
            "n": n_real,
            "sensibilidad": vp / n_real if n_real else float("nan"),
            "precision": vp / n_pred if n_pred else float("nan"),
        }
    return res


def bootstrap_por_tarjeta(
    casos: Sequence[Caso],
    estadistico: Callable[[Sequence[Caso]], float],
    repeticiones: int = 2000,
    semilla: int = 20261030,
    nivel: float = 0.95,
) -> tuple[float, float]:
    """IC por percentiles remuestreando tarjetas completas con reemplazo."""
    grupos: dict[str, list[Caso]] = defaultdict(list)
    for c in casos:
        grupos[c.tarjeta].append(c)
    tarjetas = sorted(grupos)
    if len(tarjetas) < 2:
        raise ValueError("Se necesitan al menos dos tarjetas para el bootstrap por tarjeta")
    rng = random.Random(semilla)
    valores = []
    for _ in range(repeticiones):
        muestra = [c for t in rng.choices(tarjetas, k=len(tarjetas)) for c in grupos[t]]
        v = estadistico(muestra)
        if not math.isnan(v):
            valores.append(v)
    valores.sort()
    a = (1 - nivel) / 2
    return _percentil(valores, a), _percentil(valores, 1 - a)


def _percentil(ordenados: list[float], q: float) -> float:
    if not ordenados:
        return float("nan")
    pos = q * (len(ordenados) - 1)
    i = int(math.floor(pos))
    j = min(i + 1, len(ordenados) - 1)
    return ordenados[i] + (ordenados[j] - ordenados[i]) * (pos - i)


def mcnemar_exacto(solo_a: int, solo_b: int) -> float:
    """Valor p bilateral exacto. solo_a: aciertos de A que B falló; solo_b: al revés."""
    n = solo_a + solo_b
    if n == 0:
        return 1.0
    k = min(solo_a, solo_b)
    cola = sum(math.comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, 2 * cola)


def kappa_cohen(a: Sequence[str], b: Sequence[str]) -> float:
    """Acuerdo entre dos etiquetadores corregido por azar."""
    if len(a) != len(b) or not a:
        raise ValueError("Las listas deben tener la misma longitud y no estar vacías")
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def resumen(casos: Sequence[Caso], repeticiones: int = 2000, semilla: int = 20261030) -> dict:
    """Todo lo que pide la tabla de resultados del protocolo para M1 y M2."""
    b = binaria(casos)
    out = {
        "n_uniones": len(casos),
        "n_tarjetas": len({c.tarjeta for c in casos}),
        "n_defectos": b.vp + b.fn,
        "n_aceptables": b.fp + b.vn,
        "vp": b.vp, "fn": b.fn, "fp": b.fp, "vn": b.vn,
        "sensibilidad": b.sensibilidad,
        "falsas_alarmas": b.falsas_alarmas,
        "precision": b.precision,
    }
    if b.vp + b.fn:
        out["sensibilidad_wilson95"] = wilson(b.vp, b.vp + b.fn)
    if b.fp + b.vn:
        out["falsas_alarmas_wilson95"] = wilson(b.fp, b.fp + b.vn)
    if out["n_tarjetas"] >= 2:
        out["sensibilidad_bootstrap95"] = bootstrap_por_tarjeta(
            casos, lambda cs: binaria(cs).sensibilidad, repeticiones, semilla)
        out["falsas_alarmas_bootstrap95"] = bootstrap_por_tarjeta(
            casos, lambda cs: binaria(cs).falsas_alarmas, repeticiones, semilla)
    return out
