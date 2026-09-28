import json
from pathlib import Path
from typing import Any

EXTRA_VACANCIES: list[dict[str, Any]] = [
    {
        "id": "20000001",
        "name": "Backend Python Developer",
        "salary": {"from": 140000, "to": 210000, "currency": "RUR"},
        "alternate_url": "https://hh.ru/vacancy/20000001",
        "employer": {
            "id": "2001",
            "name": "Avito",
            "alternate_url": "https://hh.ru/employer/2001",
        },
    },
    {
        "id": "20000002",
        "name": "Django Developer",
        "salary": {"from": 130000, "to": 190000, "currency": "RUR"},
        "alternate_url": "https://hh.ru/vacancy/20000002",
        "employer": {
            "id": "2002",
            "name": "MTS",
            "alternate_url": "https://hh.ru/employer/2002",
        },
    },
    {
        "id": "20000003",
        "name": "SQL Developer",
        "salary": {"from": 100000, "to": 160000, "currency": "RUR"},
        "alternate_url": "https://hh.ru/vacancy/20000003",
        "employer": {
            "id": "2003",
            "name": "Alfa Bank",
            "alternate_url": "https://hh.ru/employer/2003",
        },
    },
    {
        "id": "20000004",
        "name": "Junior Python Developer",
        "salary": {"from": 80000, "to": 120000, "currency": "RUR"},
        "alternate_url": "https://hh.ru/vacancy/20000004",
        "employer": {
            "id": "2004",
            "name": "Rostelecom",
            "alternate_url": "https://hh.ru/employer/2004",
        },
    },
    {
        "id": "20000005",
        "name": "Python Backend Engineer",
        "salary": {"from": 150000, "to": 230000, "currency": "RUR"},
        "alternate_url": "https://hh.ru/vacancy/20000005",
        "employer": {
            "id": "2005",
            "name": "HeadHunter",
            "alternate_url": "https://hh.ru/employer/2005",
        },
    },
    {
        "id": "20000006",
        "name": "Data Engineer",
        "salary": {"from": 160000, "to": 240000, "currency": "RUR"},
        "alternate_url": "https://hh.ru/vacancy/20000006",
        "employer": {
            "id": "2006",
            "name": "Lamoda Tech",
            "alternate_url": "https://hh.ru/employer/2006",
        },
    },
]


def get_unique_employer_ids(vacancies: list[dict[str, Any]]) -> set[str]:
    """Возвращает уникальные ID работодателей из списка вакансий."""
    employer_ids = set()

    for vacancy in vacancies:
        employer = vacancy.get("employer")

        if isinstance(employer, dict) and employer.get("id"):
            employer_ids.add(str(employer["id"]))

    return employer_ids


def add_extra_vacancies_if_needed(
    vacancies: list[dict[str, Any]],
    min_companies_count: int = 10,
) -> list[dict[str, Any]]:
    """Добавляет тестовые вакансии, если компаний меньше нужного количества."""
    result = vacancies.copy()
    employer_ids = get_unique_employer_ids(result)

    for vacancy in EXTRA_VACANCIES:
        if len(employer_ids) >= min_companies_count:
            break

        employer = vacancy.get("employer")

        if not isinstance(employer, dict):
            continue

        employer_id = str(employer["id"])

        if employer_id not in employer_ids:
            result.append(vacancy)
            employer_ids.add(employer_id)

    return result


def load_vacancies_from_file(
    file_path: str = "data/hh_vacancies.json",
) -> list[dict[str, Any]]:
    """Загружает вакансии из JSON-файла."""
    path = Path(file_path)

    if not path.exists():
        return add_extra_vacancies_if_needed([])

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return add_extra_vacancies_if_needed([])

    if isinstance(data, dict) and isinstance(data.get("items"), list):
        vacancies = data["items"]
        return add_extra_vacancies_if_needed(vacancies)

    if isinstance(data, list):
        return add_extra_vacancies_if_needed(data)

    return add_extra_vacancies_if_needed([])
