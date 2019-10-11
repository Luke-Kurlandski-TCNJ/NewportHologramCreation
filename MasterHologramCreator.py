# -*- coding: utf-8 -*-
"""
Master program to create holograms.

Created on 9/18/19

@author: Luke Kurlandski
"""

from MotorControl import MotorControl #file with MotorControl class
from ShutterControl import ShutterControl
from PIL import Image #package to support image work
import sys
import time
import atexit #package to support smooth closure of serial ports
        
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
        
def run_experiment(img_as_arr, expose_arr, port_motor, port_shutter, width=.02, height=.02):    
    '''
    Controls the motion of stages and shutter
        Arguments:
            (arg1) img_as_arr (list[list[int]] : image as an 2-D greyscale array
            (arg2) expose_arr (list[int]) : instructions on how long to expose
            (arg3) port_motor (string) : serial port for the motor
            (arg4) port_shutter (string) : serial port for the shutter
            (arg5) width (float) : desired width of the hologram
            (arg6) height (float) : desired height of the hologram
    '''
    
    try:
        #Number of pixels in image, size of image on hologram, distance each movement
        xPix = len(img_as_arr) 
        yPix = len(img_as_arr[0]) 
        width = width
        height = height
        xDelta = 1.0 * width / xPix
        yDelta = 1.0 * height / yPix
        #Motor, Shutter control
        shutter = ShutterControl(port = port_shutter)
        motor = MotorControl(port = port_motor)
        motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
        motor.configureAxis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
        #Read greyscale image, move as needed
        for i in range(0, yPix):
            onRow = False #indicates the motor is already at a row
            for j in range(0, xPix):
                cur_pix = img_as_arr[j][i]
                if expose_arr[cur_pix] != 0:
                    if onRow == False:
                        motor.moveAbsolute(axis=2, goToPos=i*yDelta*1000)
                    motor.moveAbsolute(axis=1, goToPos=j*xDelta*1000)
                    onRow = True
                    shutter.toggle_shutter(expose_arr[cur_pix])
    except:
        print('An error has occured:', e)
    finally:
        print('Closing the shutter and all serial ports')
        shutter.ser.close()
        motor.ser.close()
        shutter.ser.close()
    
def test():
    '''
    Test the functionality of the driving program
    '''
    
    img_as_arr = []
    for i in range(0,16):
        temp = []
        img_as_arr.append(temp)
        for j in range(0,16):
            temp.append((j+1)%2)
    expose_arr = []
    for i in range(0,256):
        expose_arr.append(i) 
    print(img_as_arr)
    run_experiment(img_as_arr, expose_arr, port_motor='COM10', port_shutter='COM11')   

test()
               