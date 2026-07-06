import json
from pathlib import Path

from hh_database_project.file_manager import (add_extra_vacancies_if_needed,
                                              get_unique_employer_ids,
                                              load_vacancies_from_file)


def test_get_unique_employer_ids() -> None:
    """Проверяет получение уникальных ID работодателей."""
    vacancies = [
        {"employer": {"id": "1", "name": "Company 1"}},
        {"employer": {"id": "2", "name": "Company 2"}},
        {"employer": {"id": "1", "name": "Company 1"}},
    ]

    result = get_unique_employer_ids(vacancies)

    assert result == {"1", "2"}


def test_add_extra_vacancies_if_needed() -> None:
    """Проверяет добавление дополнительных вакансий."""
    vacancies = [
        {
            "id": "1",
            "name": "Python Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/1",
            "employer": {
                "id": "1",
                "name": "Company 1",
                "alternate_url": "https://hh.ru/employer/1",
            },
        }
    ]

    result = add_extra_vacancies_if_needed(vacancies, min_companies_count=3)

    assert len(get_unique_employer_ids(result)) >= 3


def test_load_vacancies_from_file_with_dict_items(tmp_path: Path) -> None:
    """Проверяет загрузку вакансий из JSON со структурой items."""
    file_path = tmp_path / "vacancies.json"
    data = {
        "items": [
            {
                "id": "1",
                "name": "Python Developer",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "alternate_url": "https://hh.ru/vacancy/1",
                "employer": {
                    "id": "1",
                    "name": "Company 1",
                    "alternate_url": "https://hh.ru/employer/1",
                },
            }
        ]
    }
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_vacancies_from_file(str(file_path))

    assert result[0]["name"] == "Python Developer"


def test_load_vacancies_from_file_with_list(tmp_path: Path) -> None:
    """Проверяет загрузку вакансий из JSON-списка."""
    file_path = tmp_path / "vacancies.json"
    data = [
        {
            "id": "1",
            "name": "Backend Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/1",
            "employer": {
                "id": "1",
                "name": "Company 1",
                "alternate_url": "https://hh.ru/employer/1",
            },
        }
    ]
    file_path.write_text(json.dumps(data), encoding="utf-8")

    result = load_vacancies_from_file(str(file_path))

    assert result[0]["name"] == "Backend Developer"


def test_load_vacancies_from_file_invalid_json(tmp_path: Path) -> None:
    """Проверяет обработку некорректного JSON."""
    file_path = tmp_path / "vacancies.json"
    file_path.write_text("invalid json", encoding="utf-8")

    result = load_vacancies_from_file(str(file_path))

    assert isinstance(result, list)


def test_load_vacancies_from_missing_file() -> None:
    """Проверяет обработку отсутствующего файла."""
    result = load_vacancies_from_file("missing_file.json")

    assert isinstance(result, list)
