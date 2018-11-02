from __future__ import unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text
from Integration.helpers.file_system_helpers import check_file_exists, check_dir_write_access

def _get_user_confirmation(question, default=False):
    '''
    Ask a question and return True if user agrees or False if a user disagrees
    question: string - question that will be shown to a user
    default: bool - consider this value as a default if user does not provide an answer
    '''
    suffix = "[Y/n]" if default is True else "[y/N]"
    answer = confirm(question, suffix) or default
    return answer

def _get_user_input(text):
    '''
    Show a text and return a response from a user or None
    text: string - text to show
    '''
    input_ = prompt(text)
    if input_:
        return input_
    return None

def get_input_video_name():
    '''
    TODO
    '''
    input_video = None
    while not input_video:
        input_video = _get_user_input("Path to input video: ")
        if not input_video:
            continue
        if not check_file_exists(input_video):
            print_formatted_text("File %s doesn't exist or not available for reading. Please try again." % input_video)
            input_video = None
    # TODO check file is a video
    return input_video

def get_output_video_name():
    '''
    TODO
    '''
    output_video = None
    while not output_video:
        output_video = _get_user_input("Path to save the output_video video: ")
        if not output_video:
            continue
        if not check_dir_write_access(output_video):
            print_formatted_text("Cannot write to directory. Please try again.")
            output_video = None
            continue

        if check_file_exists(output_video):
            rewrite = _get_user_confirmation("File %s already exists. Do you want to rewrite it?" % output_video)
            if not rewrite:
                output_video = None
    return output_video

def get_low_quality_option():
    '''
    TODO
    '''
    low = _get_user_confirmation("Do you want to halve the frames aspect ratio? (may increase speed)")
    return low

def get_step_value():
    '''
    TODO
    '''
    step = None
    while not step:
        step = _get_user_input("Step of reading frames (e.g. if step==3, every 3d frame will be taken for a depth map): ")
    return step

def get_fast_depthmap_option():
    '''
    TODO
    '''
    fast = _get_user_confirmation("Use fast version of depth map creator? (may decrease quality)")
    return fast
