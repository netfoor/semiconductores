"""Genera el cartel de la jornada (90 x 120 cm, vertical) en HTML y PDF.

Los números salen de prototipo/src/inspeccion_tht/publico/resultados.json (EXP-006),
no se escriben a mano. Uso, desde la raíz del repositorio:

    uv run --no-project --with segno python 16-documentacion-final/cartel/build_cartel.py

Escribe cartel-v1.html, cartel-v1.pdf y cartel-v1-vista.png junto a este archivo.
El PDF se imprime con Chromium (Playwright), a tamaño real.
"""

from __future__ import annotations

import base64
import html
import json
import subprocess
from pathlib import Path

import segno

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
PUBLICO = RAIZ / "prototipo/src/inspeccion_tht/publico"
URL = "https://femeci.foor.dev"

# Una foto de ejemplo por clase, del conjunto de prueba de PCBSPDefect (CC BY 4.0).
EJEMPLOS = [
    ("aceptable", "036.jpg", "Aceptable"),
    ("insuficiente", "004.jpg", "Insuficiente"),
    ("puente", "039.jpg", "Puente"),
    ("sin_soldar", "026.jpg", "Sin soldar"),
    ("exceso", "041.jpg", "Exceso"),
]

AZUL, MAGENTA = "#0086c0", "#d4006f"  # línea base (cuadro) y red (círculo), validados para daltonismo
TINTA, TINTA2, GRIS, LINEA = "#2b1d30", "#57485b", "#766c7a", "#d9cfda"


def f2(x: float) -> str:
    return f"{x:.2f}"


def datos_uri(ruta: Path, tipo: str) -> str:
    return f"data:{tipo};base64,{base64.b64encode(ruta.read_bytes()).decode()}"


