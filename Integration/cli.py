import os
from Integration.helpers.cli_helpers import * # BAD PRACTICE
from Integration.Video_To_Depthmap.video_converter import VideoConverter

def main():
    '''
    TODO
    '''
    # do we need id?
    # prompt_settings = dict(history=FileHistory('.cli_history'), auto_suggest=AutoSuggestFromHistory())
    converter = VideoConverter()

    while True:
        input_video = get_input_video_name()#**prompt_settings)
        print_formatted_text("Video to process: %s" % input_video)

        output_video = get_input_video_name()#**prompt_settings)
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
            converter.convert_video(input_video, output_video, low, step, fast)
        except ValueError as err:
            print "===============> Error: ", err


if __name__ == '__main__':
    main()

