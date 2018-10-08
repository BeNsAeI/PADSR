import numpy as np
import cv2
from matplotlib import pyplot as plt

rawL = cv2.imread('Left1.jpg')
rawR = cv2.imread('Right1.jpg')

blurL = cv2.GaussianBlur(rawL,(51,51),0);
blurR = cv2.GaussianBlur(rawR,(51,51),0);

imgL = cv2.cvtColor(blurL,cv2.COLOR_BGR2GRAY)
imgR = cv2.cvtColor(blurR,cv2.COLOR_BGR2GRAY)

#stereo = cv2.StereoBM_create(numDisparities=32, blockSize=13)
stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=64, SADWindowSize=25)
disparity = stereo.compute(imgL,imgR)
cv2.imwrite("Test3.jpg", disparity)
#plt.imshow(disparity,'gray')
#plt.show()
