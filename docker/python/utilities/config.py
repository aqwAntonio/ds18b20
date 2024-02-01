import configparser
import os


def get_config(section):
    path = os.path.realpath('../config.ini')
    database_config = configparser.ConfigParser()
    database_config.read(path)
    return database_config[section]
