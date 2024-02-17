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
                    part['part_name'].capitalize() + ": " +
                    str(part['temp_min']) + "..." + str(part['temp_max']) +
                    " " + part['condition'] + ". Feels like " + str(part['feels_like']) +
                    ". Wind speed " + str(part['wind_speed']) + " up to " + str(part['wind_gust']) + " m/s",
                    font=font,
                    fill='green')
                delta_y = 20

        # Путь к сохраняемой картинке
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "weather.png")
        # Сохраняем картинку
        image.save(save_path)
