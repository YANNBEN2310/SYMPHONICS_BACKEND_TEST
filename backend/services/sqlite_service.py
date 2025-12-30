import sqlite3
from typing import List, Dict
from backend.configs.config import settings


class SQLiteService:
    """
    service de persistance sqlite utilisé en environnement local
    pour simuler bigquery.
    .
    """

    def __init__(self):
        self.db_path = settings.SQLITE_DB_PATH

    def insert_rows(self, rows: List[Dict]) -> None:
        """
        insérer une liste de metrics dans la base sqlite.
        rows attendus :
        {
            dev_id: str,
            product_id: str,
            code: str,
            value: float,
            time: int
        }
        """
        if not rows:
            return

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.executemany(
            """
            INSERT INTO device_metrics (
                dev_id,
                product_id,
                code,
                value,
                time
            ) VALUES (?, ?, ?, ?, ?);
            """,
            [
                (
                    row["dev_id"],
                    row["product_id"],
                    row["code"],
                    row["value"],
                    row["time"],
                )
                for row in rows
            ],
        )

        connection.commit()
        connection.close()
