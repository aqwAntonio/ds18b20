from fastapi import FastAPI
from peewee import *
from utilities.yandex import import_weather as import_yandex_weather
from utilities.database import db

app = FastAPI()


class YandexWeather(Model):
    temp = TextField()
    humidity = TextField()

    class Meta:
        database = db
        db_table = 'yandex_weather'


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/import/weather/{name}")
async def import_weather(name: str):
    if name == 'yandex':
        data = import_yandex_weather()
        if 'fact' in data:

            db.connect()
            # Создание таблицы
            db.create_tables([YandexWeather])
            # Вставка данных
            YandexWeather.create(**data['fact'])
            # close connection
            db.close()

            return {"message": "Weather data imported successfully", "code": True}
        else:
            return {"message": "Weather Data Error", "code": False}

    return {"message": "Weather Name Error", "code": False}


@app.post("/sensor/{name}/{temperature}/{humidity}")
async def add_sensor_data_endpoint(name: str, temperature: float, humidity: float) -> dict:
    # add_sensor_data(name, temperature, humidity)
    return {"message": "Sensor data saved successfully", "code": True}
