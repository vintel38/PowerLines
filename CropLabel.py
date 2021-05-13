# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:59:46 2021

@author: VArri

Algo : prend une image en noir et blanc en entrée et la recadre un certain 
nombre de fois de façon aléatoire. Le recadrage est alors présenté à 
l'utilisateur qui choisit si ce recadrage est considéré comme 1 ou 0 pour 
l'étiquette. Le recadrage est alors enregistré au format image ainsi que son 
étiquette avec le même nom de fichier. L'utilissateur peut alors choisir à 
n'importe quel moment de changer d'image en appuyant simplement sur la touche 
n (Next).

"""

import os 
import cv2
import matplotlib.pyplot as plt
from random import randrange, random 
from datetime import date

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


os.chdir(r"C:\Users\VArri\Documents\PowerLines\images\visuel")
path = os.getcwd()
image_path = os.path.join(path, 'steered')
dirs = os.listdir(image_path)

#import sys
#sys.exit()
i=5
image_dir = os.path.join(image_path, dirs[i])

k=0 # image count
date=str(date.today())
while True:

    steered = cv2.imread(image_dir, 0)
    #steered = cv2.cvtColor(steered, cv2.COLOR_BGR2RGB)
    #gray = cv2.cvtColor(steered, cv2.COLOR_BGR2GRAY)
    
    # Will be easier to locate the rectangle on a color image
    lst = dirs[i].split('_')[:-2]
    img_dir = '_'.join(lst) + '.jpg'
    img = cv2.imread(os.path.join(path, 'basis', img_dir), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    x, y = steered.shape
    side = 28
    HF = int(side/2)
    
    x_crop = randrange(HF, x - HF)
    y_crop = randrange(HF, y - HF)
    
    # Display the left original color image 
    cv2.rectangle(img, (y_crop-HF, x_crop-HF),(y_crop+HF, x_crop+HF),(255, 0, 0), 20) # !! reverse for x and y 
    
    # Display the right steered grayscale image
    crop = steered[x_crop-HF:x_crop+HF, y_crop-HF:y_crop+HF]
    crop_cp = crop.copy()
    cv2.rectangle(crop_cp, (HF-1, HF-1), (HF+1, HF+1), (0,0,0), 1)
    plt.figure()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(crop_cp, cmap='gray')
    plt.show()
    
    label = input("Enter label (recall 0:no cable, 1:cable) : ")
    
    if not RepresentsInt(label):
        print('changes image file')
        i+=1
        image_dir = os.path.join(image_path, dirs[i])
    else:
        k=k+1
        filename='./cropped/'+date+'_'+str(k)
        cv2.imwrite(filename+'.jpg', crop)
        f = open(filename+'.txt', "w")
        f.write(str(label))
        f.close()
