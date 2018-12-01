import mock
import pytest
import numpy as np
from Integration.tests.helpers.tester import Tester
from Integration.Video_To_Depthmap.video_converter import VideoConverter

def set_video_reader_side_effect(set_video_reader_side_effect, frames_count):
    side_effect = [np.array([i]) for i in range(frames_count)]
    magic_mock = mock.MagicMock()
    magic_mock.return_value = iter(side_effect)
    set_video_reader_side_effect.get_next_frame.return_value = magic_mock

@mock.patch('Integration.Video_To_Depthmap.video_converter.check_file_exists')
@mock.patch('Integration.Video_To_Depthmap.video_converter.VideoReader')
def test_constructor(mocked_video_reader, mocked_file_check):
    '''
    Verify that VideoConverter object is properly constructed
    '''
    mocked_file_check.return_value = True
    set_video_reader_side_effect(mocked_video_reader, 1)

    input_file = "any_input"
    output_file = "any_output"
    step = 10
    low_quality = False
    fast = True
    test_converter = VideoConverter(input_file, low_quality, step, fast, False)
    assert test_converter.input_file == input_file
    assert test_converter.low_quality == low_quality
    assert test_converter.step == step
    assert test_converter.fast == fast

@mock.patch('Integration.Video_To_Depthmap.video_converter.create_depth_map')
@mock.patch('Integration.Video_To_Depthmap.video_converter.cv2')
@mock.patch('Integration.Video_To_Depthmap.video_converter.check_file_exists')
@mock.patch('Integration.Video_To_Depthmap.video_converter.VideoReader')
def test_one_frame(mocked_video_reader, mocked_file_check, mocked_cv2, mocked_depth_map_func):
    # set required mocks
    set_video_reader_side_effect(mocked_video_reader, 1)
    # mock of VideoWriter object
    mocked_writer = mocked_cv2.VideoWriter.return_value
    # mock check_file_exists to make input file 'available'
    mocked_file_check.return_value = True

    # call tested method
    test_converter = VideoConverter("any_input", False, 1, True, False)
    test_converter.convert_video("any_output")

    assert mocked_depth_map_func.called == False
    assert mocked_writer.write.called == False

@mock.patch('Integration.Video_To_Depthmap.video_converter.create_depth_map')
def test_file_not_found(mocked_depth_map_func):
    '''
    Verify that function raises error if input does not exist
    '''
    with pytest.raises(ValueError):
        test_converter = VideoConverter("any_input", False, 1, True, False)
        test_converter.convert_video("any_output")

@mock.patch('Integration.Video_To_Depthmap.video_converter.check_file_exists') # mock os to skip checking if files exist
def test_depthmaps_step_0(mocked_file_check):
    '''
    Verify that VideoConverter raises error when step<=0
    '''
    # mock check_file_exists to make input file 'available'
    mocked_file_check.return_value = True
    # call convert_video with step 0 and check that it returns ValueError
    with pytest.raises(ValueError):
        VideoConverter("any_input", False, 0, True, False)

    # call convert_video with step -1 and check that it returns ValueError
    with pytest.raises(ValueError):
        VideoConverter("any_input", False, -1, True, False)

@mock.patch('Integration.Video_To_Depthmap.video_converter.create_depth_map')
@mock.patch('Integration.Video_To_Depthmap.video_converter.cv2')
@mock.patch('Integration.Video_To_Depthmap.video_converter.check_file_exists') # mock os to skip checking if files exist
@mock.patch('Integration.Video_To_Depthmap.video_converter.VideoReader')
def test_depthmaps_large_step(mocked_video_reader, mocked_file_check, mocked_cv2, mocked_depth_map_func):
    '''
    Verify that VideoConverter doesn't process any frames when step > number of frames
    '''
    total_frames_count = 15
    # set required mocks

    set_video_reader_side_effect(mocked_video_reader, total_frames_count)
    # mock check_file_exists to make input file 'available'
    mocked_file_check.return_value = True

    # setting create_depth_map function to return a numpy array
    mocked_depth_map_func.return_value = np.array([[0], [1]])

    # mock of VideoWriter object
    mocked_writer = mocked_cv2.VideoWriter.return_value

    test_converter = VideoConverter("any_input", False, total_frames_count+1, True, False)

    # call convert_video with step > total_frames_count and check that it doesn't save anything
    test_converter.convert_video("any_output")
    assert mocked_writer.write.call_count == 0

@pytest.mark.skip(reason="input video should be added to run this test")
def test_performance():
    tester = Tester()
    test_converter = VideoConverter("../Video to image/test.mp4", True, 1, False, False)
    print("Creating an instance...")
    print("setting up class Video_To_Depthmap...")
    tester.init_class_tracker(VideoConverter)
    tester.init_output_file_check()
    print("creating a an instance of test class")
    print("__________")
    print("Timing test:")
    tester.startTimer()
    test_converter.convert_video("out.mp4")
    tester.stopTimer()
    print("checking object size, memory and profile:")
    tester.check_object_size(test_converter)
    tester.print_object_profile(test_converter)
    tester.track_object()
    print("__________")
    print("checking Class size, memory and profile:")
    tester.snapshot_class()
    tester.get_class_summary()
    print("__________")
    print("checking for output files added:")
    print("so far there have been "+str(tester.output_file_count())+" files added.")
