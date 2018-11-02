import mock
import pytest
from Integration.helpers import cli_helpers

_EXPECTED_VIDEO_NAME = "video.mp4"

@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
def test_input_happy_path(mocked_file_check, mocked_user_input):
    '''
    Test get_input_video_name happy path
    '''
    mocked_user_input.return_value = _EXPECTED_VIDEO_NAME
    mocked_file_check.return_value = True

    user_input = cli_helpers.get_input_video_name()

    assert user_input == _EXPECTED_VIDEO_NAME

@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
def test_input_empty(mocked_file_check, mocked_user_input):
    '''
    Verify that get_input_video_name does not fail if empty answer is passed
    '''
    mocked_user_input.side_effect = [None, _EXPECTED_VIDEO_NAME]
    mocked_file_check.return_value = True

    user_input = cli_helpers.get_input_video_name()

    assert user_input == _EXPECTED_VIDEO_NAME
    assert mocked_user_input.call_count == 2

@mock.patch('Integration.helpers.cli_helpers.print_formatted_text')
@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
def test_input_not_exist(mocked_file_check, mocked_user_input, mocked_warning):
    '''
    Verify that get_input_video_name does not fail if a video does not exist
    '''
    mocked_user_input.side_effect = ['nonexistent_video.mp4', _EXPECTED_VIDEO_NAME]
    mocked_file_check.side_effect = [False, True]

    user_input = cli_helpers.get_input_video_name()

    assert user_input == _EXPECTED_VIDEO_NAME
    assert mocked_user_input.call_count == 2
    assert mocked_warning.call_count == 1

@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
@mock.patch('Integration.helpers.cli_helpers._check_dir_write_access')
def test_output_happy_path(mocked_dir_check, mocked_file_check, mocked_user_input):
    '''
    Test get_output_video_name happy path
    '''
    mocked_user_input.return_value = _EXPECTED_VIDEO_NAME
    mocked_file_check.return_value = False
    mocked_dir_check.return_value = True

    output_video_name = cli_helpers.get_output_video_name()

    assert output_video_name == _EXPECTED_VIDEO_NAME

@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
@mock.patch('Integration.helpers.cli_helpers._check_dir_write_access')
def test_output_empty(mocked_dir_check, mocked_file_check, mocked_user_input):
    '''
    Verify that get_output_video_name does not fail if empty answer is passed
    '''
    mocked_user_input.side_effect = [None, _EXPECTED_VIDEO_NAME]
    mocked_dir_check.return_value = True
    mocked_file_check.return_value = False

    user_input = cli_helpers.get_output_video_name()

    assert user_input == _EXPECTED_VIDEO_NAME
    assert mocked_user_input.call_count == 2

@mock.patch('Integration.helpers.cli_helpers.print_formatted_text')
@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
@mock.patch('Integration.helpers.cli_helpers._check_dir_write_access')
def test_output_directory_not_exist(mocked_dir_check, mocked_file_check, mocked_user_input, mocked_warning):
    '''
    Verify that get_output_video_name does not fail if a name of output video
    containe a non-existent directory
    '''
    output_path = 'somepath/' + _EXPECTED_VIDEO_NAME
    mocked_user_input.side_effect = ['nonexistent_dir/video.mp4', output_path]
    mocked_dir_check.side_effect = [False, True]
    mocked_file_check.side_effect = [False, False]

    user_input = cli_helpers.get_output_video_name()

    assert user_input == output_path
    assert mocked_user_input.call_count == 2
    assert mocked_warning.call_count == 1

@mock.patch('Integration.helpers.cli_helpers._get_user_confirmation')
@mock.patch('Integration.helpers.cli_helpers._get_user_input')
@mock.patch('Integration.helpers.cli_helpers._check_file_exists')
def test_output_already_exists(mocked_file_check, mocked_user_input, mocked_confirm):
    '''
    Verify that get_output_video_name does not fail if an output video already exists
    '''
    mocked_user_input.side_effect = [_EXPECTED_VIDEO_NAME, _EXPECTED_VIDEO_NAME]
    mocked_file_check.path.dirname.side_effct = [None, None]
    mocked_file_check.side_effect = [True, True]
    mocked_confirm.side_effect = [False, True]

    user_input = cli_helpers.get_output_video_name()

    assert user_input == _EXPECTED_VIDEO_NAME
    assert mocked_user_input.call_count == 2
    assert mocked_confirm.call_count == 2

@mock.patch('Integration.helpers.cli_helpers._get_user_confirmation')
def test_high_quality_empty(mocked_confirm):
    '''
    Verify that get_quality_option does not fail if no answer is provided to
    the high quality confirmation question and asks 
    '''
    pass
def test_high_quality_wrong_answer():
    '''
    Verify that get_quality_option does not fail if a user's answer on
    the high quality confirmation question was neither 'y' nor 'n'
    '''
    pass
def test_low_quality_empty():
    '''
    Verify that get_quality_option does not fail if no answer is provided to
    the low quality confirmation question
    '''
    pass
def test_low_quality_wrong_answer():
    '''
    Verify that get_quality_option does not fail if a user's answer on
    the low quality confirmation question was neither 'y' nor 'n'
    '''
    pass
def test_fast_depthmap_empty():
    '''
    Verify that get_fast_depthmap_option does not fail if no answer is provided to
    the fast depthmap confirmation question
    '''
    pass
def test_fast_depthmap_wrong_answer():
    '''
    Verify that get_fast_depthmap_option does not fail if a user's answer on
    the fast depthmap confirmation question was neither 'y' nor 'n'
    '''
    pass
def test_step_empty():
    '''
    Verify that get_step_value does not fail if empty answer is passed
    '''
    pass
def test_not_integer():
    '''
    Verify that get_step_value does not fail if answer is not integer
    '''
    pass
def test_step_negative():
    '''
    Verify that get_step_value does not fail if answer is a negative value
    '''
    pass


'==========================================='



def test_video_converter_failed():
    pass
