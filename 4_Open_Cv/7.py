import cv2              # Библиотека OpenCV
import numpy as np      # NumPy для работы с массивами


# Загружаем изображение упаковки.
package = cv2.imread("package.jpg")

# Загружаем изображение логотипа-шаблона.
logo = cv2.imread("logo.png")


# Переводим упаковку в оттенки серого.
# Template matching быстрее и стабильнее работает с одним каналом яркости.
package_gray = cv2.cvtColor(package, cv2.COLOR_BGR2GRAY)

# Переводим логотип в оттенки серого.
logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)


# Выполняем сопоставление шаблона.
# Функция двигает logo_gray по package_gray и считает совпадение в каждой позиции.
result = cv2.matchTemplate(
    package_gray,              # большое изображение
    logo_gray,                 # шаблон, который ищем
    cv2.TM_CCOEFF_NORMED       # метод сравнения; высокий результат означает хорошее совпадение
)


# Находим минимальные и максимальные значения на карте совпадений.
# Для метода TM_CCOEFF_NORMED нас интересует max_val и max_loc.
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)


# Порог уверенности.
# Если max_val ниже этого значения, считаем, что логотип не найден.
threshold = 0.8


# Получаем высоту и ширину логотипа.
# shape[:2] возвращает height и width.
logo_h, logo_w = logo_gray.shape[:2]


# Проверяем, достаточно ли хорошее совпадение.
if max_val >= threshold:
    # max_loc — координаты левого верхнего угла найденного логотипа.
    top_left = max_loc

    # Правый нижний угол вычисляем через размеры логотипа.
    bottom_right = (top_left[0] + logo_w, top_left[1] + logo_h)

    # Рисуем зелёную рамку вокруг найденного логотипа.
    cv2.rectangle(package, top_left, bottom_right, (0, 255, 0), 2)

    # Подписываем качество совпадения.
    cv2.putText(
        package,
        f"Logo found: {max_val:.2f}",
        (top_left[0], top_left[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # Ожидаемые координаты логотипа.
    # Их нужно настроить под конкретную упаковку.
    expected_x, expected_y = 100, 100

    # Допустимое отклонение в пикселях.
    tolerance = 30

    # Фактические координаты найденного логотипа.
    actual_x, actual_y = top_left

    # Сравниваем фактическое положение с ожидаемым.
    if abs(actual_x - expected_x) <= tolerance and abs(actual_y - expected_y) <= tolerance:
        print("Логотип найден и расположен правильно.")
    else:
        print("Ошибка: логотип найден, но расположен неправильно.")

else:
    # Если качество совпадения ниже порога — логотип не найден.
    print("Ошибка: логотип не найден.")


# Показываем результат.
cv2.imshow("Logo Check", package)

# Ждём нажатия любой клавиши.
cv2.waitKey(0)

# Закрываем окна.
cv2.destroyAllWindows()