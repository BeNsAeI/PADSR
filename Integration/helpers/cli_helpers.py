from __future__ import unicode_literals

import os
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text

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

def _check_dir_write_access(filename):
    '''
    Check if a directory where a file is located is accessible for writing,

    filename: string - the name of file to check. Can be a relative/absolute path
    return: True if dir is available for writing, False otherwise
    '''
    if not filename:
        return False
    out_dir = os.path.dirname(filename) or '.'
    return os.access(out_dir, os.W_OK)

def _check_file_exists(filename):
    '''
    Check if file is accessible for reading.

    filename: string - the name of file to check. Can be a relative/absolute path
    return: True if file exists and available for reading, False otherwise
    '''
    if not filename:
        return False
    return os.access(filename, os.R_OK)


def get_input_video_name():
    '''
    TODO
    '''
    input_video = None
    while not input_video:
        input_video = _get_user_input("Path to input video: ")
        if not input_video:
            continue
        if not _check_file_exists(input_video):
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
        if not _check_dir_write_access(output_video):
            print_formatted_text("Cannot write to directory. Please try again.")
            output_video = None
            continue

        if _check_file_exists(output_video):
            rewrite = _get_user_confirmation("File %s already exists. Do you want to rewrite it?" % output_video)
            if not rewrite:
                output_video = None
    return output_video

def get_quality_option():
    '''
    TODO
    '''
    high = False
    low = False
    high = _get_user_confirmation("Process high quality frames? (may decrease speed)")
    quality = _get_user_input("Available aspect ratio: ")
    if not high:
        low = _get_user_confirmation("Process low quality frames? (may increase speed)")
    return (high, low)

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