def grafica(filas: list[dict], metas: dict, fuente: str = "InterCartel, sans-serif",
            etiqueta_w: int = 175, panel_w: int = 300, hueco: int = 45, nota: bool = True) -> str:
    """Dos paneles de puntos con IC (sensibilidad y falsas alarmas). Unidades del SVG: mm."""
    fila_h, cab = 34, 30
    orden = [("oficial", "linea_base"), ("oficial", "red"), ("tarjeta", "linea_base"), ("tarjeta", "red")]
    por = {(f["particion"], f["modelo"]): f for f in filas}
    alto = cab + fila_h * 4 + 14 + 20
    ancho = etiqueta_w + 2 * panel_w + hueco + 8
    s = [f'<svg viewBox="0 0 {ancho} {alto}" width="{ancho}mm" height="{alto}mm" '
         f'font-family="{fuente}" role="img" aria-label="Resultados de EXP-006">']
    paneles = [
        ("Sensibilidad", "sensibilidad", metas["sensibilidad_min"], "meta M1 ≥ 0.90", "más alto es mejor"),
        ("Falsas alarmas", "falsas_alarmas", metas["falsas_alarmas_max"], "meta M2 ≤ 0.15", "más bajo es mejor"),
    ]
    y0 = cab
    # Etiquetas de fila y separador de particiones
    nombres = {"linea_base": "Línea base", "red": "Red"}
    particiones = {"oficial": "Partición oficial", "tarjeta": "Partición por tarjeta"}
    for i, (part, mod) in enumerate(orden):
        y = y0 + fila_h * i + fila_h / 2
        if mod == "linea_base":
            s.append(f'<text x="0" y="{y + fila_h / 2 + 3}" font-size="8.5" font-weight="700" fill="{TINTA}">'
                     f'{particiones[part]}</text>')
            if i:
                s.append(f'<line x1="0" x2="{ancho}" y1="{y0 + fila_h * i}" y2="{y0 + fila_h * i}" '
                         f'stroke="{LINEA}" stroke-width="0.6"/>')
        s.append(f'<text x="{etiqueta_w - 10}" y="{y + 3}" font-size="9.5" text-anchor="end" '
                 f'fill="{TINTA2}">{nombres[mod]}</text>')
    for p, (titulo, clave, meta, texto_meta, sentido) in enumerate(paneles):
        x0 = etiqueta_w + p * (panel_w + hueco)
        esc = lambda v: x0 + v * panel_w  # noqa: E731
        s.append(f'<text x="{x0}" y="10" font-size="11" font-weight="800" fill="{TINTA}">{titulo}</text>')
        s.append(f'<text x="{x0}" y="20" font-size="7.5" fill="{GRIS}">{sentido}</text>')
        base = y0 + fila_h * 4
        for t in (0, 0.25, 0.5, 0.75, 1.0):
            s.append(f'<line x1="{esc(t)}" x2="{esc(t)}" y1="{y0}" y2="{base}" stroke="{LINEA}" stroke-width="0.4"/>')
            s.append(f'<text x="{esc(t)}" y="{base + 10}" font-size="7.5" text-anchor="middle" fill="{GRIS}">'
                     f'{t:g}</text>')
        s.append(f'<line x1="{esc(meta)}" x2="{esc(meta)}" y1="{y0 - 4}" y2="{base}" stroke="{TINTA}" '
                 f'stroke-width="0.9" stroke-dasharray="3 2.2"/>')
        ancla = "end" if meta > 0.5 else "start"
        dx = -2.5 if meta > 0.5 else 2.5
        s.append(f'<text x="{esc(meta) + dx}" y="{y0 - 1}" font-size="7.5" font-weight="700" text-anchor="{ancla}" '
                 f'fill="{TINTA}">{texto_meta}</text>')
        for i, key in enumerate(orden):
            fila = por[key]
            y = y0 + fila_h * i + fila_h / 2
            v, (lo, hi) = fila[clave], fila[clave + "_ic"]
            color = AZUL if key[1] == "linea_base" else MAGENTA
            s.append(f'<line x1="{esc(lo)}" x2="{esc(hi)}" y1="{y}" y2="{y}" stroke="{color}" '
                     f'stroke-width="1.6" stroke-linecap="round"/>')
            if key[1] == "linea_base":
                s.append(f'<rect x="{esc(v) - 4}" y="{y - 4}" width="8" height="8" rx="1" fill="{color}" '
                         f'stroke="#fff" stroke-width="1.2"/>')
            else:
                s.append(f'<circle cx="{esc(v)}" cy="{y}" r="4.6" fill="{color}" stroke="#fff" stroke-width="1.2"/>')
            # Valor a la derecha del intervalo (cabe aun con el límite en 1.0, en el hueco entre paneles)
            s.append(f'<text x="{esc(hi) + 4}" y="{y + 3}" font-size="8.5" font-weight="700" fill="{TINTA}" stroke="#fff" stroke-width="2.2" paint-order="stroke">'
                     f'{f2(v)}</text>')
    if nota:
        s.append(f'<text x="{etiqueta_w}" y="{alto - 2}" font-size="7.5" fill="{GRIS}">Punto: valor medido. '
                 'Línea: intervalo de confianza de 95 % (bootstrap agrupado por tarjeta, 2000 repeticiones).</text>')
    s.append("</svg>")
    return "".join(s)


