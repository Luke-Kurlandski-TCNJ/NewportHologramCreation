# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:30:51 2019

@author: Luke Kurlandski
"""

import numpy as np #package to support array work
import matplotlib.pylab as plt #package to support image work

def png4_to_png3(image):
    myList = image.tolist()
    for row in list:
        for col in row:
            del col[3]
    print(len(myList), len(myList[0]), len(myList[0][0]))
    
def imageToGreyList(image):
    '''
    Converts an image with 3+ pixel dimentions into a greyscale list
    (arg1) image : the image to be converted (plt image)
    return list: the greyscale list (2-D list)
    '''
    
    imgList = image.tolist()
    rows = len(imgList)
    cols = len(imgList[0])
    myList = []
    for i in range (0,rows):
        tList = []
        myList.append(tList)
        for j in range (0,cols):
            myList[i].append((.2989*imgList[i][j][0])+(.587*imgList[i][j][1])+(.114*imgList[i][j][2]))
    return myList

def plotImage(image, h=8, **kwargs):
    y = image.shape[0] #pixels in the y direction
    x = image.shape[1] #pixels in the x direction
    w = h * (x/y)
    plt.figure(figsize=(w,h)) #determines the proportional size of the image
    plt.imshow(image,interpolation='none', *kwargs)
    plt.axis('off')

def toGreyScale(image, weights = np.c_[0.2989, 0.5870, 0.1140]):
    tile = np.tile(weights, reps=(image.shape[0], image.shape[1], 1))
    return np.sum(tile * image, axis=2)

def main():
    imageFile = "Earth.png"
    image = plt.imread(imageFile)
    myList = imageToGreyList(image)
    print(len(myList), len(myList[0]))
    
main()