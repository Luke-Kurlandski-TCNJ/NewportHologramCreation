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
import MasterHologramCreator #package which drives motor and shutter

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
        #Set up Frames
        self.frame_0x0 = tk.Frame(self.root) #hologram size
        self.frame_0x0.grid(row=0, column=0, pady=10)
        self.frame_1x0 = tk.Frame(self.root) #image seletion
        self.frame_1x0.grid(row=1, column=0, pady=10)
        self.frame_2x0 = tk.Frame(self.root) #image modification
        self.frame_2x0.grid(row=2, column=0, pady=10)
        self.frame_0x1 = tk.Frame(self.root) #exposure string
        self.frame_0x1.grid(column=1, row=0, pady=10)
        self.frame_0x2 = tk.Frame(self.root) #exposure values
        #self.frame_0x2.grid(column=1, row=1, pady=10)
        #Set up labels and entry for film size
        tk.Label(self.frame_0x0, text='Film Selection', font="bold").pack()
        tk.Label(self.frame_0x0, text='Enter width of image on film (m)').pack()
        self.entry_1 = tk.Entry(self.frame_0x0, width = 10)
        self.entry_1.pack()
        tk.Label(self.frame_0x0, text='Enter height of image on film (m)').pack()
        self.entry_2 = tk.Entry(self.frame_0x0, width = 10)
        self.entry_2.pack()
        #Set up labels and entry for image selection
        tk.Label(self.frame_1x0, text='Image Selection', font="bold").pack()
        self.button_chsIMG = tk.Button(self.frame_1x0, text='Select an Image', command=self.image_select)
        self.button_chsIMG.pack()
        #Set up labels and entry for image modification
        tk.Label(self.frame_2x0, text='Image Modification', font='bold').pack()
        tk.Label(self.frame_2x0, text='Enter desired gratings in horizontal direction').pack()
        self.entry_3 = tk.Entry(self.frame_2x0, width = 10)
        self.entry_3.pack()
        tk.Label(self.frame_2x0, text='Enter desired gratings in vertical direction').pack()
        self.entry_4 = tk.Entry(self.frame_2x0, width = 11)
        self.entry_4.pack()
        self.button_modIMG = tk.Button(self.frame_2x0, text='Modify Image', command=self.mod_image)
        self.button_modIMG.pack()
        #Set up exposure details
        tk.Label(self.frame_0x1, text='Exposure Details', font='bold').pack()
        tk.Label(self.frame_0x1, text='Enter the Exposure String (see help for details)').pack()
        self.button_ES = tk.Button(self.frame_0x1, text='Enter String', command=self.exposure_info)
        self.button_ES.pack()
        #Runner Button
        self.button_run = tk.Button(self.root, text='Run Experiment', font=('Helvetia', '20'), command=self.run)
        self.button_run.grid(column=0, pady=20, row=14)
        
    def exposure_info(self):
        '''
        Opens up separate windows for the user to enter information
        '''
        
        self.entry_window = tk.Toplevel(width=400, height=400)
        self.exposure_details = tk.Text(self.entry_window, width=30, height=20)
        tk.Label(self.entry_window,text='EXPOSE DETAILS').pack()
        self.exposure_details.pack()
        self.ignore_details = tk.Text(self.entry_window, width=30, height=20)
        tk.Label(self.entry_window,text='IGNORE DETAILS').pack()
        self.ignore_details.pack()
        tk.Label(self.entry_window,text='DO NOT CLOSE THIS WINDOW UNTIL RUNNING EXPERIMENT').pack()
        
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
        
        xPix = self.entry_3.get()
        yPix = self.entry_4.get()
        
        self.label_1.configure(text='Modified Image')
        self.label_img.configure(image=self.img) #FIXME
        #self.label_1.update_idletasks()
        #self.label_img.update_idletasks()
    
    def run(self):
        '''
        Runner button. Generates the information about how long to expose
            various pixel values. Calls another file.
        '''
        
        #Generate the exposure array
        lines=self.exposure_details.get('1.0','end-1c').splitlines()
        exposeArr = []
        for i in range(0,256):
            exposeArr.append(0)
        #Parse through the user's entry
        for s in lines:
            c=s.find(',')
            b=s.find(']')
            start=int(s[1:c])
            end=int(s[c+1:b])
            xLoc=s.find('x')
            if xLoc==-1:
                temp=s[b+2:len(s)]
                print(temp)
                expose_dur=float(s[b+2:len(s)])
                for i in range(start,end):
                    exposeArr[i] = expose_dur
            else:
                mult_factor=float(s[b+2:xLoc])
                for i in range(start,end):
                    exposeArr[i] = mult_factor*i
        #Override with 0s, for the ignore array
        lines2=self.ignore_details.get('1.0','end-1c').splitlines()
        for s in lines2:
            c=s.find(',')
            b=s.find(']')
            start=int(s[1:c])
            end=int(s[c+1:b])
            for i in range(start,end):
                exposeArr[i] = 0
        print(exposeArr)
        
        #Call MasterHologramCreator runner file
        '''
        width = self.entry_1.get()
        height = self.entry_2.get()
        MasterHologramCreator.run_experiment(imgArr, exposeArr,width,height)
        '''

#MainLoop
root = tk.Tk()
app = MyGUI(root)
root.mainloop()