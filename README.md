# ALL_OPEN_CV

Учебный проект по **Python + OpenCV**, включающий набор практических задач по компьютерному зрению: от базовой обработки изображений до детекции движения, поиска шаблонов, выделения углов, границ и восстановления изображений.

Проект организован по папкам, где каждая директория содержит отдельный блок задач.

---

# Структура проекта

```text
ALL_OPEN_CV/
│
├── 1_Open_Cv/
├── 2_Open_Cv/
├── 3_or_2_Open_Cv/
│
├── 4_Open_Cv/
│   ├── 6.py
│   ├── 7.py
│   ├── 8.py
│   ├── video.mp4
│   ├── package.jpg
│   ├── logo.png
│   └── building.jpg
│
├── 5_Open_Cv/
│   ├── 9.py
│   ├── 10.py
│   ├── image.jpg
│   └── road.jpg
│
└── venv/
```

---

# Установка

## Создать окружение

```bash
python -m venv venv
```

Активация:

Linux/Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## Установка зависимостей

```bash
pip install opencv-python numpy
```

---

# Теоретическая база OpenCV

## Что такое изображение в OpenCV

Изображение — это матрица NumPy.

```python
img.shape
```

Возвращает:

```text
(height, width, channels)
```

Пример:

```text
800 x 600 x 3
```

---

## Цвета

OpenCV использует:

```text
BGR
```

а не RGB.

```python
(255,0,0)   # Blue
(0,255,0)   # Green
(0,0,255)   # Red
```

---

## Координаты

```text
(0,0) — левый верхний угол

x растет вправо
y растет вниз
```

---

# Основные функции OpenCV

## Загрузка изображения

```python
cv2.imread()
```

---

## Сохранение

```python
cv2.imwrite()
```

---

## Отображение

```python
cv2.imshow()
cv2.waitKey()
cv2.destroyAllWindows()
```

---

# Блок 4 — Продвинутые задачи

---

# Задача 6 — Робастный детектор движения

## Идея

Нужно отделить:

```text
Фон
от
Движущихся объектов
```

---

## Метод MOG2

Используется:

```python
cv2.createBackgroundSubtractorMOG2()
```

Параметры:

### history

Сколько кадров помнить.

```text
больше history →
стабильнее фон
```

---

### varThreshold

Порог чувствительности.

```text
меньше → больше ложных тревог

больше → игнорирование мелкого шума
```

---

### detectShadows

```python
detectShadows=True
```

Позволяет отделять тени.

---

## Морфология

### Эрозия

```python
cv2.erode()
```

Убирает шум.

---

### Дилатация

```python
cv2.dilate()
```

Расширяет объекты.

---

## Открытие

```text
erosion + dilation
```

```python
cv2.MORPH_OPEN
```

Удаляет шум.

---

## Закрытие

```text
dilation + erosion
```

```python
cv2.MORPH_CLOSE
```

Закрывает разрывы.

---

## Контуры

```python
cv2.findContours()
```

---

## Площадь объекта

```python
cv2.contourArea()
```

Позволяет игнорировать мелкие области.

---

## Рамка вокруг движения

```python
cv2.boundingRect()
cv2.rectangle()
```

---

---

# Задача 7 — Поиск логотипа

Используется:

```python
cv2.matchTemplate()
```

---

## Принцип

Шаблон скользит по изображению:

```text
сравнить шаблон
в каждой точке
```

---

## Метод сравнения

```python
cv2.TM_CCOEFF_NORMED
```

---

## Лучшее совпадение

```python
cv2.minMaxLoc()
```

Возвращает:

```text
max_val
max_loc
```

---

## Порог качества

```text
если max_val > threshold
логотип найден
```

---

## Рамка логотипа

```python
cv2.rectangle()
```

---

---

# Задача 8 — Детектор Харриса

Поиск углов:

```python
cv2.cornerHarris()
```

---

## Что считается углом

```text
окно
стык
угол стены
крыша
```

---

## Параметры

```python
blockSize
ksize
k
```

---

### blockSize

Размер области анализа.

---

### ksize

Размер ядра Собеля.

---

### k

Коэффициент чувствительности.

Часто:

```text
0.04
```

---

## Фильтрация углов

```text
оставить только сильные
```

---

## Маршрут

```python
cv2.line()
```

Соединение угловых точек.

---

# Блок 5 — Границы

---

# Задача 9 — Фильтр Собеля

```python
cv2.Sobel()
```

---

## Sobel X

```text
Вертикальные границы
```

---

## Sobel Y

```text
Горизонтальные границы
```

---

## Производные

```python
dx=1 dy=0
dx=0 dy=1
```

---

## Объединение

```python
cv2.addWeighted()
```

---

## Инверсия

```python
cv2.bitwise_not()
```

Черные линии на белом фоне.

---

# Задача 10 — Детектор Canny

```python
cv2.Canny()
```

---

## Два порога

```python
threshold1
threshold2
```

---

### Нижний порог

Отсекает шум.

---

### Верхний порог

Оставляет сильные границы.

---

## Размытие перед Canny

```python
cv2.GaussianBlur()
```

Убирает шум.

---

## Контуры объектов

```python
cv2.findContours()
```

---

## Поиск прямоугольников

```python
cv2.approxPolyDP()
```

Если:

```text
4 вершины
```

возможно машина.

---

# Дополнительные полезные функции

## Текст

```python
cv2.putText()
```

---

## Круг

```python
cv2.circle()
```

---

## Линия

```python
cv2.line()
```

---

## Маркер

```python
cv2.drawMarker()
```

---

# Запуск задач

---

## Детектор движения

```bash
python 4_Open_Cv/6.py
```

---

## Поиск логотипа

```bash
python 4_Open_Cv/7.py
```

---

## Харрис

```bash
python 4_Open_Cv/8.py
```

---

## Sobel

```bash
python 5_Open_Cv/9.py
```

---

## Canny

```bash
python 5_Open_Cv/10.py
```

---

# Входные данные

---

## Для 6.py

```text
video.mp4
```

Видео наблюдения.

---

## Для 7.py

```text
package.jpg
logo.png
```

---

## Для 8.py

```text
building.jpg
```

---

## Для 9.py

```text
image.jpg
```

---

## Для 10.py

```text
road.jpg
```

---

# Используемые библиотеки

- Python
- OpenCV
- NumPy

---

# Темы проекта

✔ Image Processing  
✔ Motion Detection  
✔ Background Subtraction  
✔ Template Matching  
✔ Harris Corners  
✔ Sobel  
✔ Canny  
✔ Morphology  
✔ Contours

---

# Назначение проекта

Проект создан как:

- учебный практикум
- набор лабораторных работ
- портфолио по Computer Vision
- база для дальнейшего изучения OpenCV

---


Python / Computer Vision practice repository.
