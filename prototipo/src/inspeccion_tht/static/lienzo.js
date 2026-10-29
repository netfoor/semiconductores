// Lienzo compartido: dibuja la imagen en coordenadas de la plantilla, las uniones
// con el estilo de su clase, permite elegir una unión con clic o toque y, en modo
// plantilla, trazar rectángulos nuevos arrastrando.
(function () {
  const css = getComputedStyle(document.documentElement);
  const color = (v) => css.getPropertyValue(v).trim();
  const ESTILOS = {
    aceptable: { color: color("--c-aceptable"), ancho: 2, guion: [2, 4] },
    insuficiente: { color: color("--c-insuficiente"), ancho: 4, guion: [] },
    puente: { color: color("--c-puente"), ancho: 4, guion: [] },
    sin_soldar: { color: color("--c-sin_soldar"), ancho: 4, guion: [10, 6] },
    exceso: { color: color("--c-exceso"), ancho: 4, guion: [], doble: true },
    fria: { color: color("--c-fria"), ancho: 4, guion: [3, 4] },
    pendiente: { color: color("--gris"), ancho: 1.5, guion: [6, 4] },
    plantilla: { color: color("--acento"), ancho: 2, guion: [] },
  };

  class Lienzo {
    constructor(canvas, src, ancho, alto) {
      this.canvas = canvas;
      this.ctx = canvas.getContext("2d");
      this.canvas.width = ancho;
      this.canvas.height = alto;
      this.uniones = [];
      this.elegida = null;
      this.alElegir = null;
      this.alTrazar = null;
      this.trazo = null;
      this.img = new Image();
      this.listo = new Promise((ok, mal) => {
        this.img.onload = () => { this.dibujar(); ok(); };
        this.img.onerror = () => mal(new Error("No se pudo cargar la imagen"));
      });
      this.img.src = src;
      canvas.addEventListener("pointerdown", (e) => this._abajo(e));
      canvas.addEventListener("pointermove", (e) => this._mover(e));
      canvas.addEventListener("pointerup", (e) => this._arriba(e));
    }

    _punto(e) {
      const r = this.canvas.getBoundingClientRect();
      return { x: (e.clientX - r.left) * this.canvas.width / r.width, y: (e.clientY - r.top) * this.canvas.height / r.height };
    }

    unionEn(p) {
      for (let i = this.uniones.length - 1; i >= 0; i--) {
        const u = this.uniones[i];
        if (p.x >= u.x && p.x <= u.x + u.w && p.y >= u.y && p.y <= u.y + u.h) return u;
      }
      return null;
    }

    _abajo(e) {
      const p = this._punto(e);
      const u = this.unionEn(p);
      if (u || !this.alTrazar) {
        if (u) { this.elegir(u.id); if (this.alElegir) this.alElegir(u); }
        return;
      }
      this.trazo = { x0: p.x, y0: p.y, x1: p.x, y1: p.y };
      this.canvas.setPointerCapture(e.pointerId);
    }

    _mover(e) {
      if (!this.trazo) return;
      const p = this._punto(e);
      this.trazo.x1 = p.x; this.trazo.y1 = p.y;
      this.dibujar();
    }

    _arriba() {
      if (!this.trazo) return;
      const t = this.trazo; this.trazo = null;
      const r = { x: Math.round(Math.min(t.x0, t.x1)), y: Math.round(Math.min(t.y0, t.y1)),
                  w: Math.round(Math.abs(t.x1 - t.x0)), h: Math.round(Math.abs(t.y1 - t.y0)) };
      if (r.w >= 8 && r.h >= 8 && this.alTrazar) this.alTrazar(r);
      this.dibujar();
    }

    elegir(id) { this.elegida = id; this.dibujar(); }

    dibujar() {
      const c = this.ctx;
      c.clearRect(0, 0, this.canvas.width, this.canvas.height);
      if (this.img.complete && this.img.naturalWidth) c.drawImage(this.img, 0, 0, this.canvas.width, this.canvas.height);
      const escala = Math.max(1, this.canvas.width / 900);
      for (const u of this.uniones) {
        const e = ESTILOS[u.estilo] || ESTILOS.pendiente;
        c.save();
        c.strokeStyle = e.color;
        c.lineWidth = e.ancho * escala;
        c.setLineDash(e.guion.map((g) => g * escala));
        c.strokeRect(u.x, u.y, u.w, u.h);
        if (e.doble) { c.lineWidth = 1.5 * escala; c.strokeRect(u.x + 5 * escala, u.y + 5 * escala, u.w - 10 * escala, u.h - 10 * escala); }
        if (u.texto) {
          c.setLineDash([]);
          c.font = `700 ${Math.round(12 * escala)}px system-ui, sans-serif`;
          const ancho = c.measureText(u.texto).width + 8 * escala;
          c.fillStyle = e.color;
          c.fillRect(u.x, u.y - 16 * escala, ancho, 16 * escala);
          c.fillStyle = "#fff";
          c.fillText(u.texto, u.x + 4 * escala, u.y - 4 * escala);
        }
        if (u.id === this.elegida) {
          c.setLineDash([]);
          c.lineWidth = 3 * escala;
          c.strokeStyle = "#ffffff";
          c.strokeRect(u.x - 4 * escala, u.y - 4 * escala, u.w + 8 * escala, u.h + 8 * escala);
          c.strokeStyle = color("--tinta");
          c.lineWidth = 1.5 * escala;
          c.strokeRect(u.x - 6 * escala, u.y - 6 * escala, u.w + 12 * escala, u.h + 12 * escala);
        }
        c.restore();
      }
      if (this.trazo) {
        const t = this.trazo;
        c.save();
        c.strokeStyle = ESTILOS.plantilla.color;
        c.lineWidth = 2 * escala;
        c.setLineDash([6 * escala, 4 * escala]);
        c.strokeRect(Math.min(t.x0, t.x1), Math.min(t.y0, t.y1), Math.abs(t.x1 - t.x0), Math.abs(t.y1 - t.y0));
        c.restore();
      }
    }
  }

  async function enviar(url, datos) {
    const r = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(datos) });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || `Error ${r.status}`);
    return j;
  }

  function estado(el, texto, esError) {
    el.textContent = texto;
    el.classList.toggle("error", Boolean(esError));
  }

  window.Estacion = { Lienzo, enviar, estado, estilos: ESTILOS };
})();
