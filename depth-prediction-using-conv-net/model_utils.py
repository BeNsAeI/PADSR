import torch
import torch.nn as nn
import torchvision
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
import numpy as np
#from logger import Logger

def freeze_all_layers(model):
    for param in model.parameters():
        param.requires_grad = False
        
def unfreeze_all_layers(model):
    for param in model.parameters():
        param.requires_grad = True        

def get_model_predictions_on_a_sample_batch(model, dl):
    model.eval()
    with torch.no_grad():
        batch, actual_labels = iter(dl).next()
        batch = batch.to(device)
        actual_labels = actual_labels.to(device)
        predictions = model(batch)
    
    return (predictions, batch, actual_labels)

def depth_loss(preds, actual_depth):
    #preds.shape        -> [16, 1, 120, 160]
    #actual_depth.shape -> [16, 120, 160]
    n_pixels = actual_depth.shape[1]*actual_depth.shape[2]
    preds = preds.view(-1, n_pixels)
    actual_depth = actual_depth.view(-1, n_pixels)
    
    d = torch.log(preds) - torch.log(actual_depth)
    
    term_1 = torch.pow(d,2).mean(dim=1).mean() #pixel wise mean, then batch mean
    term_2 = (torch.pow(d.sum(dim=1),2)/(2*(n_pixels**2))).mean()
    
    return term_1 - term_2

def print_training_loss_summary(loss, total_steps, current_epoch, n_epochs, n_batches, print_every=10):
    #prints loss at the start of the epoch, then every 10(print_every) steps taken by the optimizer
    steps_this_epoch = (total_steps%n_batches)
    
    if(steps_this_epoch==1 or steps_this_epoch%print_every==0):
        print ('Epoch [{}/{}], Iteration [{}/{}], Loss: {:.4f}' 
               .format(current_epoch, n_epochs, steps_this_epoch, n_batches, loss))
