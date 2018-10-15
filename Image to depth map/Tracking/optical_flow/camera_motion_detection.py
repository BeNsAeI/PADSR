import cv2
import numpy as np

image1 = cv2.imread("right.jpg")
image2 = cv2.imread("left.jpg")

prvs = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
next = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
horz = cv2.normalize(flow[...,0], None, 0, 255, cv2.NORM_MINMAX)     
# vert = cv2.normalize(flow[...,1], None, 0, 255, cv2.NORM_MINMAX)
horz = flow[...,0].astype('uint8')
# vert = vert.astype('uint8')

if flow[...,0].sum() > 0:
    print("Camera moves to the right")
else:
    print("Camera moves to the left")
cv2.imshow('Horizontal Component', horz)
# cv2.imshow('Vertical Component', vert)

k = cv2.waitKey(0) & 0xff
if k == ord('s'): 
    cv2.imwrite('opticalflow_horz.pgm', horz)
    # cv2.imwrite('opticalflow_vert.pgm', vert)

cv2.destroyAllWindows()
cv2.waitKey(0)