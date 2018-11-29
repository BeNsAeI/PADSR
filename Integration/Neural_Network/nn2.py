import PIL
from PIL import Image
import torch
from torch.autograd import Variable
from torchvision import transforms
from Integration.Neural_Network.DIW_transforms import get_tfms
import numpy as np
from Integration.Neural_Network.models.hourglass import Model
import cv2

model = Model()
model.load_state_dict(torch.load('weights.ckpt', map_location='cpu'))

def batchify(raw_im_array, sz):
    tfms = get_tfms(sz)
    batch = []

    for im in raw_im_array:
        batch.append(tfms(im))

    tensor_batch = torch.stack(batch)
    return Variable(tensor_batch)

def get_pred_depth_maps(preds):
    op_size = preds.size()
    h, w = op_size[2], op_size[3]
    n_pixels = h*w
    depths_batch = preds.data

    depths_batch = depths_batch.view(-1, n_pixels)

    image_wise_min = depths_batch.min(dim=1)[0]
    image_wise_min = image_wise_min.unsqueeze(dim=1)

    depths_batch = depths_batch - image_wise_min

    image_wise_max = depths_batch.max(dim=1)[0]
    image_wise_max = image_wise_max.unsqueeze(dim=1)
    depths_batch = depths_batch / image_wise_max

    depths_batch = depths_batch.view(-1, 1, h, w)
    depths_batch = (depths_batch*255).type(torch.IntTensor)
    depths_batch = depths_batch.squeeze(dim=1).numpy()
    return depths_batch

def predict(img_left, img_right, model, size):
    # image batch would be a numpy array NxHxWx3
    im_batch = np.array([np.asarray(img_left), np.asarray(img_right)])

    with torch.no_grad():
        model.eval()
        batch = batchify(im_batch, size)
        preds = model(batch)
        return get_pred_depth_maps(preds)

def get_depth_image_using_CNN(img_left, img_right, size):
        depths_batch = predict(img_left, img_right, model, size)
        Image.fromarray(depths_batch[0].astype('uint8'))
        return depths_batch[0].astype('uint8')

