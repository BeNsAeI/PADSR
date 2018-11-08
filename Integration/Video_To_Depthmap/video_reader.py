import cv2
from Integration.helpers.file_system_helpers import check_file_exists

class VideoReader(object):
    '''
    Class-wrapper for the OpenCV VideoCapture class.
    If VideoReader object is initialized using with statement,
    VideoCapture object will be automatically destroyed
    after getting out of the with code block.
    '''
    def __init__(self, input_file, low_quality):
        '''
        input_file: string - name of input video file that will be readed
        low_quality: bool - if true, frames dimensions will be halved
        '''
        self.input_file = input_file
        self.low_quality = low_quality

        if not check_file_exists(input_file):
            raise ValueError("Please check that file %s exists." % input_file)

        # initialize VideoCapture
        self._capture = cv2.VideoCapture(self.input_file)
        if not self._capture or not self._capture.isOpened():
            raise ValueError("Failed to read file %s" % self.input_file)

        self.fps = self._capture.get(cv2.CAP_PROP_FPS)
        self.width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if self.low_quality:
            self.width /= 4
            self.height /= 4

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
        if low_quality is enabled, frames are returned with halved quality
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

            if self.low_quality:
                # Resize a frame
                next_frame = cv2.resize(next_frame, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
                next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)

            frame_count += 1
            yield next_frame
        print "VideoReader finished reading frames. Total frames in video: %d" % frame_count
