import cv2
import argparse
import numpy as np
import os

_DEFAULT_WIDTH = 600
_DEFAULT_HEIGHT = 400

def main():
    args = get_arguments()
    converter = VideoConverter()
    converter.convert_video(args.input, args.output, args.high, args.low,
            args.step)

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
    args = parser.parse_args()
    return args


class VideoConverter(object):
    def __init__(self):
        pass

    def convert_video(self, input_file, output_file, high_quality,
            low_quality, step):
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
        if high_quality and low_quality:
            raise ValueError("Please choose either high or low quality, but not both")
        if not os.access(input_file, os.R_OK):
            raise ValueError("Please check that file %s exists." % input_file)
        out_dir = os.path.dirname(output_file)
        if out_dir and not os.access(out_dir, os.W_OK):
            raise ValueError("Cannot write to directory %s. Check the permissions or choose another directory" % out_dir)

        capture = cv2.VideoCapture(input_file)
        if not capture or not capture.isOpened():
            raise ValueError("Failed to read file %s" % input_file)

        width = _DEFAULT_WIDTH #capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = _DEFAULT_HEIGHT #capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if high_quality:
            width *= 2
            height *= 2
        elif low_quality:
            width /= 2
            height /= 2

        # Set the output video parameters
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fps = capture.get(cv2.CAP_PROP_FPS)

        is_color = 0 # save depth map video in grayscale
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), is_color)

        previous_frame = None
        next_frame = None
        # Counts are added for debugging and can be removed if needed
        frame_count = 0
        depthmap_count = 0

        while capture.isOpened():
            # Capture frame-by-frame
            for s in range(step):
                ret, next_frame = capture.read()
                if not ret:
                    print "No frames to read, exit loop"
                    break
            if next_frame is None:
                break

            frame_count += step
            print "Processing frame_%s" % frame_count
            # Resize a frame
            next_frame = cv2.resize(next_frame, (width, height), interpolation=cv2.INTER_LINEAR)

            if previous_frame is not None and next_frame is not None:
                # Trying to figure out which direction camera moves
                # calcOpticalFlowFarneback requires grayscale images
                previous_frame_gr = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
                next_frame_gr = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)

                flow = cv2.calcOpticalFlowFarneback(previous_frame_gr, next_frame_gr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                if flow[..., 0].sum() > 0:
                    print "Camera moves to the right"
                else:
                    print "Camera moves to the left"

                # Create a depth map
                depth_map = create_depth_map(previous_frame, next_frame, width)
                #depth_map = cv2.resize(depth_map, (width, height), interpolation=cv2.INTER_LINEAR)
                # Write the result to video file
                out.write(depth_map)
                depthmap_count += 1

            previous_frame = next_frame

        print "Finished video processing. Frames: %s, Depth maps: %s" % (frame_count, depthmap_count)

        out.release()
        capture.release()
        cv2.destroyAllWindows()

def create_depth_map(imgL, imgR, width):
    margin = width/2
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
    #cv2.imshow('disparity', (disp-min_disp)/num_disp)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    #exit()
    #print(disp.shape)
    return disp

if __name__ == "__main__":
    main()
