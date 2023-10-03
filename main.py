import configparser

import requests
import json
from miio import FanMiot
from miio.fan_common import OperationMode


def get_weather(lat, lon, lang, api_key):
    data = requests.get('https://api.weather.yandex.ru/v2/informers/',
                        params={'lat': lat, 'lon': lon, 'lang': lang},
                        headers={'X-Yandex-API-Key': api_key})

    return json.loads(data.text)


def fan_control(device, wind_speed, temp_out, feels_like_out):
    print("the temp is " + str(temp_out) + " (feels like " + str(feels_like_out) + ")")
    print("the wind speed is " + str(wind_speed))

    if feels_like_out < 20:
        device.off()
        print("the fan is switched off")
    else:
        if wind_speed < 3:
            device.set_speed(1)
            print("set speed 1")
            device.set_mode(OperationMode.Nature)
            print("operation mode is nature")
            device.on()
            print("the fan is switched on")
        elif wind_speed < 6:
            device.set_speed(1)
            print("set speed 1")
            device.set_mode(OperationMode.Normal)
            print("operation mode is normal")
            device.on()
            print("the fan is switched on")
        else:
            device.off()
            print("the fan is switched off")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    weather = get_weather(config['yandex.weather']['lat'],
                          config['yandex.weather']['lon'],
                          config['yandex.weather']['lang'],
                          config['yandex.weather']['api_key'])
    if 'fact' in weather:
        fan = FanMiot(config['xiaomi.fan']['ip'], config['xiaomi.fan']['token'])
        fan_control(fan,
                    weather['fact']['wind_speed'],
                    weather['fact']['temp'],
                    weather['fact']['feels_like'])
    else:
        print(weather)

