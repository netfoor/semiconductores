import csv
import hashlib
import io
import json
import struct
from datetime import datetime, timezone

import cv2
import numpy as np
import pytest

from inspeccion_tht import captura, manifiesto
from inspeccion_tht.app import LIMITE_FOTO_MB, crear_app
from inspeccion_tht.cli import main as tht

UA_ANDROID = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Mobile Safari/537.36"


def jpeg(img=None, orientacion=None, marca=None, modelo=None, gps=False, orden=">") -> bytes:
    """JPEG con un EXIF mínimo escrito a mano (marca, modelo, orientación y puntero GPS)."""
    if img is None:
        img = np.full((60, 90, 3), 120, np.uint8)
    ok, buf = cv2.imencode(".jpg", img)
    assert ok
    entradas = []
    if marca:
        entradas.append((0x010F, 2, marca))
    if modelo:
        entradas.append((0x0110, 2, modelo))
    if orientacion:
        entradas.append((0x0112, 3, orientacion))
    if gps:
        entradas.append((0x8825, 4, 0))
    if not entradas:
        return buf.tobytes()
    datos_desde = 8 + 2 + 12 * len(entradas) + 4
    ifd, extra = b"", b""
    for etiqueta, tipo, valor in entradas:
        if tipo == 2:
            crudo = valor.encode() + b"\x00"
            cuenta = len(crudo)
            if cuenta <= 4:
                campo = crudo.ljust(4, b"\x00")
            else:
                campo = struct.pack(orden + "I", datos_desde + len(extra))
                extra += crudo
        elif tipo == 3:
            cuenta, campo = 1, struct.pack(orden + "H", valor) + b"\x00\x00"
        else:
            cuenta, campo = 1, struct.pack(orden + "I", valor)
        ifd += struct.pack(orden + "HHI", etiqueta, tipo, cuenta) + campo
    tiff = (b"MM\x00*" if orden == ">" else b"II*\x00") + struct.pack(orden + "I", 8)
    tiff += struct.pack(orden + "H", len(entradas)) + ifd + struct.pack(orden + "I", 0) + extra
    app1 = b"Exif\x00\x00" + tiff
    b = buf.tobytes()
    return b[:2] + b"\xff\xe1" + struct.pack(">H", len(app1) + 2) + app1 + b[2:]


def formulario(foto: bytes, **campos):
    datos = {"tarjeta": "T07", "lado": "B", "iluminacion": "1", "responsable": "fortino", "nota": "", **campos}
    datos["foto"] = (io.BytesIO(foto), "foto.jpg")
    return datos


@pytest.fixture
def raiz(tmp_path):
    return tmp_path / "datos"


@pytest.fixture
def cliente(raiz):
    app = crear_app(raiz)
    app.testing = True
    return app.test_client()


def enviar(cliente, foto, **campos):
    return cliente.post("/capturar", data=formulario(foto, **campos), content_type="multipart/form-data",
                        headers={"User-Agent": UA_ANDROID})


def filas_manifiesto(raiz):
    with open(raiz / "crudos" / "MANIFIESTO.csv", newline="", encoding="utf-8") as f:
        return {fila["archivo"]: fila["sha256"] for fila in csv.DictReader(f)}


def test_subida_valida_guarda_original_png_json_y_dos_huellas(cliente, raiz):
    foto = jpeg(marca="Google", modelo="Pixel 7", orientacion=1)
    r = enviar(cliente, foto, nota="reflejo arriba")
    assert r.status_code == 302 and "/capturar/T07_B_il1_" in r.headers["Location"]

    png = next((raiz / "crudos" / "T07").glob("*.png"))
    original = png.with_suffix(".jpg")
    assert original.read_bytes() == foto  # bytes intactos
    meta = json.loads(png.with_suffix(".json").read_text(encoding="utf-8"))
    huella = hashlib.sha256(foto).hexdigest()
    assert meta["camara"] == "celular" and meta["modelo_camara"] == "Google Pixel 7"
    assert meta["user_agent"] == UA_ANDROID and meta["nota"] == "reflejo arriba"
    assert meta["original"] == original.name and meta["original_sha256"] == huella
    assert meta["tiene_gps"] is False and (meta["ancho"], meta["alto"]) == (90, 60)

    filas = filas_manifiesto(raiz)
    assert filas == {f"T07/{original.name}": huella, f"T07/{png.name}": manifiesto.sha256_archivo(png)}
    assert manifiesto.verificar(raiz / "crudos") == []

    pagina = cliente.get(r.headers["Location"]).get_data(as_text=True)
    assert "Crear diseño con esta foto" in pagina and huella in pagina


