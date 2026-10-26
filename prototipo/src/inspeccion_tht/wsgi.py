"""Punto de entrada para un servidor de demostración en la nube (por ejemplo, Railway).

La estación real corre en local y sin internet. Esta demostración pública:
- usa la carpeta THT_DATOS (un volumen persistente);
- si la carpeta está vacía, genera datos SINTÉTICOS, congela la partición y entrena
  la línea base, para que la interfaz se pueda revisar sin tarjetas;
- si existen THT_USUARIO y THT_CLAVE, pide usuario y contraseña (HTTP Basic).

Nunca se suben aquí imágenes de terceros (D-011).
"""

import hmac
import os
from pathlib import Path

from flask import Response, request

from .app import crear_app
from .cli import main as tht


def _preparar(raiz: Path) -> None:
    if (raiz / "crudos").exists() and any((raiz / "crudos").rglob("*.png")):
        return
    tht(["demo", "--salida", str(raiz), "--tarjetas", "12"])
    tht(["particion", "--datos", str(raiz), "--nota", "Demostración sintética"])
    tht(["entrenar", "--datos", str(raiz)])


def crear() -> "object":
    raiz = Path(os.environ.get("THT_DATOS", "/data/tht"))
    raiz.mkdir(parents=True, exist_ok=True)
    _preparar(raiz)
    app = crear_app(raiz, operador=os.environ.get("THT_OPERADOR", ""),
                    modelo_nombre=os.environ.get("THT_MODELO", "linea_base"), en_linea=True)
    usuario, clave = os.environ.get("THT_USUARIO"), os.environ.get("THT_CLAVE")
    if usuario and clave:
        @app.before_request
        def pedir_credenciales():
            if request.path == "/salud":
                return None
            a = request.authorization
            if a and hmac.compare_digest(a.username or "", usuario) and hmac.compare_digest(a.password or "", clave):
                return None
            return Response("Se requiere usuario y contraseña.", 401,
                            {"WWW-Authenticate": 'Basic realm="Estacion THT"'})
    return app


app = crear()
