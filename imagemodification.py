# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:39:14 2019

@author: Luke Kurlandski and Matthew Van Soelon
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
        if(newX > image.width or newY > image.height):
            raise Exception
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

def crop_image(dimentions,image):
    '''
    Recieves an image and dimensions,
    outputs a new image cropped to new dimenstions
    (arg1) dimentions : string entered as "(x1,y1),(x2,y2)" == (topLeft),(bottomRight)
    (arg2) image : image to be cropped (PIL image)
    '''
    # splices the dimenstions string to extract coordinates as integers
    x1 = int(dimentions[1:dimentions.find(",")])
    y1 = int(dimentions[dimentions.find(",")+1:dimentions.find(")")])
    dimentions = dimentions[dimentions.find(")")+3:]
    x2 = int(dimentions[:dimentions.find(",")])
    y2 = int(dimentions[dimentions.find(",")+1:dimentions.find(")")])
    
    # x and y conditions check to make coordinates entered are with in bounds
    # order condition checks if (x1,y1) is less than (y1,y2)
    width, height = image.size
    print(image.size)
    x_condition = x1 > 0 and x1 < width and x2 > 0 and x2 < width
    y_condition = y1 > 0 and y1 < width and y2 > 0 and y2 < width
    order_condition = x1 < x2 and y1 < y2

    #if conditions are true returns new cropped image
    #otherwise returns issue with dimentions string
    if x_condition and y_condition and order_condition:
        new_image = image.crop((x1,y1,x2,y2))
        new_image.show()
        return new_image
    elif not order_condition:
        print("The dimentions entered are out of order")
    else:
        print("The dimentions entered are not with-in the bounds of the image")
    return image


def test():
    '''
    Used for local testing.
    '''
   