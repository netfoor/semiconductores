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
    fotos = json.loads((PUBLICO / "fotos.json").read_text(encoding="utf-8"))
    por = {(f["particion"], f["modelo"]): f for f in r["filas"]}
    lb, red = por[("oficial", "linea_base")], por[("oficial", "red")]
    lb_t, red_t = por[("tarjeta", "linea_base")], por[("tarjeta", "red")]
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
body {{ width: 1500mm; height: 1200mm; font-family: {FUENTE}; color: var(--tinta); font-size: 13.6mm;
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
.panel {{ padding: 13mm 20mm 12mm; display: flex; flex-direction: column; gap: 10mm; min-height: 0; overflow: hidden; }}
.panel + .panel {{ border-left: 0.6mm dashed var(--linea); }}
h2 {{ font-size: 18mm; margin: 0 0 3mm; color: var(--acento); line-height: 1.1; }}
p {{ margin: 0 0 3mm; }}
ul {{ margin: 0; padding-left: 9mm; }} li {{ margin-bottom: 2mm; }}
.meta {{ background: var(--banda); border-left: 3mm solid var(--marca); padding: 8mm 10mm; }}
.meta h2 {{ color: var(--marca); }}
.meta .pregunta {{ font-weight: 700; font-size: 13.6mm; line-height: 1.3; margin-bottom: 4mm; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12.4mm; }}
td {{ padding: 2mm 0; border-top: 0.5mm solid var(--linea); vertical-align: top; }}
td:first-child {{ font-weight: 700; width: 22mm; color: var(--acento); }}
td:last-child {{ text-align: right; white-space: nowrap; font-weight: 700; padding-left: 4mm; }}
figure {{ margin: 0; }}
figcaption, .credito {{ font-size: 8.6mm; color: var(--gris); line-height: 1.3; margin-top: 2mm; }}
figcaption b {{ color: var(--tinta-2); }}
.pasos {{ list-style: none; margin: 0; padding: 0; counter-reset: p; display: grid; gap: 2.5mm; }}
.pasos li {{ counter-increment: p; display: grid; grid-template-columns: 13mm 1fr; align-items: baseline; margin: 0; }}
.pasos li::before {{ content: counter(p); font-weight: 700; font-size: 11mm; color: var(--marca); }}
.pasos b {{ color: var(--tinta); }}
.ejemplos {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 3.5mm; }}
.ejemplos img {{ width: 100%; aspect-ratio: 1; display: block; }}
.ejemplos figcaption {{ font-size: 8.4mm; font-weight: 700; color: var(--tinta); text-align: center; margin-top: 1.5mm; }}
.inspeccion img {{ width: 88%; margin: 0 auto; display: block; border: 0.4mm solid var(--linea); }}
.cifras {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }}
.cifra {{ font-size: 30mm; font-weight: 700; line-height: 1; color: var(--marca); }}
.cifra-pie {{ font-size: 11mm; color: var(--tinta-2); margin-top: 1.5mm; line-height: 1.25; }}
.leyenda {{ display: flex; gap: 9mm; font-size: 10mm; color: var(--tinta-2); }}
.leyenda span {{ display: inline-flex; align-items: center; gap: 2.5mm; }}
.leyenda .cuadro {{ width: 5.5mm; height: 5.5mm; background: {AZUL}; border-radius: 0.6mm; }}
.leyenda .circulo {{ width: 6.5mm; height: 6.5mm; background: {MAGENTA}; border-radius: 50%; }}
.grafica svg {{ width: 100%; height: auto; display: block; }}
.aviso {{ font-weight: 700; }}
.refs {{ font-size: 9.6mm; line-height: 1.3; color: var(--tinta-2); }}
.refs p {{ margin: 0 0 2mm; padding-left: 6mm; text-indent: -6mm; }}
.nota-ia {{ font-size: 9.6mm; color: var(--tinta-2); margin-top: auto; line-height: 1.3; }}
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
    <p>Puebla y México buscan crecer en ensamble electrónico y semiconductores (CANIETI, 2024; OECD, 2026). Cuando una línea de ensamble crece, la calidad depende de qué tan bien se detectan los defectos, y no solo de qué tan rápido se produce.</p>
    <p>En los componentes through-hole, las patillas atraviesan la tarjeta y se sueldan por el lado inferior. Esas uniones todavía se revisan en buena medida a ojo.</p>
  </div>
  <figure>
    <div class="ejemplos">{ejemplos}</div>
    <figcaption><b>Figura 1.</b> Defectos que busca el sistema, además de la unión aceptable. Fotografías tomadas de PCBSPDefect (Tsang et al., 2023), CC BY 4.0, sin modificar.</figcaption>
  </figure>
  <div>
    <h2>Antecedentes</h2>
    <ul>
      <li>La inspección visual humana deja pasar entre 20&nbsp;% y 30&nbsp;% de los defectos en la mayoría de las tareas (See, 2015).</li>
      <li>Las uniones through-hole son difíciles de inspeccionar con máquinas: hay componentes altos que tapan zonas y la unión está del lado inferior (GÖPEL electronic, s.&nbsp;f.).</li>
      <li>Personal técnico de una empresa de ensamble de Puebla nos dijo que la validación de piezas conserva pasos manuales y que, cuando algo falla, se revisa con más resolución a ojo (comunicación personal, octubre de 2026).</li>
      <li>Ya existen redes ligeras para detectar defectos; lo que falta es evaluarlas con datos propios y criterios fijados antes de medir.</li>
    </ul>
  </div>
  <div class="meta">
    <h2>Meta de ingeniería</h2>
    <p class="pregunta">Construir una estación de bajo costo que, sin internet, señale las uniones sospechosas con una sensibilidad y una tasa de falsas alarmas medidas y aceptables.</p>
    <table>
      <tr><td>M1</td><td>Sensibilidad para cualquier defecto</td><td>≥ 0.90</td></tr>
      <tr><td>M2</td><td>Falsas alarmas (uniones buenas señaladas)</td><td>≤ 0.15</td></tr>
      <tr><td>M3</td><td>Inspección con apoyo frente a sin apoyo</td><td>con ≥ sin</td></tr>
      <tr><td>M4</td><td>Tiempo por tarjeta en la computadora de placa única</td><td>≤ 5 s</td></tr>
      <tr><td>M5</td><td>Funciona con la red desconectada</td><td>100 %</td></tr>
      <tr><td>M6</td><td>Pérdida de sensibilidad con otra luz o posición</td><td>≤ 0.05</td></tr>
    </table>
  </div>
  <div>
    <h2>Justificación</h2>
    <ul>
      <li><b>Para el inspector:</b> menos carga visual y menos omisiones; la decisión sigue siendo suya.</li>
      <li><b>Confidencialidad:</b> las fotos de una planta no salen del equipo, porque todo se procesa en local.</li>
      <li><b>Bajo costo:</b> una computadora de placa única y una cámara, o un celular sin instalar nada.</li>
      <li><b>Resultado útil siempre:</b> si las metas no se cumplen, el análisis de errores dice qué condiciones lo impiden.</li>
    </ul>
  </div>
