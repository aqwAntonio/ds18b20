from PIL import Image, ImageDraw, ImageFont

# Создаем прозрачную картинку
image = Image.new('RGBA', (450, 20), (255, 255, 255, 0))

# Загружаем шрифт TrueType
font = ImageFont.truetype("Arial.ttf", 16)

# Создаем объект ImageDraw для рисования на картинке
draw = ImageDraw.Draw(image)

# Устанавливаем координаты для текста
x = 10
y = 0

# Рисуем текст "вентилятор" на картинке
draw.text((x, y), "Вечером: -16...-13 (-19); Ночью: -18...-16 (-23);", font=font, fill='yellow')

# Добавляем черную рамку
draw.rectangle(((0, 0), (449, 19)), outline='yellow')

# Сохраняем картинку
image.save('ventilator.png')
