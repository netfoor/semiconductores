"""Etiquetas por unión, hechas por cada etiquetador por separado (protocolo, sección 6.3)."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .clases import validar
from .metricas import kappa_cohen


@dataclass
class Anotacion:
    imagen: str
    tarjeta: str
    diseno: str
    etiquetador: str
    etiquetas: dict[str, str] = field(default_factory=dict)  # union_id -> clase
    actualizado_utc: str = ""

    def poner(self, union_id: str, clase: str) -> None:
        self.etiquetas[union_id] = validar(clase)

    def ruta(self, carpeta: Path) -> Path:
        return Path(carpeta) / f"{Path(self.imagen).stem}.{self.etiquetador}.json"

    def guardar(self, carpeta: Path) -> Path:
        self.actualizado_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
        r = self.ruta(carpeta)
        r.parent.mkdir(parents=True, exist_ok=True)
        r.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")
        return r

    @classmethod
    def cargar(cls, ruta: Path) -> "Anotacion":
        return cls(**json.loads(Path(ruta).read_text(encoding="utf-8")))


def todas(carpeta: Path) -> list[Anotacion]:
    return [Anotacion.cargar(p) for p in sorted(Path(carpeta).glob("*.json"))]


@dataclass
class Comparacion:
    uniones: int
    acuerdos: int
    kappa: float
    discrepancias: list[tuple[str, str, str, str]]  # (imagen, union, clase_a, clase_b)


def comparar(a: list[Anotacion], b: list[Anotacion]) -> Comparacion:
    """Acuerdo entre dos etiquetadores sobre las uniones que ambos etiquetaron."""
    por_imagen_b = {x.imagen: x for x in b}
    xa, xb, disc = [], [], []
    for an in a:
        otro = por_imagen_b.get(an.imagen)
        if not otro:
            continue
        for uid, ca in sorted(an.etiquetas.items()):
            if uid in otro.etiquetas:
                cb = otro.etiquetas[uid]
                xa.append(ca)
                xb.append(cb)
                if ca != cb:
                    disc.append((an.imagen, uid, ca, cb))
    if not xa:
        raise ValueError("No hay uniones etiquetadas por ambos")
    return Comparacion(len(xa), len(xa) - len(disc), kappa_cohen(xa, xb), disc)


def consenso(a: Anotacion, b: Anotacion, resueltas: dict[str, str], etiquetador: str = "consenso") -> Anotacion:
    """Etiquetas finales: donde coinciden se toma su etiqueta; donde no, la resuelta por ambos."""
    final = Anotacion(a.imagen, a.tarjeta, a.diseno, etiquetador)
    for uid in sorted(set(a.etiquetas) & set(b.etiquetas)):
        if a.etiquetas[uid] == b.etiquetas[uid]:
            final.poner(uid, a.etiquetas[uid])
        elif uid in resueltas:
            final.poner(uid, resueltas[uid])
        else:
            raise ValueError(f"Falta resolver la discrepancia en {a.imagen} {uid}")
    return final
