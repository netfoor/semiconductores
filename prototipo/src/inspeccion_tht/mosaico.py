"""Tarjeta-mosaico para la demostración: fotos REALES de uniones, acomodadas como una tarjeta.

No hay un conjunto público con fotos de tarjetas through-hole completas y licencia abierta.
El mosaico acomoda en una cuadrícula fotos del conjunto de prueba oficial de PCBSPDefect
(CC BY 4.0, las mismas de la página Fotos reales), que la red de EXP-006 nunca vio al entrenar.
Se imprime en papel y se fotografía con el celular, de modo que la demostración pasa por todo
el flujo (captura, alineación, recortes, clasificación y decisión) con uniones reales.

No es una tarjeta física ni es DS-01: el texto del propio mosaico lo dice.
"""

import json
import random
import shutil
from pathlib import Path

import cv2
import numpy as np

from . import captura
from .clases import NOMBRES
from .datos import Carpetas
from .plantilla import Plantilla, Union

PUBLICO = Path(__file__).parent / "publico"
DISENO = "mosaico-01"
TARJETA = "T90"
FILAS, COLUMNAS, CELDA, HUECO, BORDE = 5, 6, 280, 36, 110
CLASES_MOSAICO = ("aceptable", "insuficiente", "puente", "sin_soldar", "exceso")
LEYENDA = "MOSAICO DE DEMOSTRACION: fotos reales de PCBSPDefect (Tsang et al., 2023), CC BY 4.0. No es una tarjeta fisica."


class _CamaraImagen(captura.Camara):
    nombre = "mosaico"

    def __init__(self, img: np.ndarray):
        self._img = img

    def capturar(self) -> np.ndarray:
        return self._img


def componer(semilla: int = 20261030) -> tuple[np.ndarray, Plantilla, dict[str, dict]]:
    """Imagen del mosaico, su plantilla y la clase real de cada unión (con su foto de origen)."""
    fotos = json.loads((PUBLICO / "fotos.json").read_text(encoding="utf-8"))["fotos"]
    por_clase: dict[str, list[dict]] = {}
    for f in fotos:
        por_clase.setdefault(f["clase"], []).append(f)
    n = FILAS * COLUMNAS // len(CLASES_MOSAICO)
    rng = random.Random(semilla)
    elegidas = [f for c in CLASES_MOSAICO for f in rng.sample(sorted(por_clase[c], key=lambda f: f["archivo"]), n)]
    rng.shuffle(elegidas)

    alto = 2 * BORDE + FILAS * CELDA + (FILAS - 1) * HUECO
    ancho = 2 * BORDE + COLUMNAS * CELDA + (COLUMNAS - 1) * HUECO
    img = np.full((alto, ancho, 3), (38, 66, 28), np.uint8)  # verde de máscara antisoldante
    # Marcas en tres esquinas y un círculo en la cuarta: dan puntos firmes y una orientación única.
    for x, y in ((24, 24), (ancho - 84, 24), (24, alto - 84)):
        cv2.rectangle(img, (x, y), (x + 60, y + 60), (245, 245, 245), -1)
    cv2.circle(img, (ancho - 54, alto - 54), 30, (245, 245, 245), -1)
    caja = int(round(CELDA / 1.3))  # con el margen de 15 % por lado, el recorte cubre la foto completa
    desfase = (CELDA - caja) // 2
    uniones, verdad = [], {}
    for k, f in enumerate(elegidas):
        i, j = divmod(k, COLUMNAS)
        x, y = BORDE + j * (CELDA + HUECO), BORDE + i * (CELDA + HUECO)
        foto = cv2.imread(str(PUBLICO / "fotos" / f["archivo"]), cv2.IMREAD_COLOR)
        img[y:y + CELDA, x:x + CELDA] = cv2.resize(foto, (CELDA, CELDA), interpolation=cv2.INTER_AREA)
        uid = f"{chr(65 + i)}{j + 1}"
        cv2.putText(img, uid, (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (230, 230, 230), 2, cv2.LINE_AA)
        uniones.append(Union(uid, x + desfase, y + desfase, caja, caja))
        verdad[uid] = {"clase": f["clase"], "foto": f["archivo"], "original": f["original"]}
    cv2.putText(img, LEYENDA, (BORDE, alto - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (245, 245, 245), 2, cv2.LINE_AA)
    return img, Plantilla(DISENO, f"{DISENO}.png", ancho, alto, uniones), verdad


def crear(salida: Path, semilla: int = 20261030) -> Carpetas:
    """Carpeta de datos lista para `tht servir --modelo red`: diseño, una captura, modelo y respuestas."""
    salida = Path(salida)
    if salida.exists() and any(salida.iterdir()):
        raise FileExistsError(f"{salida} ya existe y no está vacía; bórrela para regenerarla.")
    c = Carpetas(salida).crear()
    img, plantilla, verdad = componer(semilla)
    cv2.imwrite(str(c.plantillas / plantilla.referencia), img)
    plantilla.guardar(c.plantillas / f"{DISENO}.json")
    captura.capturar(_CamaraImagen(img), c.crudos, TARJETA, "B", "1", "tht mosaico",
                     "Mosaico digital (sin imprimir) de fotos públicas de PCBSPDefect", DISENO)
    for ext in (".onnx", ".json"):
        shutil.copyfile(PUBLICO / f"red_pcbspdefect{ext}", c.modelos / f"red{ext}")
    cv2.imwrite(str(c.raiz / "mosaico-imprimir.png"), img)
    (c.raiz / "verdad_mosaico.json").write_text(json.dumps(verdad, ensure_ascii=False, indent=2), encoding="utf-8")
    fotos = json.loads((PUBLICO / "fotos.json").read_text(encoding="utf-8"))
    respuestas = "\n".join(f"  {uid}: {NOMBRES[v['clase']]}" for uid, v in verdad.items())
    (c.raiz / "LEEME_MOSAICO.txt").write_text(f"""Tarjeta-mosaico de demostración, generada con `tht mosaico` (semilla {semilla}).

Qué es: {FILAS * COLUMNAS} fotos REALES de uniones through-hole del conjunto de prueba oficial de PCBSPDefect,
acomodadas en una cuadrícula como si fueran una tarjeta. No es una tarjeta física ni es parte de DS-01.
La red (modelos/red.onnx) es la de EXP-006, entrenada con otras fotos del mismo conjunto: no vio estas.

Uso en la mesa:
  1. Imprima mosaico-imprimir.png en color, en hoja carta horizontal, «ajustar a la página».
  2. make mesa DATOS={salida} MODELO=red
  3. Fotografíe la hoja con el celular desde /capturar (tarjeta {TARJETA}, diseño {DISENO}) y abra la inspección.

Fuente: {fotos['cita']}
Conjunto: {fotos['url']} (licencia {fotos['licencia']}). Fotos sin modificar salvo su acomodo en la cuadrícula.

Clase real de cada unión (para comparar con lo que marque el sistema):
{respuestas}
""", encoding="utf-8")
    return c
