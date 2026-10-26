import math

import pytest

from inspeccion_tht.metricas import (Caso, binaria, bootstrap_por_tarjeta, kappa_cohen, matriz_confusion,
                                     mcnemar_exacto, por_clase, resumen, wilson)


def test_wilson_cero_exitos_forma_cerrada():
    lo, hi = wilson(0, 10)
    z2 = 1.959963984540054 ** 2
    assert lo == 0.0
    assert hi == pytest.approx(z2 / (10 + z2), rel=1e-9)


def test_wilson_simetrico_y_contiene_p():
    lo, hi = wilson(85, 100)
    lo2, hi2 = wilson(15, 100)
    assert lo == pytest.approx(1 - hi2) and hi == pytest.approx(1 - lo2)
    assert lo < 0.85 < hi


def test_wilson_semiamplitud_del_protocolo():
    # Protocolo 6.3: con ~150 defectos y sensibilidad ~0.90, semiamplitud aproximada de 0.05.
    lo, hi = wilson(135, 150)
    assert (hi - lo) / 2 == pytest.approx(0.048, abs=0.004)


def test_wilson_valida_entradas():
    with pytest.raises(ValueError):
        wilson(1, 0)
    with pytest.raises(ValueError):
        wilson(5, 3)


def casos_ejemplo():
    return [
        Caso("T01", "U1", "puente", "puente"),        # vp
        Caso("T01", "U2", "insuficiente", "aceptable"),  # fn
        Caso("T01", "U3", "aceptable", "exceso"),     # fp
        Caso("T02", "U1", "aceptable", "aceptable"),  # vn
        Caso("T02", "U2", "fria", "insuficiente"),    # vp (defecto detectado aunque con otra clase)
        Caso("T02", "U3", "aceptable", "aceptable"),  # vn
    ]


def test_binaria():
    b = binaria(casos_ejemplo())
    assert (b.vp, b.fn, b.fp, b.vn) == (2, 1, 1, 2)
    assert b.sensibilidad == pytest.approx(2 / 3)
    assert b.falsas_alarmas == pytest.approx(1 / 3)
    assert b.precision == pytest.approx(2 / 3)


def test_matriz_y_por_clase():
    m = matriz_confusion(casos_ejemplo())
    assert sum(map(sum, m)) == 6
    pc = por_clase(casos_ejemplo())
    assert pc["puente"]["sensibilidad"] == 1.0
    assert pc["aceptable"]["n"] == 3
    assert math.isnan(pc["sin_soldar"]["sensibilidad"])


def test_mcnemar_exacto():
    assert mcnemar_exacto(0, 5) == pytest.approx(0.0625)
    assert mcnemar_exacto(3, 3) == 1.0
    assert mcnemar_exacto(0, 0) == 1.0


def test_kappa_ejemplo_conocido():
    # 20 sí-sí, 5 sí-no, 10 no-sí, 15 no-no: kappa = 0.4
    a = ["si"] * 25 + ["no"] * 25
    b = ["si"] * 20 + ["no"] * 5 + ["si"] * 10 + ["no"] * 15
    assert kappa_cohen(a, b) == pytest.approx(0.4)
    assert kappa_cohen(["a", "b"], ["a", "b"]) == 1.0


def test_bootstrap_por_tarjeta_es_reproducible_y_acotado():
    cs = casos_ejemplo() * 5
    cs = [Caso(f"T{i // 3:02d}", c.union, c.verdad, c.prediccion) for i, c in enumerate(cs)]
    f = lambda xs: binaria(xs).sensibilidad
    a = bootstrap_por_tarjeta(cs, f, repeticiones=500, semilla=1)
    b = bootstrap_por_tarjeta(cs, f, repeticiones=500, semilla=1)
    assert a == b
    assert 0.0 <= a[0] <= a[1] <= 1.0


def test_bootstrap_requiere_dos_tarjetas():
    with pytest.raises(ValueError):
        bootstrap_por_tarjeta([Caso("T01", "U1", "puente", "puente")], lambda xs: 1.0)


def test_resumen_tiene_intervalos():
    r = resumen(casos_ejemplo(), repeticiones=200)
    assert r["n_tarjetas"] == 2
    assert "sensibilidad_wilson95" in r and "falsas_alarmas_bootstrap95" in r
