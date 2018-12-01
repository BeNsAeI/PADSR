from __future__ import unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm
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

def _get_user_input(text, default=None):
    '''
    Show a text and return a response from a user or None
    text: string - text to show
    '''
    if default:
        to_print = text + " [Default is %s] " % default
    else:
        to_print = text

    input_ = prompt(to_print)

    if input_:
        return input_
    elif default:
        return default
    return None

def get_input_video_name():
    '''
    Asks user to provide a filename of input video.
    return: string - filename of input video provided by a user.
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
    Asks user to provide a filename of output video.
    return: string - filename of output video provided by a user.
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
    Asks if user wants to quarter the frames aspect ratio
    return: bool - true if user decides to quarter the frames aspect ratio,
    otherwise false
    '''
    low = _get_user_confirmation("Do you want to quarter the frames aspect ratio? (may increase speed)", default=True)
    return low

def get_step_value():
    '''
    Asks user to specify a frame step
    return: int - frame step specified by a user.
    '''
    step = None
    while not step:
        step = _get_user_input("Step of reading frames (e.g. if step==3, every 3d frame will be taken for a depth map): ",
                default=1)
        try:
            step = int(step)
        except:
            print_formatted_text("Please enter an integer value")
            step = None
            continue
        if step <= 0:
            print_formatted_text("Step should be greater than 0")
            step = None
    return step

def get_fast_depthmap_option():
    '''
    Asks if user wants to generate a depth map using fast method.
    return: bool - true if user decides to use fast depthmap, otherwise false
    '''
    fast = _get_user_confirmation("Use fast version of depth map creator? (may decrease quality)")
    return fast

def get_nn_depthmap_option():
    '''
    Asks if user wants to generate a depth map using neural network.
    return: bool - true if user decides to use neural-net depthmap, otherwise false
    '''
    nn = _get_user_confirmation("Use a neural network to generate depthmap?")
    return nn

def get_command():
    '''
    Asks user to select a command
    return: int - number that represents a command
    '''
    command = None
    while not command:
        command = _get_user_input("Choose command:\n  1) Save depthmap video;\n  2) Open 3d.\n To select command type 1 or 2: ")
        if not command:
            continue
        try:
            command = int(command)
            if command != 1 and command != 2:
                command = None
                continue
        except ValueError:
            print("Please type 1 or 2")
            command = None
    return command

