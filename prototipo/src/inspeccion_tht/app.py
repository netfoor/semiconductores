"""Interfaz local (Flask): plantillas, etiquetado ciego e inspección asistida.

No usa recursos de internet: todo se sirve desde esta carpeta.
"""

import json
import shutil
import threading
from dataclasses import asdict
from pathlib import Path

import cv2
from flask import Flask, abort, jsonify, redirect, render_template, request, send_from_directory, url_for

from . import __version__, captura
from .anotaciones import Anotacion, todas
from .clases import CLASES, NOMBRES, validar
from .datos import Carpetas
from .flujo import inspeccionar, leer
from . import clasificador
from .plantilla import Plantilla, Union, al_marco_de_referencia, alinear
from .registro import Registro

LIMITE_FOTO_MB = 30


def crear_app(raiz: Path, operador: str = "", modelo_nombre: str = "linea_base", en_linea: bool = False) -> Flask:
    """`en_linea`: demostración pública en un servidor (cambia los textos que hablan de operar sin internet
    y quita la captura desde el celular, que solo existe en la estación local)."""
    c = Carpetas(Path(raiz)).crear()
    app = Flask(__name__)
    app.config["CARPETAS"] = c
    registro = Registro(c.decisiones)
    cache_modelo: dict[str, object] = {}

    def disenos() -> list[str]:
        return sorted(p.stem for p in c.plantillas.glob("*.json"))

    def es_sintetico() -> bool:
        return (c.raiz / "LEEME_SINTETICO.txt").exists()

    def es_mosaico() -> bool:
        return (c.raiz / "LEEME_MOSAICO.txt").exists()

    if modelo_nombre not in clasificador.MODELOS:
        raise ValueError(f"Modelo desconocido: {modelo_nombre}")

    def modelo():
        ruta = clasificador.ruta_principal(c.modelos, modelo_nombre)
        if not ruta.exists():
            return None
        mt = ruta.stat().st_mtime
        if cache_modelo.get("mt") != mt:
            cache_modelo.update(mt=mt, m=clasificador.cargar(c.modelos, modelo_nombre))
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
                "nombres": NOMBRES, "mosaico": es_mosaico(), "operador": operador, "modelo_nombre": modelo_nombre, "en_linea": en_linea}

    @app.get("/salud")
    def salud():
        return jsonify(ok=True, version=__version__, sintetico=es_sintetico(), modelo=modelo_nombre, en_linea=en_linea)

    publico = Path(__file__).parent / "publico" / "resultados.json"

    def pagina_proyecto():
        resultados = json.loads(publico.read_text(encoding="utf-8"))
        return render_template("landing.html", resultados=resultados, ocultar_aviso=True)

    carpeta_publica = publico.parent
    cache_red: dict[str, object] = {}

    def red_publica():
        if "m" not in cache_red:
            cache_red["m"] = clasificador.ClasificadorONNX(carpeta_publica / "red_pcbspdefect.onnx")
        return cache_red["m"]

    def leer_publico(nombre: str):
        return json.loads((carpeta_publica / nombre).read_text(encoding="utf-8"))

    @app.get("/fotos-reales")
    def fotos_reales():
        return render_template("fotos.html", fotos=leer_publico("fotos.json"), ocultar_aviso=True)

    @app.get("/reto")
    def reto():
        return render_template("reto.html", fotos=leer_publico("fotos.json"), ocultar_aviso=True)

    def confusiones(resultados: dict, modelo: str, n: int = 2) -> list[dict]:
        """Las confusiones más frecuentes, calculadas de la matriz (para no escribir lecturas a mano)."""
        cl, m = resultados["clases"], resultados["matrices"]["oficial"][modelo]["matriz"]
        pares = [(m[i][j], cl[i], cl[j]) for i in range(len(cl)) for j in range(len(cl)) if i != j and m[i][j]]
        return [{"n": k, "real": NOMBRES[a], "predicha": NOMBRES[b]} for k, a, b in sorted(pares, reverse=True)[:n]]

    @app.get("/experimentos")
    def experimentos():
        resultados = leer_publico("resultados.json")
        return render_template("experimentos.html", experimentos=leer_publico("experimentos.json"), resultados=resultados,
                               conf_base=confusiones(resultados, "linea_base"), conf_red=confusiones(resultados, "red"),
                               ocultar_aviso=True)

    @app.get("/publico/fotos/<nombre>")
    def foto_publica(nombre):
        return send_from_directory(carpeta_publica / "fotos", nombre, max_age=86400)

    @app.get("/api/foto/<nombre>")
    def api_foto(nombre):
        import time as _t
        datos = leer_publico("fotos.json")
        foto = next((f for f in datos["fotos"] if f["archivo"] == nombre), None)
        if foto is None:
            abort(404, f"No existe la foto {nombre}")
        img = leer(carpeta_publica / "fotos" / nombre)
        m = red_publica()
        t = _t.perf_counter()
        p = m.probabilidades([img])[0]
        ms = (_t.perf_counter() - t) * 1000
        orden = sorted(zip(m.clases, p.tolist()), key=lambda x: -x[1])
        return jsonify(archivo=nombre, verdad=foto["clase"], prediccion=orden[0][0], acierto=orden[0][0] == foto["clase"],
                       probabilidades=[{"clase": c, "nombre": NOMBRES[c], "p": v} for c, v in orden], milisegundos=ms)

    # En línea, la raíz es la página del proyecto y la interfaz de trabajo vive en /demo.
    # En la estación local, la raíz es la interfaz de trabajo y la página está en /proyecto.
    app.add_url_rule("/" if en_linea else "/proyecto", "proyecto", pagina_proyecto)

    @app.get("/demo" if en_linea else "/")
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
                               hay_modelo=modelo() is not None, raiz=str(c.raiz))

    @app.get("/api/inspeccion/<imagen>")
    def api_inspeccion(imagen):
        m = modelo()
        if m is None:
            abort(409, f"No hay modelo {modelo_nombre} entrenado. Ejecute `tht entrenar` o `tht entrenar-red` primero.")
        diseno = diseno_de(imagen)
        p, ref = c.plantilla(diseno)
        resultados, tiempos, _ = inspeccionar(leer(c.imagen(imagen)), ref, p, m)
        return jsonify(diseno=diseno, modelo=modelo_nombre, ancho=p.ancho, alto=p.alto, tiempos=tiempos,
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

    # Captura desde un celular en la red local de la mesa. Solo existe en la estación local:
    # la demostración en línea nunca recibe fotos (D-011).
    if not en_linea:
        app.config["MAX_CONTENT_LENGTH"] = LIMITE_FOTO_MB * 1024 * 1024
        candado = threading.Lock()  # dos envíos simultáneos no deben pisar el manifiesto ni el nombre

        @app.get("/capturar")
        def pagina_capturar():
            return render_template("capturar.html", disenos=disenos(), limite_mb=LIMITE_FOTO_MB)

        @app.post("/capturar")
        def subir_captura():
            fotos = [f for f in request.files.getlist("foto") if f and f.filename]
            if not fotos:
                abort(400, "Falta la foto. Use «Tomar foto» o «Elegir de la galería».")
            if len(fotos) > 1:
                abort(400, "Se recibieron dos fotos. Envíe solo una por captura.")
            f = request.form
            responsable = (f.get("responsable") or "").strip()
            if not responsable:
                abort(400, "Falta el nombre de quien captura.")
            diseno = (f.get("diseno") or "").strip()
            if diseno and diseno not in disenos():
                abort(400, f"No existe el diseño {diseno}.")
            camara = captura.CamaraMemoria(fotos[0].read(), request.headers.get("User-Agent", ""))
            with candado:
                try:
                    ruta = captura.capturar(camara, c.crudos, (f.get("tarjeta") or "").strip().upper(),
                                            (f.get("lado") or "").strip().upper(), (f.get("iluminacion") or "1").strip(),
                                            responsable, (f.get("nota") or "").strip(), diseno)
                except FileExistsError:
                    abort(409, "Ya existe una captura con ese nombre (misma tarjeta, lado e iluminación en el mismo "
                               "segundo). No se sobrescribió nada; espere un segundo y envíela otra vez.")
            diseno = diseno or (disenos()[0] if len(disenos()) == 1 else "")
            if diseno:
                return redirect(url_for("pagina_inspeccionar", imagen=ruta.name, diseno=diseno, etiquetador=responsable))
            return redirect(url_for("captura_guardada", imagen=ruta.name))

        @app.get("/capturar/<imagen>")
        def captura_guardada(imagen):
            meta = json.loads(c.imagen(imagen).with_suffix(".json").read_text(encoding="utf-8"))
            return render_template("capturada.html", imagen=imagen, meta=meta, disenos=disenos())

    @app.errorhandler(413)
    def error_tamano(e):
        return responder_error(413, f"La foto pesa más de {LIMITE_FOTO_MB} MB. Tómela con menor resolución o "
                                    "envíela desde la laptop con «tht capturar --archivo».")

    @app.errorhandler(captura.FormatoNoSoportado)
    def error_formato(e):
        return responder_error(415, str(e))

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
