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
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = capture.get(cv2.CAP_PROP_FPS)
        width = 600
        height = 400
        is_color = 0 # save depth map video in grayscale
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height), is_color)

        previous_frame = None
        next_frame = None
        # Counts are added for debugging and can be removed if needed
        frame_count = 0
        depthmap_count = 0

        while capture.isOpened():
            # Capture frame-by-frame
            ret, next_frame = capture.read()
            if not ret:
                print "No frames to read, exit loop"
                break

            print "Processing frame_%s" % frame_count
            # Resize a frame to 600x400
            next_frame = cv2.resize(next_frame, (width, height), interpolation=cv2.INTER_LINEAR)

            if previous_frame is not None and next_frame is not None:
                # Create a depth map
                depth_map = create_depth_map(previous_frame, next_frame)
                # Write the result to video file
                out.write(depth_map)
                depthmap_count += 1

            previous_frame = next_frame
            frame_count += 1

        print "Finished video processing. Frames: %s, Depth maps: %s" % (frame_count, depthmap_count)

        out.release()
        capture.release()
        cv2.destroyAllWindows()

def create_depth_map(imgL, imgR):
    """
    Temporary function copied from 'Image to depth map'/example2.
    Will be removed after integration with other modules.
    """
    if imgL is None or imgR is None:
        raise ValueError("Please check the parameters")

    # SGBM Parameters -----------------
    window_size = 5 # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely

    left_matcher = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=160, # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=5,
        P1=8 * 3 * window_size ** 2,
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )

    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    # FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    displ = left_matcher.compute(imgL, imgR)  # .astype(np.float32)/16
    dispr = right_matcher.compute(imgR, imgL)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filteredImg = wls_filter.filter(displ, imgL, None, dispr)  # important to put "imgL" here!!!

    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    filteredImg = np.uint8(filteredImg)
    del displ
    del dispr
    del left_matcher
    del right_matcher
    del wls_filter
    return filteredImg

if __name__ == "__main__":
    converter = VideoConverter()
    converter.convert_video("../Video to image/example.mp4", "out.mp4")
