# Estación de inspección THT: operación de la mesa. Ejecute `make` para ver los objetivos.
# Guía del día de la feria: MESA.md.

DATOS ?= datos
PUERTO ?= 8000
MODELO ?= linea_base
IMAGEN ?=
DISENO ?=
IMAGEN_DOCKER ?= estacion-tht

# Interfaces que no son la red de la mesa (Docker, máquinas virtuales).
FILTRO_IF := ^(lo|docker|br-|veth|virbr)
IP ?= $(shell ip -4 -o addr show scope global 2>/dev/null | awk '$$2 !~ /$(FILTRO_IF)/ {split($$4, a, "/"); print a[1]; exit}')

.DEFAULT_GOAL := ayuda
.PHONY: ayuda instalar probar demo mosaico paquete-pi fotos-prueba mesa url latencia docker-construir docker-mesa

ayuda: ## Muestra esta lista
	@echo "Uso: make <objetivo> [DATOS=carpeta] [PUERTO=8000] [MODELO=linea_base|red]"
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-17s %s\n", $$1, $$2}'

instalar: ## Instala las dependencias (uv sync)
	uv sync

probar: ## Corre las pruebas automáticas
	uv run pytest

demo: ## Datos SINTÉTICOS listos en datos-demo: manifiesto, partición y modelo
	@test ! -e datos-demo || { echo "datos-demo ya existe. Bórrela (rm -r datos-demo) para regenerarla."; exit 1; }
	uv run tht demo --salida datos-demo
	uv run tht manifiesto generar datos-demo/crudos
	uv run tht particion --datos datos-demo --nota "Demostración sintética"
	uv run tht entrenar --datos datos-demo

mosaico: ## Tarjeta-mosaico con fotos REALES públicas (PCBSPDefect) en datos-mosaico, con la red de EXP-006
	uv run tht mosaico --salida datos-mosaico

paquete-pi: ## Paquete para instalar en la Raspberry Pi de 64 bits SIN internet (se arma aquí, con internet)
	bash pi/armar_paquete.sh

fotos-prueba: ## Fotos JPEG para probar /capturar (sintéticas del diseño de datos-demo y públicas)
	uv run tht fotos-prueba --salida fotos-prueba

mesa: url ## Sirve la estación a la red local (solo en un hotspot propio con contraseña)
	uv run tht servir --datos $(DATOS) --host 0.0.0.0 --puerto $(PUERTO) --modelo $(MODELO)

url: ## Muestra la IP local y la URL que debe abrir el celular
	@test -n "$(IP)" || { echo "No hay IP en la red local. Conéctese al hotspot de la mesa (MESA.md §2)."; exit 1; }
	@ip -4 -o addr show scope global | awk '$$2 !~ /$(FILTRO_IF)/ {split($$4, a, "/"); printf "  %-10s http://%s:$(PUERTO)/capturar\n", $$2, a[1]}'
	@echo "Abra en el celular: http://$(IP):$(PUERTO)/capturar"
	@if command -v qrencode >/dev/null; then qrencode -t ansiutf8 "http://$(IP):$(PUERTO)/capturar"; \
	 else echo "(Para un código QR: sudo apt install qrencode)"; fi

latencia: ## Mide la latencia: make latencia IMAGEN=ruta.png DISENO=nombre (prueba de software salvo en el equipo de EXP-003)
	@test -n "$(IMAGEN)" -a -n "$(DISENO)" || { echo "Uso: make latencia IMAGEN=datos/crudos/T01/T01_B_il1_....png DISENO=practica-01 [DATOS=datos]"; exit 1; }
	uv run tht latencia --datos $(DATOS) --imagen $(IMAGEN) --diseno $(DISENO) --modelo $(MODELO)

docker-construir: ## Construye la imagen del Dockerfile (la misma de Railway)
	docker build -t $(IMAGEN_DOCKER) .

docker-mesa: ## La misma imagen en modo local, con DATOS montada en /data/tht y el puerto solo en la IP de la mesa
	@test -n "$(IP)" || { echo "No hay IP en la red local. Conéctese al hotspot de la mesa (MESA.md §2)."; exit 1; }
	@mkdir -p $(DATOS)
	@echo "Abra en el celular: http://$(IP):$(PUERTO)/capturar"
	docker run --rm -it -p $(IP):$(PUERTO):8000 -v "$(abspath $(DATOS))":/data/tht \
	  --user "$$(id -u):$$(id -g)" --hostname "$$(hostname)" -e HOME=/tmp -e UV_CACHE_DIR=/tmp/uv \
	  $(IMAGEN_DOCKER) uv run --no-sync tht servir --datos /data/tht --host 0.0.0.0 --puerto 8000 --modelo $(MODELO)
