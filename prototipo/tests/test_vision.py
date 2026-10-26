import numpy as np
import pytest

from inspeccion_tht import sintetico
from inspeccion_tht.clases import CLASES
from inspeccion_tht.flujo import inspeccionar
from inspeccion_tht.linea_base import ClasificadorCentroide, caracteristicas
from inspeccion_tht.metricas import Caso, binaria
from inspeccion_tht.plantilla import Plantilla, al_marco_de_referencia, alinear


def entrenar_sintetico(n=40, semilla=0, variabilidad=1.0):
    rng = np.random.default_rng(semilla)
    X, y = [], []
    for c in CLASES:
        for _ in range(n):
            X.append(caracteristicas(sintetico.celda(c, rng, variabilidad=variabilidad)))
            y.append(c)
    return ClasificadorCentroide.entrenar(np.array(X), y)


def test_caracteristicas_tienen_forma_fija():
    rng = np.random.default_rng(1)
    v = caracteristicas(sintetico.celda("aceptable", rng))
    assert v.shape == (9,) and np.all(np.isfinite(v))


def test_linea_base_supera_el_azar_en_clases_sinteticas(tmp_path):
    # Con variabilidad alta la línea base clásica falla a propósito en clases sutiles
    # (insuficiente, fría): es la referencia que debe superar el clasificador ligero.
    modelo = entrenar_sintetico(n=60)
    rng = np.random.default_rng(99)
    aciertos, total = 0, 0
    for c in CLASES:
        for _ in range(20):
            pred = modelo.predecir(caracteristicas(sintetico.celda(c, rng)))[0]
            aciertos += pred == c
            total += 1
    assert aciertos / total > 0.6
    ruta = tmp_path / "modelo.json"
    modelo.guardar(ruta)
    cargado = ClasificadorCentroide.cargar(ruta)
    x = caracteristicas(sintetico.celda("puente", rng))
    assert cargado.predecir(x) == modelo.predecir(x)


@pytest.mark.parametrize("dx,dy,ang", [(0, 0, 0), (12, -8, 0), (-15, 10, 1.0)])
def test_alineacion_recupera_desplazamiento(dx, dy, ang):
    rng = np.random.default_rng(3)
    ref, plantilla, _ = sintetico.tarjeta(4, 5, rng)
    movida = sintetico.desplazar(ref, dx, dy, ang)
    warp = alinear(movida, ref)
    alineada = al_marco_de_referencia(movida, warp, plantilla)
    error = np.abs(alineada.astype(int) - ref.astype(int))[20:-20, 20:-20].mean()
    assert error < 6


def test_plantilla_ida_y_vuelta(tmp_path):
    _, plantilla, _ = sintetico.tarjeta(2, 2, np.random.default_rng(0))
    ruta = tmp_path / "p.json"
    plantilla.guardar(ruta)
    assert Plantilla.cargar(ruta) == plantilla


def entrenar_con_recortes(n_tarjetas=6, semilla=0):
    """Igual que con datos reales: se entrena con los recortes que produce la plantilla."""
    from inspeccion_tht.plantilla import recortes
    rng = np.random.default_rng(semilla)
    X, y = [], []
    for _ in range(n_tarjetas):
        img, plantilla, verdad = sintetico.tarjeta(5, 6, rng, prob_defecto=0.5)
        for uid, rec in recortes(img, plantilla).items():
            X.append(caracteristicas(rec))
            y.append(verdad[uid])
    return ClasificadorCentroide.entrenar(np.array(X), y)


def test_flujo_completo_en_tarjeta_sintetica():
    modelo = entrenar_con_recortes()
    rng = np.random.default_rng(11)
    ref, plantilla, verdad = sintetico.tarjeta(5, 6, rng, prob_defecto=0.4)
    captura = sintetico.desplazar(ref, 9, -6, 0.5)
    resultados, tiempos, alineada = inspeccionar(captura, ref, plantilla, modelo)
    assert len(resultados) == 30 and alineada.shape == ref.shape
    assert tiempos["total_s"] > 0
    b = binaria([Caso("T", r.union_id, verdad[r.union_id], r.sugerencia) for r in resultados])
    assert b.sensibilidad >= 0.8
