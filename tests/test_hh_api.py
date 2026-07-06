from typing import Any

import pytest

from hh_database_project.hh_api import HeadHunterAPI


class FakeResponse:
    """Фейковый ответ API."""

    def __init__(self, data: Any) -> None:
        """Инициализирует данные ответа."""
        self.data = data

    def raise_for_status(self) -> None:
        """Имитирует успешный ответ API."""

    def json(self) -> Any:
        """Возвращает JSON-данные."""
        return self.data


def test_get_employer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет получение работодателя."""
    api = HeadHunterAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse(
            {
                "id": "1001",
                "name": "Ozon Tech",
            }
        )

    monkeypatch.setattr("requests.get", fake_get)

    result = api.get_employer("1001")

    assert result["id"] == "1001"
    assert result["name"] == "Ozon Tech"


def test_get_employer_invalid_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет ошибку при некорректном ответе работодателя."""
    api = HeadHunterAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse([])

    monkeypatch.setattr("requests.get", fake_get)

    with pytest.raises(ValueError, match="Некорректный ответ API работодателя"):
        api.get_employer("1001")


def test_get_vacancies_by_employer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет получение вакансий работодателя."""
    api = HeadHunterAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse(
            {
                "items": [
                    {
                        "id": "10000001",
                        "name": "Python Developer",
                    }
                ]
            }
        )

    monkeypatch.setattr("requests.get", fake_get)

    result = api.get_vacancies_by_employer("1001")

    assert len(result) == 1
    assert result[0]["name"] == "Python Developer"


def test_get_vacancies_by_employer_without_items(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет ответ API без списка вакансий."""
    api = HeadHunterAPI()

    def fake_get(*args: Any, **kwargs: Any) -> FakeResponse:
        return FakeResponse({"items": "wrong data"})

    monkeypatch.setattr("requests.get", fake_get)

    result = api.get_vacancies_by_employer("1001")

    assert result == []
