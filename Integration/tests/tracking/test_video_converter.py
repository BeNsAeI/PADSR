import mock
import pytest
import numpy as np
from tests.helpers.tester import Tester
from tracking.video_converter import VideoConverter

@mock.patch('tracking.video_converter.create_depth_map')
@mock.patch('tracking.video_converter.cv2')
@mock.patch('tracking.video_converter.os')
def test_depthmaps_count(mocked_os, mocked_cv2, mocked_depth_map_func):
    # set required mocks
    mocked_depth_map_func.return_value = np.array([[3], [4]])
    mocked_cv2.resize.side_effect = [np.array([1]), np.array([2]), np.array([3])]
    mocked_capture = mocked_cv2.VideoCapture.return_value
    mocked_capture.isOpened.return_value = True
    mocked_capture.read.side_effect = [(True, np.array([1])), (True, np.array([2])),
            (True, np.array([3])), (False, None)]
    mocked_writer = mocked_cv2.VideoWriter.return_value

    # call tested method
    test_converter = VideoConverter()
    test_converter.convert_video("any_input", "any_output")

    assert mocked_writer.write.call_count == 2

@mock.patch('tracking.video_converter.create_depth_map')
@mock.patch('tracking.video_converter.cv2')
@mock.patch('tracking.video_converter.os')
def test_one_frame(mocked_os, mocked_cv2, mocked_depth_map_func):
    # set required mocks
    mocked_cv2.resize.side_effect = [np.array([1])]
    mocked_capture = mocked_cv2.VideoCapture.return_value
    mocked_capture.isOpened.return_value = True
    mocked_capture.read.side_effect = [(True, np.array([1])), (False, None)]
    mocked_writer = mocked_cv2.VideoWriter.return_value

    # call tested method
    test_converter = VideoConverter()
    test_converter.convert_video("any_input", "any_output")

    assert mocked_cv2.resize.call_count == 1
    assert mocked_depth_map_func.called == False
    assert mocked_writer.write.called == False

@mock.patch('tracking.video_converter.cv2')
@mock.patch('tracking.video_converter.create_depth_map')
def test_file_not_found(mocked_cv2, mocked_depth_map_func):
    test_converter = VideoConverter()
    with pytest.raises(ValueError):
        test_converter.convert_video("any_input", "any_output")

@pytest.mark.skip(reason="input video should be added")
def test_performance():
    tester = Tester()
    test_converter = VideoConverter()
    print "Creating an instance..."
    print "setting up class tracking..."
    tester.init_class_tracker(VideoConverter)
    tester.init_output_file_check()
    print "creating a an instance of test class"
    print "__________"
    print "Timing test:"
    tester.startTimer()
    test_converter.convert_video("../Video to image/example2.mp4", "out.mp4")
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
