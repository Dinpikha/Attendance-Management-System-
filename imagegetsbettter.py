import cv2
import numpy as np
image=cv2.imread("Image3.jpg")
kernel=np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
sharpened=cv2.filter2D(image,-1,kernel)
cv2.imwrite("sharpened.jpg",sharpened)