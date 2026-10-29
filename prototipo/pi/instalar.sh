#!/usr/bin/env bash
# Instala la estación en la Raspberry Pi SIN internet, desde esta carpeta.
# Uso: bash instalar.sh
set -euo pipefail
cd "$(dirname "$0")"
ENTORNO=${ENTORNO:-$HOME/tht}

arq=$(uname -m)
if [ "$arq" != "aarch64" ] && [ "${PERMITIR_OTRA_ARQ:-0}" != "1" ]; then
  echo "ALTO: este sistema es $arq. Se necesita Raspberry Pi OS de 64 bits (aarch64)."
  echo "Plan B: use la laptop (MESA.md)."; exit 1
fi
PY=$(command -v python3 || true)
[ -n "$PY" ] || { echo "ALTO: no hay python3."; exit 1; }
ver=$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
case "$ver" in 3.11|3.12|3.13) echo "Python $ver: bien." ;; *) echo "ALTO: Python $ver no está en el paquete (3.11 a 3.13)."; exit 1 ;; esac

if ! "$PY" -m venv "$ENTORNO" 2>/dev/null; then
  echo "No se pudo crear el entorno (falta python3-venv). Instalando sin entorno, solo para este usuario."
  "$PY" -m pip install --user --break-system-packages --no-index --find-links wheels inspeccion_tht-*.whl
  TH="$HOME/.local/bin/tht"
else
  "$ENTORNO/bin/pip" install -q --no-index --find-links wheels inspeccion_tht-*.whl
  TH="$ENTORNO/bin/tht"
fi
"$TH" --help >/dev/null
echo "Instalado. Comando: $TH"
echo "Siguiente: bash probar.sh"
