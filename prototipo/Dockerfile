# Demostración en la nube de la interfaz (datos sintéticos). La estación real corre en local.
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy THT_DATOS=/data/tht
RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv==0.11.32
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --group servidor --no-install-project
COPY src ./src
RUN uv sync --frozen --no-dev --group servidor
EXPOSE 8000
CMD ["sh", "-c", "uv run --no-sync gunicorn --preload --workers 2 --timeout 120 --bind 0.0.0.0:${PORT:-8000} inspeccion_tht.wsgi:app"]
