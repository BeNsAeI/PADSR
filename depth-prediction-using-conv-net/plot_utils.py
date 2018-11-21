import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math

def plot_image(tup):
    img_tensor, depth_tensor = tup
    fig, axes = plt.subplots(1, 2, figsize=(10,15))
    for i,ax in enumerate(axes.flat):
        if(i==0):
            plot_image_tensor_in_subplot(ax, img_tensor)
        else:
            plot_depth_tensor_in_subplot(ax, depth_tensor)
        hide_subplot_axes(ax)

    plt.tight_layout()
    
#subplot utils    
def hide_subplot_axes(ax):
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

def plot_image_tensor_in_subplot(ax, img_tensor):
    im = img_tensor.cpu().numpy().transpose((1,2,0))
    #pil_im = Image.fromarray(im, 'RGB')
    ax.imshow(im)

def plot_depth_tensor_in_subplot(ax, depth_tensor):
    im = depth_tensor.cpu().numpy()
    #im = im*255
    #im = im.astype(np.uint8)
    #pil_im = Image.fromarray(im, 'L')
    ax.imshow(im,'gray')
    
def tensor_to_scalar(t):
    if t.dim()==0:
        return t.item()
    else:
        return t.numpy()    
    
#plots used in largest item classifier 
def plot_trn_image_with_annotations(im_id, jpeg_dic, JPEG_DIR, annotations_dic, category_dic, figsize=(10, 10)):
    fig, ax = plt.subplots(1, figsize=figsize)
    show_img_in_subplot(ax, Image.open(JPEG_DIR/jpeg_dic[im_id]['file_name']))
    hide_subplot_axes(ax)
    
    annotations = [annotations_dic[im_id]] if(type(annotations_dic[im_id]) == tuple) else annotations_dic[im_id]
        
    for ann in annotations:
        plot_bbox_annotation(ax, ann[0], category_dic[ann[1]])
        
    plt.show()

def plot_model_predictions_on_sample_batch(batch, pred_labels, actual_labels, get_label_fn, n_items=12, plot_from=0, figsize=(16,12)):
    n_rows, n_cols = (1,n_items) if n_items<=4 else (math.ceil(n_items/4), 4)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    for i,ax in enumerate(axes.flat):
        plot_idx = plot_from + i
        plot_image_tensor_in_subplot(ax, batch[plot_idx])

        pred_label = get_label_fn(tensor_to_scalar(pred_labels[plot_idx])) 
        actual_label = get_label_fn(tensor_to_scalar(actual_labels[plot_idx]))  

        hide_subplot_axes(ax)
        add_text_to_subplot(ax, (0,0), 'Pred: '+pred_label)
        add_text_to_subplot(ax, (0,30), 'Actual: '+actual_label, color='yellow')

    plt.tight_layout()
