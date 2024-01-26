import configparser

from peewee import *

config = configparser.ConfigParser()
config.read('config.ini')

# Настройка базы данных
db = PostgresqlDatabase(
    config['database']['name'],
    user=config['database']['user'],
    password=config['database']['password'],
    host=config['database']['host'],
    port=config['database']['port']
)


# Определение модели
class MyTable(Model):
    column1 = CharField()
    column2 = CharField()

    # добавьте здесь другие столбцы по мере необходимости

    class Meta:
        database = db


# Подключение к базе данных
db.connect()

# Создание таблицы
MyTable.create_table()

# Вставка данных
row = MyTable(column1='value1', column2='value2')
row.save()
