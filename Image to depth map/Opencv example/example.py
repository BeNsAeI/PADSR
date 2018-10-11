import numpy as np
import cv2
from matplotlib import pyplot as plt

rawL = cv2.imread('Left4.jpg',0)
rawR = cv2.imread('Right4.jpg',0)

#blurL = cv2.GaussianBlur(rawL,(51,51));
#blurR = cv2.GaussianBlur(rawR,(51,51));

#imgL = cv2.cvtColor(blurL,cv2.COLOR_BGR2GRAY)
#imgR = cv2.cvtColor(blurR,cv2.COLOR_BGR2GRAY)

#stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=64, SADWindowSize=25)
#disparity = stereo.compute(imgL,imgR)
disparity = stereo.compute(rawL,rawR)
cv2.imwrite("Test5.jpg", disparity)
#plt.imshow(disparity,'gray')
#plt.show()
