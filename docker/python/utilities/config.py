import configparser
import os


def get_config(section):
    path = os.path.join(os.path.dirname(__file__), 'config', 'config.ini')
    config = configparser.ConfigParser()

    # Открытие файла для чтения
    with open(path, 'r') as config_file:
        # Чтение конфигурации из файла
        config.read_file(config_file)

    if config.has_section(section):
        return config[section]
    else:
        return None
