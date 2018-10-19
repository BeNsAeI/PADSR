import cv2
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from Image_Depth_Generator.Advanced import DepthMapCreator
from Image_Depth_Generator.Fast import DepthMapCreator_2


def init_matcher_parameters(windowSize = 0,
                            minDisparity = 0,
                            numDisparities = 16,
                            blockSize = 3,
                            disp12MaxDiff = 0,
                            preFilterCap = 0,
                            uniquenessRatio = 0,
                            speckleWindowSize = 0,
                            speckleRange = 0,
                            mode = cv2.STEREO_SGBM_MODE_SGBM):
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
    matcher_parameters['mode'] = cv2.STEREO_SGBM_MODE_SGBM

    return matcher_parameters

def change_minDisparity(matcher_paramaters, dis_value):
    """
    Minimum possible disparity value. Normally, it is zero but sometimes
    rectification algorithms can shift images, so this parameter needs to be adjusted accordingly.
    """
    matcher_paramaters['minDisparity'] = dis_value

def change_numDisparities(matcher_paramaters, num_dis):
    """
    Maximum disparity minus minimum disparity. The value is always greater than zero.
    In the current implementation, this parameter must be divisible by 16.
    """
    matcher_paramaters['numDisparities'] = num_dis

def change_blockSize(matcher_paramaters, blockSize):
    """
    Matched block size. It must be an odd number >=1 .
    Normally, it should be somewhere in the 3..11 range.
    """
    matcher_paramaters['blockSize'] = blockSize

def change_speckleWindowSize(matcher_paramaters, speckleWindowSize):
    """
    Maximum size of smooth disparity regions to consider their noise
    speckles and invalidate. Set it to 0 to disable speckle filtering.
    Otherwise, set it somewhere in the 50-200 range.
    """
    matcher_paramaters['speckleWindowSize'] = speckleWindowSize

def change_speckleRange(matcher_paramaters, speckleRange):
    """
    Maximum disparity variation within each connected component.
    If you do speckle filtering, set the parameter to a positive value,
    it will be implicitly multiplied by 16. Normally, 1 or 2 is good enough.
    """
    matcher_paramaters['speckleRange'] = speckleRange

def change_disp12MaxDiff(matcher_paramaters, disp12MaxDiff):
    """
    Maximum allowed difference (in integer pixel units) in
    the left-right disparity check. Set it to a non-positive value to disable the check.
    """
    matcher_paramaters['disp12MaxDiff'] = disp12MaxDiff

def test_both_methods(imgL, imgR):
    """
    Make function calls of DepthMapCreator and DepthCreator_2
    Visually compare output
    """
    matcher_parameters = init_matcher_parameters(windowSize=3,
                            minDisparity = 16,
                            numDisparities = 16,
                            blockSize = 15,
                            disp12MaxDiff = 1,
                            uniquenessRatio = 10,
                            speckleWindowSize = 100,
                            speckleRange = 32,
                            mode = cv2.STEREO_SGBM_MODE_SGBM)

    # FILTER Parameters
    filter_parameters = dict()
    filter_parameters['lmbda'] = 80000
    filter_parameters['sigma'] = 1.2

    dmc = DepthMapCreator(filter_parameters, matcher_parameters)
    dmc_2 = DepthMapCreator_2(matcher_parameters)

    return dmc, dmc_2

def test_DMC_1(imgL, imgR):
    matcher_parameters = init_matcher_parameters(windowSize=5,
                            minDisparity = 0,
                            numDisparities = 16 * 3,
                            blockSize = 5,
                            disp12MaxDiff = 1,
                            uniquenessRatio = 5,
                            speckleWindowSize = 0,
                            speckleRange = 2,
                            preFilterCap=63,
                            mode = cv2.STEREO_SGBM_MODE_SGBM)

    filter_parameters = dict()
    filter_parameters['lmbda'] = 80000
    filter_parameters['sigma'] = 1.20

    dmc = DepthMapCreator(filter_parameters, matcher_parameters)


    depth_image = dmc.get_depth_image(imgL, imgR)

    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

    cv2.imwrite("test_DMC1.jpg", depth_image)

    return depth_image

