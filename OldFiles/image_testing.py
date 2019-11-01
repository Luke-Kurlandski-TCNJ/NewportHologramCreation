#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 15:42:36 2019

@author: matthewvansoelen
"""
import numpy as np #package to support array work
import matplotlib.pylab as plt #package to support image work
from PIL import Image


image = Image.open('Earth_jpeg.jpeg').convert('LA')
print ("Image Format: %s, Size: %s, Mode: %s" % (image.format, image.size, image.mode))

pixelMatrix = image.load()

with open("tab_out_file.txt", "w") as out_file:  
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            out_file.write("(%d,%d): %s" % (i, j, pixelMatrix[i,j]))
        out_file.write("\n")
        
        
image.show()