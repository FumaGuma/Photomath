import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from itertools import compress
from os import listdir
from os.path import isfile, join
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models

def get_rectangles(img_name):
    img = cv.imread(img_name)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = cv.blur(gray,(6,6))
    thresh = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,31,3)
    if thresh.mean() > 255/2:
        thresh = cv.bitwise_not(thresh)
    kernel_size = 2
    kernel = np.ones((kernel_size,kernel_size),np.uint8)
    thresh = cv.dilate(thresh, (20,20), iterations=3)
    #thresh = cv.erode(thresh, (20,20), iterations=3)
    thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    rect_dat = []
    for cnt in contours:
        x,y,w,h = cv.boundingRect(cnt)
        rect_dat.append((x,y,w,h))
    rect_dat = get_area_above_min(0.05,rect_dat)
    rect_dat = sorted(rect_dat, key=lambda x: x[0])
    return rect_dat

def get_area_above_min(percent_max,rect_dat):
    max_area = max([x[2]*x[3] for x in rect_dat[:]])
    fil = [x[2]*x[3]>max_area*percent_max for x in rect_dat[:]]
    return list(compress(rect_dat, fil))

def draw_rectangles(img_name,rect_dat):
    img = cv.imread(img_name)
    for i in range(len(rect_dat)):
        x,y,w,h = rect_dat[i]
        rect = cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    return img

def save_img_with_rect(img_name,rect_dat):
    img = draw_rectangles(img_name,rect_dat)
    img = cv.resize(img, (640,480), interpolation=cv.INTER_AREA)
    cv.imwrite(img_name.partition(".")[0] + '_rect.jpg', img)

def cropped_dataset(img_name,rect_dat):
    cropped = []
    buffer = 3
    for i in range(len(rect_dat)):
        img_c = cv.imread(img_name)
        try:
            crop_img = img_c[rect_dat[i][1]-buffer:rect_dat[i][1]+rect_dat[i][3]+buffer, rect_dat[i][0]-buffer:rect_dat[i][0]+rect_dat[i][2]+buffer]
        except:
            print("buffer_too_large")
        #resized_img = cv.resize(crop_img, (45,45), interpolation=cv.INTER_AREA)
        thresh_res = cv.cvtColor(crop_img,cv.COLOR_BGR2GRAY)
        thresh_res = cv.resize(thresh_res, (45,45), interpolation=cv.INTER_AREA)
        ret, thresh_res = cv.threshold(thresh_res,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        #thresh = cv.adaptiveThreshold(resized_img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,5,3)
        thresh_res = cv.ximgproc.thinning(thresh_res)
        #thresh_res = cv.resize(thresh_res, (45,45), interpolation=cv.INTER_AREA)
        #ret, thresh_res = cv.threshold(crop_img,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
        #thresh_res = cv.ximgproc.thinning(thresh_res)
        M = cv.moments(thresh_res)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        translate_x = int(thresh_res.shape[0]/2)-cX
        translate_y = int(thresh_res.shape[1]/2)-cY
        translate = np.float32([[1,0,translate_x],[0,1,translate_y]])
        thresh_res = cv.warpAffine(thresh_res, translate, (thresh_res.shape[1], thresh_res.shape[0]))
        cropped.append(thresh_res)
    cropped = np.asarray(cropped)/255
    cropped = cropped.reshape((cropped.shape[0],cropped.shape[1],cropped.shape[2],1))
    return cropped

def data_to_model(cropped):
    eq = []
    all_path = ['7','(','2','5','/','8','6','x',')','0','3','-','+','9','1','4']
    model = keras.models.load_model('model2')
    for i in range(cropped.shape[0]):
        eq.append(all_path[int(np.asarray(tf.math.argmax(model(cropped[i:i+1])[0])))])
    eq = ''.join(eq)
    return eq
