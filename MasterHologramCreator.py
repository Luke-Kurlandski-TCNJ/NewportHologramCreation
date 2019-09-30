# -*- coding: utf-8 -*-
"""
Master program to create holograms.

Created on 9/18/19

@author: Luke Kurlandski
"""

import numpy as np #package to support array work
import matplotlib.pylab as plt #package to support image work
from MotorControl import MotorControl #file with MotorControl class
from PIL import Image #package to support image work

def getGrayScaleImage(image, *args):
    '''
    Accepts PIL image and optional length, width
    if there is a length, width then resize image
    Converts image to grayscale and returns array of grayscale values
    '''
    if len(args) == 2:
        image.resize(args[0], args[1])

    image = image.convert('LA')
    matrix = image.load()
    pixelMatrix = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixelMatrix[i,j] = matrix[i,j][1]
    
    
    return pixelMatrix

def imageToGreyList(image):
    '''
    Converts an image with 3+ pixel dimentions into a greyscale list
    (arg1) image : the image to be converted (plt image)
    (return) list: the greyscale list (2-D list)
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

def inRange(pixVal, minVal, maxVal, ignoreVals = None):
    '''
    Determines whether or not the pixel value causes exposure.
    (arg1) pixVal : the value of the pixel
    (arg2) minVal : the minimum pixel value that will cause an exposure
    (arg3) maxVal : the maximum pixel value that will cause an exposure
    (arg4) ignoreVals : a listof values that should not be exposed
    (return) True/False : whether or not to expose
    '''
    
    if pixVal < minVal or pixVal > maxVal:
        return False
    if ignoreVals != None:
        for i in ignoreVals:
            if pixVal == i:
                return False
    return True
    
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
        
def run_experiment(imgArr, exposeArr, width=.02, height=.02):    
    #Image selection, conversion, exposure details
    '''
    imageFile = "Earth.png"
    image = plt.imread(imageFile)
    imgArr = imageToGreyList(image)
    minVal = -1
    maxVal = 255
    ignoreVals = [30, 50, 100]
    '''
    
    #Number of pixels in image, size of image on hologram, distance each movement
    xPix = len(imgArr) #safer than using the user's input
    yPix = len(imgArr[0]) #safer than using the user's input
    width = width
    height = height
    xDelta = 1.0 * xLength / xPixel
    yDelta = 1.0 * yLength / yPixel
    
    #Motor control
    motor = MotorControl(port = 'COM7')
    motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
    
    #Read greyscale image, move as needed
    for i in range(0, xPixel):
        onRow = False #indicates the motor is already at a row
        for j in range(0, yPixel):
            if inRange(imgArr[i][j], minVal, maxVal, ignoreVals) == True:
                if onRow == False:
                    motor.moveAbsolute(axis=2, goToPos=j*yDelta)
                motor.moveAbsolute(axis=1, goToPos=j*yDelta)
                onRow = True
                expose(imgArr[i][j])
    
def test():
    print('Success')
    