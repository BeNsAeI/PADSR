import argparse
import cv2
import numpy as np
from Integration.helpers.depthmap_helpers import create_depth_map
from Integration.Video_To_Depthmap.video_reader import VideoReader
from Integration.helpers.file_system_helpers import check_file_exists, check_dir_write_access

class VideoConverter(object):
    def __init__(self, input_file, low_quality, step, fast, nn):
        """
        input_file: string - name of the video that will be converted to a depthmap video
        low_quality: bool - if true, frames dimensions will be halved
        step: int - step of reading frames, e.g. if step==3, every third frame
            will be taken for creating a depth map
        fast: bool - if true, fast depthmap function will be used
        nn: bool - if true, neural net depthmap function will be used
        """

        # checking arguments
        if step <= 0:
            raise ValueError("Step should be greater than 0")
        if fast and nn:
            raise ValueError("Please choose either fast or neural net depthmap")
        self.input_file = input_file
        self.low_quality = low_quality
        self.step = step
        self.fast = fast
        self.neural_net = nn
        self.video_reader = None
        self.size = None

        if self.neural_net:
            self.size = (320, 240)

    def _get_frame(self, video_reader):
        previous_frame = None
        next_frame = None
        to_skip = 0
        depth_map = None

        # Counts are added for debugging and can be removed if needed
        for next_frame in video_reader.get_next_frame():

            if previous_frame is not None and next_frame is not None:
                # Trying to figure out which direction camera moves
                # calcOpticalFlowFarneback requires grayscale images
                if to_skip == 0:
                    to_skip = self.step - 1
                    prev_frame_gr = cv2.cvtColor(previous_frame, cv2.COLOR_RGB2GRAY)
                    next_frame_gr = cv2.cvtColor(next_frame, cv2.COLOR_RGB2GRAY)

                    flow = cv2.calcOpticalFlowFarneback(prev_frame_gr, next_frame_gr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                    if flow[..., 0].sum() > 0:
                        print("Camera moves to the left")
                        # swapping left and right images
                        previous_frame, next_frame = next_frame, previous_frame
                    else:
                        print("Camera moves to the right")

                    # Create a depth map
                    # In order to use the CNN replace False by True
                    depth_map = create_depth_map(previous_frame, next_frame, self.fast, self.neural_net)
                    depth_map = cv2.cvtColor(depth_map, cv2.COLOR_GRAY2RGB)

                else:
                    to_skip -= 1

                yield depth_map, next_frame

            previous_frame = next_frame

    def convert_video(self, output_file):
        """
        Convert input video to a depthma p video.
        Currently only MP4 format is supported.
        output_file: string - name of the output depthmap video
        """
        if self.input_file == output_file:
            raise ValueError("Input and output file cannot have the same names")
        if not check_dir_write_access(output_file):
            raise ValueError("Cannot write to directory to save %s file. Check permissions or choose another path",
                    output_file)

        with VideoReader(self.input_file, self.low_quality, self.size) as video_reader:
            width = video_reader.width
            height = video_reader.height

            # Set the output video parameters
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')

            is_color = 1 # save depth map video in grayscale
            out = cv2.VideoWriter(output_file, fourcc, video_reader.fps, (width, height), is_color)

            for depth_map, _ in self._get_frame(video_reader):
                # Write the result to video file
                out.write(depth_map)

            out.release()

    def get_frame_and_depth_map(self):
        with VideoReader(self.input_file, self.low_quality, self.size) as video_reader:
            for depth_map, next_frame in self._get_frame(video_reader):
                yield depth_map, next_frame

            cv2.destroyAllWindows()