def construir() -> str:
    r = json.loads((PUBLICO / "resultados.json").read_text(encoding="utf-8"))
    fotos = json.loads((PUBLICO / "fotos.json").read_text(encoding="utf-8"))
    por = {(f["particion"], f["modelo"]): f for f in r["filas"]}
    lb, red = por[("oficial", "linea_base")], por[("oficial", "red")]
    clases = r["clases"]
    m_lb = r["matrices"]["oficial"]["linea_base"]["matriz"]
    m_red = r["matrices"]["oficial"]["red"]["matriz"]
    ia = clases.index("aceptable")
    conf = {c: (m_lb[clases.index(c)][ia], m_red[clases.index(c)][ia], sum(m_lb[clases.index(c)]))
            for c in ("exceso", "puente")}
    qr = segno.make(URL, error="m").svg_inline(scale=1, border=0, dark=TINTA, omitsize=True)

    ejemplos = "".join(
        f'<figure><img src="{datos_uri(PUBLICO / "fotos" / archivo, "image/jpeg")}" alt="Unión con clase {nombre}">'
        f'<figcaption><i class="c-{clase}"></i>{nombre}</figcaption></figure>'
        for clase, archivo, nombre in EJEMPLOS
    )
    e = html.escape
    return f"""<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><title>Cartel FEMECI 2026 — Estación THT</title>
<style>
@page {{ size: 900mm 1200mm; margin: 0; }}
/* Inter en TrueType estática (OFL 1.1, fuentes/OFL.txt): así el PDF incrusta fuentes normales y no Type 3 */
@font-face {{ font-family: InterCartel; src: url(fuentes/Inter-400.ttf) format('truetype'); font-weight: 400; }}
@font-face {{ font-family: InterCartel; src: url(fuentes/Inter-600.ttf) format('truetype'); font-weight: 600; }}
@font-face {{ font-family: InterCartel; src: url(fuentes/Inter-700.ttf) format('truetype'); font-weight: 700; }}
@font-face {{ font-family: InterCartel; src: url(fuentes/Inter-800.ttf) format('truetype'); font-weight: 800; }}
@font-face {{ font-family: InterCartel; src: url(fuentes/Inter-400-italica.ttf) format('truetype'); font-weight: 400; font-style: italic; }}
:root {{ --tinta:{TINTA}; --tinta-2:{TINTA2}; --gris:{GRIS}; --linea:{LINEA}; --banda:#f7f3f7;
  --marca:#d4006f; --marca-profunda:#9c0051; --acento:#6c2a7c; --cian:#0098d4; --amarillo:#f1b400; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: #fff; }}
body {{ width: 900mm; height: 1200mm; font-family: InterCartel, sans-serif; color: var(--tinta);
  font-size: 9.6mm; line-height: 1.38; display: flex; flex-direction: column; overflow: hidden; }}
.motivo {{ display: flex; height: 9mm; flex: none; }}
.motivo i {{ flex: 1; }}
.motivo i:nth-child(1) {{ background: var(--marca); }} .motivo i:nth-child(2) {{ background: var(--cian); }}
.motivo i:nth-child(3) {{ background: var(--amarillo); }} .motivo i:nth-child(4) {{ background: var(--acento); }}
.hoja {{ flex: 1; padding: 22mm 40mm 20mm; display: flex; flex-direction: column; gap: 12mm; }}
.sobre {{ display: flex; justify-content: space-between; font-size: 7.6mm; font-weight: 600; color: var(--acento); }}
h1 {{ font-size: 44mm; line-height: 0.98; letter-spacing: -0.035em; margin: 3mm 0 7mm; font-weight: 800; }}
h1 span {{ color: var(--marca); }}
.titulo-formal {{ font-size: 10.2mm; color: var(--tinta-2); margin: 0 0 7mm; max-width: 760mm; line-height: 1.3; }}
.equipo {{ font-size: 8.4mm; color: var(--tinta-2); margin: 0; }}
.equipo b {{ color: var(--tinta); }}
h2 {{ font-size: 15mm; letter-spacing: -0.02em; margin: 0 0 5mm; color: var(--acento); line-height: 1.1; }}
p {{ margin: 0 0 4mm; }}
.dos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 22mm; }}
.cifra {{ font-size: 30mm; font-weight: 800; line-height: 1; color: var(--marca); letter-spacing: -0.01em; }}
.cifra-pie {{ font-size: 8mm; color: var(--tinta-2); margin-top: 2mm; }}
.pregunta {{ font-size: 11mm; font-weight: 700; line-height: 1.3; border-left: 3mm solid var(--marca); padding-left: 8mm; }}
.metas {{ width: 100%; border-collapse: collapse; font-size: 8.4mm; margin-top: 5mm; }}
.metas td {{ padding: 2.6mm 0; border-top: 0.5mm solid var(--linea); vertical-align: top; }}
.metas td:first-child {{ font-weight: 800; width: 20mm; color: var(--acento); }}
.metas td:last-child {{ text-align: right; white-space: nowrap; font-weight: 700; }}
.banda {{ background: var(--banda); margin: 0 -40mm; padding: 13mm 40mm; }}
.pasos {{ list-style: none; display: grid; grid-template-columns: repeat(5, 1fr); gap: 7mm; margin: 6mm 0 0; padding: 0; counter-reset: p; }}
.pasos li {{ counter-increment: p; border-top: 2mm solid var(--marca); padding-top: 4mm; font-size: 7.8mm; line-height: 1.3; color: var(--tinta-2); }}
.pasos li:last-child {{ border-color: var(--acento); }}
.pasos li::before {{ content: counter(p); display: block; font-size: 13mm; font-weight: 800; color: var(--marca); line-height: 1; }}
.pasos li:last-child::before {{ color: var(--acento); }}
.pasos b {{ display: block; color: var(--tinta); font-size: 9mm; margin: 2mm 0; }}
.ejemplos {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 7mm; margin-top: 9mm; }}
.ejemplos figure {{ margin: 0; }}
.ejemplos img {{ width: 100%; aspect-ratio: 1; display: block; image-rendering: auto; }}
.ejemplos figcaption {{ font-size: 7.8mm; font-weight: 700; margin-top: 2.5mm; display: flex; align-items: center; gap: 3mm; }}
.ejemplos i {{ width: 5mm; height: 5mm; display: inline-block; border: 1.1mm solid; }}
.c-aceptable {{ border-color:#2e8b45 !important; border-style: dotted !important; }} .c-insuficiente {{ border-color:#c26a00; }}
.c-puente {{ border-color:#d4006f; }} .c-sin_soldar {{ border-color:#0076a8; border-style: dashed !important; }}
.c-exceso {{ border-color:#9a7200; border-style: double !important; border-width: 1.6mm !important; }}
.pie-foto {{ font-size: 6.2mm; color: var(--gris); margin-top: 3mm; }}
.resultados-cab {{ display: flex; justify-content: space-between; align-items: end; gap: 15mm; }}
.leyenda {{ display: flex; gap: 10mm; font-size: 8mm; color: var(--tinta-2); white-space: nowrap; }}
.leyenda span {{ display: inline-flex; align-items: center; gap: 3mm; }}
.leyenda .cuadro {{ width: 6mm; height: 6mm; background: {AZUL}; border-radius: 0.8mm; }}
.leyenda .circulo {{ width: 7mm; height: 7mm; background: {MAGENTA}; border-radius: 50%; }}
.grafica {{ margin-top: 5mm; }}
.lecturas {{ display: grid; grid-template-columns: 1fr 1fr 1.25fr; gap: 14mm; margin-top: 8mm; }}
.lecturas p {{ font-size: 8.3mm; line-height: 1.33; color: var(--tinta-2); }}
.lecturas b {{ color: var(--tinta); }}
.fin {{ display: grid; grid-template-columns: 1.55fr 1fr; gap: 22mm; align-items: start; }}
.estado {{ list-style: none; margin: 0; padding: 0; font-size: 8.3mm; }}
.estado li {{ display: grid; grid-template-columns: 38mm 1fr; gap: 5mm; padding: 2.6mm 0; border-top: 0.5mm solid var(--linea); }}
.estado b {{ color: var(--acento); }}
.estado .hecho b {{ color: var(--marca); }}
.qr {{ display: grid; grid-template-columns: 82mm 1fr; gap: 9mm; align-items: center; }}
.qr svg {{ width: 82mm; height: 82mm; display: block; }}
.qr p {{ font-size: 8.3mm; line-height: 1.32; margin: 0 0 3mm; }}
.url {{ font-weight: 800; color: var(--marca-profunda); font-size: 9mm; }}
.nota {{ font-size: 7.4mm; color: var(--tinta-2); line-height: 1.32; margin-top: 7mm; }}
.refs {{ margin-top: auto; border-top: 0.6mm solid var(--linea); padding-top: 6mm; font-size: 5.6mm; line-height: 1.36; color: var(--gris); columns: 2; column-gap: 16mm; }}
.refs p {{ margin: 0 0 2.2mm; padding-left: 6mm; text-indent: -6mm; break-inside: avoid; }}
.refs .titulo-refs {{ font-weight: 800; color: var(--tinta-2); text-indent: 0; padding: 0; }}
</style></head>
<body>
<div class="motivo" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<main class="hoja">

<header>
  <div class="sobre"><span>FEMECI Capítulo Puebla 2026</span><span>Ingenierías: Sistemas Informáticos y Computación</span></div>
  <h1>Una segunda mirada<br>para cada <span>soldadura</span></h1>
  <p class="titulo-formal">Estación de inspección visual asistida con procesamiento local para uniones soldadas through-hole en el ensamble electrónico: diseño y validación experimental de un prototipo</p>
  <p class="equipo"><b>Fortino Romero Mantilla, Israel Jesús García Osorio y María José de la Rosa Hernández.</b>
  Asesor: José Francisco Espinosa Garita. Universidad Tecnológica de Puebla.</p>
</header>

<section class="dos">
  <div>
    <h2>El problema</h2>
    <p>En el ensamble electrónico, muchas uniones through-hole se revisan a ojo. La inspección visual humana deja pasar entre 20&nbsp;% y 30&nbsp;% de los defectos en la mayoría de las tareas (See, 2015).</p>
    <p>Personal técnico de una empresa de ensamble de Puebla nos contó que la validación de piezas conserva pasos manuales y que, cuando algo falla, se revisa con más resolución a ojo humano.</p>
  </div>
  <div>
    <h2>El reto</h2>
    <p class="pregunta">¿Puede una estación de bajo costo, sin internet, señalar las uniones sospechosas con una sensibilidad y una tasa de falsas alarmas medidas y aceptables?</p>
    <table class="metas">
      <tr><td>M1</td><td>Sensibilidad para cualquier defecto</td><td>≥ 0.90</td></tr>
      <tr><td>M2</td><td>Falsas alarmas</td><td>≤ 0.15</td></tr>
      <tr><td>M4</td><td>Tiempo por tarjeta en Raspberry Pi 5</td><td>≤ 5 s</td></tr>
      <tr><td>M5</td><td>Funciona con la red desconectada</td><td>100 %</td></tr>
    </table>
  </div>
</section>

<section class="banda">
  <h2>La propuesta: el sistema señala, la persona decide</h2>
  <ol class="pasos">
    <li><b>Capturar</b>Cámara de 12 MP o más, en un soporte fijo con luz difusa.</li>
    <li><b>Alinear</b>La foto se ajusta a la plantilla del diseño de la tarjeta.</li>
    <li><b>Recortar</b>Cada unión se recorta según la plantilla, sin detector.</li>
    <li><b>Clasificar</b>Una red convolucional pequeña sugiere la clase, en el mismo equipo.</li>
    <li><b>Decide la persona</b>Ve solo las sospechosas, confirma o corrige, y queda registrado.</li>
  </ol>
  <div class="ejemplos">{ejemplos}</div>
  <p class="pie-foto">Fotos reales del conjunto de prueba de PCBSPDefect (Tsang et al., 2023), licencia CC BY 4.0, sin modificar. La sexta clase del proyecto, unión fría, no está en ese conjunto.</p>
</section>

<section>
  <div class="resultados-cab">
    <h2 style="margin:0">Resultado preliminar con fotos reales (EXP-006)</h2>
    <div class="leyenda"><span><i class="cuadro"></i>Línea base clásica</span><span><i class="circulo"></i>Red convolucional</span></div>
  </div>
  <p style="font-size:8.3mm;color:var(--tinta-2);margin-top:4mm">PCBSPDefect: 622 uniones de 121 tarjetas, tres iluminaciones cada una. La red se eligió con el conjunto de validación; el de prueba se usó una sola vez, al final.</p>
  <div class="grafica">{grafica(r["filas"], r["metas"])}</div>
  <div class="lecturas">
    <div><div class="cifra">{f2(red["sensibilidad"])}</div><div class="cifra-pie">sensibilidad de la red, contra {f2(lb["sensibilidad"])} de la línea base (partición oficial)</div></div>
    <div><div class="cifra">{f2(red["falsas_alarmas"])}</div><div class="cifra-pie">falsas alarmas de la red, contra {f2(lb["falsas_alarmas"])} de la línea base</div></div>
    <div>
      <p>La línea base tomó como aceptables <b>{conf["exceso"][0]}</b> fotos con exceso de soldadura y <b>{conf["puente"][0]}</b> con puente; la red, <b>{conf["exceso"][1]}</b> y <b>{conf["puente"][1]}</b>.</p>
      <p>La red cumple M1. Su falsa alarma cumple M2 en el valor medido, pero el intervalo llega a {f2(red["falsas_alarmas_ic"][1])}: <b>todavía no podemos afirmar M2.</b></p>
    </div>
  </div>
</section>

<section class="fin">
  <div>
    <h2>Lo que sigue</h2>
    <p style="font-size:8.3mm;color:var(--tinta-2)">EXP-006 usa la cámara y las tarjetas de otro grupo. Las metas se validan con nuestras propias tarjetas.</p>
    <ol class="estado">
      <li class="hecho"><b>Hecho</b><span>Software completo, que funciona sin internet, y validación con datos públicos.</span></li>
      <li><b>5 nov</b><span>Visita técnica a una planta de ensamble electrónico del estado.</span></li>
      <li><b>Nov</b><span>30 tarjetas propias con defectos sembrados; inspección humana sin apoyo (EXP-001), clasificador (EXP-002) y tiempo en la Raspberry Pi (EXP-003).</span></li>
      <li><b>Dic</b><span>Robustez a la luz y a la posición (EXP-004) e inspección con y sin apoyo (EXP-005).</span></li>
    </ol>
  </div>
  <div>
    <h2>Pruébelo</h2>
    <div class="qr">{qr}<div><p>Clasifique fotos reales en vivo y compita con la red en «¿Lo detectas tú?».</p><p class="url">femeci.foor.dev</p></div></div>
    <p class="nota">Usamos un asistente de IA (Claude; Anthropic, 2026) para buscar información, organizar el repositorio y programar. El equipo verificó cada resultado y es responsable del contenido.</p>
  </div>
</section>

<footer class="refs">
  <p class="titulo-refs">Referencias</p>
  <p>Anthropic. (2026). <i>Claude</i> [Modelo de lenguaje de gran tamaño]. https://claude.ai</p>
  <p>See, J. E. (2015). Visual inspection reliability for precision manufactured parts. <i>Human Factors, 57</i>(8), 1427–1442. https://doi.org/10.1177/0018720815602389</p>
  <p>{e(r["cita"]).replace("Advanced Intelligent Systems, 5, ", "<i>Advanced Intelligent Systems, 5</i>, Artículo ")}. Datos: {e(fotos["url"])}, CC BY 4.0.</p>
</footer>
</main>
</body></html>"""


