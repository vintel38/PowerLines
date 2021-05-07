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
import matplotlib.pyplot as plt
# import numpy as np

img = cv2.imread('./images/tree.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#edge = cv2.Canny(gray, 100, 200)
blur = cv2.GaussianBlur(img,(5,5),0)
smooth = cv2.addWeighted(img,1.5,blur,-0.5,0)

plt.imshow(smooth, cmap='gray')
plt.show()
cv2.imwrite('./images/tree_edge.jpg', smooth)