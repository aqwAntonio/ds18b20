from utilities.yandex import import_data, save_data
from utilities.userbar import image_generating

if __name__ == "__main__":
    data = import_data()
    print(data)
    if save_data(data):
        image_generating(data)
