# -*- coding: utf-8 -*-
"""
Master program to create holograms.

Created on 9/18/19

@author: Luke Kurlandski
"""

from MotorControl import MotorControl #file with MotorControl class
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
        image.resize((newX,newY))
    if convert == True:
        image = image.convert('L')
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
    
def expose(pixVal):
    '''
    Exposes the film based upon the value of the pixel.
    (arg1) pixVal : the value of the pixel
    '''
    
    if pixVal < 25:
        print("Ignore")
        return
    if pixVal < 100:
        print("Exposing for the 25-100 range: ", pixVal * .01)
        return
    if pixVal < 200:
        print("Exposing for the 100-200 range: ", pixVal * .02)
    else:
        ("Exposing for the 200+ range: ", pixVal * .03)
        
def run_experiment(img_as_arr, expose_arr, width=.02, height=.02):    
    '''
    FIXME: add port
    '''
    
    #Number of pixels in image, size of image on hologram, distance each movement
    xPix = len(img_as_arr) 
    yPix = len(img_as_arr[0]) 
    width = width
    height = height
    xDelta = 1.0 * width / xPix
    yDelta = 1.0 * height / yPix
    
    #Motor control
    motor = MotorControl(port = 'COM7')
    motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
    
    #Read greyscale image, move as needed
    for i in range(0, xPix):
        onRow = False #indicates the motor is already at a row
        for j in range(0, yPix):
            if expose_arr[img_as_arr[i][j]] != 0:
                #expose
                if onRow == False:
                    motor.moveAbsolute(axis=2, goToPos=j*yDelta)
                motor.moveAbsolute(axis=1, goToPos=j*xDelta)
                onRow = True
                expose(expose_arr[img_as_arr[i][j]])
    
def test():
    print('Success')
    