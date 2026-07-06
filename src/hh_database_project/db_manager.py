from typing import Any

import psycopg2


class DBManager:
    """Класс для работы с данными в PostgreSQL."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Инициализирует параметры подключения к БД."""
        self.params = params

    def _execute_query(
        self,
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        """Выполняет SQL-запрос и возвращает результат."""
        connection = psycopg2.connect(**self.params)

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
        finally:
            connection.close()

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """Получает компании и количество вакансий у каждой компании."""
        query = """
            SELECT employers.employer_name, COUNT(vacancies.vacancy_id)
            FROM employers
            LEFT JOIN vacancies USING(employer_id)
            GROUP BY employers.employer_name
            ORDER BY COUNT(vacancies.vacancy_id) DESC;
        """
        return self._execute_query(query)

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """Получает все вакансии с компанией, зарплатой и ссылкой."""
        query = """
            SELECT
                employers.employer_name,
                vacancies.vacancy_name,
                vacancies.salary_from,
                vacancies.salary_to,
                vacancies.salary_avg,
                vacancies.vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
            ORDER BY employers.employer_name;
        """
        return self._execute_query(query)

    def get_avg_salary(self) -> list[tuple[Any, ...]]:
        """Получает среднюю зарплату по вакансиям."""
        query = """
            SELECT AVG(salary_avg)
            FROM vacancies
            WHERE salary_avg IS NOT NULL;
        """
        return self._execute_query(query)

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """Получает вакансии, у которых зарплата выше средней."""
        query = """
            SELECT
                employers.employer_name,
                vacancies.vacancy_name,
                vacancies.salary_avg,
                vacancies.vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
            WHERE vacancies.salary_avg > (
                SELECT AVG(salary_avg)
                FROM vacancies
                WHERE salary_avg IS NOT NULL
            )
            ORDER BY vacancies.salary_avg DESC;
        """
        return self._execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """Получает вакансии, в названии которых есть ключевое слово."""
        query = """
            SELECT
                employers.employer_name,
                vacancies.vacancy_name,
                vacancies.salary_avg,
                vacancies.vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
            WHERE LOWER(vacancies.vacancy_name) LIKE LOWER(%s)
            ORDER BY vacancies.vacancy_name;
        """
        return self._execute_query(query, (f"%{keyword}%",))
