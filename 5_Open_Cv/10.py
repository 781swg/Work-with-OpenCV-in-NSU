import cv2              # OpenCV
import numpy as np      # NumPy


# Загружаем изображение дороги или парковки.
img = cv2.imread("road.jpg")


# Переводим изображение в оттенки серого.
# Детектор Canny работает с яркостью.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Размываем серое изображение гауссовым фильтром.
# Это уменьшает шум: текстуру асфальта, мелкие камни, блики.
blurred = cv2.GaussianBlur(gray, (5, 5), 0)


# Применяем детектор границ Canny.
# threshold1 — нижний порог.
# threshold2 — верхний порог.
# Сильные границы выше threshold2 сохраняются.
# Слабые ниже threshold1 отбрасываются.
# Промежуточные сохраняются только если связаны с сильными.
edges = cv2.Canny(
    blurred,
    threshold1=50,
    threshold2=150
)


# Ищем контуры по найденным границам.
# Контуры позволяют анализировать формы объектов.
contours, _ = cv2.findContours(
    edges,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


# Создаём копию исходного изображения.
# На ней будем рисовать найденные препятствия.
output = img.copy()


# Перебираем все найденные контуры.
for contour in contours:
    # Считаем площадь контура.
    # Маленькие контуры считаем шумом.
    area = cv2.contourArea(contour)

    # Отбрасываем слишком маленькие объекты.
    if area < 500:
        continue

    # Считаем периметр контура.
    # Он нужен для упрощения формы.
    perimeter = cv2.arcLength(contour, True)

    # Упрощаем контур до многоугольника.
    # Чем больше коэффициент, тем сильнее упрощение.
    approx = cv2.approxPolyDP(
        contour,
        0.02 * perimeter,
        True
    )

    # Рисуем крупный контур красным цветом.
    cv2.drawContours(output, [contour], -1, (0, 0, 255), 2)

    # Если после упрощения получилось 4 вершины,
    # считаем объект похожим на прямоугольное препятствие.
    if len(approx) == 4:
        # Получаем рамку вокруг прямоугольного контура.
        x, y, w, h = cv2.boundingRect(approx)

        # Рисуем зелёную рамку вокруг препятствия.
        cv2.rectangle(
            output,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Подписываем найденный объект.
        cv2.putText(
            output,
            "Obstacle",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


# Показываем исходное изображение.
cv2.imshow("Original", img)


# Показываем найденные границы Canny.
cv2.imshow("Canny Edges", edges)


# Показываем итог с выделенными препятствиями.
cv2.imshow("Parking Sensor Result", output)


# Сохраняем результат.
cv2.imwrite("parking_sensor_result.jpg", output)


# Ждём нажатия клавиши.
cv2.waitKey(0)


# Закрываем окна.
cv2.destroyAllWindows()