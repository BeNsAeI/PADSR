import argparse
# ugly temporary solution to make this file executable (for manual testing)
if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from Integration.Video_To_Depthmap.video_converter import VideoConverter
    main()


def main():
    args = get_arguments()
    converter = VideoConverter(args.input, args.low, args.step, args.fast)
    converter.convert_video(args.output)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, dest='input',
            help="Path to read the input video")
    parser.add_argument("-o", "--output", required=True, dest='output',
            help="Path to save the output video")
    parser.add_argument("--low", required=False, action='store_true', dest='low',
            help="Resize frames to decrease halve the original aspect ratio - may increase speed")
    parser.add_argument("-s", "--step", required=False, type=int, default=1, dest='step',
            help="Step of reading frames, e.g. if step==3, every 3d frame will be taken for a depth map")
    parser.add_argument("--fast", required=False, action='store_true', dest='fast',
            help="Use fast version of depth map creator")
    args = parser.parse_args()
    return args

