import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def get_db_params(db_name: str | None = None) -> dict[str, Any]:
    """Возвращает параметры подключения к PostgreSQL."""
    database_name = db_name or os.getenv("DB_NAME") or "hh_project"
    user = os.getenv("DB_USER") or "postgres"
    password = os.getenv("DB_PASSWORD") or ""
    host = os.getenv("DB_HOST") or "localhost"
    port = int(os.getenv("DB_PORT") or "5432")

    return {
        "dbname": database_name,
        "user": user,
        "password": password,
        "host": host,
        "port": port,
    }