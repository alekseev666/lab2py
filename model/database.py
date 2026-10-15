import os
import sqlite3
from datetime import datetime

from .house import House

DB_PATH = os.environ.get("DB_PATH", os.path.join("data", "houses.db"))

class Database:


    def __init__(self, path=DB_PATH):
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS calculations (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                date    TEXT NOT NULL,
                address TEXT NOT NULL,
                area    REAL NOT NULL,
                volume  REAL NOT NULL,
                t_in    REAL NOT NULL,
                t_out   REAL NOT NULL,
                k       REAL NOT NULL,
                q       REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rooms (
                calc_id INTEGER NOT NULL REFERENCES calculations(id),
                flat    INTEGER NOT NULL,
                name    TEXT NOT NULL,
                a       REAL NOT NULL,
                b       REAL NOT NULL,
                c       REAL NOT NULL
            );
        """)

    def save(self, house, t_in, t_out, k):
        """Сохраняет расчёт и все комнаты дома, возвращает id расчёта"""
        q = house.heat_power(t_in, t_out, k)
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO calculations (date, address, area, volume, t_in, t_out, k, q) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (datetime.now().strftime("%d.%m.%Y %H:%M"), house.address,
                 house.area(), house.volume(), t_in, t_out, k, q))
            calc_id = cur.lastrowid
            self.conn.executemany(
                "INSERT INTO rooms VALUES (?, ?, ?, ?, ?, ?)",
                [(calc_id, f.number, r.name, r.a, r.b, r.c)
                 for f in house.flats for r in f.rooms])
        return calc_id

    def history(self):
        """Все расчёты: список кортежей (id, дата, адрес, площадь, мощность)"""
        return self.conn.execute(
            "SELECT id, date, address, area, q FROM calculations ORDER BY id").fetchall()

    def load_house(self, calc_id):
        """Восстанавливает дом из сохранённого расчёта (None, если такого id нет)"""
        row = self.conn.execute(
            "SELECT address FROM calculations WHERE id = ?", (calc_id,)).fetchone()
        if row is None:
            return None
        h = House(row[0])
        flats = {}
        for flat, name, a, b in self.conn.execute(
                "SELECT flat, name, a, b FROM rooms WHERE calc_id = ? ORDER BY rowid",
                (calc_id,)):
            if flat not in flats:
                flats[flat] = h.add_flat(flat)
            flats[flat].add_room(name, a, b)
        return h

    def close(self):
        self.conn.close()

    def __len__(self):
        return self.conn.execute("SELECT COUNT(*) FROM calculations").fetchone()[0]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        return f"Database({len(self)} расчётов)"
