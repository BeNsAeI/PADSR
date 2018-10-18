import mock
import pytest
import numpy as np
from tests.helpers.tester import Tester
from Video_To_Depthmap.video_converter import VideoConverter

def mock_video_capture(mocked_cv2,total_frames_count):
    '''
    Helper method that mocks VideoCapture to return total_frames_count
    number to frames
    mocked_cv2: mocked cv2 module
    total_frames_count: int - number of frames to return
    '''
    mocked_capture = mocked_cv2.VideoCapture.return_value
    mocked_capture.isOpened.return_value = True
    # setting VideoCapture.read() function to return total_frames_count frames and then return None
    mocked_capture.read.side_effect = [(True, np.array([i])) for i in range(total_frames_count)] + [(False, None)]


@mock.patch('Video_To_Depthmap.video_converter.create_depth_map')
@mock.patch('Video_To_Depthmap.video_converter.cv2')
@mock.patch('Video_To_Depthmap.video_converter.os') # mock os to skip checking if files exist
def test_depthmaps_step_1(mocked_os, mocked_cv2, mocked_depth_map_func):
    '''
    Verify that VideoConverter doesn't skip any frames when step=1
    '''
    total_frames_count = 15
    # set required mocks

    # mock VideoCapture object
    mock_video_capture(mocked_cv2, total_frames_count)

    # setting create_depth_map function to return a numpy array
    mocked_depth_map_func.return_value = np.array([[0], [1]])

    # setting cv2.resize() function to return a numpy array
    mocked_cv2.resize.return_value = [np.array(0)]

    # mock of VideoWriter object
    mocked_writer = mocked_cv2.VideoWriter.return_value

    test_converter = VideoConverter()
    # call convert_video with step 1 and check that it saved total_frames_count-1 depth maps
    test_converter.convert_video("any_input", "any_output", False, False, 1, True)
    assert mocked_writer.write.call_count == total_frames_count-1

@mock.patch('Video_To_Depthmap.video_converter.create_depth_map')
@mock.patch('Video_To_Depthmap.video_converter.cv2')
@mock.patch('Video_To_Depthmap.video_converter.os') # mock os to skip checking if files exist
def test_depthmaps_step_3(mocked_os, mocked_cv2, mocked_depth_map_func):
    '''
    Verify that VideoConverter processes every 3d frame when step=3
    '''
    total_frames_count = 15
    # set required mocks

    # mock VideoCapture object
    mock_video_capture(mocked_cv2, total_frames_count)

    # setting create_depth_map function to return a numpy array
    mocked_depth_map_func.return_value = np.array([[0], [1]])

    # setting cv2.resize() function to return a numpy array
    mocked_cv2.resize.return_value = [np.array(0)]

    # mock of VideoWriter object
    mocked_writer = mocked_cv2.VideoWriter.return_value

    test_converter = VideoConverter()
    # call convert_video with step 3 and check that it saved (total_frames_count/3)-1 depth maps
    test_converter.convert_video("any_input", "any_output", False, False, 3, True)
    assert mocked_writer.write.call_count == (total_frames_count/3)-1

@mock.patch('Video_To_Depthmap.video_converter.os') # mock os to skip checking if files exist
def test_depthmaps_step_0(mocked_os):
    '''
    Verify that VideoConverter raises error when step<=0
    '''
    test_converter = VideoConverter()
    # call convert_video with step 0 and check that it returns ValueError
    with pytest.raises(ValueError):
        test_converter.convert_video("any_input", "any_output", False, False, 0, True)

    # call convert_video with step -1 and check that it returns ValueError
    with pytest.raises(ValueError):
        test_converter.convert_video("any_input", "any_output", False, False, -1, True)

@mock.patch('Video_To_Depthmap.video_converter.create_depth_map')
@mock.patch('Video_To_Depthmap.video_converter.cv2')
@mock.patch('Video_To_Depthmap.video_converter.os') # mock os to skip checking if files exist
def test_depthmaps_large_step(mocked_os, mocked_cv2, mocked_depth_map_func):
    '''
    Verify that VideoConverter doesn't process any frames when step > number of frames
    '''
    total_frames_count = 15
    # set required mocks

    # mock VideoCapture object
    mock_video_capture(mocked_cv2, total_frames_count)

    # setting create_depth_map function to return a numpy array
    mocked_depth_map_func.return_value = np.array([[0], [1]])

    # setting cv2.resize() function to return a numpy array
    mocked_cv2.resize.return_value = [np.array(0)]

    # mock of VideoWriter object
    mocked_writer = mocked_cv2.VideoWriter.return_value

    test_converter = VideoConverter()

    # call convert_video with step > total_frames_count and check that it doesn't save anything
    test_converter.convert_video("any_input", "any_output", False, False, total_frames_count+1, True)
    assert mocked_writer.write.call_count == 0

@mock.patch('Video_To_Depthmap.video_converter.create_depth_map')
@mock.patch('Video_To_Depthmap.video_converter.cv2')
@mock.patch('Video_To_Depthmap.video_converter.os') # mock os to skip checking if files exist
def test_one_frame(mocked_os, mocked_cv2, mocked_depth_map_func):
    # set required mocks
    mocked_cv2.resize.side_effect = [np.array([1])]
    # set mocked VideoCapture to return 1 frame
    mock_video_capture(mocked_cv2, 1)
    # mock of VideoWriter object
    mocked_writer = mocked_cv2.VideoWriter.return_value

    # call tested method
    test_converter = VideoConverter()
    test_converter.convert_video("any_input", "any_output", False, False, 1, True)

    assert mocked_cv2.resize.call_count == 1
    assert mocked_depth_map_func.called == False
    assert mocked_writer.write.called == False

@mock.patch('Video_To_Depthmap.video_converter.create_depth_map')
def test_file_not_found(mocked_depth_map_func):
    '''
    Verify that function raises error if input does not exist
    '''
    test_converter = VideoConverter()
    with pytest.raises(ValueError):
        test_converter.convert_video("any_input", "any_output", False, False, 1, True)

@pytest.mark.skip(reason="input video should be added to run this test")
def test_performance():
    tester = Tester()
    test_converter = VideoConverter()
    print "Creating an instance..."
    print "setting up class Video_To_Depthmap..."
    tester.init_class_tracker(VideoConverter)
    tester.init_output_file_check()
    print "creating a an instance of test class"
    print "__________"
    print "Timing test:"
    tester.startTimer()
    test_converter.convert_video("../Video to image/test.mp4", "out.mp4", False, True, 1, False)
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
