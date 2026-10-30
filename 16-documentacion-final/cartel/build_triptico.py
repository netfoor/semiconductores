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
import re
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
    celular = datos_uri(AQUI / "img" / "inspeccion-celular.jpg", "image/jpeg")
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
.panel {{ font-size: 15mm; padding: 18mm 28mm 16mm; display: flex; flex-direction: column; justify-content: space-between; gap: 14mm; min-height: 0; overflow: hidden; }}
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
.inspeccion img {{ width: 62%; margin: 0 auto; display: block; border: 0.4mm solid var(--linea); }}
.cifras {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }}
.cifra {{ font-size: 52mm; font-weight: 700; line-height: 1; color: var(--marca); }}
.cifra-pie {{ font-size: 14mm; color: var(--tinta-2); margin-top: 1.5mm; line-height: 1.25; }}
.leyenda {{ display: flex; gap: 12mm; font-size: 13mm; color: var(--tinta-2); }}
.leyenda span {{ display: inline-flex; align-items: center; gap: 2.5mm; }}
.leyenda .cuadro {{ width: 5.5mm; height: 5.5mm; background: {AZUL}; border-radius: 0.6mm; }}
.leyenda .circulo {{ width: 6.5mm; height: 6.5mm; background: {MAGENTA}; border-radius: 50%; }}
.grafica svg {{ width: 100%; height: auto; display: block; }}
.aviso {{ font-weight: 700; }}
.refs {{ font-size: 8mm; line-height: 1.3; color: var(--tinta-2); }}
.refs p {{ margin: 0 0 2mm; padding-left: 6mm; text-indent: -6mm; }}
.integrantes {{ margin-top: 3mm !important; font-size: 11mm !important; color: var(--tinta) !important; }}
.cortes {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }}
.cortes svg {{ width: 100%; height: auto; display: block; }}
.cortes b {{ display: block; font-size: 12mm; color: var(--tinta); margin-bottom: 1mm; }}
.corte-tarjeta {{ fill: #2f6b3c; }} .corte-cobre, .corte-hueco {{ fill: #ddb04a; }} .corte-componente {{ fill: #24222a; }}
.corte-patilla {{ stroke: #7d858a; stroke-width: 4; }} .corte-soldadura {{ fill: #c9cdd0; stroke: #6f777b; stroke-width: 1.5; }}
.corte-t {{ font: 700 13px {FUENTE}; fill: var(--marca); }}
.metodo {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 10mm; align-items: start; }}
.metodo img {{ width: 100%; display: block; border: 0.8mm solid var(--tinta); border-radius: 6mm; }}
.ruta {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; }}
.ruta li {{ margin: 0; background: var(--banda); padding: 6mm 7mm; border-top: 2mm solid var(--acento); font-size: 13.5mm; line-height: 1.25; }}
.ruta li.hoy {{ border-top-color: var(--marca); }}
.ruta b {{ display: block; color: var(--tinta); }}
.nota-ia {{ font-size: 8.6mm; color: var(--tinta-2); line-height: 1.3; }}
</style></head>
<body>
<div class="motivo" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<header class="titulo">
  <h1>Estación de inspección visual asistida con procesamiento local para uniones soldadas <span>through-hole</span> en el ensamble electrónico</h1>
  <p>Diseño y validación experimental de un prototipo</p>
  <p class="integrantes">Fortino Romero Mantilla · Israel Jesus Garcia Osorio · María José de la Rosa Hernández</p>
</header>
<main class="paneles">

<section class="panel">
  <div>
    <h2>Introducción</h2>
    <p>En el ensamble electrónico, muchas uniones through-hole todavía se revisan a ojo. Puebla busca crecer en esta industria (CANIETI, 2024; OECD, 2026).</p>
  </div>
  <figure>
    <div class="cortes">
      <div><b>Montaje superficial (SMD)</b>
        <svg viewBox="0 0 330 80" role="img" aria-label="Componente de montaje superficial soldado sobre la tarjeta">
          <rect x="10" y="50" width="280" height="22" class="corte-tarjeta"/>
          <rect x="105" y="44" width="22" height="6" class="corte-cobre"/><rect x="173" y="44" width="22" height="6" class="corte-cobre"/>
          <rect x="112" y="26" width="76" height="18" class="corte-componente"/>
          <path d="M104 44 Q112 32 120 44 Z M180 44 Q188 32 196 44 Z" class="corte-soldadura"/>
        </svg></div>
      <div><b>Through-hole (THT)</b>
        <svg viewBox="0 0 330 100" role="img" aria-label="Patillas que atraviesan la tarjeta y se sueldan por el lado inferior">
          <rect x="112" y="6" width="76" height="22" rx="8" class="corte-componente"/>
          <rect x="10" y="44" width="280" height="22" class="corte-tarjeta"/>
          <rect x="118" y="44" width="16" height="22" class="corte-hueco"/><rect x="166" y="44" width="16" height="22" class="corte-hueco"/>
          <path d="M126 28 V86 M174 28 V86" class="corte-patilla"/>
          <path d="M112 66 Q126 86 140 66 Z M160 66 Q174 86 188 66 Z" class="corte-soldadura"/>
          <text x="196" y="90" class="corte-t">unión, lado inferior</text>
        </svg></div>
    </div>
    <figcaption><b>Figura 1.</b> En THT la patilla atraviesa la tarjeta y la unión queda abajo: ahí trabaja la estación. Ilustración de elaboración propia.</figcaption>
  </figure>
  <figure>
    <div class="ejemplos">{ejemplos}</div>
    <figcaption><b>Figura 2.</b> Defectos que busca el sistema. Fotografías tomadas de PCBSPDefect (Tsang et al., 2023), CC BY 4.0.</figcaption>
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
      <li><b>Menos defectos que pasan:</b> la atención del inspector va primero a las uniones sospechosas.</li>
      <li><b>Apoyo, no sustitución:</b> la persona sigue decidiendo.</li>
      <li><b>Bajo costo:</b> una computadora pequeña y una cámara, en lugar de una máquina de inspección automática.</li>
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
    <div class="metodo">
    <ol class="pasos">
      <li><span><b>Capturar</b> con el celular, sin internet</span></li>
      <li><span><b>Alinear</b> con la plantilla de la tarjeta</span></li>
      <li><span><b>Recortar</b> cada unión</span></li>
      <li><span><b>Clasificar</b> con una red pequeña, en local</span></li>
      <li><span><b>La persona</b> revisa una unión a la vez: confirma o corrige</span></li>
    </ol>
    <figure><img src="{celular}" alt="Pantalla del celular: acercamiento a una unión, sugerencia del sistema y las clases para confirmar o corregir">
    <figcaption><b>Figura 3.</b> Revisión en el celular, una unión a la vez. Captura de elaboración propia; foto de PCBSPDefect, CC&nbsp;BY&nbsp;4.0.</figcaption></figure>
    </div>
    <p><b>Metas y conjunto de prueba fijados antes de medir.</b></p>
  </div>
  <figure class="inspeccion">
    <img src="{inspeccion}" alt="Interfaz del prototipo con las uniones sospechosas marcadas por clase">
    <figcaption><b>Figura 4.</b> El prototipo marca las uniones sospechosas. Captura de elaboración propia (foto simulada); fotos de PCBSPDefect, CC&nbsp;BY&nbsp;4.0.</figcaption>
  </figure>
  <div>
    <h2>Creatividad e innovación</h2>
    <ul>
      <li><b>Plantilla por diseño:</b> las uniones de cada tarjeta se marcan una sola vez, sin entrenar un detector.</li>
      <li><b>Confidencialidad:</b> las fotos de la planta se procesan en el mismo equipo y nunca salen de él.</li>
      <li><b>Señala, no rechaza:</b> cada decisión del inspector se vuelve un ejemplo para el modelo de su planta.</li>
    </ul>
  </div>
</section>

<section class="panel">
  <div>
    <h2>Resultados preliminares</h2>
    <p>622 uniones reales de un conjunto público (Tsang et al., 2023).</p>
  </div>
  <div class="cifras">
    <div><div class="cifra">{f2(red["sensibilidad"])}</div><div class="cifra-pie">sensibilidad<br>(línea base: {f2(lb["sensibilidad"])})</div></div>
    <div><div class="cifra">{f2(red["falsas_alarmas"])}</div><div class="cifra-pie">falsas alarmas<br>(línea base: {f2(lb["falsas_alarmas"])})</div></div>
  </div>
  <figure class="grafica">
    <div class="leyenda"><span><i class="cuadro"></i>Línea base clásica</span><span><i class="circulo"></i>Red convolucional</span></div>
    {grafica(r["filas"], r["metas"], FUENTE, etiqueta_w=92, panel_w=125, hueco=24, nota=False)}
    <figcaption><b>Figura 5.</b> Punto: valor medido; línea: intervalo de confianza de 95&nbsp;%. Gráfica de elaboración propia.</figcaption>
  </figure>
  <div>
    <h2>Conclusiones</h2>
    <ul>
      <li>La red cumple M1; M2 aún no se puede afirmar (intervalo hasta {f2(red["falsas_alarmas_ic"][1])}).</li>
      <li>La visión clásica no basta.</li>
      <li>El prototipo ya corre en una Raspberry&nbsp;Pi&nbsp;4, en local y sin internet.</li>
      <li>Falta medir con tarjetas propias y frente a la inspección sin apoyo.</li>
    </ul>
  </div>
  <div>
    <h2>Hacia dónde va</h2>
    <ol class="ruta">
      <li class="hoy"><b>1. Apoyo</b>El inspector revisa primero lo marcado (este proyecto)</li>
      <li><b>2. Piloto por planta</b>Un modelo por empresa, entrenado con sus tarjetas</li>
      <li><b>3. Automatización gradual</b>Solo las uniones dudosas llegan a la persona</li>
    </ol>
  </div>
  <div class="refs">
    <h2>Referencias</h2>
    <p>Cámara Nacional de la Industria Electrónica, de Telecomunicaciones y Tecnologías de la Información. (2024). <i>Plan maestro para el desarrollo de la industria de semiconductores 2024–2030</i>. CANIETI.</p>
    <p>Organisation for Economic Co-operation and Development. (2026). <i>Promoting the development of the semiconductor ecosystem in Mexico: Assessment and recommendations</i>. OECD Publishing.</p>
    <p>See, J. E. (2015). Visual inspection reliability for precision manufactured parts. <i>Human Factors, 57</i>(8), 1427–1442. https://doi.org/10.1177/0018720815602389</p>
    <p>{cita_tsang}</p>
  </div>
</section>
</main>
</body></html>"""


def escalar(doc: str, k: float) -> str:
    """Multiplica por `k` las medidas en mm del estilo de los paneles (letra, márgenes y espacios)."""
    ini, fin = doc.index(".paneles {"), doc.index("</style>")
    bloque = re.sub(r"(\d+(?:\.\d+)?)mm", lambda m: f"{float(m.group(1)) * k:.2f}mm", doc[ini:fin])
    return doc[:ini] + bloque + doc[fin:]


MEDIR = r"""
const {chromium} = require('playwright');
(async () => {
  const [html] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 5669, height: 4535}});
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  // Altura natural del contenido de cada panel (sin repartir el espacio sobrante) / altura disponible
  const r = await p.evaluate(() => [...document.querySelectorAll('.panel')].map(e => {
    e.style.justifyContent = 'flex-start';
    const cs = getComputedStyle(e), hijos = [...e.children];
    const ult = hijos[hijos.length - 1].getBoundingClientRect(), top = e.getBoundingClientRect().top;
    return (ult.bottom - top + parseFloat(cs.paddingBottom)) / e.clientHeight;
  }));
  console.log(JSON.stringify(r));
  await b.close();
})();
"""


def ajustar(doc: str, ruta: Path) -> tuple[str, float]:
    """Escala más grande con la que ningún panel se desborda (búsqueda binaria)."""
    script = AQUI / ".medir-triptico.js"
    script.write_text(MEDIR, encoding="utf-8")
    try:
        def lleno(k: float) -> float:
            ruta.write_text(escalar(doc, k), encoding="utf-8")
            salida = subprocess.run(["node", str(script), str(ruta)], check=True, capture_output=True, text=True)
            return max(json.loads(salida.stdout.strip().splitlines()[-1]))
        bajo, alto = 0.8, 1.6
        for _ in range(7):
            k = (bajo + alto) / 2
            bajo, alto = (k, alto) if lleno(k) <= 0.985 else (bajo, k)
        return escalar(doc, bajo), bajo
    finally:
        script.unlink()


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
    html_ruta = AQUI / "triptico-v2.html"
    doc, k = ajustar(construir(), html_ruta)
    html_ruta.write_text(doc, encoding="utf-8")
    print(f"escala {k:.3f}")
    script = AQUI / ".imprimir-triptico.js"
    script.write_text(IMPRIMIR, encoding="utf-8")
    grande = AQUI / "triptico-v2-vista-completa.png"
    try:
        subprocess.run(["node", str(script), str(html_ruta), str(AQUI / "triptico-v2.pdf"), str(grande)], check=True)
    finally:
        script.unlink()
    from PIL import Image  # noqa: PLC0415
    im = Image.open(grande)
    im.thumbnail((1800, 1440))
    im.save(AQUI / "triptico-v2-vista.png", optimize=True)
    grande.unlink()


if __name__ == "__main__":
    main()