</section>

<section class="panel">
  <div>
    <h2>Objetivos</h2>
    <p><b>General.</b> Diseñar, construir y evaluar una estación de inspección visual asistida de uniones through-hole con procesamiento local.</p>
    <ul>
      <li>Definir cinco clases de defecto y una de unión aceptable, con la norma IPC-A-610 como referencia.</li>
      <li>Construir un conjunto de datos propio, etiquetado por dos personas y partido por tarjeta.</li>
      <li>Comparar una línea base de visión clásica, una red ligera y la inspección humana sin apoyo.</li>
    </ul>
  </div>
  <div>
    <h2>Metodología</h2>
    <ol class="pasos">
      <li><span><b>Capturar:</b> cámara en un soporte o el celular desde una página de la estación, por una red local sin internet.</span></li>
      <li><span><b>Alinear:</b> la foto se ajusta a la plantilla del diseño de la tarjeta, aunque esté girada o en perspectiva.</span></li>
      <li><span><b>Recortar</b> cada unión según la plantilla, sin necesidad de un detector.</span></li>
      <li><span><b>Clasificar</b> con una red convolucional pequeña (52 mil parámetros), en el mismo equipo.</span></li>
      <li><span><b>Decide la persona:</b> confirma o corrige cada unión marcada, y la decisión queda registrada.</span></li>
    </ol>
  </div>
  <figure class="inspeccion">
    <img src="{inspeccion}" alt="Interfaz del prototipo con las uniones sospechosas marcadas por clase">
    <figcaption><b>Figura 2.</b> El prototipo marca las uniones sospechosas por clase en una tarjeta-mosaico de fotos reales. Captura de pantalla de elaboración propia, con una foto simulada de la hoja impresa; fotos de PCBSPDefect (Tsang et al., 2023), CC BY 4.0.</figcaption>
  </figure>
  <div>
    <p><b>Datos y pruebas.</b> Al menos 30 tarjetas propias con defectos sembrados, partición por tarjeta y criterios fijados antes de medir. Mientras llegan, validamos el método con fotos reales públicas (PCBSPDefect; experimento EXP-006).</p>
  </div>
  <div>
    <h2>Creatividad e innovación</h2>
    <ul>
      <li><b>Humano en el ciclo:</b> el sistema no rechaza piezas, señala dónde mirar.</li>
      <li><b>Plantilla por diseño:</b> se marcan las uniones una vez y se inspecciona cualquier foto, con muchas menos etiquetas que un detector.</li>
      <li><b>Celular como cámara</b> sin instalar ninguna app y sin internet; cada foto queda con su huella digital (SHA-256).</li>
      <li><b>Evaluación honesta:</b> metas y conjunto de prueba fijados antes de medir, intervalos de confianza y comparación con la inspección humana.</li>
    </ul>
  </div>
