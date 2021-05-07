# -*- coding: utf-8 -*-
"""
Created on Fri May  7 17:42:39 2021

@author: VArri

Canny edge detection fast response
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np


img = cv2.imread('./images/tree.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


edge = cv2.Canny(gray, 100, 200)

plt.imshow(edge, cmap='gray')
plt.show()