import psycopg2

from hh_database_project.config import get_db_params

params = get_db_params("postgres")

print("Проверяю подключение к PostgreSQL...")

connection = psycopg2.connect(**params)
connection.close()

print("Подключение успешно")
