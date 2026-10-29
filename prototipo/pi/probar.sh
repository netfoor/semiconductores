#!/usr/bin/env bash
# Prueba la estación en la Raspberry Pi: crea la tarjeta-mosaico, mide el tiempo de inspección
# y deja la estación lista para el celular. Uso: bash probar.sh
set -euo pipefail
TH=${TH:-$HOME/tht/bin/tht}
[ -x "$TH" ] || TH="$HOME/.local/bin/tht"
DATOS=${DATOS:-$HOME/datos-mosaico}

[ -d "$DATOS" ] || "$TH" mosaico --salida "$DATOS"
IMG=$(ls "$DATOS"/crudos/T90/*.png | head -1)
echo "== Tiempo de inspección en este equipo (5 repeticiones, imagen digital del mosaico) =="
"$TH" latencia --datos "$DATOS" --imagen "$IMG" --diseno mosaico-01 --modelo red --repeticiones 5 \
  --nota "Prueba de software en $(hostname), no es EXP-003"
echo
echo "== Para el celular =="
hostname -I 2>/dev/null | tr ' ' '\n' | grep -E '^[0-9]+\.' | while read -r ip; do echo "  http://$ip:8000/capturar"; done
echo "Arrancar la estación:  $TH servir --datos $DATOS --modelo red --host 0.0.0.0 --puerto 8000"
