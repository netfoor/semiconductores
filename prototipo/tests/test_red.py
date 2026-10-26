import numpy as np
import pytest

torch = pytest.importorskip("torch")

from inspeccion_tht import sintetico
from inspeccion_tht.clases import CLASES
from inspeccion_tht.clasificador import ClasificadorONNX, cargar, preparar
from inspeccion_tht.entrenamiento_red import entrenar, exactitud_balanceada, exportar
from inspeccion_tht.flujo import inspeccionar


def datos(n, semilla):
    rng = np.random.default_rng(semilla)
    rec, cls = [], []
    for c in CLASES:
        for _ in range(n):
            rec.append(sintetico.celda(c, rng))
            cls.append(c)
    return rec, cls


@pytest.fixture(scope="module")
def red_entrenada(tmp_path_factory):
    er, ec = datos(30, 0)
    vr, vc = datos(8, 1)
    res = entrenar(er, ec, vr, vc, semilla=3, epocas=12)
    ruta = exportar(res, tmp_path_factory.mktemp("m") / "red.onnx", "prueba", len(er))
    return res, ruta


def test_entrena_mejor_que_el_azar(red_entrenada):
    res, _ = red_entrenada
    assert res.clases == sorted(CLASES)
    assert res.val_exactitud_balanceada > 0.5  # azar: 1/6


def test_onnx_coincide_con_pytorch(red_entrenada):
    res, ruta = red_entrenada
    rec, _ = datos(3, 7)
    with torch.no_grad():
        p_torch = torch.softmax(res.modelo(torch.from_numpy(preparar(rec))), 1).numpy()
    p_onnx = ClasificadorONNX(ruta).probabilidades(rec)
    assert np.allclose(p_torch, p_onnx, atol=1e-4)


def test_interfaz_comun_y_flujo(red_entrenada):
    _, ruta = red_entrenada
    m = cargar(ruta.parent, "red")
    sug, punt = m.evaluar_recortes(datos(1, 5)[0])
    assert len(sug) == len(CLASES) and punt.shape == (len(CLASES),)
    rng = np.random.default_rng(2)
    ref, plantilla, _ = sintetico.tarjeta(2, 3, rng)
    resultados, tiempos, _ = inspeccionar(ref, ref, plantilla, m)
    assert len(resultados) == 6 and {"recortes_s", "clasificacion_s"} <= set(tiempos)


def test_exactitud_balanceada():
    assert exactitud_balanceada(["a", "a", "b"], ["a", "b", "b"], ["a", "b"]) == pytest.approx(0.75)


def test_modelo_desconocido(tmp_path):
    with pytest.raises(ValueError):
        cargar(tmp_path, "otro")
