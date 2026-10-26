import numpy as np
import pytest

from inspeccion_tht.cli import main as tht


@pytest.fixture(scope="module")
def datos(tmp_path_factory):
    d = tmp_path_factory.mktemp("demo")
    tht(["demo", "--salida", str(d), "--tarjetas", "4", "--filas", "3", "--columnas", "4"])
    tht(["particion", "--datos", str(d)])
    tht(["entrenar", "--datos", str(d), "--con-validacion"])
    return d


@pytest.fixture
def cliente(datos):
    from inspeccion_tht.app import crear_app
    app = crear_app(datos)
    app.testing = True
    return app.test_client()


def test_inicio_avisa_que_es_sintetico(cliente):
    r = cliente.get("/")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "Datos sintéticos" in html and "T01_B_il1_SINTETICO.png" in html


def test_paginas_principales(cliente):
    for url in ["/plantilla/sintetica-01", "/etiquetar/T01_B_il1_SINTETICO.png?etiquetador=prueba",
                "/inspeccionar/T01_B_il1_SINTETICO.png"]:
        assert cliente.get(url).status_code == 200, url


def test_imagenes(cliente):
    assert cliente.get("/img/crudo/T01_B_il1_SINTETICO.png").mimetype == "image/png"
    assert cliente.get("/img/plantilla/sintetica-01").mimetype == "image/png"
    assert cliente.get("/img/alineada/T01_B_il1_SINTETICO.png").mimetype == "image/jpeg"


def test_api_inspeccion_y_decision(cliente):
    r = cliente.get("/api/inspeccion/T01_B_il1_SINTETICO.png").get_json()
    assert len(r["resultados"]) == 12 and r["tiempos"]["total_s"] > 0
    u = r["resultados"][0]
    ok = cliente.post("/api/decision", json={"operador": "prueba", "imagen": "T01_B_il1_SINTETICO.png",
                                            "union_id": u["union_id"], "sugerencia": u["sugerencia"],
                                            "puntaje": u["puntaje_defecto"], "decision": "aceptable", "segundos": 1.2})
    assert ok.status_code == 200 and ok.get_json()["ok"]
    mal = cliente.post("/api/decision", json={"operador": "prueba", "imagen": "T01_B_il1_SINTETICO.png",
                                             "union_id": "U0101", "sugerencia": "aceptable", "decision": "inventada"})
    assert mal.status_code == 400 and "Clase desconocida" in mal.get_json()["error"]


def test_api_anotacion_requiere_persona(cliente, datos):
    base = {"imagen": "T02_B_il1_SINTETICO.png", "diseno": "sintetica-01", "etiquetas": {"U0101": "puente"}}
    assert cliente.post("/api/anotacion", json={**base, "etiquetador": ""}).status_code == 400
    r = cliente.post("/api/anotacion", json={**base, "etiquetador": "israel"})
    assert r.status_code == 200
    assert (datos / "anotaciones" / "T02_B_il1_SINTETICO.israel.json").exists()


def test_api_plantilla_rechaza_ids_repetidos(cliente):
    u = {"id": "U1", "x": 1, "y": 1, "w": 10, "h": 10}
    assert cliente.post("/api/plantilla/sintetica-01", json={"uniones": [u, u]}).status_code == 400


def test_error_amable_si_no_existe(cliente):
    r = cliente.get("/img/crudo/T99_B_il1_X.png")
    assert r.status_code == 404


def test_estacion_local_tiene_la_pagina_del_proyecto_aparte(cliente):
    r = cliente.get("/proyecto")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "Sensibilidad" in html and "SHA-256" in html


def test_secciones_publicas(cliente):
    for url in ["/fotos-reales", "/reto", "/experimentos"]:
        r = cliente.get(url)
        assert r.status_code == 200, url
    html = cliente.get("/experimentos").get_data(as_text=True)
    assert "EXP-006" in html and "tomada como" in html
    assert cliente.get("/publico/fotos/001.jpg").mimetype == "image/jpeg"


def test_api_foto_clasifica_en_vivo(cliente):
    d = cliente.get("/api/foto/001.jpg").get_json()
    assert d["prediccion"] in {p["clase"] for p in d["probabilidades"]}
    assert abs(sum(p["p"] for p in d["probabilidades"]) - 1) < 1e-4
    assert d["milisegundos"] > 0
    assert cliente.get("/api/foto/999.jpg").status_code == 404
