import datetime
import json
import requests
from .config import get_config
from .database import db
from peewee import *

tz = datetime.timezone(datetime.timedelta(hours=5))


# {'now': 1706802976, 'now_dt': '2024-02-01T15:56:16.197475Z',
#  'info': {'url': 'https://yandex.ru/pogoda/50?lat=58.001123&lon=56.272769', 'lat': 58.001123, 'lon': 56.272769},
#  'fact': {'obs_time': 1706801400, 'temp': -4, 'feels_like': -10, 'icon': 'ovc', 'condition': 'overcast',
#           'wind_speed': 5, 'wind_dir': 'sw', 'pressure_mm': 744, 'pressure_pa': 991, 'humidity': 80,
#           'daytime': 'n', 'polar': False, 'season': 'winter', 'wind_gust': 6.9},
#  'forecast': {'date': '2024-02-02', 'date_ts': 1706814000, 'week': 5, 'sunrise': '09:18', 'sunset': '17:38',
#               'moon_code': 4, 'moon_text': 'moon-code-4', 'parts': [
#          {'part_name': 'night', 'temp_min': -6, 'temp_avg': -6, 'temp_max': -5, 'wind_speed': 3.1,
#           'wind_gust': 6.2, 'wind_dir': 'se', 'pressure_mm': 743, 'pressure_pa': 990, 'humidity': 88,
#           'prec_mm': 0.7, 'prec_prob': 30, 'prec_period': 480, 'icon': 'ovc_-sn', 'condition': 'light-snow',
#           'feels_like': -11, 'daytime': 'n', 'polar': False},
#          {'part_name': 'morning', 'temp_min': -7, 'temp_avg': -6, 'temp_max': -6, 'wind_speed': 3.6,
#           'wind_gust': 8.6, 'wind_dir': 'se', 'pressure_mm': 741, 'pressure_pa': 987, 'humidity': 87,
#           'prec_mm': 0.6, 'prec_prob': 30, 'prec_period': 360, 'icon': 'ovc_-sn', 'condition': 'light-snow',
#           'feels_like': -11, 'daytime': 'n', 'polar': False}]}}
class YandexWeather(Model):
    obs_time = IntegerField()
    temp = TextField()
    feels_like = TextField()
    icon = TextField()
    condition = TextField()
    wind_speed = TextField()
    wind_dir = TextField()
    pressure_mm = TextField()
    pressure_pa = TextField()
    humidity = TextField()
    daytime = TextField()
    polar = TextField()
    season = TextField()
    wind_gust = TextField()
    created_at = DateTimeField(default=datetime.datetime.now(tz))

    class Meta:
        database = db
        db_table = 'yandex_weather'


def import_data():
    data = requests.get(
        'https://api.weather.yandex.ru/v2/informers/',
        params=get_config('yandex.weather.params'),
        headers=get_config('yandex.weather.headers')
    )
    return json.loads(data.text)


def save_data(data):
    if 'fact' in data:
        db.connect()
        # Создание таблицы
        db.create_tables([YandexWeather])
        # Вставка данных
        YandexWeather.create(**data['fact'])
        # close connection
        db.close()

        return True

    return False


def run_import():
    data = import_data()
    print(data)
    return save_data(data)
