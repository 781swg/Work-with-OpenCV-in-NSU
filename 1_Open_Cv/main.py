import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('/1_Open_Cv/куки.jpg')


# plt.imshow(img)
# plt.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
b, g, r = cv2.split(img)
img = cv2.merge([b, g, r])
cv2.imshow("Result", b)
cv2.waitKey(0)
