"""Línea de comandos `tht`. Ejecute `uv run tht --help`."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def _fecha() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _json(obj) -> str:
    def conv(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, tuple):
            return list(o)
        raise TypeError(type(o))
    return json.dumps(obj, ensure_ascii=False, indent=2, default=conv)


def cmd_iniciar(a):
    from .datos import Carpetas
    Carpetas(Path(a.datos)).crear()
    print(f"Carpetas creadas en {a.datos}")


def cmd_manifiesto(a):
    from . import manifiesto
    if a.accion == "generar":
        print(manifiesto.generar(Path(a.carpeta)))
    else:
        problemas = manifiesto.verificar(Path(a.carpeta))
        for d in problemas:
            print(f"{d.problema}\t{d.archivo}")
        print("Íntegro" if not problemas else f"{len(problemas)} discrepancias")
        sys.exit(1 if problemas else 0)


def cmd_capturar(a):
    from . import captura
    from .datos import Carpetas
    c = Carpetas(Path(a.datos)).crear()
    cam = captura.CamaraArchivo([Path(a.archivo)]) if a.archivo else captura.abrir(a.camara)
    try:
        ruta = captura.capturar(cam, c.crudos, a.tarjeta, a.lado, a.iluminacion, a.responsable, a.nota)
    finally:
        cam.cerrar()
    print(ruta)


def cmd_particion(a):
    from . import particion
    from .datos import Carpetas
    c = Carpetas(Path(a.datos))
    if c.particion.exists() and not a.forzar:
        sys.exit("Ya existe particion.json. El conjunto de prueba está congelado; use --forzar solo si se documenta en la bitácora.")
    tarjetas = sorted({p.parent.name for p in c.imagenes()})
    asignacion = particion.particionar(tarjetas, semilla=a.semilla)
    datos = particion.guardar(asignacion, c.particion, a.semilla, a.nota)
    print(_json(datos))


def cmd_acuerdo(a):
    from .anotaciones import comparar, todas
    from .datos import Carpetas
    c = Carpetas(Path(a.datos))
    anot = todas(c.anotaciones)
    comp = comparar([x for x in anot if x.etiquetador == a.a], [x for x in anot if x.etiquetador == a.b])
    print(_json({"uniones": comp.uniones, "acuerdos": comp.acuerdos, "kappa": comp.kappa,
                 "discrepancias": comp.discrepancias}))


def _conjuntos(c, etiquetador):
    from . import particion
    from .datos import ejemplos
    asignacion = particion.cargar(c.particion)
    ej = ejemplos(c, etiquetador)
    sin_asignar = sorted({e.tarjeta for e in ej} - set(asignacion))
    if sin_asignar:
        sys.exit(f"Tarjetas sin partición: {', '.join(sin_asignar)}")
    return {k: [e for e in ej if asignacion[e.tarjeta] == k] for k in ("entrenamiento", "validacion", "prueba")}


def cmd_entrenar(a):
    from .datos import Carpetas
    from .linea_base import ClasificadorCentroide
    c = Carpetas(Path(a.datos)).crear()
    conj = _conjuntos(c, a.etiquetador)
    ent = conj["entrenamiento"] + (conj["validacion"] if a.con_validacion else [])
    modelo = ClasificadorCentroide.entrenar(np.stack([e.x for e in ent]), [e.clase for e in ent])
    ruta = c.modelos / "linea_base.json"
    modelo.guardar(ruta)
    print(f"Modelo entrenado con {len(ent)} uniones: {ruta}")


def _evaluar_modelo(modelo, evaluado):
    from .metricas import Caso, matriz_confusion, por_clase, resumen
    pred, puntajes = modelo.evaluar_recortes([e.recorte for e in evaluado])
    casos = [Caso(e.tarjeta, e.union_id, e.clase, p) for e, p in zip(evaluado, pred)]
    return {"resumen": resumen(casos), "por_clase": por_clase(casos), "matriz_confusion": matriz_confusion(casos)}


def cmd_evaluar(a):
    from . import clasificador
    from .datos import Carpetas
    c = Carpetas(Path(a.datos)).crear()
    conj = _conjuntos(c, a.etiquetador)
    evaluado = conj[a.conjunto]
    if not evaluado:
        sys.exit(f"No hay uniones etiquetadas en el conjunto {a.conjunto}")
    salida = {"experimento": "EXP-002", "modelo": a.modelo, "conjunto": a.conjunto}
    if a.modelo == "red":
        semillas = sorted(c.modelos.glob("red_s*.onnx"))
        if not semillas:
            sys.exit("No hay modelos red_s*.onnx. Ejecute `uv run --group cnn tht entrenar-red` primero.")
        por_semilla = {}
        for ruta in semillas:
            por_semilla[ruta.stem] = _evaluar_modelo(clasificador.cargar(c.modelos, "red", ruta), evaluado)
        sens = [r["resumen"]["sensibilidad"] for r in por_semilla.values()]
        fa = [r["resumen"]["falsas_alarmas"] for r in por_semilla.values()]
        salida["por_semilla"] = por_semilla
        salida["entre_semillas"] = {"sensibilidad_media": float(np.mean(sens)), "sensibilidad_de": float(np.std(sens)),
                                    "falsas_alarmas_media": float(np.mean(fa)), "falsas_alarmas_de": float(np.std(fa))}
        salida["modelo_elegido_por_validacion"] = _evaluar_modelo(clasificador.cargar(c.modelos, "red"), evaluado)
        mostrar = {"entre_semillas": salida["entre_semillas"],
                   "elegido": salida["modelo_elegido_por_validacion"]["resumen"]}
    else:
        salida.update(_evaluar_modelo(clasificador.cargar(c.modelos, "linea_base"), evaluado))
        mostrar = salida["resumen"]
    ruta = c.resultados / f"EXP-002_{a.modelo}_{a.conjunto}_{_fecha()}.json"
    ruta.write_text(_json(salida), encoding="utf-8")
    print(_json(mostrar))
    print(f"Guardado en {ruta}")


def cmd_entrenar_red(a):
    import shutil
    from .datos import Carpetas
    from .entrenamiento_red import entrenar, exportar
    c = Carpetas(Path(a.datos)).crear()
    conj = _conjuntos(c, a.etiquetador)
    ent, val = conj["entrenamiento"], conj["validacion"]
    if not ent or not val:
        sys.exit("Se necesitan uniones etiquetadas en entrenamiento y en validación")
    mejor = None
    for s in a.semillas:
        res = entrenar([e.recorte for e in ent], [e.clase for e in ent], [e.recorte for e in val], [e.clase for e in val],
                       semilla=s, arquitectura=a.arquitectura, epocas=a.epocas)
        ruta = exportar(res, c.modelos / f"red_s{s}.onnx", a.nota, n_entrenamiento=len(ent))
        print(f"Semilla {s}: mejor época {res.mejor_epoca}, exactitud balanceada en validación "
              f"{res.val_exactitud_balanceada:.3f} -> {ruta.name}")
        if mejor is None or res.val_exactitud_balanceada > mejor[0]:
            mejor = (res.val_exactitud_balanceada, ruta)
    shutil.copyfile(mejor[1], c.modelos / "red.onnx")
    shutil.copyfile(mejor[1].with_suffix(".json"), c.modelos / "red.json")
    print(f"Modelo en uso (elegido por validación, no por prueba): {mejor[1].name} -> red.onnx")


def cmd_latencia(a):
    from . import latencia
    from .datos import Carpetas
    from . import clasificador
    from .flujo import inspeccionar, leer
    c = Carpetas(Path(a.datos)).crear()
    plantilla, ref = c.plantilla(a.diseno)
    img = leer(a.imagen)
    modelo = clasificador.cargar(c.modelos, a.modelo)
    res = latencia.medir(lambda: inspeccionar(img, ref, plantilla, modelo), a.repeticiones)
    tam = Path(a.imagen).stat().st_size
    res["imagen"] = Path(a.imagen).name
    res["modelo"] = a.modelo
    res["bytes_imagen"] = tam
    res["subida_estimada_s"] = {f"{m} Mbit/s": latencia.subida_estimada(tam, m) for m in (5, 20, 100)}
    ruta = latencia.guardar(res, c.resultados / f"EXP-003_latencia_{_fecha()}.json", a.nota)
    print(_json({k: v for k, v in res.items() if k != "tiempos_s"}))
    print(f"Guardado en {ruta}")


def cmd_demo(a):
    """Genera un conjunto SINTÉTICO para probar el software (no es DS-01)."""
    import cv2
    from . import sintetico
    from .anotaciones import Anotacion
    from .datos import Carpetas
    c = Carpetas(Path(a.salida)).crear()
    rng = np.random.default_rng(a.semilla)
    ref, plantilla, _ = sintetico.tarjeta(a.filas, a.columnas, rng, prob_defecto=0.0, diseno="sintetica-01")
    cv2.imwrite(str(c.plantillas / plantilla.referencia), ref)
    plantilla.guardar(c.plantillas / "sintetica-01.json")
    for i in range(1, a.tarjetas + 1):
        t = f"T{i:02d}"
        img, _, verdad = sintetico.tarjeta(a.filas, a.columnas, rng, prob_defecto=0.35)
        img = sintetico.desplazar(img, rng.uniform(-10, 10), rng.uniform(-10, 10), rng.uniform(-0.8, 0.8))
        nombre = f"{t}_B_il1_SINTETICO.png"
        (c.crudos / t).mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(c.crudos / t / nombre), img)
        an = Anotacion(nombre, t, "sintetica-01", "consenso")
        for uid, clase in verdad.items():
            an.poner(uid, clase)
        an.guardar(c.anotaciones)
    (c.raiz / "LEEME_SINTETICO.txt").write_text(
        "Datos SINTÉTICOS generados por `tht demo` para probar el software.\n"
        "No son datos del proyecto y no deben reportarse como resultados.\n", encoding="utf-8")
    print(f"Conjunto sintético en {c.raiz} ({a.tarjetas} tarjetas)")


def cmd_externo(a):
    """EXP-006: entrena y evalúa ambos modelos con datos públicos reales."""
    from collections import Counter
    from . import externos
    from .linea_base import ClasificadorCentroide, caracteristicas
    from .metricas import Caso, matriz_confusion, por_clase, resumen
    if a.accion == "descargar":
        zip_ = externos.descargar(Path(a.ruta))
        print(f"Descargado y verificado: {zip_}")
        print(f"Extraído en: {externos.extraer(zip_, Path(a.ruta) / 'extraido')}")
        return
    muestras = externos.leer_pcbspdefect(Path(a.ruta))
    imgs = externos.cargar_imagenes(muestras)
    salida = {"experimento": "EXP-006", "datos": "PCBSPDefect b_dip", "cita": externos.CITA_PCBSPDEFECT,
              "sha256_zip": externos.SHA256_PCBSPDEFECT, "fecha_utc": _fecha(), "particiones": {}}
    for particion in a.particiones:
        conj = externos.asignar(muestras, particion)
        sel = {k: [i for i, c in enumerate(conj) if c == k] for k in ("entrenamiento", "validacion", "prueba")}
        info = {k: {"imagenes": len(v), "uniones": len({muestras[i].union for i in v}),
                    "tarjetas": len({muestras[i].tarjeta for i in v}),
                    "clases": dict(Counter(muestras[i].clase for i in v))} for k, v in sel.items()}
        casos_de = lambda pred: [Caso(muestras[i].tarjeta, f"{muestras[i].union}_{muestras[i].luz}", muestras[i].clase, p)
                                 for i, p in zip(sel["prueba"], pred)]
        bloque = {"conjuntos": info}
        X = np.stack([caracteristicas(im) for im in imgs])
        base = ClasificadorCentroide.entrenar(X[sel["entrenamiento"]], [muestras[i].clase for i in sel["entrenamiento"]])
        cs = casos_de(base.predecir(X[sel["prueba"]]))
        bloque["linea_base"] = {"resumen": resumen(cs), "por_clase": por_clase(cs), "matriz_confusion": matriz_confusion(cs)}
        print(f"[{particion}] línea base: sensibilidad {bloque['linea_base']['resumen']['sensibilidad']:.3f}, "
              f"falsas alarmas {bloque['linea_base']['resumen']['falsas_alarmas']:.3f}")
        if a.sin_red:
            salida["particiones"][particion] = bloque
            continue
        from .clasificador import ClasificadorONNX
        from .entrenamiento_red import entrenar, exportar
        import tempfile
        semillas, mejor = {}, None
        with tempfile.TemporaryDirectory() as td:
            for s in a.semillas:
                res = entrenar([imgs[i] for i in sel["entrenamiento"]], [muestras[i].clase for i in sel["entrenamiento"]],
                               [imgs[i] for i in sel["validacion"]], [muestras[i].clase for i in sel["validacion"]],
                               semilla=s, epocas=a.epocas)
                ruta = exportar(res, Path(td) / f"red_s{s}.onnx", f"EXP-006 {particion}", len(sel["entrenamiento"]))
                pred, _ = ClasificadorONNX(ruta).evaluar_recortes([imgs[i] for i in sel["prueba"]])
                cs = casos_de(pred)
                semillas[f"s{s}"] = {"val_exactitud_balanceada": res.val_exactitud_balanceada, "mejor_epoca": res.mejor_epoca,
                                     "resumen": resumen(cs), "por_clase": por_clase(cs), "matriz_confusion": matriz_confusion(cs)}
                print(f"[{particion}] red semilla {s}: val {res.val_exactitud_balanceada:.3f}, prueba sensibilidad "
                      f"{semillas[f's{s}']['resumen']['sensibilidad']:.3f}, falsas alarmas {semillas[f's{s}']['resumen']['falsas_alarmas']:.3f}")
                if mejor is None or res.val_exactitud_balanceada > mejor[1]:
                    mejor = (f"s{s}", res.val_exactitud_balanceada)
                    if a.guardar_modelo:
                        import shutil
                        Path(a.guardar_modelo).mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(ruta, Path(a.guardar_modelo) / f"red_pcbspdefect_{particion}.onnx")
                        shutil.copyfile(ruta.with_suffix(".json"), Path(a.guardar_modelo) / f"red_pcbspdefect_{particion}.json")
        sens = [v["resumen"]["sensibilidad"] for v in semillas.values()]
        fa = [v["resumen"]["falsas_alarmas"] for v in semillas.values()]
        bloque["red"] = {"por_semilla": semillas, "elegida_por_validacion": mejor[0],
                         "entre_semillas": {"sensibilidad_media": float(np.mean(sens)), "sensibilidad_de": float(np.std(sens)),
                                            "falsas_alarmas_media": float(np.mean(fa)), "falsas_alarmas_de": float(np.std(fa))}}
        salida["particiones"][particion] = bloque
    Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
    Path(a.salida).write_text(_json(salida), encoding="utf-8")
    print(f"Guardado en {a.salida}")


def cmd_servir(a):
    from .app import crear_app
    app = crear_app(Path(a.datos), operador=a.operador, modelo_nombre=a.modelo)
    print(f"Abrir http://{a.host}:{a.puerto} (sin internet; solo en esta red)")
    app.run(host=a.host, port=a.puerto, debug=False)


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tht", description="Estación de inspección asistida de uniones through-hole")
    s = p.add_subparsers(dest="comando", required=True)

    x = s.add_parser("iniciar", help="Crea la estructura de carpetas de datos")
    x.add_argument("--datos", default="datos")
    x.set_defaults(f=cmd_iniciar)

    x = s.add_parser("manifiesto", help="Genera o verifica las huellas SHA-256")
    x.add_argument("accion", choices=["generar", "verificar"])
    x.add_argument("carpeta")
    x.set_defaults(f=cmd_manifiesto)

    x = s.add_parser("capturar", help="Captura una imagen con nombre, metadatos y huella")
    x.add_argument("--datos", default="datos")
    x.add_argument("--tarjeta", required=True)
    x.add_argument("--lado", choices=["A", "B"], required=True)
    x.add_argument("--iluminacion", default="1")
    x.add_argument("--responsable", required=True)
    x.add_argument("--camara", default="auto", choices=["auto", "picamera2", "opencv"])
    x.add_argument("--archivo", help="Tomar la imagen de un archivo en lugar de la cámara")
    x.add_argument("--nota", default="")
    x.set_defaults(f=cmd_capturar)

    x = s.add_parser("particion", help="Parte por tarjeta y congela el conjunto de prueba")
    x.add_argument("--datos", default="datos")
    x.add_argument("--semilla", type=int, default=20261026)
    x.add_argument("--nota", default="")
    x.add_argument("--forzar", action="store_true")
    x.set_defaults(f=cmd_particion)

    x = s.add_parser("acuerdo", help="Kappa de Cohen entre dos etiquetadores")
    x.add_argument("--datos", default="datos")
    x.add_argument("--a", required=True)
    x.add_argument("--b", required=True)
    x.set_defaults(f=cmd_acuerdo)

    x = s.add_parser("entrenar", help="Entrena la línea base clásica")
    x.add_argument("--datos", default="datos")
    x.add_argument("--etiquetador", default="consenso")
    x.add_argument("--con-validacion", action="store_true")
    x.set_defaults(f=cmd_entrenar)

    x = s.add_parser("entrenar-red", help="Entrena el clasificador ligero (requiere uv sync --group cnn)")
    x.add_argument("--datos", default="datos")
    x.add_argument("--etiquetador", default="consenso")
    x.add_argument("--semillas", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    x.add_argument("--epocas", type=int, default=40)
    x.add_argument("--arquitectura", default="pequena", choices=["pequena", "mobilenet"])
    x.add_argument("--nota", default="")
    x.set_defaults(f=cmd_entrenar_red)

    x = s.add_parser("evaluar", help="Evalúa un modelo en validación o prueba (EXP-002)")
    x.add_argument("--datos", default="datos")
    x.add_argument("--modelo", default="linea_base", choices=["linea_base", "red"])
    x.add_argument("--etiquetador", default="consenso")
    x.add_argument("--conjunto", default="prueba", choices=["validacion", "prueba"])
    x.set_defaults(f=cmd_evaluar)

    x = s.add_parser("latencia", help="Mide la latencia del flujo completo (EXP-003)")
    x.add_argument("--datos", default="datos")
    x.add_argument("--imagen", required=True)
    x.add_argument("--diseno", required=True)
    x.add_argument("--repeticiones", type=int, default=30)
    x.add_argument("--modelo", default="linea_base", choices=["linea_base", "red"])
    x.add_argument("--nota", default="")
    x.set_defaults(f=cmd_latencia)

    x = s.add_parser("demo", help="Genera datos SINTÉTICOS para probar el software")
    x.add_argument("--salida", default="datos-demo")
    x.add_argument("--tarjetas", type=int, default=10)
    x.add_argument("--filas", type=int, default=5)
    x.add_argument("--columnas", type=int, default=8)
    x.add_argument("--semilla", type=int, default=7)
    x.set_defaults(f=cmd_demo)

    x = s.add_parser("externo", help="EXP-006: datos públicos reales (PCBSPDefect)")
    x.add_argument("accion", choices=["descargar", "evaluar"])
    x.add_argument("--ruta", required=True, help="Carpeta de descarga o carpeta extraída")
    x.add_argument("--particiones", nargs="+", default=["oficial", "tarjeta"], choices=["oficial", "tarjeta"])
    x.add_argument("--semillas", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    x.add_argument("--epocas", type=int, default=40)
    x.add_argument("--sin-red", action="store_true")
    x.add_argument("--guardar-modelo", help="Carpeta donde guardar la red elegida por validación")
    x.add_argument("--salida", default="resultados/EXP-006.json")
    x.set_defaults(f=cmd_externo)

    x = s.add_parser("servir", help="Abre la interfaz local de etiquetado e inspección")
    x.add_argument("--datos", default="datos")
    x.add_argument("--operador", default="")
    x.add_argument("--modelo", default="linea_base", choices=["linea_base", "red"])
    x.add_argument("--host", default="127.0.0.1")
    x.add_argument("--puerto", type=int, default=8000)
    x.set_defaults(f=cmd_servir)
    return p


def main(argv: list[str] | None = None) -> None:
    a = construir_parser().parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
