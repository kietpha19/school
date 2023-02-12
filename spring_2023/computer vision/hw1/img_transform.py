import numpy as np
import skimage.io as io
import skimage.color as color
from skimage import transform
from numpy.lib import stride_tricks
import os, sys
import random
import math

#function from 1st atk
def rgb_to_hsv(img_rgb):
    #normalize if rgb still in [0,255]
    if img_rgb.dtype == np.uint8 or img_rgb.dtype == np.uint16:
        img_rgb = np.array(img_rgb, dtype=float) / 255.
    
    #init img_hsv matrix
    img_hsv = np.empty_like(img_rgb)

    #calculate the Value matrix
    #V = img_rgb.max(-1) #alternative way
    V = np.max(img_rgb, axis =2)
    
    #calculate the Chroma matrix, also called delta in some resource
    #delta = img_rgb.ptp(-1) #alternative way
    C = V - np.min(img_rgb, axis=2)

    #calculate the Saturation matrix
    #noticed that: S = C/V. If V=0, then S=0
    #S = np.divide(C,V, out=np.zeros_like(C), where=V!=0)
    Ignore_divided_0 = np.seterr(invalid='ignore')
    S = C / V
    S[C == 0.] = 0.

    # Calculate the Hue Matrix
    # we will store the H' in img_hsv[idx, 0] temporarily
    # red is max
    idx = (img_rgb[..., 0] == V)
    img_hsv[idx, 0] = ((img_rgb[idx, 1] - img_rgb[idx, 2]) / C[idx]) % 6
    
    # green is max
    idx = (img_rgb[..., 1] == V)
    img_hsv[idx, 0] = 2. + (img_rgb[idx, 2] - img_rgb[idx, 0]) / C[idx]
    
    # blue is max
    idx = (img_rgb[..., 2] == V)
    img_hsv[idx, 0] = 4. + (img_rgb[idx, 0] - img_rgb[idx, 1]) / C[idx]
    
    #H = (img_hsv[..., 0] / 6.) % 1. #this is if we want to normalize H to be in [0,1]
    H = img_hsv[..., 0]*60. #this is for H in [0,360] degree
    # if C = 0
    H[C == 0.] = 0.
    
    np.seterr(**Ignore_divided_0)

    #combine all HSV components
    img_hsv[..., 0] = H
    img_hsv[..., 1] = S
    img_hsv[..., 2] = V

    # set all nan to 0
    img_hsv[np.isnan(img_hsv)] = 0
    
    return img_hsv

#function from 1st task
def hsv_to_rgb(img_hsv):
    #init img_rgb matrix
    img_rgb = np.empty_like(img_hsv)

    # generate 3 separated matrix for H, S, V
    H = img_hsv[..., 0]
    S = img_hsv[..., 1]
    V = img_hsv[..., 2]

    # Calcualte Chroma matrix
    C = V*S

    # H' matrix
    H_prime = H/60

    # X matrix
    X = C * (1- abs(H_prime%2 - 1))

    # convert H' to the condition, that is used to calculate R', G', B' later
    H_prime = H_prime.astype(int) % 6

    # m matrix
    m = V - C

    #calculate R',G',B' according to the condition of H', then add m[idx] to get RGB (see class notes)
    idx = H_prime[...] == 0
    img_rgb[idx, 0] = C[idx] + m[idx]
    img_rgb[idx, 1] = X[idx] + m[idx]
    img_rgb[idx, 2] = m[idx]

    idx = H_prime[...] == 1
    img_rgb[idx, 0] = X[idx] + m[idx]
    img_rgb[idx, 1] = C[idx] + m[idx]
    img_rgb[idx, 2] = m[idx]

    idx = H_prime[...] == 2
    img_rgb[idx, 0] = m[idx]
    img_rgb[idx, 1] = C[idx] + m[idx]
    img_rgb[idx, 2] = X[idx] + m[idx]

    idx = H_prime[...] == 3
    img_rgb[idx, 0] = m[idx]
    img_rgb[idx, 1] = X[idx] + m[idx]
    img_rgb[idx, 2] = C[idx] + m[idx]

    idx = H_prime[...] == 4
    img_rgb[idx, 0] = X[idx] + m[idx]
    img_rgb[idx, 1] = m[idx]
    img_rgb[idx, 2] = C[idx] + m[idx]

    idx = H_prime[...] == 5
    img_rgb[idx, 0] = C[idx] + m[idx]
    img_rgb[idx, 1] = m[idx]
    img_rgb[idx, 2] = X[idx] + m[idx]
    
    return img_rgb

#function from 1st task
def modify_img(img, h, s, v):
    img_hsv = rgb_to_hsv(img)
    img_hsv[..., 0] = (img_hsv[..., 0] + h) % 360
    img_hsv[..., 1] = (img_hsv[..., 1] + s) % 1
    img_hsv[..., 2] = (img_hsv[..., 2] + v) % 1

    img_rgb = hsv_to_rgb(img_hsv)
    return img_rgb


#print numpy array without scientific notation
np.set_printoptions(suppress=True)

def random_crop(img, size):
    #Convert to RGB from RGBA (if applicable)
    if img.ndim == 3 and img.shape[2] == 4:
        img = color.rgba2rgb(img)

    w, h = len(img[0]), len(img)
    if size > min(w,h):
        sys.exit("cropping size is not feasible")
    x = random.randint(0, w - size)
    y = random.randint(0, h - size)
    return img[x:x + size, y:y + size]

def extract_patches(img, size):
    #Convert to RGB from RGBA (if applicable)
    if img.ndim == 3 and img.shape[2] == 4:
        img = color.rgba2rgb(img)

    H, W, C = img.shape
    shape = [H//size, W//size] + [size, size, C]
    strides = [size*s for s in img.strides[:2]] + list(img.strides)
    patches = stride_tricks.as_strided(img, shape=shape, strides=strides)
    
    return patches

    '''
    script to test this function
    <call the function using an img input)
    
    #display all patches
    fig = plt.figure()
    nrows = patches.shape[0]
    ncols = patches.shape[1]

    for i in range(nrows):
        for j in range(ncols):
            idx = nrows*i + j
            ax = fig.add_subplot(nrows, ncols, idx+1)
            ax.imshow(patches[i][j])
            ax.tick_params(left = False, right=False, bottom=False, top=False)
    '''

def resize_img(img, factor):
    #Convert to RGB from RGBA (if applicable)
    if img.ndim == 3 and img.shape[2] == 4:
        img = color.rgba2rgb(img)

    H, W = img.shape[:2]
   
    new_H = math.floor(H*factor)
    new_W = math.floor(W*factor)
    
    #init new_img matrix
    new_img = np.empty(shape = [new_H, new_W, 3])
    
    for i in range(new_H):
        for j in range(new_W):
            #cross product of the transformation matrix and scaled img coordinate pixel
            x = math.floor(i*(1/factor))
            y = math.floor(j*(1/factor))
            
            #assign new_img pixel by the original img pixel
            new_img[i,j] = img[x,y]
    
    return new_img

def color_jitter(img, hue, saturation, value):
    hue = float(hue)
    if not (0<= hue <= 360):
        sys.exit("Heu must be in [0, 360]")

    saturation = float(saturation)
    if not (0<= saturation <= 1):
        sys.exit("Saturation must be in [0, 1]")

    value = float(value)
    if not (0<= value <= 1):
        sys.exit("Value must be in [0, 1]")
    
    h = random.uniform(0, hue)
    s = random.uniform(0, saturation)
    v = random.uniform(0, value)
    
    return modify_img(img, h, s, v)

