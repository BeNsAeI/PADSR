import cv2
import numpy as np
from sklearn.preprocessing import normalize

filename = "screenshot"

img_left  = cv2.imread(filename+'-1.png')
img_right = cv2.imread(filename+'-0.png')

window_size = 15

left_matcher = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16,
    blockSize=5,
    P1=8 * 3 * window_size ** 2,
    P2=32 * 3 * window_size ** 2,
    # disp12MaxDiff=1,
    # uniquenessRatio=15,
    # speckleWindowSize=0,
    # speckleRange=2,
    # preFilterCap=63,
    # mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)

right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
wls_filter.setLambda(80000)
wls_filter.setSigmaColor(1.2)

disparity_left  = left_matcher.compute(img_left, img_right)
disparity_right = right_matcher.compute(img_right, img_left)
disparity_left  = np.int16(disparity_left)
disparity_right = np.int16(disparity_right)
filteredImg     = wls_filter.filter(disparity_left, img_left, None, disparity_right)

depth_map = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
depth_map = np.uint8(depth_map)
depth_map = cv2.bitwise_not(depth_map) # Invert image. Optional depending on stereo pair
cv2.imwrite(filename+"-depth.png",depth_map)
