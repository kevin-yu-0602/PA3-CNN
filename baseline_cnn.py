################################################################################
# CSE 190: Programming Assignment 3
# Fall 2018
# Code author: Jenny Hamer
#
# Filename: baseline_cnn.py
# 
# Description: 
# 
# This file contains the starter code for the baseline architecture you will use
# to get a little practice with PyTorch and compare the results of with your 
# improved architecture. 
#
# Be sure to fill in the code in the areas marked #TODO.
################################################################################


# PyTorch and neural network imports
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as func
import torch.nn.init as torch_init
import torch.optim as optim

# Data utils and dataloader
import torchvision
from torchvision import transforms, utils
from xray_dataloader import ChestXrayDataset, create_split_loaders

import matplotlib.pyplot as plt
import numpy as np
import os



class BasicCNN(nn.Module):
    """ A basic convolutional neural network model for baseline comparison. 
    
    Consists of three Conv2d layers, followed by one 4x4 max-pooling layer, 
    and 2 fully-connected (FC) layers:
    
    conv1 -> conv2 -> conv3 -> maxpool -> fc1 -> fc2 (outputs)
    
    Make note: 
    - Inputs are expected to be grayscale images (how many channels does this imply?)
    - The Conv2d layer uses a stride of 1 and 0 padding by default
    """
    
    def __init__(self):
        super(BasicCNN, self).__init__()
        F1_IN_C = 1
        F1_OUT_C = 12
        F1_KERNEL = 8

        F2_OUT_C = 10
        F2_KERNEL = 8

        F3_OUT_C = 8
        F3_KERNEL = 8

        MP1_KERNEL = 3
        MP1_STRIDE = MP1_KERNEL
        
        # conv1: 1 input channel, 12 output channels, [8x8] kernel size
        self.conv1 = nn.Conv2d(in_channels=F1_IN_C, out_channels=F1_OUT_C, kernel_size=F1_KERNEL)
        
        # Add batch-normalization to the outputs of conv1
        self.conv1_normed = nn.BatchNorm2d(F1_OUT_C)
        
        # Initialized weights using the Xavier-Normal method
        torch_init.xavier_normal_(self.conv1.weight)

        #TODO: Fill in the remaining initializations replacing each '_' with
        # the necessary value based on the provided specs for each layer

        #TODO: conv2: X input channels, 10 output channels, [8x8] kernel
        self.conv2 = nn.Conv2d(in_channels=F1_OUT_C, out_channels=F2_OUT_C, kernal_size=F2_KERNEL)
        self.conv2_normed = nn.BatchNorm2d(F2_OUT_C)
        torch_init.xavier_normal_(self.conv2.weight)

        #TODO: conv3: X input channels, 8 output channels, [6x6] kernel
        self.conv3 = nn.Conv2d(in_channels=F2_OUT_C, out_channels=F3_OUT_C, kernal_size=F3_KERNEL)
        self.conv3_normed = nn.BatchNorm2d(F3_OUT_C)
        torch_init.xavier_normal_(self.conv3.weight)

        #TODO: Apply max-pooling with a [3x3] kernel using tiling (*NO SLIDING WINDOW*)
        self.pool = nn.MaxPool2d(kernel_size=MP1_KERNEL, stride=MP1_STRIDE)

        # Define 2 fully connected layers:
        #TODO: Use the value you computed in Part 1, Question 4 for fc1's in_features
        self.fc1 = nn.Linear(in_features=__, out_features=128)
        self.fc1_normed = nn.BatchNorm1d(__)
        torch_init.xavier_normal_(_______)

        #TODO: Output layer: what should out_features be?
        self.fc2 = nn.Linear(in_features=__, out_features=__).cuda()
        torch_init.xavier_normal_(_______)



    def forward(self, batch):
        """Pass the batch of images through each layer of the network, applying 
        non-linearities after each layer.
        
        Note that this function *needs* to be called "forward" for PyTorch to 
        automagically perform the forward pass. 
        
        Params:
        -------
        - batch: (Tensor) An input batch of images

        Returns:
        --------
        - logits: (Variable) The output of the network
        """
        
        # Apply first convolution, followed by ReLU non-linearity; 
        # use batch-normalization on its outputs
        batch = func.relu(self.conv1_normed(self.conv1(batch)))
        
        # Apply conv2 and conv3 similarly
        batch = _______ #func.relu(self.conv2_normed(self.conv2(batch)))
        batch = _______ #func.relu(self.conv3_normed(self.conv3(batch)))
        
        # Pass the output of conv3 to the pooling layer
        batch = self.pool(batch)

        # Reshape the output of the conv3 to pass to fully-connected layer
        batch = batch.view(-1, self.num_flat_features(batch))
        
        # Connect the reshaped features of the pooled conv3 to fc1
        batch = _______ #func.relu(self.fc1(batch))
        
        # Connect fc1 to fc2 - this layer is slightly different than the rest (why?)
        batch = _______ # self.fc2(batch)


        # Return the class predictions
        #TODO: apply an activition function to 'batch'
        return _______ # func.sigmoid(batch)
    
    

    def num_flat_features(self, inputs):
        
        # Get the dimensions of the layers excluding the inputs
        size = inputs.size()[1:]
        # Track the number of features
        num_features = 1
        
        for s in size:
            num_features *= s
        
        return num_features
