import mock
import pytest
import numpy as np
from tests.helpers.tester import Tester
from Image_Depth_Generator.CreateDepthMap import CreateDepthMap
from Image_Depth_Generator.Advanced import DepthMapCreator
from Image_Depth_Generator.Fast import DepthMapCreator_2

@mock.patch('Image_Depth_Generator.CreateDepthMap.os') # mock os to skip checking if files exist
def test_file_not_found(mocked_os):
    '''
    Verify that function raises error if input does not exist
    '''
    left_file = 'test_left_file'
    right_file = 'test_right_file'
    depth_map_creator = CreateDepthMap()
    # mock os.access so that it cannot read both files
    mocked_os.access.side_effect = [False, False]
    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image(left_file, right_file)

    # mock os.access so that it can read only first file
    mocked_os.access.side_effect = [True, False]
    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image(left_file, right_file)

    # mock os.access so that it can read only second file
    mocked_os.access.side_effect = [False, True]
    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image(left_file, right_file)

@mock.patch('Image_Depth_Generator.CreateDepthMap.cv2.imread')
@mock.patch('Image_Depth_Generator.CreateDepthMap.os') # mock os to skip checking if files exist
def test_depth_map_format(mocked_os, mocked_imread):
    '''
    Verify that function returns non-empty numpy.uint8 object
    '''
    left_file = 'test_left_file'
    right_file = 'test_right_file'

    # mock cv2.imread to return two numpy arrays of images
    mocked_imread.side_effect = [np.ones((270, 480, 3), dtype=np.uint8), np.ones((270, 480, 3), dtype=np.uint8)*2]
    depth_map_creator = CreateDepthMap()
    depth_map = depth_map_creator.get_depth_image(left_file, right_file)
    assert depth_map is not None
    assert depth_map.shape == (480, 858) # hardcoded values in the tested class

def test_image_path_not_given():
    '''
    Verify that function raises error if input does not exist
    '''
    print('testing if raises error when img_src is not provided')
    depth_map_creator = CreateDepthMap()
    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image('', '')

    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image('../Image to depth map/Opencv example/ambush_5_left.jpg', '')

    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image('', '../Image to depth map/Opencv example/ambush_5_left.jpg')


def test_performance():
    tester = Tester()
    depth_map_creator = CreateDepthMap()
    print("Creating an instance...")
    print("setting up class tracking...")
    tester.init_class_tracker(CreateDepthMap)
    tester.init_output_file_check()
    print("creating a an instance of test class")
    print("__________")
    print("Timing test:")
    tester.startTimer()
    depth_map_creator.get_depth_image("../Image to depth map/Opencv example/ambush_5_left.jpg", "../Image to depth map/Opencv example/ambush_5_right.jpg")
    tester.stopTimer()
    print("checking object size, memory and profile:")
    tester.check_object_size(depth_map_creator)
    tester.print_object_profile(depth_map_creator)
    tester.track_object()
    print("__________")
    print("checking Class size, memory and profile:")
    tester.snapshot_class()
    tester.get_class_summary()
    print("__________")
    print("checking for output files added:")
    print("so far there have been "+str(tester.output_file_count())+" files added.")
