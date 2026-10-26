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


def cmd_evaluar(a):
    from .datos import Carpetas
    from .linea_base import ClasificadorCentroide
    from .metricas import Caso, matriz_confusion, por_clase, resumen
    c = Carpetas(Path(a.datos)).crear()
    conj = _conjuntos(c, a.etiquetador)
    evaluado = conj[a.conjunto]
    if not evaluado:
        sys.exit(f"No hay uniones etiquetadas en el conjunto {a.conjunto}")
    modelo = ClasificadorCentroide.cargar(c.modelos / "linea_base.json")
    pred = modelo.predecir(np.stack([e.x for e in evaluado]))
    casos = [Caso(e.tarjeta, e.union_id, e.clase, p) for e, p in zip(evaluado, pred)]
    salida = {"experimento": "EXP-002", "modelo": "linea_base_centroide", "conjunto": a.conjunto,
              "resumen": resumen(casos), "por_clase": por_clase(casos), "matriz_confusion": matriz_confusion(casos)}
    ruta = c.resultados / f"EXP-002_linea_base_{a.conjunto}_{_fecha()}.json"
    ruta.write_text(_json(salida), encoding="utf-8")
    print(_json(salida["resumen"]))
    print(f"Guardado en {ruta}")


def cmd_latencia(a):
    from . import latencia
    from .datos import Carpetas
    from .flujo import inspeccionar, leer
    from .linea_base import ClasificadorCentroide
    c = Carpetas(Path(a.datos)).crear()
    plantilla, ref = c.plantilla(a.diseno)
    img = leer(a.imagen)
    modelo = ClasificadorCentroide.cargar(c.modelos / "linea_base.json")
    res = latencia.medir(lambda: inspeccionar(img, ref, plantilla, modelo), a.repeticiones)
    tam = Path(a.imagen).stat().st_size
    res["imagen"] = Path(a.imagen).name
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


def cmd_servir(a):
    from .app import crear_app
    app = crear_app(Path(a.datos), operador=a.operador)
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

    x = s.add_parser("evaluar", help="Evalúa la línea base (EXP-002)")
    x.add_argument("--datos", default="datos")
    x.add_argument("--etiquetador", default="consenso")
    x.add_argument("--conjunto", default="prueba", choices=["validacion", "prueba"])
    x.set_defaults(f=cmd_evaluar)

    x = s.add_parser("latencia", help="Mide la latencia del flujo completo (EXP-003)")
    x.add_argument("--datos", default="datos")
    x.add_argument("--imagen", required=True)
    x.add_argument("--diseno", required=True)
    x.add_argument("--repeticiones", type=int, default=30)
    x.add_argument("--nota", default="")
    x.set_defaults(f=cmd_latencia)

    x = s.add_parser("demo", help="Genera datos SINTÉTICOS para probar el software")
    x.add_argument("--salida", default="datos-demo")
    x.add_argument("--tarjetas", type=int, default=10)
    x.add_argument("--filas", type=int, default=5)
    x.add_argument("--columnas", type=int, default=8)
    x.add_argument("--semilla", type=int, default=7)
    x.set_defaults(f=cmd_demo)

    x = s.add_parser("servir", help="Abre la interfaz local de etiquetado e inspección")
    x.add_argument("--datos", default="datos")
    x.add_argument("--operador", default="")
    x.add_argument("--host", default="127.0.0.1")
    x.add_argument("--puerto", type=int, default=8000)
    x.set_defaults(f=cmd_servir)
    return p


def main(argv: list[str] | None = None) -> None:
    a = construir_parser().parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
