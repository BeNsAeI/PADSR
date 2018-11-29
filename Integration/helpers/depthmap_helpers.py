import cv2
from Integration.Image_Depth_Generator.Advanced import DepthMapCreator
from Integration.Image_Depth_Generator.Fast import DepthMapCreator_2

import Integration.Neural_Network.DIW_transforms
from Integration.Neural_Network.nn2 import get_depth_image_using_CNN

def create_depth_map(img_left, img_right, fast, nn):
    """
    Convert left image and right image into depth map image.
    Need to pick a good set of matcher parameter to create
    good quality depth map image

    Input: left image and right image (either RGB fornmat or gray format)

    Output: depth map image
    """

    if nn:
        size = (img_left.shape[1], img_left.shape[0])
        print("Create Depth maps using CNN")
        return get_depth_image_using_CNN(img_left, img_right, size)

    matcher_parameters = init_matcher_parameters(windowSize=5,
            minDisparity=0,
            numDisparities=16 * 3,
            blockSize=5,
            disp12MaxDiff=1,
            uniquenessRatio=5,
            speckleWindowSize=0,
            speckleRange=2,
            preFilterCap=63,
            mode=cv2.STEREO_SGBM_MODE_SGBM)

    filter_parameters = dict()
    filter_parameters['lmbda'] = 80000
    filter_parameters['sigma'] = 1.20

    dmc = None
    if fast:
        # fast depthmap creator
        dmc = DepthMapCreator_2(matcher_parameters)
    else:
        # advance depthmap creator
        dmc = DepthMapCreator(filter_parameters, matcher_parameters)

    depth_image = dmc.get_depth_image(img_left, img_right)

    return depth_image


def init_matcher_parameters(windowSize=0,
                            minDisparity=0,
                            numDisparities=16,
                            blockSize=3,
                            disp12MaxDiff=0,
                            preFilterCap=0,
                            uniquenessRatio=0,
                            speckleWindowSize=0,
                            speckleRange=0,
                            mode=cv2.STEREO_SGBM_MODE_SGBM):
    """
    Initiate all parameters for SGBM matching call
    TODO:   Should factor initiating matcher parameters to
            Seperate class.
    """
    matcher_parameters = dict()
    matcher_parameters['minDisparity'] = minDisparity
    matcher_parameters['numDisparities'] = numDisparities
    matcher_parameters['blockSize'] = blockSize
    matcher_parameters['P1'] = 8 * 3 * windowSize ** 2
    matcher_parameters['P2'] = 32 * 3 * windowSize ** 2
    matcher_parameters['disp12MaxDiff'] = disp12MaxDiff
    matcher_parameters['uniquenessRatio'] = uniquenessRatio
    matcher_parameters['speckleWindowSize'] = speckleWindowSize
    matcher_parameters['speckleRange'] = speckleRange
    matcher_parameters['preFilterCap'] = preFilterCap
    matcher_parameters['mode'] = mode

    return matcher_parameters

