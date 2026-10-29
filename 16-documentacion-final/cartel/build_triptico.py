"""Genera el tríptico de la jornada (150 x 120 cm, tres paneles de 50 cm) en HTML y PDF.

Sigue las recomendaciones de la SECIHTI Puebla del 26 de octubre: estructura sugerida para
Ingenierías, tipografía Arial (en Linux se incrusta Liberation Sans, de métricas idénticas),
fondo claro, letra oscura, imágenes numeradas con su crédito, sin logotipos ni referencias a la
institución o al asesor, y sin páginas web ni códigos QR (inciso e). Las cifras salen de resultados.json de EXP-006.

    uv run --no-project --with segno --with pillow python 16-documentacion-final/cartel/build_triptico.py
"""

from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path

import build_cartel
from build_cartel import AZUL, EJEMPLOS, MAGENTA, PUBLICO, datos_uri, f2, grafica

AQUI = Path(__file__).resolve().parent
FUENTE = "Arial, 'Liberation Sans', sans-serif"
TINTA, TINTA2, GRIS, LINEA = "#1f1623", "#3b2f3f", "#3b2f3f", "#d9cfda"  # sin grises claros en el texto


def construir() -> str:
    build_cartel.GRIS = TINTA2  # la gráfica toma sus grises de build_cartel
    r = json.loads((PUBLICO / "resultados.json").read_text(encoding="utf-8"))
    por = {(f["particion"], f["modelo"]): f for f in r["filas"]}
    lb, red = por[("oficial", "linea_base")], por[("oficial", "red")]
    clases = r["clases"]
    m_lb = r["matrices"]["oficial"]["linea_base"]["matriz"]
    m_red = r["matrices"]["oficial"]["red"]["matriz"]
    ia = clases.index("aceptable")
    conf = {c: (m_lb[clases.index(c)][ia], m_red[clases.index(c)][ia]) for c in ("exceso", "puente")}
    ejemplos = "".join(
        f'<figure><img src="{datos_uri(PUBLICO / "fotos" / archivo, "image/jpeg")}" alt="Unión con clase {nombre}">'
        f'<figcaption>{nombre}</figcaption></figure>'
        for _, archivo, nombre in EJEMPLOS
    )
    inspeccion = datos_uri(AQUI / "img" / "inspeccion-mosaico.jpg", "image/jpeg")
    cita_tsang = html.escape(r["cita"]).replace(
        "Advanced Intelligent Systems, 5, ", "<i>Advanced Intelligent Systems, 5</i>, Artículo ")
    return f"""<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><title>Tríptico FEMECI 2026 — Inspección asistida THT</title>
<style>
@page {{ size: 1500mm 1200mm; margin: 0; }}
:root {{ --tinta:{TINTA}; --tinta-2:{TINTA2}; --gris:{GRIS}; --linea:{LINEA}; --banda:#f6f1f6;
  --marca:#c10066; --acento:#5f2470; --cian:#0098d4; --amarillo:#f1b400; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: #fff; }}
body {{ width: 1500mm; height: 1200mm; font-family: {FUENTE}; color: var(--tinta); font-size: 17.5mm;
  line-height: 1.3; display: flex; flex-direction: column; overflow: hidden; }}
.motivo {{ display: flex; height: 8mm; flex: none; }}
.motivo i {{ flex: 1; }}
.motivo i:nth-child(1) {{ background: var(--marca); }} .motivo i:nth-child(2) {{ background: var(--cian); }}
.motivo i:nth-child(3) {{ background: var(--amarillo); }} .motivo i:nth-child(4) {{ background: var(--acento); }}
.titulo {{ flex: none; padding: 14mm 30mm 12mm; border-bottom: 0.8mm solid var(--linea); text-align: center; }}
.titulo h1 {{ margin: 0 auto; max-width: 1380mm; font-size: 31mm; line-height: 1.1; letter-spacing: -0.01em; font-weight: 700; }}
.titulo h1 span {{ color: var(--marca); }}
.titulo p {{ margin: 5mm auto 0; font-size: 12.5mm; color: var(--tinta-2); max-width: 1250mm; }}
.paneles {{ flex: 1; display: grid; grid-template-columns: 1fr 1fr 1fr; min-height: 0; }}
.panel {{ padding: 18mm 28mm 16mm; display: flex; flex-direction: column; gap: 24mm; min-height: 0; overflow: hidden; }}
.panel + .panel {{ border-left: 0.6mm dashed var(--linea); }}
h2 {{ font-size: 23mm; margin: 0 0 3mm; color: var(--acento); line-height: 1.1; }}
p {{ margin: 0 0 3mm; }}
ul {{ margin: 0; padding-left: 9mm; }} li {{ margin-bottom: 3.5mm; }}
.meta {{ background: var(--banda); border-left: 3mm solid var(--marca); padding: 10mm 12mm; }}
.meta h2 {{ color: var(--marca); }}
.meta .pregunta {{ font-weight: 700; font-size: 17.5mm; line-height: 1.3; margin-bottom: 4mm; }}
table {{ width: 100%; border-collapse: collapse; font-size: 16mm; }}
td {{ padding: 2mm 0; border-top: 0.5mm solid var(--linea); vertical-align: top; }}
td:first-child {{ font-weight: 700; width: 28mm; color: var(--acento); }}
td:last-child {{ text-align: right; white-space: nowrap; font-weight: 700; padding-left: 4mm; }}
figure {{ margin: 0; }}
figcaption, .credito {{ font-size: 10.5mm; color: var(--gris); line-height: 1.3; margin-top: 2mm; }}
figcaption b {{ color: var(--tinta-2); }}
.pasos {{ list-style: none; margin: 0; padding: 0; counter-reset: p; display: grid; gap: 4mm; }}
.pasos li {{ counter-increment: p; display: grid; grid-template-columns: 17mm 1fr; align-items: baseline; margin: 0; }}
.pasos li::before {{ content: counter(p); font-weight: 700; font-size: 17.5mm; color: var(--marca); }}
.pasos b {{ color: var(--tinta); }}
.ejemplos {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 3.5mm; }}
.ejemplos img {{ width: 100%; aspect-ratio: 1; display: block; }}
.ejemplos figcaption {{ font-size: 10.5mm; font-weight: 700; color: var(--tinta); text-align: center; margin-top: 1.5mm; }}
.inspeccion img {{ width: 100%; display: block; border: 0.4mm solid var(--linea); }}
.cifras {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }}
.cifra {{ font-size: 52mm; font-weight: 700; line-height: 1; color: var(--marca); }}
.cifra-pie {{ font-size: 14mm; color: var(--tinta-2); margin-top: 1.5mm; line-height: 1.25; }}
.leyenda {{ display: flex; gap: 12mm; font-size: 13mm; color: var(--tinta-2); }}
.leyenda span {{ display: inline-flex; align-items: center; gap: 2.5mm; }}
.leyenda .cuadro {{ width: 5.5mm; height: 5.5mm; background: {AZUL}; border-radius: 0.6mm; }}
.leyenda .circulo {{ width: 6.5mm; height: 6.5mm; background: {MAGENTA}; border-radius: 50%; }}
.grafica svg {{ width: 100%; height: auto; display: block; }}
.aviso {{ font-weight: 700; }}
.refs {{ font-size: 10.6mm; line-height: 1.3; color: var(--tinta-2); }}
.refs p {{ margin: 0 0 2mm; padding-left: 6mm; text-indent: -6mm; }}
.nota-ia {{ font-size: 11mm; color: var(--tinta-2); margin-top: auto; line-height: 1.3; }}
</style></head>
<body>
<div class="motivo" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<header class="titulo">
  <h1>Estación de inspección visual asistida con procesamiento local para uniones soldadas <span>through-hole</span> en el ensamble electrónico</h1>
  <p>Diseño y validación experimental de un prototipo</p>
</header>
<main class="paneles">

<section class="panel">
  <div>
    <h2>Introducción</h2>
    <p>En el ensamble electrónico, muchas uniones through-hole todavía se revisan a ojo. Puebla busca crecer en esta industria (CANIETI, 2024; OECD, 2026).</p>
  </div>
  <figure>
    <div class="ejemplos">{ejemplos}</div>
    <figcaption><b>Figura 1.</b> Defectos que busca el sistema. Fotografías tomadas de PCBSPDefect (Tsang et al., 2023), CC BY 4.0.</figcaption>
  </figure>
  <div>
    <h2>Antecedentes</h2>
    <ul>
      <li>La inspección visual humana deja pasar del 20&nbsp;% al 30&nbsp;% de los defectos (See, 2015).</li>
      <li>En una empresa de ensamble poblana, las fallas se revisan a ojo con más resolución (comunicación personal, 2026).</li>
    </ul>
  </div>
  <div class="meta">
    <h2>Meta de ingeniería</h2>
    <p class="pregunta">Una estación de bajo costo que, sin internet, señale las uniones sospechosas.</p>
    <table>
      <tr><td>M1</td><td>Sensibilidad</td><td>≥ 0.90</td></tr>
      <tr><td>M2</td><td>Falsas alarmas</td><td>≤ 0.15</td></tr>
      <tr><td>M4</td><td>Tiempo por tarjeta</td><td>≤ 5 s</td></tr>
      <tr><td>M5</td><td>Funciona sin internet</td><td>100 %</td></tr>
    </table>
  </div>
  <div>
    <h2>Justificación</h2>
    <ul>
      <li>Menos omisiones; la persona decide.</li>
      <li>Las fotos no salen del equipo.</li>
      <li>Bajo costo: Raspberry Pi y un celular.</li>
    </ul>
  </div>
</section>

<section class="panel">
  <div>
    <h2>Objetivo</h2>
    <p>Diseñar, construir y evaluar la estación con datos propios, frente a la inspección humana y a una línea base clásica.</p>
  </div>
  <div>
    <h2>Metodología</h2>
    <ol class="pasos">
      <li><span><b>Capturar</b> con el celular, sin internet</span></li>
      <li><span><b>Alinear</b> con la plantilla de la tarjeta</span></li>
      <li><span><b>Recortar</b> cada unión</span></li>
      <li><span><b>Clasificar</b> con una red pequeña, en local</span></li>
      <li><span><b>La persona</b> confirma o corrige</span></li>
    </ol>
  </div>
  <figure class="inspeccion">
    <img src="{inspeccion}" alt="Interfaz del prototipo con las uniones sospechosas marcadas por clase">
    <figcaption><b>Figura 2.</b> El prototipo marca las uniones sospechosas. Captura de elaboración propia (foto simulada); fotos de PCBSPDefect, CC BY 4.0.</figcaption>
  </figure>
  <div>
    <h2>Creatividad e innovación</h2>
    <ul>
      <li>Señala, no rechaza: humano en el ciclo.</li>
      <li>El celular es la cámara, sin app ni internet.</li>
      <li>Metas fijadas antes de medir.</li>
    </ul>
  </div>
</section>

<section class="panel">
  <div>
    <h2>Resultados preliminares</h2>
    <p>622 uniones reales de un conjunto público (Tsang et al., 2023).</p>
  </div>
  <div class="cifras">
    <div><div class="cifra">{f2(red["sensibilidad"])}</div><div class="cifra-pie">sensibilidad (línea base: {f2(lb["sensibilidad"])})</div></div>
    <div><div class="cifra">{f2(red["falsas_alarmas"])}</div><div class="cifra-pie">falsas alarmas (línea base: {f2(lb["falsas_alarmas"])})</div></div>
  </div>
  <figure class="grafica">
    <div class="leyenda"><span><i class="cuadro"></i>Línea base clásica</span><span><i class="circulo"></i>Red convolucional</span></div>
    {grafica(r["filas"], r["metas"], FUENTE, etiqueta_w=92, panel_w=125, hueco=24, nota=False)}
    <figcaption><b>Figura 3.</b> Punto: valor medido; línea: intervalo de confianza de 95 %. Gráfica de elaboración propia.</figcaption>
  </figure>
  <div>
    <h2>Conclusiones</h2>
    <ul>
      <li>La red cumple M1; M2 aún no se puede afirmar (intervalo hasta {f2(red["falsas_alarmas_ic"][1])}).</li>
      <li>La visión clásica no basta.</li>
      <li>Falta medir con tarjetas propias y en la Raspberry Pi 4.</li>
    </ul>
  </div>
  <div class="refs">
    <h2>Referencias</h2>
    <p>Anthropic. (2026). <i>Claude</i> [Modelo de lenguaje de gran tamaño]. https://claude.ai</p>
    <p>Cámara Nacional de la Industria Electrónica, de Telecomunicaciones y Tecnologías de la Información. (2024). <i>Plan maestro para el desarrollo de la industria de semiconductores 2024–2030</i>. CANIETI.</p>
    <p>Organisation for Economic Co-operation and Development. (2026). <i>Promoting the development of the semiconductor ecosystem in Mexico: Assessment and recommendations</i>. OECD Publishing.</p>
    <p>See, J. E. (2015). Visual inspection reliability for precision manufactured parts. <i>Human Factors, 57</i>(8), 1427–1442. https://doi.org/10.1177/0018720815602389</p>
    <p>{cita_tsang}</p>
  </div>
  <p class="nota-ia">Apoyo de IA (Claude; Anthropic, 2026) en búsqueda y programación, verificado por el equipo.</p>
</section>
</main>
</body></html>"""


