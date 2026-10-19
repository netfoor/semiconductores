"""Genera la versión de la bitácora para el expediente (Markdown listo para build.py).

Une las entradas diarias, quita propiedades y enlaces internos y reserva el nombre de
organizaciones del sector (D-011). El registro íntegro queda en la bóveda y en git.
Uso: python exportar_bitacora.py SALIDA.md
"""
import re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RESERVAR = {r"guia-contacto-yankuilotl": "guia-contacto-empresa-a", r"yankuilotl": "Empresa A"}

def limpiar(t):
    t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)
    t = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", t)
    t = re.sub(r"\[\[([^\]]+)\]\]", r"\1", t)
    t = re.sub(r"^> \[![a-z]+\]\s*", "> ", t, flags=re.M)
    for k, v in RESERVAR.items():
        t = re.sub(k, v, t, flags=re.I)
    t = t.replace("Empresa A.md", "Empresa A")
    return t

def main(out):
    partes = ["""::: {custom-style="TitlePageTitle"}
Bitácora de investigación
:::

::: {custom-style="TitlePageText"}
Estación de inspección visual asistida con procesamiento local para uniones soldadas through-hole en el ensamble electrónico
:::

::: {custom-style="TitlePageText"}
Fortino Romero Mantilla (líder del proyecto) e Israel Jesus Garcia Osorio
:::

::: {custom-style="TitlePageText"}
FEMECI-PUEBLA 2026 · Registro cronológico de actividades
:::

> **Nota sobre el nombre de organizaciones.** Por confidencialidad (decisión D-011), en esta versión el nombre de la empresa de ensamble electrónico con la que se conversó se sustituye por "Empresa A". El registro íntegro, con sellos de tiempo verificables, está en el repositorio git del proyecto y se puede mostrar al comité si lo solicita. Las entradas no se reescriben: las correcciones se agregan con fecha. El apoyo de IA se identifica en cada actividad (Claude (IA)).

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
"""]
    for f in sorted((RAIZ / "02-bitacora").glob("2026-*.md")):
        partes.append(limpiar(f.read_text(encoding="utf-8")).strip() + "\n")
    Path(out).write_text("\n\n".join(partes), encoding="utf-8")

main(sys.argv[1])
