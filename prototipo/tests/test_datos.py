import json

import numpy as np
import pytest

from inspeccion_tht import manifiesto, particion
from inspeccion_tht.anotaciones import Anotacion, comparar, consenso
from inspeccion_tht.captura import CamaraArchivo, capturar, nombre_archivo
from inspeccion_tht.registro import Registro

import cv2
from datetime import datetime


def test_manifiesto_detecta_cambios(tmp_path):
    (tmp_path / "T01").mkdir()
    a = tmp_path / "T01" / "a.png"
    cv2.imwrite(str(a), np.zeros((10, 10, 3), np.uint8))
    manifiesto.generar(tmp_path)
    assert manifiesto.verificar(tmp_path) == []
    cv2.imwrite(str(a), np.full((10, 10, 3), 7, np.uint8))
    cv2.imwrite(str(tmp_path / "T01" / "b.png"), np.zeros((5, 5, 3), np.uint8))
    problemas = {(d.archivo, d.problema) for d in manifiesto.verificar(tmp_path)}
    assert problemas == {("T01/a.png", "modificado"), ("T01/b.png", "no_registrado")}


def test_nombre_archivo_valida():
    t = datetime(2026, 10, 26, 10, 15, 0)
    assert nombre_archivo("T07", "A", "1", t) == "T07_A_il1_20261026T101500.png"
    with pytest.raises(ValueError):
        nombre_archivo("tarjeta7", "A", "1", t)
    with pytest.raises(ValueError):
        nombre_archivo("T07", "C", "1", t)


def test_capturar_desde_archivo(tmp_path):
    origen = tmp_path / "origen.png"
    cv2.imwrite(str(origen), np.full((20, 30, 3), 100, np.uint8))
    destino = capturar(CamaraArchivo([origen]), tmp_path / "crudos", "T01", "B", "1", "prueba")
    meta = json.loads(destino.with_suffix(".json").read_text())
    assert meta["ancho"] == 30 and meta["alto"] == 20 and meta["camara"] == "archivo"
    assert manifiesto.verificar(tmp_path / "crudos") == []


def test_particion_por_tarjeta_determinista_y_congelada(tmp_path):
    tarjetas = [f"T{i:02d}" for i in range(1, 31)]
    a = particion.particionar(tarjetas, semilla=5)
    assert a == particion.particionar(tarjetas, semilla=5)
    conteo = {c: sum(v == c for v in a.values()) for c in particion.CONJUNTOS}
    assert conteo == {"entrenamiento": 18, "validacion": 6, "prueba": 6}
    ruta = tmp_path / "particion.json"
    particion.guardar(a, ruta, semilla=5)
    assert particion.cargar(ruta) == a
    datos = json.loads(ruta.read_text())
    datos["conjuntos"]["prueba"][0], datos["conjuntos"]["entrenamiento"][0] = (
        datos["conjuntos"]["entrenamiento"][0], datos["conjuntos"]["prueba"][0])
    ruta.write_text(json.dumps(datos))
    with pytest.raises(ValueError):
        particion.cargar(ruta)


def test_particion_requiere_tres_tarjetas():
    with pytest.raises(ValueError):
        particion.particionar(["T01", "T02"])


def test_anotaciones_comparacion_y_consenso(tmp_path):
    a = Anotacion("T01_B.png", "T01", "d1", "fortino")
    b = Anotacion("T01_B.png", "T01", "d1", "israel")
    for uid, ca, cb in [("U1", "aceptable", "aceptable"), ("U2", "puente", "puente"), ("U3", "fria", "insuficiente")]:
        a.poner(uid, ca)
        b.poner(uid, cb)
    a.guardar(tmp_path)
    assert Anotacion.cargar(a.ruta(tmp_path)).etiquetas == a.etiquetas
    comp = comparar([a], [b])
    assert comp.uniones == 3 and comp.acuerdos == 2
    assert comp.discrepancias == [("T01_B.png", "U3", "fria", "insuficiente")]
    with pytest.raises(ValueError):
        consenso(a, b, {})
    final = consenso(a, b, {"U3": "fria"})
    assert final.etiquetas == {"U1": "aceptable", "U2": "puente", "U3": "fria"}
    with pytest.raises(ValueError):
        a.poner("U9", "rara")


def test_registro_sqlite(tmp_path):
    r = Registro(tmp_path / "decisiones.sqlite")
    r.anotar("fortino", "T01_B.png", "T01", "U1", "puente", 0.9, "puente", 2.5)
    r.anotar("fortino", "T01_B.png", "T01", "U2", "exceso", 0.6, "aceptable", 1.0)
    filas = r.todas()
    assert [f["decision"] for f in filas] == ["puente", "aceptable"]
    salida = r.exportar_csv(tmp_path / "d.csv")
    assert salida.read_text().count("\n") == 3
