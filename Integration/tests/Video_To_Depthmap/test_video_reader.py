import mock
import cv2
import pytest
import numpy as np
from Integration.tests.helpers.tester import Tester
from Integration.Video_To_Depthmap.video_reader import VideoReader

_MOCK_WIDTH = 100
_MOCK_HEIGHT = 100
_MOCK_FPS = 100

def mock_video_capture(mocked_cv2, total_frames_count):
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
    mocked_capture.get.side_effect = [_MOCK_FPS, _MOCK_WIDTH, _MOCK_HEIGHT]

@mock.patch('Integration.Video_To_Depthmap.video_reader.cv2')
@mock.patch('Integration.Video_To_Depthmap.video_reader.check_file_exists')
def test_constructor(mocked_file_check, mocked_cv2):
    input_file = 'test_file_name'
    step = 10
    low_quality = True

    # mock VideoCapture object
    mock_video_capture(mocked_cv2, 1)
    # mock check_file_exists() to make file 'available'
    mocked_file_check.return_value = True

    with VideoReader(input_file, low_quality, None) as video_reader:
        assert video_reader.input_file == input_file

@mock.patch('Integration.Video_To_Depthmap.video_reader.cv2')
@mock.patch('Integration.Video_To_Depthmap.video_reader.check_file_exists')
def test_low_quality_endabled(mocked_file_check, mocked_cv2):
    input_file = 'test_file_name'
    step = 10
    low_quality = True

    # mock VideoCapture object
    mock_video_capture(mocked_cv2, 1)
    # mock check_file_exists() to make file 'available'
    mocked_file_check.return_value = True

    with VideoReader(input_file, low_quality, None) as video_reader:
        assert video_reader.width == _MOCK_WIDTH / 4
        assert video_reader.height == _MOCK_HEIGHT / 4

@mock.patch('Integration.Video_To_Depthmap.video_reader.cv2')
@mock.patch('Integration.Video_To_Depthmap.video_reader.check_file_exists')
def test_low_quality_disabled(mocked_file_check, mocked_cv2):
    input_file = 'test_file_name'
    step = 10
    low_quality = False

    # mock VideoCapture object
    mock_video_capture(mocked_cv2, 1)
    # mock check_file_exists() to make file 'available'
    mocked_file_check.return_value = True

    with VideoReader(input_file, low_quality, None) as video_reader:
        assert video_reader.width == _MOCK_WIDTH
        assert video_reader.height == _MOCK_HEIGHT
