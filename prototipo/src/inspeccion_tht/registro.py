"""Registro local de las decisiones del operador (SQLite, sin red)."""

import csv
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ESQUEMA = """
CREATE TABLE IF NOT EXISTS decisiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_utc TEXT NOT NULL,
    operador TEXT NOT NULL,
    imagen TEXT NOT NULL,
    tarjeta TEXT,
    union_id TEXT NOT NULL,
    sugerencia TEXT NOT NULL,
    puntaje REAL,
    decision TEXT NOT NULL,
    segundos REAL,
    modo TEXT NOT NULL DEFAULT 'asistido'
);
"""

CAMPOS = ("id", "fecha_utc", "operador", "imagen", "tarjeta", "union_id", "sugerencia",
          "puntaje", "decision", "segundos", "modo")


class Registro:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self._con() as c:
            c.executescript(ESQUEMA)

    def _con(self) -> sqlite3.Connection:
        return sqlite3.connect(self.ruta)

    def anotar(self, operador: str, imagen: str, tarjeta: str | None, union_id: str, sugerencia: str,
               puntaje: float | None, decision: str, segundos: float | None, modo: str = "asistido") -> int:
        with self._con() as c:
            cur = c.execute(
                "INSERT INTO decisiones (fecha_utc, operador, imagen, tarjeta, union_id, sugerencia, puntaje,"
                " decision, segundos, modo) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(timespec="seconds"), operador, imagen, tarjeta,
                 union_id, sugerencia, puntaje, decision, segundos, modo))
            return int(cur.lastrowid)

    def todas(self) -> list[dict]:
        with self._con() as c:
            c.row_factory = sqlite3.Row
            return [dict(r) for r in c.execute("SELECT * FROM decisiones ORDER BY id")]

    def exportar_csv(self, salida: Path) -> Path:
        with open(salida, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS)
            w.writeheader()
            w.writerows(self.todas())
        return Path(salida)
