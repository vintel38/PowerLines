# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:59:46 2021

@author: VArri

Algo : prend une image en COULEUR en entrée et la recadre un certain 
nombre de fois de façon choisie par l'utilisateur. L'utilisateur clique un 
certain nombre de fois sur l'image pour localiser les pixels cable qui sont 
alors recadrés et enregistrés dans le dossier associé. 

Les vastes images utilisées pour l'expression des étiquettes sont 
majoritairement remplies avec du bruit. Pour palier à ce problème et pour éviter
une sur-représentation des pixels bruits dans le dataset d'entraînement du CNN,
ce programme permet de sélectionner directement sur l'image les pixels des cables.
"""

import numpy as np
import os 
import cv2
from random import randrange
from datetime import date

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


os.chdir(r"C:\Users\VArri\Documents\PowerLines\images\visuel")
path = os.getcwd()
image_path = os.path.join(path, 'steered1000')
dirs = os.listdir(image_path)

i=randrange(0,len(dirs)+1) # !!!!! TO CHANGE AT EVERY ITERATION 
image_dir = os.path.join(image_path, dirs[i])

k=497 # !!!!! TO CHANGE AT EVERY ITERATION 
date=str(date.today())

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
    
print("NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE NOISE ")
print("[INFO] Click the left button: select the point, right click: delete the last selected point, click the middle button: determine the ROI area")
print("[INFO] Press ‘S’ to determine the selection area and save it")
print("[INFO] Press ESC to quit")

while True:
    
    img = cv2.imread(image_dir)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    x, y = gray.shape
    side = 28
    HF = int(side/2)
    
    pts = []
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_roi)
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            cv2.destroyAllWindows()
            import sys
            sys.exit()
        if key == ord("s"):
            saved_data = pts
            print("{} points ont été tracés dans la photo ".format(len(saved_data)))
            break
    cv2.destroyAllWindows()
    
    # print('{} points ont été trouvés dans l image'.format(len(pts)))
    for point in pts:
        y_crop = point[0]
        x_crop = point[1]
    
        crop = img[x_crop-HF:x_crop+HF, y_crop-HF:y_crop+HF,:]

        k=k+1
        #filename='./cropped1000/0/'+date+'_'+str(k)
        filename='./cropped_test1000/valid_0/'+date+'_'+str(k)
        cv2.imwrite(filename+'.jpeg', crop)
        
    i=randrange(0,len(dirs)+1)
    image_dir = os.path.join(image_path, dirs[i])