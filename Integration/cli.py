from __future__ import unicode_literals

import os
from Video_To_Depthmap.video_converter import VideoConverter
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text

def main():
    '''
    TODO
    '''
    prompt_settings = dict(history=FileHistory('.cli_history'), auto_suggest=AutoSuggestFromHistory())
    converter = VideoConverter()

    while True:
        input_video = get_input_video_name(**prompt_settings)
        print_formatted_text("Video to process: %s" % input_video)

        output_video = get_input_video_name(**prompt_settings)
        print_formatted_text("Output will be saved: %s" % output_video)

        high, low = get_quality_option()
        if high:
            print_formatted_text("High quality enabled")
        if low:
            print_formatted_text("Low quality enabled")

        step = get_step_value()
        print_formatted_text("Step is: %s" % step)

        fast = get_fast_depthmap_option()
        if fast:
            print_formatted_text("Fast depth map enabled")

        try:
            converter.convert_video(input_video, output_video, high, low, step, fast)
        except ValueError as err:
            print "===============> Error: ", err

def get_input_video_name(**prompt_settings):
    '''
    TODO
    '''
    input_video = None
    while not input_video:
        input_video = prompt("Path to input video: ", **prompt_settings)
        if not os.access(input_video, os.R_OK):
            print_formatted_text("File %s doesn't exist or not available for reading. Please try again." % input_video)
            input_video = None
    # TODO check file is a video
    return input_video

def get_output_video_name(**prompt_settings):
    '''
    TODO
    '''
    output_video = None
    while not output_video:
        output_video = prompt("Path to save the output_video video: ", **prompt_settings)
        out_dir = os.path.dirname(output_video)
        if out_dir and not os.access(out_dir, os.W_OK):
            print_formatted_text("Cannot write to directory %s. Please try again." % out_dir)

        if os.access(output_video, os.R_OK):
            rewrite = confirm("File %s already exists. Do you want to rewrite it?" % output_video, "[y/N]") or False
            if not rewrite:
                output_video = None
    return output_video

def get_quality_option():
    '''
    TODO
    '''
    high = False
    low = False
    high = confirm("Process high quality frames? (may decrease speed)", "[y/N]") or False
    if not high:
        low = confirm("Process low quality frames? (may increase speed)", "[y/N]") or False
    return (high, low)

def get_step_value(**prompt_settings):
    '''
    TODO
    '''
    step = None
    while not step:
        step = prompt("Step of reading frames (e.g. if step==3, every 3d frame will be taken for a depth map): ", **prompt_settings)
    return step

def get_fast_depthmap_option():
    '''
    TODO
    '''
    fast = confirm("Use fast version of depth map creator? (may decrease quality)", "[y/N]") or False
    return fast

if __name__ == '__main__':
    main()

