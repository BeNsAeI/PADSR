import cv2

import numpy as np
import os

class VideoConverter(object):
    def __init__(self):
        pass

    def convert_video(self, input_file, output_file):
        """
        Convert input video to a depthmap video.
        Currently only MP4 format is supported.

        input_file: string - name of the video that will be converted to a
        depthmap video
        output_file: string - name of the output depthmap video
        """

        # Check if file exists
        if not os.path.isfile(input_file):
            raise ValueError("File %s not found" % input_file)

        capture = cv2.VideoCapture(input_file)
        if not capture or not capture.isOpened():
            raise ValueError("Failed to read file %s" % input_file)

        # Set the output video parameters
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        fps = capture.get(cv2.CAP_PROP_FPS)
        width = 600
        height = 400
    #if flag =='h':
        #    width = 1200
        #    height = 800
        #if flag == 'l':
        #    width = 300
        #    height = 200
        is_color = 0 # save depth map video in grayscale
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), is_color)

        previous_frame = None
        next_frame = None
        # Counts are added for debugging and can be removed if needed
        frame_count = 0
        depthmap_count = 0

        while capture.isOpened():
            # Capture frame-by-frame
            capture.read()
            capture.read()
            ret, next_frame = capture.read()
            if not ret:
                print "No frames to read, exit loop"
                break

            print "Processing frame_%s" % frame_count
            # Resize a frame to 600x400
            next_frame = cv2.resize(next_frame, (width, height), interpolation=cv2.INTER_LINEAR)

            if previous_frame is not None and next_frame is not None:
                # Create a depth map
                depth_map = create_depth_map(previous_frame, next_frame, width)
        #depth_map = cv2.resize(depth_map, (width, height), interpolation=cv2.INTER_LINEAR)
                # Write the result to video file
                out.write(depth_map)
                depthmap_count += 1

            previous_frame = next_frame
            frame_count += 3

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
    converter = VideoConverter()
    converter.convert_video("../../Video to image/example.mp4", "out.avi")
