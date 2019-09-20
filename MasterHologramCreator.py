# -*- coding: utf-8 -*-
"""
Master program to create holograms.

Created on 9/18/19

@author: Luke Kurlandski
"""

import numpy as np #package to support array work
import matplotlib.pylab as plt #package to support image work
from MotorControl import MotorControl #file with MotorControl class

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

def inRange(pixVal):
    '''
    Determines whether or not the pixel value causes exposure.
    (arg1) pixVal : the value of the pixel
    (return) True/False : whether or not to expose
    '''
    
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
        
    
#Image selection and conversion
imageFile = "Earth.png"
image = plt.imread(imageFile)
imgArr = imageToGreyList(image)

#Number of pixels in image, size of image on hologram, distance each movement
xPixel = len(imgArr)
yPixel = len(imgArr[0])
xLength = .01
yLength = .01
xDelta = xLength / xPixel
yDelta = yLength / yPixel

#Motor control
motor = MotorControl(port = 'COM7')
motor.configureAxis(axis=1, velocity=1, acceleration=4, moveHome=True)

#Read greyscale image, move as needed
for i in range(0, xPixel):
    onRow = False #indicates the motor is already at a row
    for j in range(0, yPixel):
        if inRange(imgArr[i][j]) == True:
            if onRow == False:
                motor.moveAbsolute(axis=2, goToPos=j*yDelta)
            motor.moveAbsolute(axis=1, goToPos=j*yDelta)
            onRow = True
            expose(imgArr[i][j])
    

