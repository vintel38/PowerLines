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

Les vastes images utilisées pour l'expression des étiquettes sont 
majoritairement remplies avec du bruit. Pour palier à ce problème et pour éviter
une sur-représentation des pixels bruits dans le dataset d'entraînement du CNN,
ce programme permet de sélectionner directement sur l'image les pixels des cables.
"""

import numpy as np
#import tensorflow as tf 
import os 
import cv2
import matplotlib.pyplot as plt
#from random import randrange
from datetime import date

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


os.chdir(r"C:\Users\VArri\Documents\PowerLines\images")
path = os.getcwd()
image_folder = 'visuel'
image_path = os.path.join(path, image_folder)
dirs = os.listdir(image_path)

#import sys
#sys.exit()
i=0 # !!!!! TO CHANGE AT EVERY ITERATION 
image_dir = os.path.join(image_path, dirs[i])

k=0 # !!!!! TO CHANGE AT EVERY ITERATION 
date=str(date.today())

img = cv2.imread(image_dir)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

x, y = gray.shape
side = 28
HF = int(side/2)

# crop = tf.image.random_crop(img, size = [28,28])


#import imutils
pts = [] # for storing points
# :mouse callback function
def draw_roi(event, x, y, flags, param):
    img2 = img.copy()
 
    if event == cv2.EVENT_LBUTTONDOWN: # Left click, select point
        pts.append((x, y))  
 
    if event == cv2.EVENT_RBUTTONDOWN: # Right click to cancel the last selected point
        pts.pop()  
 
    if event == cv2.EVENT_MBUTTONDOWN: # 
        mask = np.zeros(img.shape, np.uint8)
        points = np.array(pts, np.int32)
        points = points.reshape((-1, 1, 2))
                 # 
        mask = cv2.polylines(mask, [points], True, (255, 255, 255), 2)
        mask2 = cv2.fillPoly(mask.copy(), [points], (255, 255, 255)) # for ROI
        mask3 = cv2.fillPoly(mask.copy(), [points], (0, 255, 0)) # for displaying images on the desktop
 
        show_image = cv2.addWeighted(src1=img, alpha=0.8, src2=mask3, beta=0.2, gamma=0)
 
        cv2.imshow("mask", mask2)
        cv2.imshow("show_img", show_image)
 
        ROI = cv2.bitwise_and(mask2, img)
        cv2.imshow("ROI", ROI)
        cv2.waitKey(0)
 
    if len(pts) > 0:
                 # Draw the last point in pts
        cv2.circle(img2, pts[-1], 3, (0, 0, 255), -1)
 
    if len(pts) > 1:
                 # 
        for i in range(len(pts) - 1):
            cv2.circle(img2, pts[i], 5, (0, 0, 255), -1) # x ,y is the coordinates of the mouse click place
            # cv2.line(img=img2, pt1=pts[i], pt2=pts[i + 1], color=(255, 0, 0), thickness=2)
 
    cv2.imshow('image', img2)
 
 
#Create images and windows and bind windows to callback functions
#img = cv2.imread('HL.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = imutils.resize(img, width=500)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_roi)
print("[INFO] Click the left button: select the point, right click: delete the last selected point, click the middle button: determine the ROI area")
print("[INFO] Press ‘S’ to determine the selection area and save it")
print("[INFO] Press ESC to quit")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    if key == ord("s"):
        saved_data = pts
        #joblib.dump(value=saved_data, filename="config.pkl")
        #print("[INFO] ROI coordinates have been saved to local.")
        print(saved_data)
        break
cv2.destroyAllWindows()

print('{} points ont été trouvés dans l image'.format(pts.size))
for point in pts:
    print(point)
    y_crop = point[0]
    x_crop = point[1]

    #x_crop = randrange(HF, x - HF)
    #y_crop = randrange(HF, y - HF)
    
    crop = gray[x_crop-HF:x_crop+HF, y_crop-HF:y_crop+HF]
    cv2.rectangle(img, (y_crop-HF, x_crop-HF),(y_crop+HF, x_crop+HF),(255, 0, 0), 20) # !! reverse for x and y 
    
    crop_cp = crop.copy()
    cv2.rectangle(crop_cp, (HF-1, HF-1), (HF+1, HF+1), (0,0,0), 1)
    plt.figure()
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(crop_cp, cmap='gray')
    plt.show()
    
    # label = input("Enter label (recall 0:no cable, 1:cable) : ")
    label = 1 # !!!! EACH AND EVERY POINT IS A CABLE POINT
    if not RepresentsInt(label):
        print('change image file')
        i+=1
        image_dir = os.path.join(image_path, dirs[i])
    else:
        filename='./visuel/cropped/'+date+'_'+str(k)
        k=k+1
        cv2.imwrite(filename+'.jpg', crop)
        f = open(filename+'.txt', "w")
        f.write(str(label))
        f.close()

# useful documentation for the process of classification and 
# runcell(0, 'C:/Users/VArri/Documents/GitHub/PowerLines/CropLabel.py')