def test_orientacion_exif_de_foto_vertical(cliente, raiz):
    # Sensor horizontal (90 x 60) con la mitad izquierda blanca; orientación 6 = girar 90° a la derecha.
    img = np.zeros((60, 90, 3), np.uint8)
    img[:, :45] = 255
    assert enviar(cliente, jpeg(img, orientacion=6)).status_code == 302
    png = next((raiz / "crudos" / "T07").glob("*.png"))
    guardada = cv2.imread(str(png), cv2.IMREAD_UNCHANGED)
    assert guardada.shape[:2] == (90, 60)  # vertical
    assert guardada[:40].mean() > 200 and guardada[50:].mean() < 50  # lo blanco quedó arriba
    meta = json.loads(png.with_suffix(".json").read_text(encoding="utf-8"))
    assert (meta["ancho"], meta["alto"], meta["orientacion_exif"]) == (60, 90, 6)


@pytest.mark.parametrize("contenido,texto", [
    (b"\x00\x00\x00\x18ftypheic\x00\x00\x00\x00mif1heic" + b"\x00" * 64, "Más compatible"),
    (cv2.imencode(".png", np.zeros((8, 8, 3), np.uint8))[1].tobytes(), "Solo se aceptan fotos JPEG"),
    (b"\xff\xd8\xff\xe0" + b"basura" * 20, "dañado o incompleto"),
])
def test_formato_invalido(cliente, raiz, contenido, texto):
    r = enviar(cliente, contenido)
    assert r.status_code == 415 and texto in r.get_data(as_text=True)
    assert not list((raiz / "crudos").rglob("*.*"))  # no se escribió nada


def test_tamano_excedido(cliente, raiz):
    grande = b"\xff\xd8\xff" + b"\x00" * (LIMITE_FOTO_MB * 1024 * 1024 + 1)
    r = enviar(cliente, grande)
    assert r.status_code == 413 and f"más de {LIMITE_FOTO_MB} MB" in r.get_data(as_text=True)


@pytest.mark.parametrize("campos,texto", [
    ({"tarjeta": "07"}, "La tarjeta se nombra"),
    ({"tarjeta": "T7"}, "La tarjeta se nombra"),
    ({"lado": "C"}, "El lado es A"),
    ({"iluminacion": "../1"}, "La iluminación"),
    ({"responsable": " "}, "Falta el nombre"),
    ({"diseno": "no-existe"}, "No existe el diseño"),
])
def test_tarjeta_o_campos_invalidos(cliente, raiz, campos, texto):
    r = enviar(cliente, jpeg(), **campos)
    assert r.status_code == 400 and texto in r.get_data(as_text=True)
    assert not list((raiz / "crudos").rglob("*.*"))


def test_sin_foto(cliente):
    r = cliente.post("/capturar", data={"tarjeta": "T07", "lado": "B", "responsable": "x"})
    assert r.status_code == 400 and "Falta la foto" in r.get_data(as_text=True)


def test_no_sobrescribe(cliente, raiz, monkeypatch):
    fijo = datetime(2026, 10, 30, 10, 0, 0, tzinfo=timezone.utc)

    class Reloj(datetime):
        @classmethod
        def now(cls, tz=None):
            return fijo

    monkeypatch.setattr(captura, "datetime", Reloj)
    primera = jpeg(marca="Google", modelo="Pixel 7")
    assert enviar(cliente, primera).status_code == 302
    r = enviar(cliente, jpeg(np.zeros((60, 90, 3), np.uint8)))
    assert r.status_code == 409 and "No se sobrescribió" in r.get_data(as_text=True)
    assert (raiz / "crudos" / "T07" / "T07_B_il1_20261030T100000.jpg").read_bytes() == primera
    assert len(filas_manifiesto(raiz)) == 2


def test_gps_se_avisa(cliente):
    r = enviar(cliente, jpeg(modelo="iPhone 15", marca="Apple", gps=True, orden="<"))
    pagina = cliente.get(r.headers["Location"]).get_data(as_text=True)
    assert "datos de ubicación" in pagina and "Apple iPhone 15" in pagina


