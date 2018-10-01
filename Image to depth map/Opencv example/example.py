import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('Left3.jpg',0)
imgR = cv2.imread('Right3.jpg',0)
#stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=16, SADWindowSize=15)
disparity = stereo.compute(imgL,imgR)
cv2.imwrite("Test3.jpg", disparity)
#plt.imshow(disparity,'gray')
#plt.show()
