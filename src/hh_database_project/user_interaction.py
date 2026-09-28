from hh_database_project.config import get_db_params
from hh_database_project.db_manager import DBManager


def print_menu() -> None:
    """Выводит меню пользователя."""
    print()
    print("1. Показать компании и количество вакансий")
    print("2. Показать все вакансии")
    print("3. Показать среднюю зарплату")
    print("4. Показать вакансии с зарплатой выше средней")
    print("5. Найти вакансии по ключевому слову")
    print("0. Выйти")


def show_companies_and_vacancies_count(db_manager: DBManager) -> None:
    """Выводит компании и количество вакансий."""
    companies = db_manager.get_companies_and_vacancies_count()

    if not companies:
        print("Компании не найдены")
        return

    for company_name, vacancies_count in companies:
        print(f"{company_name}: {vacancies_count} вакансий")


def show_all_vacancies(db_manager: DBManager) -> None:
    """Выводит все вакансии."""
    vacancies = db_manager.get_all_vacancies()

    if not vacancies:
        print("Вакансии не найдены")
        return

    for company, vacancy, salary_from, salary_to, salary_avg, url in vacancies:
        print(
            f"{company} | {vacancy} | "
            f"от {salary_from} до {salary_to} | "
            f"средняя: {salary_avg} | {url}"
        )


def show_avg_salary(db_manager: DBManager) -> None:
    """Выводит среднюю зарплату."""
    avg_salary = db_manager.get_avg_salary()

    if not avg_salary or avg_salary[0][0] is None:
        print("Средняя зарплата не найдена")
        return

    print(f"Средняя зарплата: {round(avg_salary[0][0])}")


def show_vacancies_with_higher_salary(db_manager: DBManager) -> None:
    """Выводит вакансии с зарплатой выше средней."""
    vacancies = db_manager.get_vacancies_with_higher_salary()

    if not vacancies:
        print("Вакансии не найдены")
        return

    for company, vacancy, salary_avg, url in vacancies:
        print(f"{company} | {vacancy} | {salary_avg} | {url}")


def show_vacancies_with_keyword(db_manager: DBManager) -> None:
    """Выводит вакансии по ключевому слову."""
    keyword = input("Введите ключевое слово: ")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)

    if not vacancies:
        print("Вакансии не найдены")
        return

    for company, vacancy, salary_avg, url in vacancies:
        print(f"{company} | {vacancy} | {salary_avg} | {url}")


def user_interaction() -> None:
    """Запускает взаимодействие с пользователем."""
    params = get_db_params("hh_project")
    db_manager = DBManager(params)

    while True:
        print_menu()
        user_choice = input("Выберите пункт меню: ")

        if user_choice == "1":
            show_companies_and_vacancies_count(db_manager)

        elif user_choice == "2":
            show_all_vacancies(db_manager)

        elif user_choice == "3":
            show_avg_salary(db_manager)

        elif user_choice == "4":
            show_vacancies_with_higher_salary(db_manager)

        elif user_choice == "5":
            show_vacancies_with_keyword(db_manager)

        elif user_choice == "0":
            print("Выход из программы")
            break

        else:
            print("Некорректный пункт меню")
