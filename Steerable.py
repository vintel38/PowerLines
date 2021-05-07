# -*- coding: utf-8 -*-
"""
Created on Fri May  7 16:33:08 2021

@author: VArri

Edge Feature Detector with multiple steerable filters 
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

import scipy.signal as signal

def Exists(E):
    try: 
        E.astype(np.float32)
        return True
    except ValueError:
        return False

img = cv2.imread('./images/tree.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

sigma=1.0
filter_size = 2 * int(4 * sigma + 0.5) + 1 # taille du filtre en fonction du sigma recherché 

# Second order filter initialization
G2 = np.zeros((filter_size, filter_size, 3), np.float32) # création du filtre vide 


m = filter_size//2
n = filter_size//2

for x in range(-m, m+1):
    for y in range(-n, n+1):
        
        # Second order 
        # le filtre est balayé de par le centre d'où la range selon x et selon y 
        G2[x+m, y+n,0] = 0.9213*(2*x**2-1)*np.exp(-(x**2 + y**2))
        G2[x+m, y+n,1] = 1.843*x*y*np.exp(-(x**2 + y**2))
        G2[x+m, y+n,2] = 0.9213*(2*y**2-1)*np.exp(-(x**2 + y**2))

Start=True
#♥for theta in np.linspace(0, 2*np.pi, 100):
for theta in [np.pi/2]:
    
    print(theta)

    kG2 = [np.cos(theta)**2, - 2*np.sin(theta)*np.cos(theta), np.sin(theta)**2]    
    G2comb = kG2[0]*G2[:,:,0] +kG2[1]*G2[:,:,1] +kG2[2]*G2[:,:,2]
    
    Gray_i = signal.convolve2d(gray, G2comb)
    
    if Start:
        E_i = np.zeros(Gray_i.shape, np.float32)
        Start = False
    
    E_i = np.sqrt(np.square(E_i) + np.square(Gray_i))
    

    # plt.close('all')
    # plt.figure(figsize=(22, 8))
    # plt.subplot(121),
    # plt.imshow(img, cmap='gray')
    # plt.title('img'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),
    # plt.imshow(E_i, cmap='gray')
    # plt.title('E_i'), plt.xticks([]), plt.yticks([])
    # plt.show()
    
    plt.imshow(E_i, cmap='gray')
    plt.show()