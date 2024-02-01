from config import get_config
from peewee import PostgresqlDatabase


def get_database():
    config = get_config('database')

    return PostgresqlDatabase(
        database=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )


db = get_database()
