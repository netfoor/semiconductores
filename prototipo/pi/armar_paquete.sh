#!/usr/bin/env bash
# Arma en la laptop (con internet) el paquete para instalar la estación en una Raspberry Pi
# de 64 bits SIN internet. Uso, desde prototipo/:  bash pi/armar_paquete.sh
# Resultado: paquete-pi/ (cópielo completo a una memoria USB).
set -euo pipefail
cd "$(dirname "$0")/.."
SALIDA=${SALIDA:-paquete-pi}
ARQ=${ARQ:-aarch64}          # aarch64 = Raspberry Pi OS de 64 bits (x86_64 solo para probar el paquete en una PC)
rm -rf "$SALIDA" && mkdir -p "$SALIDA/wheels"

uv build --wheel -o "$SALIDA" >/dev/null
# Ruedas binarias para Python 3.11 (Raspberry Pi OS Bookworm), 3.12 y 3.13 (Trixie).
# Se resuelve una lista por versión y plataforma, con las mismas versiones del uv.lock cuando aplican.
uv export --no-dev --no-hashes --no-emit-project --format requirements-txt -o "$SALIDA/.lock.txt" >/dev/null
for py in 3.11 3.12 3.13; do
  uv pip compile -q pyproject.toml --python-version "$py" --python-platform "${ARQ}-manylinux_2_28" \
    --constraints "$SALIDA/.lock.txt" -o "$SALIDA/requisitos-$py.txt" 2>/dev/null || \
  uv pip compile -q pyproject.toml --python-version "$py" --python-platform "${ARQ}-manylinux_2_28" -o "$SALIDA/requisitos-$py.txt"
  uvx pip download -q --only-binary=:all: --implementation cp --python-version "$py" \
    --platform "manylinux_2_28_$ARQ" --platform "manylinux_2_27_$ARQ" --platform "manylinux_2_17_$ARQ" \
    --platform "manylinux2014_$ARQ" --no-deps -r "$SALIDA/requisitos-$py.txt" -d "$SALIDA/wheels"
done
rm -f "$SALIDA/.lock.txt"

cp pi/instalar.sh pi/probar.sh pi/LEEME.txt "$SALIDA/"
echo "Paquete listo en $SALIDA ($(du -sh "$SALIDA" | cut -f1)). Cópielo completo a la memoria USB."
