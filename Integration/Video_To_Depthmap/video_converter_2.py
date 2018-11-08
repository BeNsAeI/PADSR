import cv2
import argparse
import numpy as np
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Image_Depth_Generator.Advanced import DepthMapCreator
from Image_Depth_Generator.Fast import DepthMapCreator_2

_DEFAULT_WIDTH = 600
_DEFAULT_HEIGHT = 400

def main():
    args = get_arguments()
    converter = VideoConverter2()
    frameList, depthmapList = converter.convert_video(args.input, args.output, args.high, args.low,
            args.step, args.fast)

    print(len(frameList))
    print(len(depthmapList))

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, dest='input',
            help="Path to read the input video")
    parser.add_argument("-o", "--output", required=True, dest='output',
            help="Path to save the output video")
    parser.add_argument("--high", required=False, action='store_true', dest='high',
            help="Process high quality frames - may decrease speed")
    parser.add_argument("--low", required=False, action='store_true', dest='low',
            help="Process low quality frames - may increase speed")
    parser.add_argument("-s", "--step", required=False, type=int, default=1, dest='step',
            help="Step of reading frames, e.g. if step==3, every 3d frame will be taken for a depth map")
    parser.add_argument("--fast", required=False, action='store_true', dest='fast',
            help="Use fast version of depth map creator")
    args = parser.parse_args()
    return args


class VideoConverter2(object):
    def __init__(self):
        pass

    def convert_data(self, input_file, high_quality, step, fast):
        """
        Convert input video to a depthmap video.
        Currently only MP4 format is supported.

        input_file: string - name of the video that will be converted to a
            depthmap video
        output_file: string - name of the output depthmap video
        high_quality: boolean - if true, frames dimensions will be doubled
        low_quality: boolean - if true, frames dimensions will halved
        step: int - step of reading frames, e.g. if step==3, every third frame
            will be taken for creating a depth map
        """

        # checking arguments
        if step <= 0:
            raise ValueError("Step should be greater than 0")
        if not os.access(input_file, os.R_OK):
            raise ValueError("Please check that file %s exists." % input_file)
        
        capture = cv2.VideoCapture(input_file)
        if not capture or not capture.isOpened():
            raise ValueError("Failed to read file %s" % input_file)

        width = _DEFAULT_WIDTH #capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = _DEFAULT_HEIGHT #capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if high_quality:
            width *= 2
            height *= 2
        else:
            width /= 2
            height /= 2

        previous_frame = None
        next_frame = None
        # Counts are added for debugging and can be removed if needed
        frame_count = 0
        depthmap_count = 0

        frameList = list()
        depthmapList = list()

        while capture.isOpened():
            # Capture frame-by-frame
            for s in range(step):
                ret, next_frame = capture.read()
                if not ret:
                    #print "No frames to read, exit loop"
                    break
                
                frameList.append(next_frame[...,::-1])

            if next_frame is None:
                break

            frame_count += step
            
            # Resize a frame
            next_frame = cv2.resize(next_frame, (width, height), interpolation=cv2.INTER_LINEAR)

            if previous_frame is not None and next_frame is not None:
                # Trying to figure out which direction camera moves
                # calcOpticalFlowFarneback requires grayscale images
                previous_frame_gr = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
                next_frame_gr = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

                flow = cv2.calcOpticalFlowFarneback(previous_frame_gr, next_frame_gr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                if flow[..., 0].sum() > 0:
                    #print "Camera moves to the left"
                    # swapping left and right images
                    previous_frame, next_frame = next_frame, previous_frame
                #else:
                    #print "Camera moves to the right"

                # Create a depth map
                depth_map = self.create_depth_map(previous_frame, next_frame, fast)
                depthmapList.append(depth_map)
                
                depthmap_count += 1

            previous_frame = next_frame

        capture.release()
        #cv2.destroyAllWindows()

        return frameList, depthmapList

    def create_depth_map(self, img_left, img_right, fast):
        """
        Convert left image and right image into depth map image.
        Need to pick a good set of matcher parameter to create
        good quality depth map image

        Input: left image and right image (either RGB fornmat or gray format)

        Output: depth map image
        """
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

        dmc = None
        if fast:
            # fast depthmap creator
            dmc = DepthMapCreator_2(matcher_parameters)
        else:
            # advance depthmap creator
            dmc = DepthMapCreator(filter_parameters, matcher_parameters)

        depth_image = dmc.get_depth_image(img_left, img_right)

        return depth_image


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


if __name__ == "__main__":
    main()
