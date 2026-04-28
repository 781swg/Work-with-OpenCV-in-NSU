import cv2              # OpenCV
import numpy as np      # NumPy


# Загружаем изображение фасада здания.
img = cv2.imread("building.jpg")


# Переводим изображение в оттенки серого.
# Детектор Харриса работает с яркостью, а не с цветом.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Переводим изображение в float32.
# cv2.cornerHarris требует такой тип данных.
gray = np.float32(gray)


# Запускаем детектор углов Харриса.
corners = cv2.cornerHarris(
    gray,          # серое изображение float32
    blockSize=2,   # размер области, где анализируется угол
    ksize=3,       # размер ядра Собеля
    k=0.04         # эмпирический коэффициент чувствительности
)


# Расширяем найденные области углов.
# Так точки становятся заметнее и их легче визуализировать.
corners = cv2.dilate(corners, None)


# Порог отбора углов.
# Берём только те точки, чей отклик больше 1% от максимального.
threshold = 0.01 * corners.max()


# Список для хранения координат найденных углов.
points = []


# Получаем высоту и ширину карты углов.
height, width = corners.shape


# Проходим по всем пикселям карты углов.
for y in range(height):
    for x in range(width):
        # Если значение в этой точке больше порога,
        # считаем её угловой точкой.
        if corners[y, x] > threshold:
            points.append((x, y))


# Список отфильтрованных точек.
filtered_points = []


# Минимальное расстояние между выбранными точками.
# Нужно, чтобы не брать много почти одинаковых точек рядом.
min_distance = 30


# Перебираем все найденные точки.
for point in points:
    x, y = point

    # Предполагаем, что точка не слишком близко к уже выбранным.
    too_close = False

    # Проверяем расстояние до каждой уже выбранной точки.
    for selected in filtered_points:
        sx, sy = selected

        # Евклидово расстояние между двумя точками.
        distance = np.sqrt((x - sx) ** 2 + (y - sy) ** 2)

        # Если расстояние меньше допустимого, точку не берём.
        if distance < min_distance:
            too_close = True
            break

    # Если точка достаточно далеко от остальных, добавляем её.
    if not too_close:
        filtered_points.append(point)


# Сортируем точки снизу вверх.
# В изображениях координата y растёт сверху вниз,
# поэтому нижние точки имеют большее значение y.
filtered_points = sorted(filtered_points, key=lambda p: p[1], reverse=True)


# Создаём копию изображения, чтобы рисовать маршрут,
# не изменяя исходное изображение.
output = img.copy()


# Рисуем метки на всех выбранных угловых точках.
for point in filtered_points:
    x, y = point

    cv2.drawMarker(
        output,
        (x, y),
        (0, 0, 255),
        markerType=cv2.MARKER_CROSS,
        markerSize=12,
        thickness=2
    )


# Соединяем точки линиями, создавая маршрут квадрокоптера.
for i in range(len(filtered_points) - 1):
    cv2.line(
        output,
        filtered_points[i],
        filtered_points[i + 1],
        (0, 255, 0),
        2
    )


# Выводим координаты точек в консоль.
print("Список угловых точек:")
for i, point in enumerate(filtered_points):
    print(f"{i + 1}: x={point[0]}, y={point[1]}")


# Показываем результат.
cv2.imshow("Drone Route", output)

# Ждём нажатия клавиши.
cv2.waitKey(0)

# Закрываем окна.
cv2.destroyAllWindows()