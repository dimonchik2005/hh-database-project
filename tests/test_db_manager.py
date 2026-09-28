from typing import Any

import pytest

from hh_database_project.db_manager import DBManager


def test_get_companies_and_vacancies_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет метод получения компаний и количества вакансий."""
    db_manager = DBManager({})
    expected = [("Yandex", 5)]

    def fake_execute_query(
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        assert "JOIN" in query
        assert "COUNT" in query
        return expected

    monkeypatch.setattr(db_manager, "_execute_query", fake_execute_query)

    assert db_manager.get_companies_and_vacancies_count() == expected


def test_get_all_vacancies(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет метод получения всех вакансий."""
    db_manager = DBManager({})
    expected = [("Yandex", "Python Developer", 100000, 200000, 150000, "url")]

    def fake_execute_query(
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        assert "JOIN" in query
        assert "vacancy_name" in query
        return expected

    monkeypatch.setattr(db_manager, "_execute_query", fake_execute_query)

    assert db_manager.get_all_vacancies() == expected


def test_get_avg_salary(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет метод получения средней зарплаты."""
    db_manager = DBManager({})
    expected = [(150000,)]

    def fake_execute_query(
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        assert "AVG" in query
        return expected

    monkeypatch.setattr(db_manager, "_execute_query", fake_execute_query)

    assert db_manager.get_avg_salary() == expected


def test_get_vacancies_with_higher_salary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет метод получения вакансий выше средней зарплаты."""
    db_manager = DBManager({})
    expected = [("Yandex", "Python Developer", 200000, "url")]

    def fake_execute_query(
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        assert "AVG" in query
        assert ">" in query
        return expected

    monkeypatch.setattr(db_manager, "_execute_query", fake_execute_query)

    assert db_manager.get_vacancies_with_higher_salary() == expected


def test_get_vacancies_with_keyword(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяет метод поиска вакансий по ключевому слову."""
    db_manager = DBManager({})
    expected = [("Yandex", "Python Developer", 150000, "url")]

    def fake_execute_query(
        query: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        assert "LIKE" in query
        assert params == ("%python%",)
        return expected

    monkeypatch.setattr(db_manager, "_execute_query", fake_execute_query)

    assert db_manager.get_vacancies_with_keyword("python") == expected
