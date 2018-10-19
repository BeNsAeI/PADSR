import os
import numpy as np
from sklearn.preprocessing import normalize
import cv2

class DepthMapCreator:
    """ Description goes here """

    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
    window_size = 3      


    def __init__(self, filter_parameters, matcher_parameters = None):
        if filter_parameters is None:
            raise ValueError("filter_parameters is None")

        if (matcher_parameters is None):
            self.left_matcher = cv2.StereoSGBM_create(minDisparity=0)
        else:
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


        # initiate right matcher
        self.right_matcher = cv2.ximgproc.createRightMatcher(self.left_matcher)

        # initiate filter
        self.wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=self.left_matcher)
        self.wls_filter.setLambda(filter_parameters['lmbda'])
        self.wls_filter.setSigmaColor(filter_parameters['sigma'])


    def get_depth_image(self, left_image, right_image):

        if left_image is None:
            raise ValueError("left_image is None")
        if right_image is None:
            raise ValueError("right_image is None")

        displ = self.left_matcher.compute(left_image, right_image)
        dispr = self.right_matcher.compute(right_image, left_image)

        displ = np.int16(displ)
        dispr = np.int16(dispr)

        filtered_image = self.wls_filter.filter(displ, left_image, None, dispr)  # important to put "imgL" here!!!

        filtered_image = cv2.normalize(src=filtered_image, dst=filtered_image, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
        return np.uint8(filtered_image)
