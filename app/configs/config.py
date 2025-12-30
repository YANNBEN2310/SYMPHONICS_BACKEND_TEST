from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

## appeler le répetroire du projet 
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """
    configuration globale de l'application.
    centraliser tous les paramètres liés à l'infrastructure.
    """

    # Env
    ENV: str = "local"  # local | prod

    # GCP
    PROJECT_ID: str = "symphonics-iot-subpub-project"

    # BIG QUERY
    BIGQUERY_DATASET: str = "iot_dataset"
    BIGQUERY_TABLE: str = "device_metrics"

    # sqlite (mode local) pour tester
     SQLITE_DB_PATH: str = str(BASE_DIR / "iot_energy.db")

    # pub/sub
    PUBSUB_TOPIC: str = "send_command"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
