import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Video_To_Depthmap/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Direction_detection/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'OpenGL_python/')))
from video_converter import VideoConverter
from video_converter_2 import VideoConverter2
from Shader import ShaderProcessor


class ThreeDimensionVideo(object):

    def __init__(self):
        self.depthmapConverter = VideoConverter()
        self.depthmapConverter2 = VideoConverter2()
        self.shaderProcessor = ShaderProcessor()

    def get_depthmap_video(self, input_video, output_video):
        """
        Convert input video to depthmap video.

        """   

        self.depthmapConverter.convert_video(input_video, output_video, True, False, 1, True)

    def get_frame_data(self, input_video, high_quality = False, step = 1, fast = True):
        """
        Return the iterator of video frame collection and depthmap image collection.       
        """
        frameList, depthList = self.depthmapConverter2.convert_data(input_video, high_quality, step, fast)
        return iter(frameList), iter(depthList)


    def getNextFrame(self, list_iter):
        """
        Function to get next image on the list via the list_iter
        """
        try:
            return list_iter.next()
        except StopIteration:
            return None
        

    def getVertexShader(self):
        """
        Create vertex shader
        """
        return self.shaderProcessor.createVertexShader()

    
    def getFragmentShader(self):
        """
        Create fragment shader
        """ 
        return self.shaderProcessor.createFragmentShader()


    def getDepthImage(self, imageLeft, imageRight, fast = False):
        """
        Function to create depth map image from leftImage and rightImage
        """
        self.depthmapConverter.create_depth_map(imageLeft, imageRight, fast)

    
