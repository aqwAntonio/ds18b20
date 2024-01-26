import configparser
import json
import requests


def get_weather(lat, lon, lang, api_key):
    data = requests.get('https://api.weather.yandex.ru/v2/informers/',
                        params={'lat': lat, 'lon': lon, 'lang': lang},
                        headers={'X-Yandex-API-Key': api_key})

    return json.loads(data.text)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    weather = get_weather(config['yandex.weather']['lat'],
                          config['yandex.weather']['lon'],
                          config['yandex.weather']['lang'],
                          config['yandex.weather']['api_key'])
    if 'fact' in weather:
        print(weather)