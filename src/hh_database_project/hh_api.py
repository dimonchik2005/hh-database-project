from typing import Any

import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter."""

    BASE_URL = "https://api.hh.ru"

    def __init__(self) -> None:
        """Инициализирует заголовки для запросов."""
        self.headers = {
            "User-Agent": (
                "hh-database-project/1.0 " "(dima.stepanov20050909@gmail.com)"
            ),
            "HH-User-Agent": (
                "hh-database-project/1.0 " "(dima.stepanov20050909@gmail.com)"
            ),
            "Accept": "application/json",
        }

    def get_employer(self, employer_id: str) -> dict[str, Any]:
        """Получает данные о работодателе по ID."""
        response = requests.get(
            f"{self.BASE_URL}/employers/{employer_id}",
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Некорректный ответ API работодателя")

        return data

    def get_vacancies_by_employer(
        self,
        employer_id: str,
        per_page: int = 100,
    ) -> list[dict[str, Any]]:
        """Получает список вакансий работодателя."""
        params: dict[str, str | int] = {
            "employer_id": employer_id,
            "per_page": per_page,
            "page": 0,
            "host": "hh.ru",
        }

        response = requests.get(
            f"{self.BASE_URL}/vacancies",
            params=params,
            headers=self.headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        vacancies = data.get("items", [])

        if not isinstance(vacancies, list):
            return []

        return vacancies
