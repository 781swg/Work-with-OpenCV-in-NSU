import cv2
import numpy as np

img = cv2.imread('/1_Open_Cv/куки.jpg')

rows,cols = img.shape[:2]

rotaion_matrix = cv2.getRotationMatrix2D((cols/2,rows/2),45,1)
rotated_img = cv2.warpAffine(img, rotaion_matrix, (cols, rows))
cv2.circle(rotated_img,(100,100),50,(0,0,255),-1)
cv2.rectangle(rotated_img,(200,200),(300,300),(0,255,0),2)
cv2.putText(rotated_img, 'Hello!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.imwrite('output.jpg', rotated_img)
