import cv2
from Integration.helpers.file_system_helpers import check_file_exists

class VideoReader(object):
    '''
    Class-wrapper for the OpenCV VideoCapture class.
    If VideoReader object is initialized using with statement,
    VideoCapture object will be automatically destroyed
    after getting out of the with code block.
    '''
    def __init__(self, input_file, low_quality, size):
        '''
        input_file: string - name of input video file that will be readed
        low_quality: bool - if true, frames dimensions will be halved
        '''

        if low_quality and size:
            raise ValueError("Please provide either a fized size or a low-quality option")
        self.input_file = input_file

        if not check_file_exists(input_file):
            raise ValueError("Please check that file %s exists." % input_file)

        # initialize VideoCapture
        self._capture = cv2.VideoCapture(self.input_file)
        if not self._capture or not self._capture.isOpened():
            raise ValueError("Failed to read file %s" % self.input_file)

        self.fps = self._capture.get(cv2.CAP_PROP_FPS)
        self.width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.resize = True
        if low_quality:
            self.width /= 4
            self.height /= 4
        elif size:
            self.width = size[0]
            self.height = size[1]
        else:
            self.resize = False

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        print "Destroying VideoCapture object"
        self._capture.release()
        del self._capture
        del self.fps
        del self.width
        del self.height

    def get_next_frame(self):
        '''
        Generator that returns a new frame on each call
        if self.resize is True, frames are returned with halved quality
        '''
        frame_count = 0 # for debugging
        next_frame = None
        while self._capture.isOpened():
            # Capture frame-by-frame
            ret, next_frame = self._capture.read()
            if not ret:
                print "No frames to read, exit loop"
                break

            if next_frame is None:
                break

            if self.resize:
                # Resize a frame
                next_frame = cv2.resize(next_frame, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
                next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)

            frame_count += 1
            yield next_frame
        print "VideoReader finished reading frames. Total frames in video: %d" % frame_count
