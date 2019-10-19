# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:39:14 2019

@author: laserlab
"""

from PIL import Image #package to support image work

def convert_grey_downsize(image_file, newX=None, newY=None, convert=False):
    '''
    Converts and optionall downsizes an image
    (arg1) image_file : file path of the incomming image (string)
    (arg2) new X : new size in the x direction (int)
    (arg3) newY : new size in the y direction (int)
    (arg4) convert : determines whether or not to convert the image (boolean)
    (return) image : new image (PIL image)
    '''
    
    image = Image.open(image_file)
    if(newX != None and newY != None):
        image = image.resize((newX,newY))
    if convert == True:
        image = image.convert('L')
    print(image)
    return image

def get_image_array(image):
    '''
    Recieves an image, outputs the array representation
    (arg1) image : image to convert (PIL image)
    (return) pixelMatrix : array representation (list)
    FIXME: possibly transposes the matrix unintentionally
    '''
    
    pixelMatrix = []
    for i in range(image.width): #possibly replace with image.height
        temp = []
        pixelMatrix.append(temp)
        for j in range(image.height): #possibly replace with image.width
            temp.append(image.getpixel((i,j)))
    return pixelMatrix

def test():
    '''
    Used for local testing.
    '''