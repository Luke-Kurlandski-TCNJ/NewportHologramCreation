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
        self.root.attributes('-fullscreen' ,True)
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
        self.entry_Ypix = tk.Entry(self.frame_2x0, width = 11)
        self.entry_Ypix.pack()
        self.entry_Ypix.insert(1,'100')
        self.button_modIMG = tk.Button(self.frame_2x0, text='Modify Image', command=self.mod_image)
        self.button_modIMG.pack()
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
        #Set up exposure details, time estimation
        tk.Label(self.frame_4x0, text='Exposure Details,\nTime Estimation', font='bold').pack()
        self.button_details = tk.Button(self.frame_4x0, text='Enter Details', command=self.exposure_info)
        self.button_details.pack()
        self.button_time = tk.Button(self.frame_4x0, text='Generate Time Estimation\nRun Experiment', command=self.run_time)
        self.button_time.pack()
        #Set up runner/quitter Button
        self.button_run = tk.Button(self.frame_5x0, text='Run Experiment', command=self.run)
        self.button_run.pack()
        self.button_quit = tk.Button(self.frame_5x0, text='Quit All', command=self.root.destroy)
        self.button_quit.pack()
    
    def image_select(self):
        '''
        Command off of a button. Allows user to select an image. Displays image 
            in a new window. Auto downsizes to 400x400
        '''
        
        self.file = filedialog.askopenfilename()
        self.img_pil = imagework.convert_grey_downsize(self.file, 400, 400)
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.image_orig_window = tk.Toplevel()
        self.image_orig_window.title('Original Image')
        tk.Label(self.image_orig_window, image=self.img_tk).pack()
        
    def mod_image(self):
        '''
        Command off of a button. Modifies the image into greyscale. Downsizes. 
            Displays image and the image as an array.
        '''
        
        #Acquire width and height of image
        try:
            xPix = int(self.entry_Xpix.get())
            yPix = int(self.entry_Ypix.get())
        except:
            xPix = self.img_pil.width
            yPix = self.img_pil.height
        #Modify self.img_tk and update on new window
        self.img_pil = imagework.convert_grey_downsize(self.file, xPix, yPix, True)
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.image_mod_window = tk.Toplevel()
        self.image_mod_window.title('Modified Image')
        tk.Label(self.image_mod_window, image=self.img_tk).pack()
        #Configure array window, display, and scrollbars
        self.array_window = tk.Toplevel(self.root)
        tk.Label(self.array_window, text='Your Image as an Array (white=0, black=255)').pack(side=tk.TOP)
        self.scrollbar_y = tk.Scrollbar(self.array_window)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_x = tk.Scrollbar(self.array_window, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_arr = tk.Text(self.array_window, yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set, width=xPix*4, height=yPix, wrap=tk.NONE)
        self.text_arr.pack()
        self.scrollbar_y.configure(command=self.text_arr.yview)
        self.scrollbar_x.configure(command=self.text_arr.xview)
        #Print the array to screen
        self.img_as_array = imagework.get_image_array(self.img_pil)
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
        
    def exposure_info(self):
        '''
        Opens up separate windows for the user to enter information.
        '''
        
        self.entry_window = tk.Toplevel(width=400, height=400)
        tk.Label(self.entry_window,text='EXPOSE DETAILS').pack()
        self.exposure_details = tk.Text(self.entry_window, width=30, height=20)
        self.exposure_details.pack()
        self.exposure_details.insert(tk.END, '[0,50]:1\n[50,100]:1.5\n[100,150]:2\n[150,200]:2.5\n[200,255]:3')
        tk.Label(self.entry_window,text='IGNORE DETAILS').pack()
        self.ignore_details = tk.Text(self.entry_window, width=30, height=20)
        self.ignore_details.pack()
        self.ignore_details.insert(tk.END, '[0,0]\n[255,255]')
        tk.Label(self.entry_window,text='DO NOT CLOSE THIS WINDOW UNTIL RUNNING EXPERIMENT').pack()
    
    def run_time(self):
        '''
        Generates the information about how long to expose pixel values. 
            Creates a run time estimation. Prompts the user to start the
            experiment.
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
        #Generate and display the run time estimation
        expose_time = 0
        width = len(self.img_as_array)
        height = len(self.img_as_array[0])
        for i in range (height):
            visited_row = False
            farthest_x = 0
            for j in range (width):
                add = self.exposeArr[self.img_as_array[j][i]]
                if add != 0:
                    visited_row = True
                    farthest_x = j
                    expose_time = expose_time + add
            if visited_row == True:
                expose_time = expose_time + ((farthest_x / width) / .001)
        self.time_window = tk.Toplevel(self.root)
        tk.Label(self.time_window, text = 'Rough Time Estimation: \n' 
                 + str(expose_time/3600) + ' hours').pack()
        #Set up abort button
        self.button_abort = tk.Button(self.time_window, text='Abort Experiment', command=self.dont_run)
        self.button_abort.pack()
    
    def dont_run(self):
        self.time_window.destroy()
        self.entry_window.destroy()
        self.array_window.destroy()
        self.image_mod_window.destroy()
        self.image_orig_window.destroy()
    
    def run(self):
        '''
        Command off of a button. Calls run_experiment method of movement.py
        '''
        
        #Call movement.py runner file
        width = float(self.entry_width.get())
        height = float(self.entry_height.get())
        port_mot = self.entry_port_mot.get()
        port_shut = self.entry_port_shut.get()
        movement.run_experiment(self.img_as_array, self.exposeArr, port_mot, port_shut, width, height)
        

#MainLoop
root = tk.Tk()
app = MyGUI(root)
root.mainloop()