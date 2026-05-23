import os
import sqlite3
import datetime


class Database:
    """Pequeña capa de persistencia usando SQLite.

    Proporciona `guardar_ejercicio(ecuacion, resultado)` y
    `obtener_historial()` usadas por la interfaz.
    """

    def __init__(self, db_path: str | None = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if db_path is None:
            db_path = os.path.join(base_dir, "omni_db.sqlite3")

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                ecuacion TEXT NOT NULL,
                resultado TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def guardar_ejercicio(self, ecuacion: str, resultado: str) -> None:
        fecha = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO historial (fecha, ecuacion, resultado) VALUES (?, ?, ?)",
            (fecha, ecuacion, resultado),
        )
        self.conn.commit()

    def obtener_historial(self) -> list:
        cur = self.conn.cursor()
        cur.execute("SELECT id, fecha, ecuacion, resultado FROM historial ORDER BY id DESC")
        rows = cur.fetchall()
        return rows

    def cerrar(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass
