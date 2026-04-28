import cv2
import numpy as np

img1 = cv2.imread('/1_Open_Cv/куки.jpg')
img2 = cv2.imread('/1_Open_Cv/жирность.jpg')

if img1 is None or img2 is None:
    print("Не удалось найти файлы по указанным путям!")
    exit()

height, width = img1.shape[:2]
img2_resized = cv2.resize(img2, (width, height))

summed = cv2.addWeighted(img1, 0.5, img2_resized, 0.5, 0)

mean = 0
var = 10
sigma = var ** 0.5
noise = np.random.normal(mean, sigma, summed.shape).astype(np.uint8)
noisy_img = cv2.add(summed, noise)

cv2.imshow('Noisy Summed Image', noisy_img)
cv2.waitKey(0)
cv2.destroyAllWindows()