import torch
import torchvision
import torchvision.transforms as transforms

import numpy as np
from PIL import Image


class ResizeImgAndDepth(object):
    def __init__(self, size_tup):
        self.size = size_tup
        
    def __call__(self, sample):
        img = Image.fromarray(sample['image'],  'RGB').resize(self.size)
        depth = Image.fromarray(sample['depth'], 'L').resize((self.size[0]//4, self.size[1]//4))
        return { 'image' : np.array(img), 'depth' : np.array(depth) }

class RandomHorizontalFlip(object):    
    def __call__(self, sample):
        img = sample["image"]
        depth = sample["depth"]
        if np.random.random() > 0.5:
            img = np.fliplr(sample['image']).copy()
            depth = np.fliplr(sample['depth']).copy()
        return { 'image' : img, 'depth' : depth }
    
    
class ImgAndDepthToTensor(object):        
    def __init__(self):
        self.ToTensor = transforms.ToTensor()
        
    def __call__(self, sample):        
        return { 'image' : self.ToTensor(sample['image']), 'depth' : torch.tensor(sample['depth']/255, dtype=torch.float) }      

class NormalizeImg(object):
    def __init__(self, mean, std):
        self.normalize = transforms.Normalize(mean, std)
    
    def __call__(self, sample):
        return { 'image' : self.normalize(sample['image']), 'depth' : sample['depth'] }


class UnNormalizeImg(object):
    def __init__(self, mean, std):
        self.mean = mean.reshape((3,1,1))
        self.std = std.reshape((3,1,1))
    
    def __call__(self, tup):
        un_img = (tup[0]*self.std) + self.mean
        return (un_img, tup[1])
