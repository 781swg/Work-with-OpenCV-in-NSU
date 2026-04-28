import cv2
import numpy as np


# Открываем видеофайл.
# Если хочешь использовать веб-камеру, замени 'video.mp4' на 0.
cap = cv2.VideoCapture('video.mp4')


# Создаём модель вычитания фона MOG2.
# history — сколько кадров используется для построения модели фона.
# varThreshold — чувствительность: чем больше значение, тем меньше ложных срабатываний.
# detectShadows=True — включает обнаружение теней.
back_sub = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=50,
    detectShadows=True
)


# Создаём ядро для морфологических операций.
# Оно нужно, чтобы удалять мелкий шум и соединять разорванные части объектов.
kernel = np.ones((5, 5), np.uint8)


while True:
    # Считываем очередной кадр из видео.
    # ret показывает, успешно ли считан кадр.
    # frame — сам кадр изображения.
    ret, frame = cap.read()

    # Если кадр не считался, значит видео закончилось или произошла ошибка.
    if not ret:
        break

    # Уменьшаем размер кадра для повышения производительности.
    # Это помогает программе работать быстрее в реальном времени.
    frame = cv2.resize(frame, (800, 450))

    # Слегка размываем кадр.
    # GaussianBlur уменьшает мелкий шум: дождь, снег, дрожание камеры, листья.
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    # Применяем модель вычитания фона.
    # На выходе получаем маску:
    # 0 — фон,
    # 127 — тень,
    # 255 — движущийся объект.
    fg_mask = back_sub.apply(blurred)

    # Убираем тени и слабые изменения.
    # Всё, что меньше 200, становится чёрным.
    # Всё, что больше 200, становится белым.
    _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

    # Морфологическое открытие.
    # Удаляет мелкие белые точки и случайный шум.
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Морфологическое закрытие.
    # Соединяет близкие белые области, если объект получился разорванным.
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

    # Дополнительное расширение белых областей.
    # Помогает лучше объединить части одного движущегося объекта.
    cleaned = cv2.dilate(cleaned, kernel, iterations=2)

    # Находим контуры на очищенной маске.
    # Контуры — это границы белых областей, то есть возможных движущихся объектов.
    contours, _ = cv2.findContours(
        cleaned,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Флаг тревоги.
    # Станет True, если найден крупный движущийся объект.
    motion_detected = False

    # Проходим по всем найденным контурам.
    for contour in contours:
        # Считаем площадь контура.
        area = cv2.contourArea(contour)

        # Игнорируем маленькие области.
        # Это помогает не реагировать на дождь, листья, шум, блики.
        if area < 1500:
            continue

        # Если контур достаточно большой, считаем, что движение обнаружено.
        motion_detected = True

        # Получаем прямоугольник, который охватывает движущийся объект.
        x, y, w, h = cv2.boundingRect(contour)

        # Рисуем зелёную рамку вокруг движущегося объекта.
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Подписываем объект.
        cv2.putText(
            frame,
            "Moving object",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Если найдено существенное движение, выводим предупреждение.
    if motion_detected:
        cv2.putText(
            frame,
            "ALARM: MOTION DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )
    else:
        cv2.putText(
            frame,
            "No significant motion",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    # Показываем итоговый кадр с рамками.
    cv2.imshow("Robust Motion Detection", frame)

    # Показываем очищенную маску движения.
    # Это нужно для контроля качества обработки.
    cv2.imshow("Motion Mask", cleaned)

    # Останавливаем программу, если нажата клавиша q.
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


# Освобождаем видеофайл или камеру.
cap.release()

# Закрываем все окна OpenCV.
cv2.destroyAllWindows()