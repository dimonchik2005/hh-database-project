from typing import Any

import psycopg2

from hh_database_project.config import get_db_params
from hh_database_project.db_creator import create_database, create_tables
from hh_database_project.file_manager import load_vacancies_from_file


def get_salary_avg(salary: dict[str, Any] | None) -> int | None:
    """Возвращает среднее значение зарплаты."""
    if salary is None:
        return None

    salary_from = salary.get("from")
    salary_to = salary.get("to")

    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)

    if salary_from:
        return int(salary_from)

    if salary_to:
        return int(salary_to)

    return None


def insert_employer(cursor: Any, employer: dict[str, Any]) -> None:
    """Добавляет работодателя в таблицу employers."""
    cursor.execute(
        """
        INSERT INTO employers (employer_id, employer_name, employer_url)
        VALUES (%s, %s, %s)
        ON CONFLICT (employer_id) DO NOTHING;
        """,
        (
            int(employer["id"]),
            employer["name"],
            employer.get("alternate_url"),
        ),
    )


def insert_vacancy(cursor: Any, vacancy: dict[str, Any]) -> None:
    """Добавляет вакансию в таблицу vacancies."""
    salary = vacancy.get("salary")
    salary_avg = get_salary_avg(salary)

    salary_from = None
    salary_to = None
    currency = None

    if salary:
        salary_from = salary.get("from")
        salary_to = salary.get("to")
        currency = salary.get("currency")

    cursor.execute(
        """
        INSERT INTO vacancies (
            vacancy_id,
            employer_id,
            vacancy_name,
            salary_from,
            salary_to,
            salary_avg,
            currency,
            vacancy_url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vacancy_id) DO NOTHING;
        """,
        (
            int(vacancy["id"]),
            int(vacancy["employer"]["id"]),
            vacancy["name"],
            salary_from,
            salary_to,
            salary_avg,
            currency,
            vacancy.get("alternate_url"),
        ),
    )


def fill_database() -> None:
    """Создает БД, таблицы и заполняет их данными из JSON-файла."""
    db_name = "hh_project"
    params = get_db_params(db_name)

    create_database(db_name, params)
    create_tables(params)

    vacancies = load_vacancies_from_file()

    print(f"Загружаю вакансии из файла: {len(vacancies)}")

    connection = psycopg2.connect(**params)

    try:
        with connection:
            with connection.cursor() as cursor:
                for vacancy in vacancies:
                    insert_employer(cursor, vacancy["employer"])
                    insert_vacancy(cursor, vacancy)

        print("Данные успешно загружены в базу")
    finally:
        connection.close()
