"""
Factory de service de stockage.

Actuellement non utilisé.
SQLite reste le backend actif en local pour tester.

Ce fichier montre comment basculer vers bigquery
en environnement prod sans refactor majeur.
"""

from app.configs.config import settings
from app.services.sqlite_service import SQLiteService
from app.services.bigquery_service import BigQueryService


def get_storage_service():
    """
    Retourne le service de persistance approprié
    selon l'environnement.
    """
    if settings.ENV == "prod":
        # En production, on utiliserait BigQuery
        return BigQueryService()

    # Par défaut (local), on utilise SQLite
    return SQLiteService()
