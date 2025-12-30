import sqlite3
from pathlib import Path

DB_PATH = Path("iot_energy.db")


def init_database():
    """
    Initialiser la base SQLite locale pour simuler bigquery.
    Créer la table device_metrics avec les colonnes requises.
    """

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS device_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dev_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            code TEXT NOT NULL,
            value REAL NOT NULL,
            time INTEGER NOT NULL
        );
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_device_time
        ON device_metrics (dev_id, time);
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_code_time
        ON device_metrics (code, time);
        """
    )

    connection.commit()
    connection.close()

    print("DB created.")


if __name__ == "__main__":
    init_database()
