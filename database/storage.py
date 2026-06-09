"""SQLite save/load support for Cyber City."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from models.city import CityMap


class CityStorage:
    """Persist city layouts in an offline SQLite database."""

    def __init__(self, database_path: Path | str = "cyber_city.db") -> None:
        self.database_path = Path(database_path)
        self._initialise()

    def save_city(self, name: str, city: CityMap) -> None:
        payload = json.dumps(city.to_dict(), indent=2)
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO city_saves(name, payload)
                VALUES(?, ?)
                ON CONFLICT(name) DO UPDATE SET payload = excluded.payload,
                                                updated_at = CURRENT_TIMESTAMP
                """,
                (name, payload),
            )

    def load_city(self, name: str) -> CityMap:
        with sqlite3.connect(self.database_path) as connection:
            row = connection.execute(
                "SELECT payload FROM city_saves WHERE name = ?",
                (name,),
            ).fetchone()
        if row is None:
            raise KeyError(f"No saved city named {name!r} exists.")
        return CityMap.from_dict(json.loads(row[0]))

    def list_cities(self) -> list[str]:
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute("SELECT name FROM city_saves ORDER BY updated_at DESC, name").fetchall()
        return [str(row[0]) for row in rows]

    def _initialise(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS city_saves(
                    name TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
