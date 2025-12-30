from typing import List, Dict
from google.cloud import bigquery
from app.configs.config import settings


class BigQueryService:
    """
    Service de persistance BigQuery (utilisé en production).
    """

    def __init__(self):
        self.client = bigquery.Client(project=settings.PROJECT_ID)
        self.table_id = (
            f"{settings.PROJECT_ID}."
            f"{settings.BIGQUERY_DATASET}."
            f"{settings.BIGQUERY_TABLE}"
        )

    def insert_rows(self, rows: List[Dict]) -> None:
        """
        Insère une liste de métriques dans BigQuery.
        """
        if not rows:
            return

        errors = self.client.insert_rows_json(self.table_id, rows)

        if errors:
            raise RuntimeError(f"bigquery insertion errors: {errors}")

    def get_power_report(self) -> dict:
        """
        retrun un rapport agrégé de la consommation électrique
        par jour et par heure depuis BigQuery.
        """
        query = f"""
        SELECT
            DATE(TIMESTAMP_MILLIS(time)) AS day,
            FORMAT_TIMESTAMP('%H:00', TIMESTAMP_MILLIS(time)) AS hour,
            SUM(value) AS total_power
        FROM `{self.table_id}`
        WHERE code = 'instant_power'
        GROUP BY day, hour
        ORDER BY day, hour
        """

        result = self.client.query(query).result()

        report = {}

        for row in result:
            day = str(row.day)
            hour = row.hour

            report.setdefault(day, {})
            report[day][hour] = int(row.total_power)

        return report
