import cv2
import numpy as np

# 1. Загружаем большое изображение и логотип
# Проверь, чтобы названия файлов совпадали с теми, что лежат в папке
large_image = cv2.imread('large_image.png')
logo = cv2.imread('small_logo.png')

# 2. Выбираем метод сопоставления
# TM_CCOEFF_NORMED — один из самых точных методов
method = cv2.TM_CCOEFF_NORMED

# 3. Проводим сопоставление шаблона
result = cv2.matchTemplate(large_image, logo, method)

# 4. Находим координаты лучшего совпадения
# minMaxLoc возвращает: мин. значение, макс. значение, позицию минимума, позицию максимума
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 5. Определяем координаты рамки
top_left = max_loc  # Верхний левый угол (x, y)
logo_height, logo_width = logo.shape[:2] # Высота и ширина шаблона
bottom_right = (top_left[0] + logo_width, top_left[1] + logo_height) # Нижний правый угол

# 6. Условие порога (необязательно, но полезно)
threshold = 0.8
if max_val >= threshold:
    # 7. Рисуем рамку вокруг найденного логотипа (цвет BGR: зеленый, толщина 2)
    cv2.rectangle(large_image, top_left, bottom_right, (0, 255, 0), 2)
    print(f"Логотип найден! Совпадение: {round(max_val, 2)}")
else:
    print("Логотип не найден (низкий процент совпадения)")

# 8. Показываем результат
cv2.imshow('Logo Detection Result', large_image)
cv2.waitKey(0)
cv2.destroyAllWindows()