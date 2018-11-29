import torchvision.transforms as transforms
import PIL
from PIL import Image
import numpy as np

class Resize(object):
    def __init__(self, size_tup):
        self.size = size_tup
    
    def __call__(self, im_array):
        pil_img = Image.fromarray(im_array)
        return np.asarray(pil_img.resize(self.size, resample=PIL.Image.BILINEAR))

def get_tfms(sz):
    return transforms.Compose([
            Resize(sz),
            transforms.ToTensor()
            ])