def test_DMC_2(imgL, imgR):
    matcher_parameters = init_matcher_parameters(windowSize=5,
                            minDisparity = 0,
                            numDisparities = 16 * 3,
                            blockSize = 5,
                            disp12MaxDiff = 1,
                            uniquenessRatio = 5,
                            speckleWindowSize = 0,
                            speckleRange = 2,
                            preFilterCap=63,
                            mode = cv2.STEREO_SGBM_MODE_SGBM)

    dmc_2 = DepthMapCreator_2(matcher_parameters)

    depth_image = dmc_2.get_depth_image(imgL, imgR)

    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

    cv2.imwrite("test_DMC2.jpg", depth_image)

    return depth_image

def test_windowSize(imgL, imgR, resultPath = 'windowSizeResult'):
    """
    Test different value of windowSize in range of [0,25]
    """

    matcher_paramaters = init_matcher_parameters()
    dmc_2 = DepthMapCreator_2(matcher_paramaters)


    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for windowSize in range(50):
        file_name = 'result' + str(windowSize) + '.jpg'

        dmc_2.set_window_size(windowSize)
        depth_image = dmc_2.get_depth_image(imgL, imgR)
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_numDisparities(imgL, imgR, resultPath = 'test_numDisparities'):
    """
    Test different value of numDisparities with multiplier in range of [1, 25]
    """

    matcher_paramaters = init_matcher_parameters()

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for multiplier in range(1, 25):
        numDisparities = 16 * multiplier
        file_name = 'result' + str(numDisparities) + '.jpg'

        change_numDisparities(matcher_paramaters, numDisparities)

        dmc_2 = DepthMapCreator_2(matcher_paramaters)


        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_minDisparity(imgL, imgR, resultPath = 'test_minDisparity'):
    """
    Test different value of minDisparity in range of [0,25]
    """

    matcher_paramaters = init_matcher_parameters()

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for minDisparity in range(50):
        file_name = 'result' + str(minDisparity) + '.jpg'

        change_minDisparity(matcher_paramaters, minDisparity)

        dmc_2 = DepthMapCreator_2(matcher_paramaters)

        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_blockSize(imgL, imgR, resultPath = 'test_blockSize'):
    """
    Test different value of blockSize in range of [0,25]
    """

    matcher_paramaters = init_matcher_parameters()

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for blockSize in range(3, 29):
        file_name = 'result' + str(blockSize) + '.jpg'

        print("Saving file " + file_name)

        change_blockSize(matcher_paramaters, blockSize)

        dmc_2 = DepthMapCreator_2(matcher_paramaters)

        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_preFilterCap(imgL, imgR, resultPath = 'test_preFilterCap'):
    """
    Test different value of preFilterCap in range of [1,200]
    """

    matcher_paramaters = init_matcher_parameters()
    dmc_2 = DepthMapCreator_2(matcher_paramaters)


    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for value in range(1, 200):
        file_name = 'result' + str(value) + '.jpg'

        dmc_2.set_preFilterCap(value)

        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_UniquenessRatio(imgL, imgR, resultPath = 'test_UniquenessRatio'):
    """
    Test different value of UniquenessRatio in range of [1, 15]
    """

    matcher_paramaters = init_matcher_parameters()
    dmc_2 = DepthMapCreator_2(matcher_paramaters)


    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for value in range(1, 15):
        file_name = 'result' + str(value) + '.jpg'

        dmc_2.set_uniquenessRatio(value)

        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_speckleWindowSize(imgL, imgR, resultPath = 'test_speckleWindowSize'):
    """
    Test different value of speckleWindowSize with multiplier in range of [50, 200]
    """

    matcher_paramaters = init_matcher_parameters()

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for value in range(50, 200):
        file_name = 'result' + str(value) + '.jpg'

        change_speckleWindowSize(matcher_paramaters, value)

        dmc_2 = DepthMapCreator_2(matcher_paramaters)

        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_speckleRange(imgL, imgR, resultPath = 'test_speckleRange'):
    """
    Test different value of speckleRange with multiplier in range of [1, 20]
    """

    matcher_paramaters = init_matcher_parameters()

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for value in range(1, 20):
        file_name = 'result' + str(value) + '.jpg'

        change_speckleRange(matcher_paramaters, value)

        dmc_2 = DepthMapCreator_2(matcher_paramaters)

        depth_image = dmc_2.get_depth_image(imgL, imgR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def test_allParameters(imgL, imgR,
                        minDisp_list = [0, 16],
                        numDisp_multiplier_list = [6, 7, 8],
                        blockSize_list = [3, 7, 11],
                        speckleRange_list = [32],
                        sWS_list = [100],
                        windowSize_list = [3, 5, 7],
                        disp12MaxDiff_list = [1],
                        preFilterCap_list = [100],
                        uniquenessRatio_list = [15],
                        resultPath = 'test_allParameters_1'):
    """
    Parameters to tests:
        minDisparity(md):
        numDisparity(nd):
        blockSize(bs):
        speckleRange(sR) :
        speckleWindowSize(sWS):
        disp12MaxDiff(d12MD)
        windowSize(wS):
        preFilterCap(pFC):
        uniquenessRatio(uR):
    """

    print('Test all parameters')
    matcher_paramaters = init_matcher_parameters()

    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    for md in minDisp_list:
        change_minDisparity(matcher_paramaters, md)

        for multiplier in numDisp_multiplier_list:
            nd = multiplier * 16
            change_numDisparities(matcher_paramaters, nd)

            for bS in blockSize_list:
                change_blockSize(matcher_paramaters, bS)

                for sR in speckleRange_list:
                    change_speckleRange(matcher_paramaters, sR)

                    for sWS in sWS_list:
                        change_speckleWindowSize(matcher_paramaters, sWS)

                        for d12MD in disp12MaxDiff_list:
                            change_disp12MaxDiff(matcher_paramaters, d12MD)

                            dmc_2 = DepthMapCreator_2(matcher_paramaters)

                            for wS in windowSize_list:
                                dmc_2.set_window_size(wS)

                                for pFC in preFilterCap_list:
                                    dmc_2.set_preFilterCap(pFC)

                                    for uR in uniquenessRatio_list:
                                        dmc_2.set_uniquenessRatio(uR)

                                        file_name = 'md'  + str(md) + '_nd' + str(nd) + '_bS' + str(bS) + '_sR' + str(sR) + '_sWS' + str(sWS) + '_d12MD' + str(d12MD) + '_wS' + str(wS) + '_pFC' + str(pFC) + '_uR' + str(uR) + '.jpg'
                                        print(file_name + ' is processing ...')

                                        depth_image = dmc_2.get_depth_image(imgL, imgR)

                                        font = cv2.FONT_HERSHEY_SIMPLEX
                                        #cv2.putText(depth_image, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)

                                        cv2.imwrite(os.path.join(resultPath, file_name), depth_image)

def create_depth_map(imgL, imgR):

    margin = int(imgL.shape[1] / 2)
    imgL=cv2.copyMakeBorder(imgL, top=0, bottom=0, left=margin, right=0, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
    imgR=cv2.copyMakeBorder(imgR, top=0, bottom=0, left=margin, right=0, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
    # disparity range is tuned for 'aloe' image pair
    window_size = 3
    min_disp = 16
    max_disp = 128
    num_disp = max_disp-min_disp
    stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
        numDisparities = num_disp,
        blockSize = 8,
        P2 = 8*3*window_size**2,
        P1 = 32*3*window_size**2,
        disp12MaxDiff = 1,
        uniquenessRatio = 10,
        speckleWindowSize = 100,
        speckleRange = 32
    )
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0
    disp = disp[:,margin:]
    disp = np.uint8((disp))

    return disp






imgL = cv2.imread('Left4.jpg')
imgR = cv2.imread('Right4.jpg')

imgL = cv2.resize(imgL, (0,0), fx=0.8, fy=0.8)
imgR = cv2.resize(imgR, (0,0), fx=0.8, fy=0.8)

dm = create_depth_map(imgL, imgR)
font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(dm, str(executing_time),(10,10), font, 0.3,(255,255,255),1,cv2.LINE_AA)
cv2.imshow('frame-dm', dm)
cv2.waitKey()

dm_2 = test_DMC_2(imgL, imgR)
print(dm_2.shape)
cv2.imshow('frame-dm2', dm_2)
cv2.waitKey()

dm_1 = test_DMC_1(imgL, imgR)
print(dm_1.shape)
cv2.imshow('frame-dm1', dm_1)
cv2.waitKey()


test_DMC_2(imgL, imgR)
test_windowSize(imgL, imgR)

test_minDisparity(imgL, imgR)

test_numDisparities(imgL, imgR)

test_blockSize(imgL, imgR)

test_preFilterCap(imgL, imgR)

test_UniquenessRatio(imgL, imgR)

test_speckleWindowSize(imgL, imgR)
test_speckleRange(imgL, imgR)

test_allParameters(imgL, imgR)

