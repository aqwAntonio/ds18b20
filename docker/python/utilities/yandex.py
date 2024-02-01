import json
import requests
from config import get_config


def import_weather():
    data = requests.get(
        'https://api.weather.yandex.ru/v2/informers/',
        params=get_config('yandex.weather.params'),
        headers=get_config('yandex.weather.headers')
    )
    return json.loads(data.text)
