import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Video_To_Depthmap/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Direction_detection/')))
from video_converter import VideoConverter
import subprocess
import cv2


def main():

    three_d_video_creator = ThreeDimensionVideo()
    three_d_video_creator.get_depthmap_video("data/test.avi", "data/test_output.avi")
    three_d_video_creator.call_shader_subprocess("./out")


class ThreeDimensionVideo(object):

    def __init__(self):
        self.depthmapConverter = VideoConverter()

    def get_depthmap_video(self, input_video, output_video):
        """
        Convert input video to depthmap video.

        TODO: should use dependency injection for VideoConverter object.
        """   

        self.depthmapConverter.convert_video(input_video, output_video, True, False, 1, True)
    

    def call_shader_subprocess(self, pathToRoutine):
        """
        Function to call C++ subroutine to create shader from depthMap video.
        """
        # path to subprocess executing file
        args = (pathToRoutine)

        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()

    def getDepthImage(self, imageLeft, imageRight, fast = False):
        """
        Function to create depth map image from leftImage and rightImage
        """
        self.depthmapConverter.create_depth_map(imageLeft, imageRight, fast)

if __name__ == "__main__":
    main()
    
