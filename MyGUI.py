# -*- coding: utf-8 -*-
"""
Master GUI class

Created on 9/22/19

@author: Luke Kurlandski
"""

import tkinter as tk #support GUI
from tkinter import filedialog #support file selection
import matplotlib.pylab as plt #support image work
import numpy as np #package to support array work

class MyGUI:
    def __init__(self, root):
        '''
        Constructor for myGUI class
        (arg1) root : the root object (tkinter object)
        '''
        
        #Set up root
        self.root = root
        self.root.attributes('-fullscreen' ,True)
        self.root.title('Hologram Creation')
        #Set up menu
        self.menu = tk.Menu(self.root)
        self.menu.add_command(label='Quit', command=self.my_destroy)
        self.root.config(menu=self.menu)
        #Set up labels and entry for film size
        tk.Label(self.root, text='Film Selection').grid(column=0, row=0, sticky=tk.W+tk.E)
        tk.Label(self.root, text='Enter width of image on film (m)').grid(column = 0, row = 1)
        self.entry_1 = tk.Entry(self.root, width = 10)
        self.entry_1.grid(column = 0, row = 2)
        tk.Label(self.root, text='Enter height of image on film (m)').grid(column = 0, row = 3)
        self.entry_2 = tk.Entry(self.root, width = 10)
        self.entry_2.grid(column = 0, row = 4)
        #Set up labels and entry for image selection
        tk.Label(self.root, text='Image Selection').grid(column=0, row=5, pady = 10, sticky=tk.W+tk.E)
        self.button_chsIMG = tk.Button(self.root, text='Select an Image', command=self.image_select)
        self.button_chsIMG.grid(column=0, pady=5, row=6)
        #Set up labels and entry for image modification
        tk.Label(self.root, text='Image Modification').grid(column = 0, pady=5, row = 7)
        tk.Label(self.root, text='Enter desired gratings in horizontal direction').grid(column = 0, row = 8)
        self.entry_3 = tk.Entry(self.root, width = 10)
        self.entry_3.grid(column = 0, row = 9)
        tk.Label(self.root, text='Enter desired gratings in vertical direction').grid(column = 0, row = 10)
        self.entry_4 = tk.Entry(self.root, width = 11)
        self.entry_4.grid(column = 0, row = 12)
        self.button_modIMG = tk.Button(self.root, text='Modify Image', command=self.mod_image)
        self.button_modIMG.grid(column=0, pady=10, row=13)
        #Runner Button
        self.button_run = tk.Button(self.root, text='Run Experiment', font=('Helvetia', '20'), command=self.run)
        self.button_run.grid(column=0, pady=20, row=14)
        
    def my_destroy(self): 
        '''
        Command off menu. Destroys current window, and breaks mainloop.
        '''
        
        self.root.destroy()  
        
    def image_select(self):
        '''
        Command off button. Allows user to select an image. Prints image to label.
        FIXME: should auto downsize the image to 400x400
        FIXME: should basically fit the image into the 400x400 space
        FIXME: possibly requires reworking entire logic, possibly using canvas
        '''
        
        self.img = tk.PhotoImage(file=filedialog.askopenfilename())
        self.label_1 = tk.Label(self.root, text='Original Image:')
        self.label_1.grid(row=0, column=1)
        self.label_img = tk.Label(self.root, image=self.img).grid(row=1, column=1, padx=100, rowspan=400, columnspan=400)
        
    def mod_image(self):
        '''
        Command off button. 
        FIXME: should apply the given modifications to self.img 
            and display the greyscale result
        FIXME: should also create a the 2-D array of greyscale values
        '''
        
        self.label_1.configure(text='Modified Image')
        self.label_img.configure(image=self.img) #FIXME
        #self.label_1.update_idletasks()
        #self.label_img.update_idletasks()
    
    def run():
        '''
        Command off button:
        FIXME: should call to another file to begin running experiment
        '''

#MainLoop
root = tk.Tk()
app = MyGUI(root)
root.mainloop()


'''
        #Set up canvas
        tk.Label(self.root, text='Original Image').grid(column=1, row=0)
        self.canvas_1 = tk.Canvas(self.root, width=400, height=400)
        self.canvas_1.grid(column=1, row=1, columnspan=10, rowspan=10, padx=100)
        
        tk.Label(self.root, text='Altered Image:').grid(column=1, row=12, pady=20)
        self.canvas_2 = tk.Canvas(self.root, width=400, height=400)
        self.canvas_2.grid(column = 1, row=13, columnspan=10, rowspan=10, padx=100)
        '''