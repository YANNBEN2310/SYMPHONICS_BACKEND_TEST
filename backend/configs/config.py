from pydantic import BaseSettings


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
    SQLITE_DB_PATH: str = "iot_energy.db"

    # pub/sub
    PUBSUB_TOPIC: str = "send_command"

    class Config:
        env_file = ".env"


settings = Settings()
