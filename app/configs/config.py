from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """
    configuration globale de l'application.
    centralise tous les paramètres liés à l'infra.
    """

    # Env
    ENV: str = "local"

    # GCP
    PROJECT_ID: str = "symphonics-iot-subpub-project"

    # BigQuery
    BIGQUERY_DATASET: str = "iot_dataset"
    BIGQUERY_TABLE: str = "device_metrics"

    # SQLite (mode local)
    SQLITE_DB_PATH: str = str(BASE_DIR / "iot_energy.db")

    # Pub/Sub
    PUBSUB_TOPIC: str = "send_command"

    # 
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # <-- ignorer GOOGLE_APPLICATION_CREDENTIALS
    )


settings = Settings()