</section>

<section class="panel">
  <div>
    <h2>Resultados preliminares (EXP-006)</h2>
    <p>Con 622 uniones reales de 121 tarjetas del conjunto PCBSPDefect, tres iluminaciones cada una. El conjunto de prueba se usó una sola vez.</p>
  </div>
  <div class="cifras">
    <div><div class="cifra">{f2(red["sensibilidad"])}</div><div class="cifra-pie">sensibilidad de la red, contra {f2(lb["sensibilidad"])} de la línea base clásica</div></div>
    <div><div class="cifra">{f2(red["falsas_alarmas"])}</div><div class="cifra-pie">falsas alarmas de la red, contra {f2(lb["falsas_alarmas"])} de la línea base</div></div>
  </div>
  <figure class="grafica">
    <div class="leyenda"><span><i class="cuadro"></i>Línea base clásica</span><span><i class="circulo"></i>Red convolucional</span></div>
    {grafica(r["filas"], r["metas"], FUENTE, etiqueta_w=108, panel_w=165, hueco=32)}
    <figcaption><b>Figura 3.</b> Sensibilidad y falsas alarmas con intervalo de confianza de 95 % (bootstrap agrupado por tarjeta), en la partición oficial y en una partición por tarjeta. Gráfica de elaboración propia.</figcaption>
  </figure>
  <ul>
    <li>La línea base tomó como aceptables {conf["exceso"][0]} fotos con exceso de soldadura y {conf["puente"][0]} con puente; la red, {conf["exceso"][1]} y {conf["puente"][1]}.</li>
    <li>Partición por tarjeta: red {f2(red_t["sensibilidad"])} y {f2(red_t["falsas_alarmas"])}; línea base {f2(lb_t["sensibilidad"])} y {f2(lb_t["falsas_alarmas"])}.</li>
  </ul>
  <div>
    <h2>Conclusiones</h2>
    <ul>
      <li>Con fotos reales, la red cumple M1. Su falsa alarma cumple M2 en el valor medido, pero el intervalo llega a {f2(red["falsas_alarmas_ic"][1])}: <span class="aviso">todavía no podemos afirmar M2.</span></li>
      <li>La línea base clásica no cumple ninguna de las dos: hace falta aprendizaje.</li>
      <li>Con una tarjeta de otra cámara y otra luz, la red falló (prueba exploratoria): el desempeño en nuestra estación solo lo dirán nuestros datos.</li>
      <li><b>Sigue:</b> visita técnica a una planta de ensamble (5 de noviembre), tarjetas propias, inspección humana sin apoyo y tiempo en la Raspberry Pi 4 (EXP-001 a EXP-005).</li>
    </ul>
  </div>
  <div class="refs">
    <h2>Referencias</h2>
    <p>Anthropic. (2026). <i>Claude</i> [Modelo de lenguaje de gran tamaño]. https://claude.ai</p>
    <p>Cámara Nacional de la Industria Electrónica, de Telecomunicaciones y Tecnologías de la Información. (2024). <i>Plan maestro para el desarrollo de la industria de semiconductores 2024–2030</i>. CANIETI.</p>
    <p>GÖPEL electronic. (s.&nbsp;f.). <i>Optimal inspection of THT assemblies</i> [Documento técnico].</p>
    <p>Organisation for Economic Co-operation and Development. (2026). <i>Promoting the development of the semiconductor ecosystem in Mexico: Assessment and recommendations</i>. OECD Publishing.</p>
    <p>See, J. E. (2015). Visual inspection reliability for precision manufactured parts. <i>Human Factors, 57</i>(8), 1427–1442. https://doi.org/10.1177/0018720815602389</p>
    <p>{cita_tsang}. Datos: {html.escape(fotos["url"])}, CC BY 4.0.</p>
  </div>
  <p class="nota-ia">Uso de inteligencia artificial: un asistente (Claude; Anthropic, 2026) apoyó la búsqueda de información, la organización del repositorio y la programación; el equipo verificó cada resultado.</p>
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
