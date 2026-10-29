import base64
import importlib
import sys


def test_demo_en_la_nube_prepara_datos_y_pide_clave(tmp_path, monkeypatch):
    monkeypatch.setenv("THT_DATOS", str(tmp_path / "nube"))
    monkeypatch.setenv("THT_USUARIO", "femeci")
    monkeypatch.setenv("THT_CLAVE", "prueba")
    sys.modules.pop("inspeccion_tht.wsgi", None)
    wsgi = importlib.import_module("inspeccion_tht.wsgi")
    c = wsgi.app.test_client()
    assert c.get("/salud").get_json()["sintetico"] is True
    assert c.get("/").status_code == 401
    auth = {"Authorization": "Basic " + base64.b64encode(b"femeci:prueba").decode()}
    r = c.get("/", headers=auth)
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "Una segunda mirada" in html and "Primeros resultados con fotos reales" in html
    assert "Datos sintéticos." not in html  # la página del proyecto no es la demo
    demo = c.get("/demo", headers=auth).get_data(as_text=True)
    assert "etiqueta-demo" in demo and "Carpeta de datos" not in demo  # D-015: etiqueta, no banner
    assert (tmp_path / "nube" / "modelos" / "linea_base.json").exists()
