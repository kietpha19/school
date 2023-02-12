import numpy as np
import os
import skimage.io as io
import skimage.color as color
import math


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

def pyramid_img(img, height):
    '''
    code from Dr. Dillhoff Github repo
    
    rows, cols, channels = img.shape
    # Create tuple of downscaled images
    pyramid = tuple(transform.pyramid_gaussian(img, downscale=2, multichannel=True))

    comp_img = np.zeros((rows, cols+cols // 2, channels), dtype=np.double)
    # Place the largest (original) image first
    comp_img[:rows, :cols, :] = pyramid[0]

    # Add in the other images
    i_row = 0
    h = 0
    for p in pyramid[1:]:
        n_rows, n_cols = p.shape[:2]
        comp_img[i_row:i_row + n_rows, cols:cols + n_cols, :] = p
        i_row += n_rows
        h+=1
        if h == height:
            break
    '''
    rows, cols, channels = img.shape
    comp_img = np.zeros((rows, cols+cols // 2, channels), dtype=np.double)
    # Place the largest (original) image first
    comp_img[:rows, :cols, :] = img
    
    pre_img = img
    i_row = 0
    for i in range(height):
        pre_img = resize_img(pre_img, 1/2)
        n_rows, n_cols = pre_img.shape[:2]
        comp_img[i_row:i_row + n_rows, cols:cols + n_cols, :] = pre_img
        i_row += n_rows
    
    return comp_img

image_path = input("enter image's file path: ")
img = io.imread(image_path)

#Convert to RGB from RGBA (if applicable)
if img.ndim == 3 and img.shape[2] == 4:
    img = color.rgba2rgb(img)

height = input("enter the pyramd height: ")
height = int(height)

img_pyramid = pyramid_img(img, height)

org_img_name = os.path.basename(image_path)
save_img_name = os.path.splitext(org_img_name)[0] + "_2x" + os.path.splitext(org_img_name)[1]
io.imsave(save_img_name, img_pyramid)