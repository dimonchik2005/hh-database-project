from typing import Any

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database(db_name: str, params: dict[str, Any]) -> None:
    """Создает базу данных PostgreSQL."""
    connection_params = params.copy()
    connection_params["dbname"] = "postgres"

    connection = psycopg2.connect(**connection_params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
    finally:
        connection.close()


def create_tables(params: dict[str, Any]) -> None:
    """Создает таблицы employers и vacancies."""
    connection = psycopg2.connect(**params)

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                        employer_id INTEGER PRIMARY KEY,
                        employer_name VARCHAR(255) NOT NULL,
                        employer_url TEXT
                    );
                    """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id INTEGER PRIMARY KEY,
                        employer_id INTEGER REFERENCES employers(employer_id),
                        vacancy_name VARCHAR(255) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        salary_avg INTEGER,
                        currency VARCHAR(10),
                        vacancy_url TEXT
                    );
                    """)
    finally:
        connection.close()
