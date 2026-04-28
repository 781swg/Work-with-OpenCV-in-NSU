import cv2
import numpy as np
import random
path = '/1_Open_Cv/куки.jpg'
img = cv2.imread(path)

if img is None:
    print("Ошибка: не удалось найти файл по указанному пути!")
    exit()

img_original = img.copy()

img = cv2.flip(img, 1)

height, width, _ = img.shape

cv2.circle(img, (width - 100, 100), 60, (0, 215, 255), -1)

for _ in range(500):
    rx = np.random.randint(0, width)
    ry = np.random.randint(0, height)
    img[ry, rx] = [255, 255, 255]

cv2.putText(img, 'Happy Winter!', (50, height - 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

ball_center = (width // 3, height // 2)
cv2.circle(img, ball_center, 45, (0, 128, 0), -1) # Темно-зеленый шар
cv2.putText(img, 'NEW YEAR', (ball_center[0] - 40, ball_center[1] + 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

cv2.imwrite('new_year_tree.jpg', img)

cv2.imshow('Original', img_original)
cv2.imshow('New Year Result', img)

cv2.waitKey(0)
cv2.destroyAllWindows()