IMPRIMIR = r"""
const {chromium} = require('playwright');
(async () => {
  const [html, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 3402, height: 4535}});  // 900 x 1200 mm a 96 ppp
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  const desborde = await p.evaluate(() => {
    const m = document.querySelector('main');
    return {alto: m.scrollHeight, visible: m.clientHeight};
  });
  console.log(JSON.stringify(desborde));
  await p.pdf({path: pdf, width: '900mm', height: '1200mm', printBackground: true, pageRanges: '1'});
  await p.setViewportSize({width: 3402, height: 4535});
  await p.screenshot({path: png, scale: 'css'});
  await b.close();
})();
"""


def main() -> None:
    html_ruta = AQUI / "cartel-v1.html"
    html_ruta.write_text(construir(), encoding="utf-8")
    script = AQUI / ".imprimir.js"
    script.write_text(IMPRIMIR, encoding="utf-8")
    try:
        subprocess.run(["node", str(script), str(html_ruta), str(AQUI / "cartel-v1.pdf"),
                        str(AQUI / "cartel-v1-vista-completa.png")], check=True)
    finally:
        script.unlink()
    # Vista previa ligera para revisar en pantalla
    from PIL import Image  # noqa: PLC0415
    grande = AQUI / "cartel-v1-vista-completa.png"
    im = Image.open(grande)
    im.thumbnail((1200, 1600))
    im.save(AQUI / "cartel-v1-vista.png", optimize=True)
    grande.unlink()


if __name__ == "__main__":
    main()