def test_captura_en_linea_no_existe(raiz):
    app = crear_app(raiz, en_linea=True)
    app.testing = True
    c = app.test_client()
    assert c.get("/capturar").status_code == 404
    assert enviar(c, jpeg()).status_code in (404, 405)
    assert "Capturar" not in c.get("/demo").get_data(as_text=True)
    assert app.config.get("MAX_CONTENT_LENGTH") is None  # Railway sin cambios


def test_pagina_local_tiene_formulario_y_navegacion(cliente):
    html = cliente.get("/capturar").get_data(as_text=True)
    assert 'capture="environment"' in html and 'accept="image/*"' in html
    assert html.count('type="file"') == 2  # cámara y galería
    assert 'href="/capturar"' in cliente.get("/").get_data(as_text=True)


@pytest.fixture(scope="module")
def con_diseno(tmp_path_factory):
    d = tmp_path_factory.mktemp("demo")
    tht(["demo", "--salida", str(d), "--tarjetas", "2", "--filas", "2", "--columnas", "3"])
    return d


def test_con_diseno_lleva_a_inspeccionar(con_diseno):
    app = crear_app(con_diseno)
    app.testing = True
    c = app.test_client()
    disenos = sorted(p.stem for p in (con_diseno / "plantillas").glob("*.json"))
    r = enviar(c, jpeg(), tarjeta="T09", diseno=disenos[0], responsable="israel")
    destino = r.headers["Location"]
    assert r.status_code == 302 and "/inspeccionar/T09_B_il1_" in destino and "etiquetador=israel" in destino
    png = next((con_diseno / "crudos" / "T09").glob("*.png"))
    assert json.loads(png.with_suffix(".json").read_text(encoding="utf-8"))["diseno"] == disenos[0]
    assert c.get(destino).status_code == 200


def test_captura_de_archivo_conserva_su_json(tmp_path):
    origen = tmp_path / "foto.png"
    cv2.imwrite(str(origen), np.zeros((10, 12, 3), np.uint8))
    ruta = captura.capturar(captura.CamaraArchivo([origen]), tmp_path / "crudos", "T01", "B", "1", "fortino")
    meta = json.loads(ruta.with_suffix(".json").read_text(encoding="utf-8"))
    assert list(meta) == ["archivo", "tarjeta", "lado", "iluminacion", "camara", "ancho", "alto",
                          "capturado_utc", "equipo", "responsable", "nota"]
    assert not ruta.with_suffix(".jpg").exists()


def test_leer_exif_tolera_datos_danados():
    assert captura.leer_exif(b"\xff\xd8\xff\xe1\x00\x10Exif\x00\x00XX\x00\x00") == {}
    assert captura.leer_exif(jpeg()) == {}


def test_fotos_prueba_se_alinean_con_el_diseno_de_demo(con_diseno, tmp_path):
    tht(["fotos-prueba", "--salida", str(tmp_path / "fotos"), "--tarjetas", "2"])
    vertical = tmp_path / "fotos" / "T12_sintetica_vertical_exif6.jpg"
    assert captura.leer_exif(vertical.read_bytes()) == {"orientacion": 6}
    assert (tmp_path / "fotos" / "LEEME.txt").exists() and len(list((tmp_path / "fotos" / "publicas-pcbspdefect").glob("*.jpg"))) == 5
    app = crear_app(con_diseno)
    c = app.test_client()
    r = enviar(c, vertical.read_bytes(), tarjeta="T12", diseno="sintetica-01")
    png = next((con_diseno / "crudos" / "T12").glob("*.png"))
    alto, ancho = cv2.imread(str(png)).shape[:2]
    assert r.status_code == 302 and ancho > alto  # quedó en la orientación del diseño


def test_verificar_sin_manifiesto_explica_que_hacer(tmp_path):
    with pytest.raises(SystemExit) as e:
        tht(["manifiesto", "verificar", str(tmp_path)])
    assert "tht manifiesto generar" in str(e.value)


def test_aviso_sin_modelo_indica_la_carpeta(con_diseno):
    c = crear_app(con_diseno).test_client()
    html = c.get("/inspeccionar/T01_B_il1_SINTETICO.png").get_data(as_text=True)
    assert f"tht entrenar --datos {con_diseno}" in html
