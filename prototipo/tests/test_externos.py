import json

import cv2
import numpy as np
import pytest

from inspeccion_tht import externos, sintetico
from inspeccion_tht.cli import main as tht

ORIG = {"good": "aceptable", "insuff": "insuficiente", "bridge": "puente", "no": "sin_soldar", "excess": "exceso"}


@pytest.fixture
def carpeta_falsa(tmp_path):
    """Imita la estructura de PCBSPDefect b_dip con celdas sintéticas (no son datos reales)."""
    rng = np.random.default_rng(0)
    for conjunto, parte in externos.PARTES_OFICIALES.items():
        for original, nuestra in ORIG.items():
            d = tmp_path / parte / original
            d.mkdir(parents=True)
            for t in range(1, 7):
                for luz in ("light1", "light2", "light3"):
                    nombre = f"b_{luz}_b{1000 + t}_dip_{original}_b{list(externos.PARTES_OFICIALES).index(conjunto)}_a0_y0_x0.jpg"
                    cv2.imwrite(str(d / nombre), cv2.resize(sintetico.celda(nuestra, rng), (280, 280)))
            (d / "ignorar_mascara.png").write_bytes(b"")
    return tmp_path


def test_lee_y_traduce_clases(carpeta_falsa):
    ms = externos.leer_pcbspdefect(carpeta_falsa)
    assert len(ms) == 3 * 5 * 6 * 3
    assert {m.clase for m in ms} == set(ORIG.values())
    assert {m.conjunto_oficial for m in ms} == {"entrenamiento", "validacion", "prueba"}
    m = ms[0]
    assert m.union.startswith(m.tarjeta) and m.luz.startswith("light")


def test_particion_por_tarjeta_no_mezcla_tarjetas(carpeta_falsa):
    ms = externos.leer_pcbspdefect(carpeta_falsa)
    conj = externos.asignar(ms, "tarjeta")
    por_tarjeta = {}
    for m, c in zip(ms, conj):
        por_tarjeta.setdefault(m.tarjeta, set()).add(c)
    assert all(len(v) == 1 for v in por_tarjeta.values())
    with pytest.raises(ValueError):
        externos.asignar(ms, "otra")


def test_comando_evalua_linea_base(carpeta_falsa, tmp_path):
    salida = tmp_path / "r.json"
    tht(["externo", "evaluar", "--ruta", str(carpeta_falsa), "--sin-red", "--salida", str(salida)])
    r = json.loads(salida.read_text())
    assert set(r["particiones"]) == {"oficial", "tarjeta"}
    assert r["particiones"]["oficial"]["conjuntos"]["prueba"]["imagenes"] == 90
    assert 0 <= r["particiones"]["oficial"]["linea_base"]["resumen"]["sensibilidad"] <= 1


def test_sin_imagenes_falla_claro(tmp_path):
    with pytest.raises(FileNotFoundError):
        externos.leer_pcbspdefect(tmp_path)
