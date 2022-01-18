import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from itertools import compress
from os import listdir
from os.path import isfile, join
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models
import solver

def data_to_model(cropped):
    eq = []
    all_path = ['7','(','2','5','/','8','6','x',')','0','3','-','+','9','1','4']
    model = keras.models.load_model('model')
    for i in range(cropped.shape[0]):
        eq.append(all_path[int(np.asarray(tf.math.argmax(model(cropped[i:i+1])[0])))])
    eq = ''.join(eq)
    return eq

def draw_rectangles(img_name,rect_dat):
    img = cv.imread(img_name)
    img = reshape_input_img(img)
    for i in range(len(rect_dat)):
        x,y,w,h = rect_dat[i]
        rect = cv.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    return img

def save_img_with_rect(img_name):
    rect_dat = segment_image(img_name)
    img = draw_rectangles(img_name,rect_dat)
    img = cv.resize(img, (640,480), interpolation=cv.INTER_AREA)
    cv.imwrite(img_name.partition(".")[0] + '_rect.jpg', img)
    return img_name.partition(".")[0] + '_rect.jpg'

def get_area_above_min(percent_max,rect_dat):
    max_area = max([x[2]*x[3] for x in rect_dat[:]])
    fil = [x[2]*x[3]>max_area*percent_max for x in rect_dat[:]]
    return list(compress(rect_dat, fil))

def center_image(img):
    M = cv.moments(img)
    if (M["m00"] == 0):
        return img
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    translate_x = int(img.shape[0]/2)-cX
    translate_y = int(img.shape[1]/2)-cY
    translate = np.float32([[1,0,translate_x],[0,1,translate_y]])
    return cv.warpAffine(img, translate, (img.shape[1], img.shape[0]))

def compare_dimensions(rect,ratio=3,buffer_rate=0.2):
    if (rect[3]/rect[2])>ratio:
        return int(rect[2]*buffer_rate)
    else:
        return 0

def get_new_dimensions(img):
    x_dim = img.shape[0]
    y_dim = img.shape[1]
    while x_dim*y_dim > 1500*1500:
        x_dim = int(x_dim/2)
        y_dim = int(y_dim/2)
    return (x_dim, y_dim)

def reshape_input_img(img):
    reshape_img = get_new_dimensions(img)
    img = cv.resize(img, (reshape_img[1],reshape_img[0]), interpolation=cv.INTER_AREA)
    return img

def segment_image(img_name,dilate_multiplier=0.008,minimum_area=0.05):
    img = cv.imread(img_name)
    img = reshape_input_img(img) #Reduce the size of big images
    fat = int((img.shape[0]+img.shape[1])*dilate_multiplier)   #Number of dilations depends on image dimensions
    img = cv.blur(cv.cvtColor(img,cv.COLOR_BGR2GRAY),(6,6))   #Image to grayscale and added blur
    img = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,31,3)  #Adaptive thresholding helps deal with unequal background illumination
    if img.mean() > 255/2:   #Flips the binarized values so that 0s are more frequent
        img = cv.bitwise_not(img)
    img = cv.dilate(img, (20,20), iterations=fat)  #Dilates the image, helps to connect disconnected parts
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE) #Find contours of objects
    rect_dat = []
    for cnt in contours:
        x,y,w,h = cv.boundingRect(cnt)
        rect_dat.append((x,y,w,h)) #Get bounding rectangles of objects
    if not rect_dat: return rect_dat #Check if contours exist
    rect_dat = get_area_above_min(minimum_area,rect_dat) # Discard noise
    rect_dat = sorted(rect_dat, key=lambda x: x[0]) # Sorty by image x value
    return rect_dat

def cropped_dataset(img_name,dilate_multiplier=0.008,minimum_area=0.05,image_dim=(45,45)):
    rect_dat = segment_image(img_name,dilate_multiplier,minimum_area)
    cropped = []
    buffer = 2 #adds padding to the image
    for i in range(len(rect_dat)):
        buffer_vertical = compare_dimensions(rect_dat[i]) #change crop dimensions if the symbol is a bracket
        img_c = cv.imread(img_name)
        img_c = reshape_input_img(img_c) #Reduce the size of big images
        try:
            img = img_c[rect_dat[i][1]-buffer+buffer_vertical:rect_dat[i][1]+rect_dat[i][3]+buffer-buffer_vertical, rect_dat[i][0]-buffer-buffer_vertical:rect_dat[i][0]+rect_dat[i][2]+buffer+buffer_vertical]
            #Get cropped image
        except:
            print("buffer_too_large")
        if len(img) == 0: continue
        img = cv.cvtColor(img,cv.COLOR_BGR2GRAY) #Grayscale it
        img = cv.resize(img, image_dim, interpolation=cv.INTER_AREA) #Reshape to the size of our training dataset
        ret, img = cv.threshold(img,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU) #Binarize with threshold
        img = cv.ximgproc.thinning(img) #Thin the image to make it more like our train dataset
        img = center_image(img)
        cropped.append(img)
    if len(cropped)==0: return np.zeros((1, image_dim[0], image_dim[1],1)) #Debugging
    if len(cropped)>100: return np.zeros((1, image_dim[0], image_dim[1],1)) #Debugging
    cropped = np.asarray(cropped)/255
    cropped = cropped.reshape((cropped.shape[0],cropped.shape[1],cropped.shape[2],1))
    return cropped

def process_image(img_name):
    cropped = cropped_dataset(img_name)
    return data_to_model(cropped)

def image_to_solution(img_name):
    cropped = cropped_dataset(img_name)
    eq = data_to_model(cropped)
    return solver.solve(eq)
