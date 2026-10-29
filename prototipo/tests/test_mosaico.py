"""Tarjeta-mosaico, alineación por homografía y normalización de color."""

import json

import cv2
import numpy as np
import pytest

from inspeccion_tht import clasificador, mosaico
from inspeccion_tht.datos import Carpetas
from inspeccion_tht.flujo import inspeccionar, leer
from inspeccion_tht.plantilla import al_marco_de_referencia, alinear, normalizar_color


@pytest.fixture(scope="module")
def carpeta(tmp_path_factory):
    return mosaico.crear(tmp_path_factory.mktemp("mosaico") / "datos-mosaico")


def _foto_de_la_hoja(img, semilla, brillo=(1.0, 0.0)):
    """Como una foto de celular de la hoja impresa: escala, perspectiva, desenfoque, brillo y JPEG."""
    rng = np.random.default_rng(semilla)
    grande = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    h, w = grande.shape[:2]
    src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst = src + rng.uniform(-0.04, 0.04, src.shape).astype(np.float32) * min(w, h) + np.float32([300, 250])
    foto = cv2.warpPerspective(grande, cv2.getPerspectiveTransform(src, dst), (w + 600, h + 500),
                               borderValue=(200, 200, 205))
    foto = cv2.GaussianBlur(foto, (0, 0), 1.5)
    foto = np.clip(foto.astype(np.float32) * brillo[0] + brillo[1], 0, 255).astype(np.uint8)
    return cv2.imdecode(cv2.imencode(".jpg", foto, [cv2.IMWRITE_JPEG_QUALITY, 85])[1], cv2.IMREAD_COLOR)


def _aciertos(c: Carpetas, foto):
    plantilla, ref = c.plantilla(mosaico.DISENO)
    verdad = json.loads((c.raiz / "verdad_mosaico.json").read_text(encoding="utf-8"))
    res, _, _ = inspeccionar(foto, ref, plantilla, clasificador.cargar(c.modelos, "red"))
    return sum(r.sugerencia == verdad[r.union_id]["clase"] for r in res), len(res)


def test_carpeta_lista_para_servir(carpeta):
    c = carpeta
    assert (c.plantillas / "mosaico-01.json").exists() and (c.modelos / "red.onnx").exists()
    assert (c.raiz / "LEEME_MOSAICO.txt").read_text(encoding="utf-8").count("CC BY 4.0") == 1
    assert len(c.imagenes()) == 1
    verdad = json.loads((c.raiz / "verdad_mosaico.json").read_text(encoding="utf-8"))
    clases = [v["clase"] for v in verdad.values()]
    assert len(clases) == 30 and all(clases.count(k) == 6 for k in mosaico.CLASES_MOSAICO)
    with pytest.raises(FileExistsError):
        mosaico.crear(c.raiz)


def test_captura_digital(carpeta):
    ok, n = _aciertos(carpeta, leer(carpeta.imagenes()[0]))
    assert ok >= 24, f"{ok}/{n}"


@pytest.mark.parametrize("semilla,brillo", [(3, (1.0, 0.0)), (4, (1.0, 20.0)), (5, (0.85, -15.0))])
def test_foto_de_la_hoja(carpeta, semilla, brillo):
    _, ref = carpeta.plantilla(mosaico.DISENO)
    ok, n = _aciertos(carpeta, _foto_de_la_hoja(ref, semilla, brillo))
    assert ok >= 22, f"{ok}/{n}"


def test_homografia_corrige_perspectiva(carpeta):
    plantilla, ref = carpeta.plantilla(mosaico.DISENO)
    foto = _foto_de_la_hoja(ref, 7)
    m = alinear(foto, ref)
    assert m.shape == (3, 3)
    alineada = al_marco_de_referencia(foto, m, plantilla)
    d = cv2.absdiff(cv2.cvtColor(alineada, cv2.COLOR_BGR2GRAY), cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY))
    assert float(np.median(d)) < 12


def test_normalizar_color_quita_corrimiento():
    rng = np.random.default_rng(0)
    ref = rng.integers(30, 220, (60, 80, 3), dtype=np.uint8)
    oscura = np.clip(ref.astype(np.int16) - 25, 0, 255).astype(np.uint8)
    n = normalizar_color(oscura, ref)
    assert abs(float(n.mean()) - float(ref.mean())) < 1.5
