import numpy as np
from sklearn.preprocessing import normalize
import cv2

class CreateDepthMap:
    window_size = 5
    std_img_size = (858,480) #480p at 16:9 resolution
    default_matcher_params = {
        'minDisparity' : 0,
        'numDisparities' : 16*3,
        'blockSize' : 5,
        'P1' : 8 * 3 * window_size ** 2,
        'P2' : 32 * 3 * window_size ** 2,
        'disp12MaxDiff' : 1,
        'uniquenessRatio' : 15,
        'speckleWindowSize' : 0,
        'speckleRange' : 2,
        'preFilterCap' : 63,
        'mode' : cv2.STEREO_SGBM_MODE_SGBM_3WAY
    }
    
    default_filter_params = {
        'lmbda' : 8000,
        'sigma' : 1.2,
        'visual_multiplier' : 1.0  
    }

    def __init__(self, matcher_parameters=default_matcher_params, filter_parameters=default_filter_params):
        self.left_matcher = cv2.StereoSGBM_create(
                                minDisparity=matcher_parameters['minDisparity'],
                                numDisparities=matcher_parameters['numDisparities'],             
                                blockSize=matcher_parameters['blockSize'],
                                P1=matcher_parameters['P1'],    
                                P2=matcher_parameters['P2'],
                                disp12MaxDiff=matcher_parameters['disp12MaxDiff'],
                                uniquenessRatio=matcher_parameters['uniquenessRatio'],
                                speckleWindowSize=matcher_parameters['speckleWindowSize'],
                                speckleRange=matcher_parameters['speckleRange'],
                                preFilterCap=matcher_parameters['preFilterCap'],
                                mode=matcher_parameters['mode']
        )

        self.right_matcher = cv2.ximgproc.createRightMatcher(self.left_matcher)
        
        self.wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=self.left_matcher)
        self.wls_filter.setLambda(filter_parameters['lmbda'])
        self.wls_filter.setSigmaColor(filter_parameters['sigma'])


    def get_depth_image(self, left_image, right_image):
        left_image = cv2.resize(left_image, self.std_img_size)
        right_image = cv2.resize(right_image, self.std_img_size)
        
        displ = self.left_matcher.compute(left_image, right_image)  
        dispr = self.right_matcher.compute(right_image, left_image) 
        displ = np.int16(displ)
        dispr = np.int16(dispr)

        filtered_image = self.wls_filter.filter(displ, left_image, None, dispr)
        filtered_image = cv2.normalize(src=filtered_image, dst=filtered_image, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
        return np.uint8(filtered_image)

#x = CreateDepthMap()
#plt.imshow(x.get_depth_image(cv2.imread('frame-left.jpg'), cv2.imread('frame-right.jpg')), 'gray')