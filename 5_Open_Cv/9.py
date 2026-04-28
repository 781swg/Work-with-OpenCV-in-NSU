import cv2              # OpenCV
import numpy as np      # NumPy


# Загружаем цветное изображение.
img = cv2.imread("image.jpg")


# Переводим изображение в оттенки серого.
# Для выделения границ цвет не нужен, важны перепады яркости.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Применяем фильтр Собеля по оси X.
# Он ищет вертикальные границы, где яркость меняется слева направо.
sobel_x = cv2.Sobel(
    gray,        # исходное серое изображение
    cv2.CV_64F,  # тип результата: float64 для точности
    dx=1,        # производная по X
    dy=0,        # по Y производную не берём
    ksize=5      # размер ядра фильтра
)


# Применяем фильтр Собеля по оси Y.
# Он ищет горизонтальные границы, где яркость меняется сверху вниз.
sobel_y = cv2.Sobel(
    gray,
    cv2.CV_64F,
    dx=0,
    dy=1,
    ksize=5
)


# Преобразуем результат Sobel X в uint8.
# convertScaleAbs берёт модуль значений и переводит их в диапазон 0–255.
abs_sobel_x = cv2.convertScaleAbs(sobel_x)


# Преобразуем результат Sobel Y в uint8.
abs_sobel_y = cv2.convertScaleAbs(sobel_y)


# Объединяем вертикальные и горизонтальные границы.
# 0.5 и 0.5 — равный вклад обоих изображений.
edges = cv2.addWeighted(
    abs_sobel_x,
    0.5,
    abs_sobel_y,
    0.5,
    0
)


# Инвертируем цвета.
# Было: белые линии на чёрном фоне.
# Станет: чёрные линии на белом фоне, как карандашный рисунок.
sketch = cv2.bitwise_not(edges)


# Показываем исходное изображение.
cv2.imshow("Original", img)


# Показываем карандашный набросок.
cv2.imshow("Pencil Sketch", sketch)


# Сохраняем результат в файл.
cv2.imwrite("pencil_sketch.jpg", sketch)


# Ждём нажатия любой клавиши.
cv2.waitKey(0)


# Закрываем все окна.
cv2.destroyAllWindows()