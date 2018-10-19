import mock
import pytest
import numpy as np
from Image_Depth_Generator.Fast import DepthMapCreator_2

_matcher_parameters = {'minDisparity': 0,
    'numDisparities': 16*3,
    'blockSize': 5,
    'P1': 8*3*5**2,
    'P2': 32*3*5**2,
    'disp12MaxDiff': 1,
    'uniquenessRatio': 5,
    'speckleWindowSize': 0,
    'speckleRange': 2,
    'preFilterCap': 63,
    'mode': 0}

def test_empty_arguments():
    '''
    Verify that function raises error if input does not exist
    '''
    left_file = np.ones((270, 480, 3), dtype=np.uint8)
    right_file = np.ones((270, 480, 3), dtype=np.uint8)*2

    depth_map_creator = DepthMapCreator_2()

    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image(None, right_file)

    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image(left_file, None)

    with pytest.raises(ValueError):
        depth_map_creator.get_depth_image(None, None)

def test_depth_map_format():
    '''
    Verify that function returns non-empty numpy.uint8 object
    '''

    left_file = np.ones((270, 480, 3), dtype=np.uint8)
    right_file = np.ones((270, 480, 3), dtype=np.uint8)*2
    depth_map_creator = DepthMapCreator_2()
    depth_map = depth_map_creator.get_depth_image(left_file, right_file)
    assert depth_map is not None
    assert depth_map.shape == (270, 480)
