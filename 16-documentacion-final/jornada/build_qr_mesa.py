"""Tarjeta de la mesa con los QR de la jornada (hoja carta), en HTML y PDF.

La clave de la red de la Raspberry Pi no se guarda en el repositorio: se pasa por variable de entorno.

    CLAVE_RED='...' uv run --no-project --with segno python 16-documentacion-final/jornada/build_qr_mesa.py SALIDA.pdf

Requiere node con playwright (como el tríptico).
"""
from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import segno

RED = os.environ.get("RED", "Estacion-THT")
CLAVE = os.environ["CLAVE_RED"]
IP = os.environ.get("IP_PI", "10.42.0.1")
FUENTE = "Arial, 'Liberation Sans', sans-serif"


def svg(texto: str) -> str:
    b = io.BytesIO()
    segno.make(texto, error="m").save(b, kind="svg", omitsize=True, border=2, dark="#1f1623", xmldecl=False, svgns=True)
    return b.getvalue().decode()


def wifi(ssid: str, clave: str) -> str:
    esc = lambda s: "".join("\\" + c if c in r'\;,:"' else c for c in s)  # noqa: E731
    return f"WIFI:T:WPA;S:{esc(ssid)};P:{esc(clave)};;"


def tarjeta(n: int, titulo: str, qr: str, pie: str) -> str:
    return f'''<div class="qr"><div class="n">{n}</div><h2>{titulo}</h2>{svg(qr)}<p>{pie}</p></div>'''


def html() -> str:
    t = [
        tarjeta(1, "Conéctate a la estación", wifi(RED, CLAVE),
                f"Red <b>{RED}</b><br>Clave <b>{CLAVE}</b><br>Red local, sin internet"),
        tarjeta(2, "Inspecciona una tarjeta", f"http://{IP}:8000/capturar",
                f"Toma una foto de la hoja del mosaico<br><b>{IP}:8000/capturar</b>"),
        tarjeta(3, "Ponte a prueba", f"http://{IP}:8000/reto",
                f"¿Encuentras los defectos?<br><b>{IP}:8000/reto</b>"),
        tarjeta(4, "Conoce el proyecto", "https://femeci.foor.dev/",
                "Necesita internet: desconéctate de la estación<br><b>femeci.foor.dev</b>"),
    ]
    return f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8"><title>QR de la mesa</title><style>
@page {{ size: 279.4mm 215.9mm; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; width: 279.4mm; height: 215.9mm; font-family: {FUENTE}; color: #1f1623; padding: 12mm 12mm 10mm; display: flex; flex-direction: column; }}
.motivo {{ display: flex; height: 3mm; margin: -12mm -12mm 9mm; }} .motivo i {{ flex: 1; }}
.motivo i:nth-child(1) {{ background: #c10066; }} .motivo i:nth-child(2) {{ background: #0098d4; }}
.motivo i:nth-child(3) {{ background: #f1b400; }} .motivo i:nth-child(4) {{ background: #5f2470; }}
h1 {{ margin: 0 0 7mm; font-size: 9mm; text-align: center; }}
.fila {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 5mm; }}
.qr {{ border: 0.5mm solid #d9cfda; border-radius: 3mm; padding: 6mm 3mm 7mm; text-align: center; display: flex; flex-direction: column; align-items: center; }}
.n {{ width: 10mm; height: 10mm; border-radius: 50%; background: #c10066; color: #fff; font-weight: 700; font-size: 6mm; line-height: 10mm; }}
h2 {{ font-size: 5.6mm; margin: 3mm 0 3mm; color: #5f2470; min-height: 13mm; }}
svg {{ width: 50mm; height: 50mm; display: block; margin: 0 auto; }}
p {{ font-size: 4.2mm; line-height: 1.35; margin: 3mm 0 0; }}
.pie {{ margin-top: auto; font-size: 4mm; text-align: center; color: #3b2f3f; }}
</style></head><body><div class="motivo"><i></i><i></i><i></i><i></i></div>
<h1>Prueba la estación de inspección</h1>
<div class="fila">{"".join(t)}</div>
<p class="pie">Pasos 1 a 3: todo corre en la Raspberry Pi de la mesa, sin internet. Las fotos no salen del equipo.</p>
</body></html>"""


IMPRIMIR = r"""
const {chromium} = require('playwright');
(async () => { const [h, pdf, png] = process.argv.slice(2); const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1056, height: 816}}); await p.goto('file://' + h);
  await p.pdf({path: pdf, width: '279.4mm', height: '215.9mm', printBackground: true});
  await p.screenshot({path: png}); await b.close(); })();
"""


def main(salida: str) -> None:
    pdf = Path(salida).resolve()
    with tempfile.TemporaryDirectory() as td:
        h, js = Path(td) / "qr.html", Path.cwd() / ".imprimir-qr.js"
        h.write_text(html(), encoding="utf-8")
        js.write_text(IMPRIMIR, encoding="utf-8")
        try:
            subprocess.run(["node", str(js), str(h), str(pdf), str(pdf.with_suffix(".png"))], check=True)
        finally:
            js.unlink()
    print("OK", pdf)


if __name__ == "__main__":
    main(sys.argv[1])
