import sqlite3
from typing import List, Dict
from app.configs.config import settings


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


    def get_power_report(self) -> dict:
        """
        Retrun un rapport agrégé de la consommation électrique
        par jour et par créneau horaire.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                date(time / 1000, 'unixepoch') AS day,
                strftime('%H:00', time / 1000, 'unixepoch') AS hour,
                SUM(value) AS total_power
            FROM device_metrics
            WHERE code = 'instant_power'
            GROUP BY day, hour
            ORDER BY day, hour;
            """
        )

        rows = cursor.fetchall()
        connection.close()

        report = {}

        for day, hour, total_power in rows:
            if day not in report:
                report[day] = {}

            report[day][hour] = int(total_power)

        return report

    def get_temperature_report(self) -> dict:
        """
        return un rapport agrégé de la température moyenne
        par jour et par créneau horaire.
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                date(time / 1000, 'unixepoch') AS day,
                strftime('%H:00', time / 1000, 'unixepoch') AS hour,
                AVG(value) AS avg_temp
            FROM device_metrics
            WHERE code = 'temp_interior'
            GROUP BY day, hour
            ORDER BY day, hour;
            """
        )

        rows = cursor.fetchall()
        connection.close()

        report = {}

        for day, hour, avg_temp in rows:
            report.setdefault(day, {})
            report[day][hour] = round(avg_temp, 2)

        return report
