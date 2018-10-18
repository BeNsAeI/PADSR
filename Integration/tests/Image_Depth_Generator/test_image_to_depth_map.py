import mock
import pytest
import numpy as np
from tests.helpers.tester import Tester
from image_depth_generator.CreateDepthMap import CreateDepthMap

def test_image_path_not_given():
    '''
    Verify that function raises error if input does not exist
    '''
    print "__________"
    print('testing if raises error when img_src is not provided')
    test_converter = CreateDepthMap()
    with pytest.raises(ValueError):
        test_converter.get_depth_image('', '')

    with pytest.raises(ValueError):
        test_converter.get_depth_image('../Image to depth map/Opencv example/ambush_5_left.jpg', '')
    print "__________"
    
def test_performance():
    tester = Tester()
    test_converter = CreateDepthMap()
    print "Creating an instance..."
    print "setting up class tracking..."
    tester.init_class_tracker(CreateDepthMap)
    tester.init_output_file_check()
    print "creating a an instance of test class"
    print "__________"
    print "Timing test:"
    tester.startTimer()
    test_converter.get_depth_image("../Image to depth map/Opencv example/ambush_5_left.jpg", "../Image to depth map/Opencv example/ambush_5_right.jpg")
    tester.stopTimer()
    print "checking object size, memory and profile:"
    tester.check_object_size(test_converter)
    tester.print_object_profile(test_converter)
    tester.track_object()
    print "__________"
    print "checking Class size, memory and profile:"
    tester.snapshot_class()
    tester.get_class_summary()
    print "__________"
    print "checking for output files added:"
    print "so far there have been "+str(tester.output_file_count())+" files added."
