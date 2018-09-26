import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('Left.jpg',0)
imgR = cv2.imread('Right.jpg',0)
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
disparity = stereo.compute(imgL,imgR)
cv2.imwrite("Test.jpg", disparity)
#plt.imshow(disparity,'gray')
#plt.show()
