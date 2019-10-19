# -*- coding: utf-8 -*-
"""
Master GUI class

Created on 9/22/19

@author: Luke Kurlandski 
"""
'''

Goals:
    reduce name pollution, remove self prefix if possible, clean up name convention

'''

import tkinter as tk #support GUI
from tkinter import filedialog #support file selection
from PIL import ImageTk #package to support Pil and Tk image compatability
from datetime import datetime
from datetime import timedelta
import time
#import movement #package which drives motor and shutter
import imagework #package to support image modification

class MyGUI:
    def __init__(self, root):
        '''
        Constructor for myGUI class
        (arg1) root : the root object (tkinter object)
        '''
        
        #Set up root
        self.root = root
        #self.root.attributes('-fullscreen' ,True)
        self.root.geometry('1200x600')
        self.root.title('Main Hologram Creation')
        #Set up menu
        self.menu = tk.Menu(self.root)
        self.menu.add_command(label='Quit', command=self.root.destroy)
        self.root.config(menu=self.menu)
        #Set up Frames
        self.frame_0x0 = tk.Frame(self.root) #hologram size
        self.frame_0x0.grid(row=0, column=0, pady=10)
        self.frame_1x0 = tk.Frame(self.root) #image seletion
        self.frame_1x0.grid(row=1, column=0, pady=10)
        self.frame_2x0 = tk.Frame(self.root) #image modification
        self.frame_2x0.grid(row=2, column=0, pady=10)
        self.frame_3x0 = tk.Frame(self.root) #serial port selection
        self.frame_3x0.grid(row=3, column=0, pady=10)
        self.frame_4x0 = tk.Frame(self.root) #exposure details, time estimation
        self.frame_4x0.grid(row=4, column=0, pady=10)
        self.frame_5x0 = tk.Frame(self.root) #run button
        self.frame_5x0.grid(row=5, column=0, pady=10)
        self.frame_0x1 = tk.Frame(self.root) #image original
        self.frame_0x1.grid(row=0, column=1, pady=10, rowspan=200, columnspan=200, sticky='NW')
        self.frame_1x1 = tk.Frame(self.root) #image modified
        self.frame_1x1.grid(row=1, column=1, pady=10, rowspan=200, columnspan=200, sticky='W')
        self.frame_0x2 = tk.Frame(self.root) #exposure information
        self.frame_0x2.grid(row=0, column=2, padx=250, rowspan=200, columnspan=200, sticky='NW')
        self.frame_0x3 = tk.Frame(self.root) #Run-time information
        self.frame_0x3.grid(row=0, column=3, padx=475, pady=10, rowspan=200, columnspan=200, sticky='NW')
        #Set up labels and entry for film size
        tk.Label(self.frame_0x0, text='Film Selection', font="bold").pack()
        tk.Label(self.frame_0x0, text='Enter width of image on film (m)').pack()
        self.entry_width = tk.Entry(self.frame_0x0, width = 10, text=.02)
        self.entry_width.pack()
        self.entry_width.insert(1,'0.02')
        tk.Label(self.frame_0x0, text='Enter height of image on film (m)').pack()
        self.entry_height = tk.Entry(self.frame_0x0, width = 10)
        self.entry_height.pack()
        self.entry_height.insert(1,'0.02')
        #Set up labels and entry for image selection
        tk.Label(self.frame_1x0, text='Image Selection', font="bold").pack()
        self.button_chsIMG = tk.Button(self.frame_1x0, text='Select an Image', command=self.image_select)
        self.button_chsIMG.pack()
        #Set up labels and entry for image modification
        tk.Label(self.frame_2x0, text='Image Modification', font='bold').pack()
        tk.Label(self.frame_2x0, text='Enter desired gratings in horizontal direction').pack()
        self.entry_Xpix = tk.Entry(self.frame_2x0, width = 10)
        self.entry_Xpix.pack()
        self.entry_Xpix.insert(1,'100')
        tk.Label(self.frame_2x0, text='Enter desired gratings in vertical direction').pack()
        self.entry_Ypix = tk.Entry(self.frame_2x0, width = 10)
        self.entry_Ypix.pack()
        self.entry_Ypix.insert(1,'100')
        tk.Label(self.frame_2x0,text='Optional Cropping (see \'Help\')').pack()
        self.entry_crop = tk.Entry(self.frame_2x0, width = 10)
        self.entry_crop.pack()
        self.entry_crop.insert(1, 'none')
        #Set up serial ports 
        tk.Label(self.frame_3x0, text='Serial Ports', font='bold').pack()
        tk.Label(self.frame_3x0, text='Enter the serial port for the motor').pack()
        self.entry_port_mot = tk.Entry(self.frame_3x0, width = 10)
        self.entry_port_mot.pack()
        self.entry_port_mot.insert(1, 'COMx')
        tk.Label(self.frame_3x0, text='Enter the serial port for the shutter').pack()
        self.entry_port_shut = tk.Entry(self.frame_3x0, width = 10)
        self.entry_port_shut.pack()
        self.entry_port_shut.insert(1, 'COMx')
        #Set up the default images
        self.label_img_lbl = tk.Label(self.frame_0x1, text = 'Sample Image')
        self.label_img_lbl.pack()
        self.img_pil = imagework.convert_grey_downsize('DefaultImage.png')
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.label_img = tk.Label(self.frame_0x1, image=self.img_tk)
        self.label_img.pack()
        self.img_pil_mod = imagework.convert_grey_downsize('DefaultImage.png', convert=True)
        self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        self.label_img_lbl_mod = tk.Label(self.frame_1x1, text = 'Modified Sample Image')
        self.label_img_lbl_mod.pack()
        self.label_img_mod = tk.Label(self.frame_1x1, image=self.img_tk_mod)
        self.label_img_mod.pack()
        #Set up the exposure entry information
        tk.Label(self.frame_0x2, text='Exposure Control', font="bold").pack()
        tk.Label(self.frame_0x2,text='Exposure details (see \'Help\')').pack()
        self.exposure_details = tk.Text(self.frame_0x2, width=20, height=15)
        self.exposure_details.pack(side='top')
        self.exposure_details.insert(tk.END, '[0,50]:1\n[50,100]:1.5\n[100,150]:2\n[150,200]:2.5\n[200,255]:3')
        tk.Label(self.frame_0x2,text='Ignore details (see \'Help\')').pack()
        self.ignore_details = tk.Text(self.frame_0x2, width=20, height=15)
        self.ignore_details.pack(side='top')
        self.ignore_details.insert(tk.END, '[0,0]\n[255,255]')
        #Set up run-time information
        tk.Label(self.frame_0x3, text='Experiment Control', font="bold").pack()
        self.button_update = tk.Button(self.frame_0x3, text = 'Update all Information/\nApply Modifications/\nGenerate Runtime', command=self.update_all)
        self.button_update.pack()
        #Set up timing information
        self.label_start_time = tk.Label(self.frame_0x3, text='Start Time: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_start_time.pack()
        self.label_end_time = tk.Label(self.frame_0x3, text='Experiment End Time: In Progress')
        self.label_end_time.pack()
        self.label_end_time_est = tk.Label(self.frame_0x3, text='End Time Estimate: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_end_time_est.pack()
        #Set up run button
        self.button_run = tk.Button(self.frame_0x3, text = 'Run Experiment', command=self.run_experiment)
        self.button_run.pack()
        self.button_pause = tk.Button(self.frame_0x3, text = 'Pause Experiment')
        self.button_pause.pack()
        self.button_abort = tk.Button(self.frame_0x3, text = 'Abort Experiment')
        self.button_abort.pack()
        
        
    def image_select(self):
        '''
        Command off of a button. Allows user to select an image. Displays image 
            in a new window. Auto downsizes to displayed image to 200x200
        '''
        
        self.file = filedialog.askopenfilename()
        self.img_pil = imagework.convert_grey_downsize(self.file, newX=None, newY=None, convert=False)
        self.img_tk = ImageTk.PhotoImage(imagework.convert_grey_downsize(self.file, newX=200, newY=200, convert=False))
        self.label_img.configure(image=self.img_tk)
        self.label_img_lbl.configure(text='Original Image')
    
    def update_all(self):
        '''
        Calls other methods to modify the image, display the array, get the
            exposure data, generate a run time estimation.
        '''
        
        xPix, yPix = self.modify_image()
        self.image_as_array(xPix, yPix)
        self.generate_exposure_details()
        width = float(self.entry_width.get())
        height = float(self.entry_height.get())
        self.time_estimation(xPix, yPix, width, height)
        
    def modify_image(self):
        '''
        Modifies the image. Updates on Screen.
            Returns:
                (ret1) xPix (int) : modified image, number of pixels horizontally
                (ret2) yPix (int) : modified image, number rof pixels vertically
        '''
        
        try:
            xPix = int(self.entry_Xpix.get())
            yPix = int(self.entry_Ypix.get())
            self.img_pil_mod = imagework.convert_grey_downsize(self.file, xPix, yPix, True)
            self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
            self.label_img_mod.configure(image=self.img_tk_mod)
            self.label_img_lbl_mod.configure(text='Modified Image')
        except:
            xPix = self.img_pil.width
            yPix = self.img_pil.height
            print('Using default image size')
        return xPix, yPix
    
    def image_as_array(self, xPix, yPix):
        '''
        Converts the image into an array. Displays array in a new window.
            Arguments:
                (arg1) xPix (int) : number of pixels horizontally
                (ret2) yPix (int) : number rof pixels vertically
        '''
        
        #Configure array window, display, and scrollbars
        self.array_window = tk.Toplevel(self.root)
        tk.Label(self.array_window, text='Your Image as an Array').pack(side=tk.TOP)
        self.scrollbar_y = tk.Scrollbar(self.array_window)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = tk.Scrollbar(self.array_window, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_arr = tk.Text(self.array_window, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set, width=xPix*4, height=yPix, wrap=tk.NONE)
        self.text_arr.pack()
        self.scrollbar_y.configure(command=self.text_arr.yview)
        self.scrollbar_x.configure(command=self.text_arr.xview)
        #Print the array to screen
        self.img_as_array = imagework.get_image_array(self.img_pil_mod)
        for i in self.img_as_array:
            for j in i:
                spaces = '   '
                if j > 9:
                    spaces = '  '
                if j > 99:
                    spaces = ' '
                self.text_arr.insert(tk.END, str(j)+spaces)
            self.text_arr.insert(tk.END,'\n')
        self.array_window.configure(width=100, height=100)
    
    def generate_exposure_details(self):
        '''
        Generate the exposure and ignore arrays.
        '''
        
        #Generate the exposure array
        lines=self.exposure_details.get('1.0','end-1c').splitlines()
        self.exposeArr = []
        for i in range(0,256):
            self.exposeArr.append(0)
        #Parse through the user's entry based upon comma and bracket location
        for s in lines:
            c=s.find(',')
            b=s.find(']')
            start=int(s[1:c])
            end=int(s[c+1:b])
            xLoc=s.find('x')
            if xLoc==-1:
                expose_dur=float(s[b+2:len(s)])
                for i in range(start,end):
                    self.exposeArr[i] = expose_dur
            else:
                mult_factor=float(s[b+2:xLoc])
                for i in range(start,end):
                    self.exposeArr[i] = mult_factor*i
        #Override with 0s, for the ignore array
        lines2=self.ignore_details.get('1.0','end-1c').splitlines()
        #Parse through the user's entry based upon comma and bracket location
        for s in lines2:
            c=s.find(',')
            b=s.find(']')
            start=int(s[1:c])
            end=int(s[c+1:b])
            for i in range(start,end):
                self.exposeArr[i] = 0
            
    def time_estimation(self, xPix, yPix, width, height):
        '''
        Creates a rough time estimation for the experiment based upon movement 
            in the x and y directions.
        '''
        
        expose_time = 0
        for i in range (yPix):
            visited_row = False
            farthest_x = 0
            for j in range (xPix):
                add = self.exposeArr[self.img_as_array[j][i]]
                if add != 0:
                    visited_row = True
                    farthest_x = j
                    expose_time = expose_time + add
            if visited_row == True:
                expose_time += ((farthest_x / xPix) * width / .001)
        expose_time += height / .001
        exp = timedelta(seconds = expose_time)
        self.label_end_time_est.configure(text='Estimated End Time: ' + (datetime.now() + exp).strftime('%H:%M:%S -- %d/%m/%Y'))
    
    def dont_run(self):
        self.time_window.destroy()
        self.entry_window.destroy()
        self.array_window.destroy()
        self.image_mod_window.destroy()
        self.image_orig_window.destroy()
    
    def run_experiment(self):
        '''
        Calls run_experiment method of movement.py to run the experiment
        '''
        
        self.label_start_time.configure(text = 'Start Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        #Call movement.py runner file
        width = float(self.entry_width.get())
        height = float(self.entry_height.get())
        port_mot = self.entry_port_mot.get()
        port_shut = self.entry_port_shut.get()
        movement.run_experiment(self.img_as_array, self.exposeArr, port_mot, port_shut, width, height)
        self.label_end_time.configure(text = 'Experiment End Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
            

#MainLoop
root = tk.Tk()
app = MyGUI(root)
root.mainloop()