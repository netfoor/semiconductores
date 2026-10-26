"""Interfaz local (Flask): plantillas, etiquetado ciego e inspección asistida.

No usa recursos de internet: todo se sirve desde esta carpeta.
"""

import json
import shutil
from dataclasses import asdict
from pathlib import Path

import cv2
from flask import Flask, abort, jsonify, render_template, request, send_from_directory

from . import __version__
from .anotaciones import Anotacion, todas
from .clases import CLASES, NOMBRES, validar
from .datos import Carpetas
from .flujo import inspeccionar, leer
from .linea_base import ClasificadorCentroide
from .plantilla import Plantilla, Union, al_marco_de_referencia, alinear
from .registro import Registro


def crear_app(raiz: Path, operador: str = "") -> Flask:
    c = Carpetas(Path(raiz)).crear()
    app = Flask(__name__)
    app.config["CARPETAS"] = c
    registro = Registro(c.decisiones)
    cache_modelo: dict[str, object] = {}

    def disenos() -> list[str]:
        return sorted(p.stem for p in c.plantillas.glob("*.json"))

    def es_sintetico() -> bool:
        return (c.raiz / "LEEME_SINTETICO.txt").exists()

    def modelo() -> ClasificadorCentroide | None:
        ruta = c.modelos / "linea_base.json"
        if not ruta.exists():
            return None
        mt = ruta.stat().st_mtime
        if cache_modelo.get("mt") != mt:
            cache_modelo.update(mt=mt, m=ClasificadorCentroide.cargar(ruta))
        return cache_modelo["m"]

    def diseno_de(imagen: str) -> str:
        d = request.args.get("diseno")
        if d:
            return d
        meta = c.imagen(imagen).with_suffix(".json")
        if meta.exists():
            d = json.loads(meta.read_text(encoding="utf-8")).get("diseno")
            if d:
                return d
        for an in todas(c.anotaciones):
            if an.imagen == imagen:
                return an.diseno
        ds = disenos()
        if len(ds) == 1:
            return ds[0]
        abort(400, "Indique el diseño de tarjeta con ?diseno=")

    @app.context_processor
    def comunes():
        return {"version": __version__, "sintetico": es_sintetico(), "clases": CLASES,
                "nombres": NOMBRES, "operador": operador}

    @app.get("/salud")
    def salud():
        return jsonify(ok=True, version=__version__, sintetico=es_sintetico())

    @app.get("/")
    def inicio():
        imagenes = [p.name for p in c.imagenes()]
        por_etiquetador: dict[str, int] = {}
        for a in todas(c.anotaciones):
            por_etiquetador[a.etiquetador] = por_etiquetador.get(a.etiquetador, 0) + 1
        return render_template("inicio.html", imagenes=imagenes, disenos=disenos(),
                               por_etiquetador=por_etiquetador, hay_modelo=modelo() is not None,
                               hay_particion=c.particion.exists(), n_decisiones=len(registro.todas()),
                               raiz=str(c.raiz))

    @app.get("/plantilla/<diseno>")
    def pagina_plantilla(diseno):
        ruta = c.plantillas / f"{diseno}.json"
        if not ruta.exists():
            abort(404, f"No existe el diseño {diseno}")
        return render_template("plantilla.html", diseno=diseno, plantilla=json.loads(ruta.read_text(encoding="utf-8")))

    @app.post("/plantilla/nueva")
    def nueva_plantilla():
        diseno = (request.form.get("diseno") or "").strip()
        imagen = request.form.get("imagen") or ""
        if not diseno or not diseno.replace("-", "").replace("_", "").isalnum():
            abort(400, "El nombre del diseño solo admite letras, números, guiones y guiones bajos")
        if (c.plantillas / f"{diseno}.json").exists():
            abort(409, "Ya existe un diseño con ese nombre")
        origen = c.imagen(imagen)
        destino = c.plantillas / f"{diseno}{origen.suffix}"
        shutil.copyfile(origen, destino)
        img = leer(destino)
        Plantilla(diseno, destino.name, img.shape[1], img.shape[0], []).guardar(c.plantillas / f"{diseno}.json")
        return pagina_plantilla(diseno)

    @app.post("/api/plantilla/<diseno>")
    def guardar_plantilla(diseno):
        ruta = c.plantillas / f"{diseno}.json"
        if not ruta.exists():
            abort(404, f"No existe el diseño {diseno}")
        p = Plantilla.cargar(ruta)
        datos = request.get_json(force=True)
        ids = [u["id"] for u in datos["uniones"]]
        if len(ids) != len(set(ids)):
            abort(400, "Hay identificadores de unión repetidos")
        p.uniones = [Union(str(u["id"]), int(u["x"]), int(u["y"]), int(u["w"]), int(u["h"])) for u in datos["uniones"]]
        p.guardar(ruta)
        return jsonify(ok=True, uniones=len(p.uniones))

    @app.get("/etiquetar/<imagen>")
    def pagina_etiquetar(imagen):
        etiquetador = request.args.get("etiquetador", "").strip()
        diseno = diseno_de(imagen)
        p = Plantilla.cargar(c.plantillas / f"{diseno}.json")
        previas = {}
        if etiquetador:
            ruta = Anotacion(imagen, "", diseno, etiquetador).ruta(c.anotaciones)
            if ruta.exists():
                previas = Anotacion.cargar(ruta).etiquetas
        return render_template("etiquetar.html", imagen=imagen, diseno=diseno, etiquetador=etiquetador,
                               plantilla=asdict(p), previas=previas)

    @app.post("/api/anotacion")
    def guardar_anotacion():
        d = request.get_json(force=True)
        etiquetador = (d.get("etiquetador") or "").strip()
        if not etiquetador:
            abort(400, "Falta el nombre de quien etiqueta")
        an = Anotacion(d["imagen"], d["imagen"].split("_")[0], d["diseno"], etiquetador)
        for uid, clase in d["etiquetas"].items():
            an.poner(uid, clase)
        ruta = an.guardar(c.anotaciones)
        return jsonify(ok=True, uniones=len(an.etiquetas), archivo=ruta.name)

    @app.get("/inspeccionar/<imagen>")
    def pagina_inspeccionar(imagen):
        return render_template("inspeccionar.html", imagen=imagen, diseno=diseno_de(imagen),
                               hay_modelo=modelo() is not None)

    @app.get("/api/inspeccion/<imagen>")
    def api_inspeccion(imagen):
        m = modelo()
        if m is None:
            abort(409, "No hay modelo entrenado. Ejecute `tht entrenar` primero.")
        diseno = diseno_de(imagen)
        p, ref = c.plantilla(diseno)
        resultados, tiempos, _ = inspeccionar(leer(c.imagen(imagen)), ref, p, m)
        return jsonify(diseno=diseno, ancho=p.ancho, alto=p.alto, tiempos=tiempos,
                       resultados=[asdict(r) for r in resultados])

    @app.post("/api/decision")
    def api_decision():
        d = request.get_json(force=True)
        quien = (d.get("operador") or operador or "").strip()
        if not quien:
            abort(400, "Falta el nombre del operador")
        validar(d["decision"])
        validar(d["sugerencia"])
        i = registro.anotar(quien, d["imagen"], d["imagen"].split("_")[0], d["union_id"], d["sugerencia"],
                            d.get("puntaje"), d["decision"], d.get("segundos"), d.get("modo", "asistido"))
        return jsonify(ok=True, id=i)

    @app.get("/img/crudo/<imagen>")
    def img_crudo(imagen):
        r = c.imagen(imagen)
        return send_from_directory(r.parent, r.name)

    @app.get("/img/plantilla/<diseno>")
    def img_plantilla(diseno):
        p = Plantilla.cargar(c.plantillas / f"{diseno}.json")
        return send_from_directory(c.plantillas, p.referencia)

    @app.get("/img/alineada/<imagen>")
    def img_alineada(imagen):
        diseno = diseno_de(imagen)
        p, ref = c.plantilla(diseno)
        img = leer(c.imagen(imagen))
        al = al_marco_de_referencia(img, alinear(img, ref), p)
        ok, buf = cv2.imencode(".jpg", al, [cv2.IMWRITE_JPEG_QUALITY, 92])
        if not ok:
            abort(500)
        return app.response_class(buf.tobytes(), mimetype="image/jpeg")

    def responder_error(codigo: int, mensaje: str):
        if request.path.startswith("/api/"):
            return jsonify(ok=False, error=mensaje), codigo
        return render_template("error.html", codigo=codigo, mensaje=mensaje), codigo

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(409)
    def error_http(e):
        return responder_error(e.code, e.description)

    @app.errorhandler(FileNotFoundError)
    def error_archivo(e):
        return responder_error(404, f"No se encontró el archivo {e}. Revise que la imagen esté en crudos/.")

    @app.errorhandler(ValueError)
    def error_valor(e):
        return responder_error(400, str(e))

    return app
