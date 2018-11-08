#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Integration.helpers.cli_helpers import * # BAD PRACTICE
from Integration.Video_To_Depthmap.video_converter import VideoConverter
from Integration.opengl.OpenGL_Base_Shader import run_opengl

def main():
    '''
    TODO
    '''
    # do we need id?
    # prompt_settings = dict(history=FileHistory('.cli_history'), auto_suggest=AutoSuggestFromHistory())

    try:
        while True:
            cmd = get_command()
            if cmd == 1:
                save_depthmap_video()
            if cmd == 2:
                show_executable()
    except KeyboardInterrupt:
        sys.exit(0)

def save_depthmap_video():
    input_video = get_input_video_name()#**prompt_settings)
    print_formatted_text("Video to process: %s" % input_video)

    output_video = get_output_video_name()#**prompt_settings)
    print_formatted_text("Output will be saved: %s" % output_video)

    low = get_low_quality_option()
    if low:
        print_formatted_text("Low quality enabled")

    step = get_step_value()
    print_formatted_text("Step is: %s" % step)

    fast = get_fast_depthmap_option()
    if fast:
        print_formatted_text("Fast depth map enabled")

    try:
        converter = VideoConverter(input_video, low, step, fast)
        converter.convert_video(output_video)
    except ValueError as err:
        print "===============> Error: ", err

def show_executable():
    input_video = get_input_video_name()#**prompt_settings)
    print_formatted_text("Video to process: %s" % input_video)

    low = get_low_quality_option()
    if low:
        print_formatted_text("Low quality enabled")

    step = get_step_value()
    print_formatted_text("Step is: %s" % step)

    fast = get_fast_depthmap_option()
    if fast:
        print_formatted_text("Fast depth map enabled")

    try:
        run_opengl(input_video, low, step, fast)
    except ValueError as err:
        print "===============> Error: ", err

if __name__ == '__main__':
    main()

