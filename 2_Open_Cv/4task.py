import cv2
import numpy as np
import random

img_path = '/1_Open_Cv/куки.jpg'
original_img = cv2.imread(img_path)


height, width = original_img.shape[:2]

img_float = original_img.astype(np.float32)

img_normalized = img_float / 255.0
hsv_img = cv2.cvtColor(img_normalized, cv2.COLOR_BGR2HSV)

hsv_img[:, :, 1] = hsv_img[:, :, 1] * 0.5

img_float = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR) * 255.0

kernel_x = cv2.getGaussianKernel(width, width / 2)
kernel_y = cv2.getGaussianKernel(height, height / 2)

kernel_2d = kernel_y * kernel_x.T

# Нормализуем маску, чтобы в центре была 1.0, а по краям стремилось к 0
mask = kernel_2d / kernel_2d.max()

# Дублируем маску на 3 канала (для B, G, R)
mask_3d = np.dstack([mask, mask, mask])

# умножаем изображение на маску (края станут темными)
img_float = img_float * mask_3d

yellow_tint = np.zeros_like(img_float)
yellow_tint[:, :, 1] = 40  # Зеленый канал
yellow_tint[:, :, 2] = 50  # Красный канал

# Прибавляем желтизну, но только там, где маска яркая (в центре)
img_float = img_float + (yellow_tint * mask_3d)

noise = np.random.normal(loc=0, scale=15, size=img_float.shape)
img_float = img_float + noise

num_scratches = 30
for _ in range(num_scratches):
    x1 = random.randint(0, width)
    y1 = random.randint(0, height)

    x2 = x1 + random.randint(-20, 20)
    y2 = y1 + random.randint(-50, 50)

    # Случайный цвет царапины (от серого до белого)
    color = random.randint(150, 255)
    thickness = random.randint(1, 2)

    cv2.line(img_float, (x1, y1), (x2, y2), (color, color, color), thickness)

num_spots = 40
for _ in range(num_spots):
    cx = random.randint(0, width)
    cy = random.randint(0, height)
    radius = random.randint(1, 3)
    color = random.randint(50, 200)  # Темные и светлые пятна
    cv2.circle(img_float, (cx, cy), radius, (color, color, color), -1)

final_img = np.clip(img_float, 0, 255).astype(np.uint8)

combined = np.hstack((original_img, final_img))

# Выводим на экран (можно уменьшить размер окна, если картинка огромная)
cv2.imshow('Original vs Vintage', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()