import os

from PIL import Image, ImageDraw, ImageFont


def image_generating(data):
    if 'forecast' in data:
        # Создаем прозрачную картинку
        image = Image.new('RGBA', (450, 40), (255, 255, 255, 0))

        # Загружаем шрифт TrueType
        font = ImageFont.truetype("Arial.ttf", 14)

        # Создаем объект ImageDraw для рисования на картинке
        draw = ImageDraw.Draw(image)

        # Устанавливаем координаты для текста
        x = 10
        y = 0
        delta_y = 0

        if 'parts' in data['forecast']:
            for part in data['forecast']['parts']:
                # Рисуем текст на картинке (1st line)
                draw.text(
                    (x, y + delta_y),
                    "Evening: " +
                    part['temp_min'] + "..." + part['temp_max'] +
                    " " + part['condition'] + ". Feels like " + part['feels_like'] +
                    ". Wind speed " + part['wind_speed'] + " up to " + part['wind_gust'] + " m/s",
                    font=font,
                    fill='green')
                delta_y = 20

        # Путь к сохраняемой картинке
        save_path = os.path.join(os.getcwd(), "images", "weather.png")
        # Сохраняем картинку
        image.save(save_path)
