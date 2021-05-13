# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:42:39 2021

@author: VArri

Simple Edge Enhancing Technique as preprocessing for PLD. First step is to 
compute a slight Gaussian Blur as an average image, then substract it to the 
original image with addweighted weights to keep the same level of luminosity.
Fast and simple technique. 

Simple Canny Edge Detection is also availbale but is not that useful for PLD 
"""

import cv2
# import matplotlib.pyplot as plt
# import numpy as np
import os


def EdgeEnhancing(path, image_path):
    
    img = cv2.imread(image_path)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #edge = cv2.Canny(gray, 100, 200)
    blur = cv2.GaussianBlur(img,(5,5),0)
    smooth = cv2.addWeighted(img,1.5,blur,-0.5,0)
    
    filename, file_extension = os.path.splitext(os.path.basename(image_path))
    output_path = os.path.join(path, 'edge', filename+'_edge.jpg')
    cv2.imwrite(output_path, smooth)
    
os.chdir(r"C:\Users\VArri\Documents\PowerLines\images\visuel")
path = os.getcwd()
basis_dir = os.path.join(path, 'basis')
dirs = os.listdir(basis_dir)

for di in dirs:
    image_path = os.path.join(basis_dir, di)
    
    #print(di)
    #print(image_path)
    #break
    
    EdgeEnhancing(path, image_path)