IMPRIMIR = r"""
const {chromium} = require('playwright');
(async () => {
  const [html, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 5669, height: 4535}});  // 1500 x 1200 mm a 96 ppp
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  const desborde = await p.evaluate(() => [...document.querySelectorAll('.panel')].map(e => e.scrollHeight - e.clientHeight));
  console.log(JSON.stringify({desborde_por_panel_px: desborde}));
  await p.pdf({path: pdf, width: '1500mm', height: '1200mm', printBackground: true, pageRanges: '1'});
  await p.screenshot({path: png});
  await b.close();
})();
"""


def main() -> None:
    html_ruta = AQUI / "triptico-v1.html"
    html_ruta.write_text(construir(), encoding="utf-8")
    script = AQUI / ".imprimir-triptico.js"
    script.write_text(IMPRIMIR, encoding="utf-8")
    grande = AQUI / "triptico-v1-vista-completa.png"
    try:
        subprocess.run(["node", str(script), str(html_ruta), str(AQUI / "triptico-v1.pdf"), str(grande)], check=True)
    finally:
        script.unlink()
    from PIL import Image  # noqa: PLC0415
    im = Image.open(grande)
    im.thumbnail((1800, 1440))
    im.save(AQUI / "triptico-v1-vista.png", optimize=True)
    grande.unlink()


if __name__ == "__main__":
    main()
