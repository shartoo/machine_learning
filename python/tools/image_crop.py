# -*- coding:utf-8 -*-
'''
图像切割成正方形
'''
import scipy.misc
import numpy as np
import glob
import os

def center_crop(x, crop_h, crop_w=None, resize_w=64):
    if crop_w is None:
        crop_w = crop_h
    h, w = x.shape[:2]
    j = int(round((h - crop_h)/2.))
    i = int(round((w - crop_w)/2.))
    return scipy.misc.imresize(x[j:j+crop_h, i:i+crop_w],
                               [resize_w, resize_w])

def imread(path, is_grayscale = False):
    if (is_grayscale):
        return scipy.misc.imread(path, flatten = True).astype(np.float)
    else:
        return scipy.misc.imread(path).astype(np.float)

def imsave(image, path):
    return scipy.misc.imsave(path,image)

if __name__=='__main__':
    #data = glob(, "*.jpg")
    head = "D:/myGithub/DCGAN-tensorflow/data/human_face"
    save_head = "D:/myGithub/DCGAN-tensorflow/data/human_face_crop"
    list = os.listdir(head)
    for file in list:
        imsave(center_crop(imread(head+"/"+file,False),120),save_head+"/"+file)
        print("crop image %s saved.."%file)
