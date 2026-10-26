"""Organización de la carpeta de datos y construcción de ejemplos para entrenar y evaluar.

datos/
  crudos/T01/T01_B_il1_<fecha>.png  (+ .json de metadatos)   imágenes sin modificar
  crudos/MANIFIESTO.csv                                        huellas SHA-256
  plantillas/<diseno>.json y <diseno>.png                      uniones e imagen de referencia
  anotaciones/<imagen>.<etiquetador>.json                      etiquetas por unión
  particion.json                                               tarjetas por conjunto (prueba congelada)
  modelos/                                                     modelos entrenados
  resultados/                                                  salidas de los experimentos
  decisiones.sqlite                                            decisiones del operador
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .anotaciones import todas
from .flujo import leer
from .linea_base import caracteristicas
from .plantilla import Plantilla, al_marco_de_referencia, alinear, recortes


@dataclass(frozen=True)
class Carpetas:
    raiz: Path

    @property
    def crudos(self) -> Path: return self.raiz / "crudos"
    @property
    def plantillas(self) -> Path: return self.raiz / "plantillas"
    @property
    def anotaciones(self) -> Path: return self.raiz / "anotaciones"
    @property
    def modelos(self) -> Path: return self.raiz / "modelos"
    @property
    def resultados(self) -> Path: return self.raiz / "resultados"
    @property
    def particion(self) -> Path: return self.raiz / "particion.json"
    @property
    def decisiones(self) -> Path: return self.raiz / "decisiones.sqlite"

    def crear(self) -> "Carpetas":
        for p in (self.crudos, self.plantillas, self.anotaciones, self.modelos, self.resultados):
            p.mkdir(parents=True, exist_ok=True)
        return self

    def plantilla(self, diseno: str) -> tuple[Plantilla, np.ndarray]:
        p = Plantilla.cargar(self.plantillas / f"{diseno}.json")
        return p, leer(self.plantillas / p.referencia)

    def imagen(self, nombre: str) -> Path:
        tarjeta = nombre.split("_")[0]
        directa = self.crudos / tarjeta / nombre
        if directa.exists():
            return directa
        encontradas = list(self.crudos.rglob(nombre))
        if not encontradas:
            raise FileNotFoundError(nombre)
        return encontradas[0]

    def imagenes(self) -> list[Path]:
        return sorted(p for p in self.crudos.rglob("*.png"))


@dataclass
class Ejemplo:
    tarjeta: str
    imagen: str
    union_id: str
    clase: str
    x: np.ndarray


def ejemplos(c: Carpetas, etiquetador: str = "consenso") -> list[Ejemplo]:
    """Un ejemplo por unión etiquetada, con las características de su recorte alineado."""
    cache: dict[str, tuple[Plantilla, np.ndarray]] = {}
    out = []
    for an in todas(c.anotaciones):
        if an.etiquetador != etiquetador:
            continue
        if an.diseno not in cache:
            cache[an.diseno] = c.plantilla(an.diseno)
        plantilla, ref = cache[an.diseno]
        img = leer(c.imagen(an.imagen))
        alineada = al_marco_de_referencia(img, alinear(img, ref), plantilla)
        rec = recortes(alineada, plantilla)
        for uid, clase in sorted(an.etiquetas.items()):
            out.append(Ejemplo(an.tarjeta, an.imagen, uid, clase, caracteristicas(rec[uid])))
    return out
