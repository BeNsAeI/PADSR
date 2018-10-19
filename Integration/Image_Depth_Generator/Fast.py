import numpy as np
from sklearn.preprocessing import normalize
import cv2

class DepthMapCreator_2(object):
    """ Description goes here """

    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
    window_size = 3      

    def __init__(self, matcher_parameters = None):
        """
        https://docs.opencv.org/trunk/d2/d85/classcv_1_1StereoSGBM.html
        """

        if (matcher_parameters is None):
            self.stereo = cv2.StereoSGBM_create(minDisparity=0)
            self.min_disp = 0
            self.num_disp = 1
        else:
            self.stereo = cv2.StereoSGBM_create(
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

            self.min_disp = matcher_parameters['minDisparity']
            self.num_disp = matcher_parameters['numDisparities']


    def get_depth_image(self, left_image, right_image):

        if left_image is None:
            raise ValueError("left_image is None")
        if right_image is None:
            raise ValueError("right_image is None")

        stereo_image = self.stereo.compute(left_image, right_image).astype(np.float32)/16.0
        stereo_image = (stereo_image - self.min_disp) / self.num_disp
        filtered_image = cv2.normalize(src=stereo_image, dst=stereo_image, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)

        return np.uint8(filtered_image)

    def set_window_size(self, window_size):
        """
        P1: The first parameter controlling the disparity smoothness. 
            P1 is the penalty on the disparity change by plus or minus 1 between neighbor pixels.

        P2: The second parameter controlling the disparity smoothness.
            P2 is the penalty on the disparity change by more than 1 between neighbor pixels.

        The larger the values are, the smoother the disparity is. 
        The algorithm requires P2 > P1 . See stereo_match.cpp sample 
        where some reasonably good P1 and P2 values are shown 
        (like 8*number_of_image_channels*SADWindowSize*SADWindowSize and 
            32*number_of_image_channels*SADWindowSize*SADWindowSize , respectively).

        """
        self.stereo.setP1(8 * 3 * window_size ** 2)
        self.stereo.setP2(32 * 3 * window_size ** 2)

    def set_preFilterCap(self, preFilterCap):
        """
        Truncation value for the prefiltered image pixels. 
        The algorithm first computes x-derivative at each 
        pixel and clips its value by [-preFilterCap, preFilterCap] interval. 
        The result values are passed to the Birchfield-Tomasi pixel cost function. 
        """
        self.stereo.setPreFilterCap(preFilterCap)

    def set_uniquenessRatio(self, uniquenessRatio):
        """
        Margin in percentage by which the best (minimum) computed 
        cost function value should "win" the second best value to 
        consider the found match correct. Normally, a value within 
        the 5-15 range is good enough. 
        """
        self.stereo.setUniquenessRatio(uniquenessRatio)
