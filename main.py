from hh_database_project.db_loader import fill_database
from hh_database_project.user_interaction import user_interaction


def main() -> None:
    """Запускает проект."""
    fill_database()
    user_interaction()


if __name__ == "__main__":
    main()
