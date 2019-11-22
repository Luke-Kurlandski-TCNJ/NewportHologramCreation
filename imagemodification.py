# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:39:14 2019

@author: Luke Kurlandski and Matthew Van Soelon
"""

#Support image processing
from PIL import Image, ImageTk

def convert_grey_downsize(image_file, newX=None, newY=None, convert=False):
    """
    Convert and downsize and image; both are optional. 
    
    Arguments:
        (arg1) image_file (string) : file path of the incomming image
        (arg2) newX (int) : new size in the x direction
        (arg3) newY (int) : new size in the y direction
        (arg4) convert (boolean) : determines whether or not to convert the image
        
    Returns:
        (ret1) image (PIL image) : modified image
    """
    
    image = Image.open(image_file)
    if(newX != None and newY != None):
        if newX <= image.width and newY <= image.height:
            image = image.resize((newX,newY))
        else:
            raise Exception('Error: your input specifies a resolution greater than the image provides')
    if convert == True:
        image = image.convert('L')
    return image

def image_for_window(max_width, max_height, img_pil, img_file):
    """
    Downsizes and converts to a TK image for printing images to a main window.
    
    Arguments:
        (arg1) max_width (int) : maximum width of image allowed in window
        (arg2) max_height (int) : maximum height of image allowed in window
        (arg3) img_pil (Pil Image) : image to print
        (arg4) img_file (string) : file of the image to print
        
    Returns:
        (ret1) img_Tk (PIL PhotoImage) : Tk image appropriately sized
    """
    
    xPix, yPix = img_pil.size
    if xPix > max_width or yPix > max_height:
        if xPix > max_width and yPix <= max_height:
            img_Tk = ImageTk.PhotoImage(convert_grey_downsize(img_file, newX=200, newY=yPix, convert=True))
        if yPix > max_height and xPix <= max_width:
            img_Tk = ImageTk.PhotoImage(convert_grey_downsize(img_file, newX=xPix, newY=200, convert=True))
        if xPix > max_width and yPix > max_height:
            img_Tk = ImageTk.PhotoImage(convert_grey_downsize(img_file, newX=200, newY=200, convert=True))
    else:
        img_Tk = ImageTk.PhotoImage(img_pil)
    return img_Tk

def get_image_array(image):
    """
    Convert image into an array.
    
    Arguments:
        (arg1) image (PIL image) : image to convert into an array
        
    Returns:
        (ret1) arr (list[list[int]]) : array representation of the image
    """
    
    arr = []
    for i in range(image.width): 
        temp = []
        arr.append(temp)
        for j in range(image.height): 
            temp.append(image.getpixel((i,j)))
    return arr

def crop_image(dimentions, image):
    """
    Crops an image according to specifications.
    
    Notes:
        Crops a rectangle of the image between a top left point and a bottom right point
    
    Arguments:
        (arg1) dimentions (string) : '(x1,y1),(x2,y2)' == (bottom right),(top left)
        (arg2) image (PIL image) : image to crop
        
    Returns:
        (ret1) new_image (PIL image) : the new, cropped image
    """
    
    # splices the dimenstions string to extract coordinates as integers
    x1 = int(dimentions[1:dimentions.find(",")])
    y1 = int(dimentions[dimentions.find(",")+1:dimentions.find(")")])
    dimentions = dimentions[dimentions.find(")")+3:]
    x2 = int(dimentions[:dimentions.find(",")])
    y2 = int(dimentions[dimentions.find(",")+1:dimentions.find(")")])
    
    # x and y conditions check to make coordinates entered are with in bounds
    # order condition checks if (x1,y1) is less than (y1,y2)
    width, height = image.size
    x_condition = x1 > 0 and x1 < width and x2 > 0 and x2 < width
    y_condition = y1 > 0 and y1 < width and y2 > 0 and y2 < width
    order_condition = x1 < x2 and y1 < y2
    #if conditions are true returns new cropped image
    if x_condition and y_condition and order_condition:
        new_image = image.crop((x1,y1,x2,y2))
        #new_image.show()
        return new_image
    elif not order_condition:
        raise Exception('The cropping dimentions are not in the correct order')
    else:
        raise Exception('The cropping dimentions outside the size of the image')
    return image

def test():
    '''
    Used for local testing.
    '''
   