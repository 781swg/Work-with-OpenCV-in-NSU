import cv2
import numpy as np

# Загружаем поврежденную картину
img_path = '/1_Open_Cv/куки.jpg'
original_img = cv2.imread(img_path)

if original_img is None:
    print("Ошибка загрузки изображения!")
    exit()

# ==========================================
# ШАГ 1: Усредняющий фильтр (Размытие)
# ==========================================
# Задаем размер окна (ядра) 5x5 пикселей
blur_kernel_size = (5, 5)
blurred_img = cv2.blur(original_img, blur_kernel_size)

# ==========================================
# ШАГ 2: Морфологические операции
# ==========================================
# Создаем структурный элемент (ядро) для морфологии.
# Это просто матрица из единиц размером 5x5.
morph_kernel = np.ones((5, 5), np.uint8)

# Применяем эрозию (сужение светлых участков)
eroded_img = cv2.erode(blurred_img, morph_kernel, iterations=1)

# Применяем дилатацию (расширение светлых участков обратно)
restored_img = cv2.dilate(eroded_img, morph_kernel, iterations=1)

# ==========================================
# ФИНАЛ: Отображение результатов
# ==========================================
# Склеиваем оригинал и результат по горизонтали
combined = np.hstack((original_img, restored_img))

# Чтобы окно не было слишком огромным, можно его немного уменьшить перед выводом
# height, width = combined.shape[:2]
# combined = cv2.resize(combined, (width // 2, height // 2))

cv2.imshow('Original vs Restored', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()