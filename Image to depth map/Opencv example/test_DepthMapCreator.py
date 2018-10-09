import cv2
from DepthMapCreator import DepthMapCreator
 
print('loading images...')
imgL = cv2.imread('Left2.jpg')  # downscale images for faster processing
imgR = cv2.imread('Right2.jpg')

# SGBM Parameters -----------------
window_size = 3                     # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely

matcher_parameters = dict()
matcher_parameters['minDisparity'] = 0
matcher_parameters['numDisparities'] = 160             # max_disp has to be dividable by 16 f. E. HH 192, 256
matcher_parameters['blockSize'] = 5
matcher_parameters['P1'] = 8 * 3 * window_size ** 2    
matcher_parameters['P2'] = 32 * 3 * window_size ** 2
matcher_parameters['disp12MaxDiff'] = 1
matcher_parameters['uniquenessRatio'] = 15
matcher_parameters['speckleWindowSize'] = 0
matcher_parameters['speckleRange'] = 2
matcher_parameters['preFilterCap'] = 63
matcher_parameters['mode'] = cv2.STEREO_SGBM_MODE_SGBM_3WAY
 
# FILTER Parameters
filter_parameters = dict()
filter_parameters['lmbda'] = 80000
filter_parameters['sigma'] = 1.2
 
dmc = DepthMapCreator(matcher_parameters, filter_parameters)
filter_image = dmc.get_depth_image(imgL, imgR)

cv2.imwrite("Test_1.jpg", filter_image)

