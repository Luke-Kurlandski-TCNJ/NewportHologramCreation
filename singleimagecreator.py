# -*- coding: utf-8 -*-
"""
Master GUI class

Created on 9/22/19

@author: Luke Kurlandski
"""

import tkinter as tk #GUI library
from tkinter import filedialog #file selection of image
from PIL import ImageTk #Pil and Tk image compatability
from datetime import datetime #Assist with displaying run time
from datetime import timedelta #Assist with displaying run time
import time #Assist with pausing and waiting
import imagemodification #package to support image modification
from serialcontrol import Motor, Shutter #Allows communication with machinery
from generichologramcreator import GenericImageCreator #Parent Class

class SingleImageCreator(GenericImageCreator):
    """
    Create a single dot matrix image on a hologram.
    
    Notes:
        Child class, derives from GenericImageCreator
    """
    
    def __init__(self, root):
        """
        Constructor for creating a single image.
            
        Arguments:
            (arg1) root (Tk) : the root window
        """
        
        #Set up the main window (700x650), frames[y][x]
        super().__init__(root, 700, 650, 'Single Hologram Creation')
        self.frames = self.set_up_frames(self.root, 4, 5) #x, y
        self.frames[0][1].grid(row=0, column=1, pady=10, rowspan=200, columnspan=200, sticky='NW')
        self.frames[1][1].grid(row=1, column=1, pady=10, rowspan=200, columnspan=200, sticky='W')
        self.frames[0][2].grid(row=0, column=2, pady=10, rowspan=200, columnspan=200, sticky='NW', padx=250)
        
        #Set up main menu
        self.menu = self.set_up_menu(self.root)
        self.menu.add_command(label='Motor Serial', command=lambda: self.setup_serial_port('Motor'))
        self.menu.add_command(label='Shutter Serial', command=lambda: self.setup_serial_port('Shutter'))
        submenu_help = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=submenu_help)
        submenu_help.add_command(label='General Instructions', command=lambda: self.help_window(self.root, 'General Instructions'))
        submenu_help.add_command(label='Film Information', command=lambda: self.main_help(self.root, 'Film Information'))
        submenu_help.add_command(label='Image Selection', command=lambda: self.main_help(self.root, 'Image Selection'))
        submenu_help.add_command(label='Image Modification', command=lambda: self.main_help(self.root, 'Image Modification'))
        submenu_help.add_command(label='Exposure Information', command=lambda: self.main_help(self.root, 'Exposure Information'))
        submenu_help.add_command(label='Prepare Experiment', command=lambda: self.main_help(self.root, 'Prepare Experiment'))
        submenu_help.add_command(label='Run Experiment', command=lambda: self.main_help(self.root, 'Run Experiment'))
        
        #Set up Film Size
        tk.Label(self.frames[0][0], text='1) Film Information', font="bold").pack()
        tk.Label(self.frames[0][0], text='Image Width on Film (m)').pack()
        self.entry_width = tk.Entry(self.frames[0][0], width = 10)
        self.entry_width.pack()
        tk.Label(self.frames[0][0], text='Image Height on Film (m)').pack()
        self.entry_height = tk.Entry(self.frames[0][0], width = 10)
        self.entry_height.pack()
        
        #Set up Image Selection
        tk.Label(self.frames[1][0], text='2) Image Selection', font="bold").pack()
        self.button_chsIMG = tk.Button(self.frames[1][0], text='Select an Image', command=self.image_select)
        self.button_chsIMG.pack()
        
        #Set up Image Modification
        tk.Label(self.frames[2][0], text='3) Image Modification', font='bold').pack()
        tk.Label(self.frames[2][0], text='Desired Horizontal Gratings').pack()
        self.entry_Xpix = tk.Entry(self.frames[2][0], width = 10)
        self.entry_Xpix.pack()
        tk.Label(self.frames[2][0], text='Desired Vertical Gratings').pack()
        self.entry_Ypix = tk.Entry(self.frames[2][0], width = 10)
        self.entry_Ypix.pack()
        tk.Label(self.frames[2][0],text='Optional Cropping').pack()
        self.entry_crop = tk.Entry(self.frames[2][0], width = 10)
        self.entry_crop.pack()
        
        #Set up Default Images
        self.label_img_lbl = tk.Label(self.frames[0][1], text = 'Sample Image')
        self.label_img_lbl.pack()
        self.file = 'DefaultImage.png'
        self.img_pil = imagemodification.convert_grey_downsize('DefaultImage.png')
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.label_img = tk.Label(self.frames[0][1], image=self.img_tk)
        self.label_img.pack()
        self.img_pil_mod = imagemodification.convert_grey_downsize('DefaultImage.png', convert=True)
        self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        self.label_img_lbl_mod = tk.Label(self.frames[1][1], text = 'Modified Sample Image')
        self.label_img_lbl_mod.pack()
        self.label_img_mod = tk.Label(self.frames[1][1], image=self.img_tk_mod)
        self.label_img_mod.pack()
        
        #Set up Exposure Information
        tk.Label(self.frames[0][2], text='4) Exposure Information', font="bold").pack()
        sub_frame_1 = tk.Frame(self.frames[0][2])
        sub_frame_1.pack()
        sub_frame_2 = tk.Frame(self.frames[0][2])
        sub_frame_2.pack()
        tk.Label(sub_frame_1, text='Exposure Details').grid(row=0, column=0)
        self.exposure_details = tk.Text(sub_frame_1, width=20, height=15)
        self.exposure_details.grid(row=1, column=0)
        self.apply_scrollbars(sub_frame_1, self.exposure_details, x=True, y=True, yrow=1, ycol=1, xrow=2, xcol=0)
        tk.Label(sub_frame_2, text='Ignore Details').grid(row=0, column=0)
        self.ignore_details = tk.Text(sub_frame_2, width=20, height=15)
        self.ignore_details.grid(row=1, column=0)
        self.apply_scrollbars(sub_frame_2, self.ignore_details, x=True, y=True, yrow=1, ycol=1, xrow=2, xcol=0)
        
        #Set up Initialize Experiment
        tk.Label(self.frames[3][0], text='5) Initialize Experiment', font="bold").pack()
        self.button_update = tk.Button(self.frames[3][0], text = 'Update all Information', command=self.get_data)
        self.button_update.pack()
        self.button_update = tk.Button(self.frames[3][0], text = 'Run Experiment', 
            command=lambda: self.run_experiment(self.hologram_width, self.hologram_height, 
                self.xPix, self.yPix, self.config_shutter, self.config_motor, self.img_as_arr, 
                    self.exposure_arr))
        self.button_update.pack()
        
        #Set up Running Experiment
        tk.Label(self.frames[4][0], text='6) Running Experiment', font="bold").pack()
        self.listbox = tk.Listbox(self.frames[4][0], height=3)
        self.listbox.pack()
        self.listbox.insert(1, "Run")
        self.listbox.insert(2, "Pause")
        self.listbox.insert(3, "Abort")
        self.listbox.activate(1)
        
        #Timing and location information
        self.label_start_time = tk.Label(self.frames[4][0], text='Start Time: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_start_time.pack()
        self.label_end_time = tk.Label(self.frames[4][0], text='Experiment End Time: In Progress')
        self.label_end_time.pack()
        self.label_end_time_est = tk.Label(self.frames[4][0], text='End Time Estimate: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_end_time_est.pack()
        self.label_position = tk.Label(self.frames[4][0], text='Current Pixel (x,y): (x,y)')
        self.label_position.pack() 
        
        #Fill with values from previous experiment
        with open('Prior Experiment Data Single Image Creation.txt', 'r') as file:
            try:
                lines = file.readlines()
                print(lines)
                self.entry_width.insert(1, lines[1].rstrip())
                self.entry_height.insert(1, lines[3].rstrip())
                self.entry_Xpix.insert(1, lines[5].rstrip())
                self.entry_Ypix.insert(1, lines[7].rstrip())
                self.entry_crop.insert(1, lines[9].rstrip())
                cont = 11
                for i in range(11, lines.index('Ignore Lines\n')):
                    self.exposure_details.insert(tk.END, lines[i].rstrip() + '\n')
                    cont = i
                for j in range(cont+2, len(lines)):
                    self.ignore_details.insert(tk.END, lines[j].rstrip() + '\n')
            except:
                print('Something is wrong with the \'Prior Experiment Data Single Image Creation.txt\' file')
    
    def image_select(self):
        """
        Get image from user, downsize automatically, and display.
        """
        
        self.file = filedialog.askopenfilename()
        self.img_pil = imagemodification.convert_grey_downsize(self.file, newX=None, newY=None, convert=False)
        self.img_tk = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=200, newY=200, convert=False))
        self.label_img.configure(image=self.img_tk)
        self.label_img_lbl.configure(text='Original Image')
        self.text_communication.insert(tk.END, 'Your image is: ' + str(self.file) + '\n')
    
    def get_data(self):
        """
        Gets data from main window and drives next processes in program.
        
        Notes:
            Provides basic feedback to user if processes go wrong.
        """
        
        #Get hologram size, image modifcations
        self.hologram_width = float(self.entry_width.get())
        self.hologram_height = float(self.entry_height.get())
        try: 
            self.xPix = int(self.entry_Xpix.get())
        except:
            self.xPix = self.img_pil_mod.width
        try:
            self.yPix = int(self.entry_Ypix.get())
        except:
            self.yPix = self.img_pil_mod.height
        
        #Get exposure/ignore details and serial configurations
        cropping = self.entry_crop.get()
        self.exposure_lines = self.exposure_details.get('1.0','end-1c').splitlines()
        self.ignore_lines = self.ignore_details.get('1.0','end-1c').splitlines()
        
        #Store all the user data in a file
        subjects = ['HologramWidth', 'Hologram Height', 'xPix', 'yPix', 'Cropping', 
            'Exposure Lines', 'Ignore Lines']
        datas = [self.hologram_width, self.hologram_height, self.xPix, self.yPix, 
            cropping, self.exposure_details.get('1.0','end-1c'), self.ignore_details.get('1.0','end-1c')]
        self.store_previous_data('Prior Experiment Data Single Image Creation.txt', subjects, datas)
        
        #Work with other methods to process user data
        try:
            self.config_shutter = self.get_serial_config('Shutter')
            self.config_motor = self.get_serial_config('Motor')
        except Exception as e:
            message = 'Something went wrong with getting serial information.\n'
            message += str(e)
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
        
        #Modify the image
        try:
            self.modify_image(self.xPix, self.yPix, cropping)
        except Exception as e:
            message = 'Something went wrong with the image modification process.\n'
            message += str(e)
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
        
        #Convert the image into an array
        try:
            self.img_as_arr = self.image_as_array(self.root, self.img_pil_mod, 'Modified Image')
        except Exception as e:
            message = 'Something went wrong with turning the image into an array.\n'
            message += str(e)
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
        
        #Generate exposure arrays based upon user's entry
        try:
            self.exposure_arr = self.generate_exposure_details(self.exposure_lines, self.ignore_lines)
        except Exception as e:
            message = 'Something went wrong with the exposure details.\nCheck your input.\n'
            message += str(e)
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
        
        #Generate and print a time estimation
        run_time = self.time_estimation(self.img_as_arr, self.exposure_arr, self.xPix, 
            self.yPix, self.hologram_width,self. hologram_height)
        exp = timedelta(seconds = run_time)
        self.label_end_time_est.configure(text='Estimated End Time: ' + 
                    (datetime.now() + exp).strftime('%H:%M:%S -- %d/%m/%Y'))
        
    def modify_image(self, xPix, yPix, cropping):
        """
        Modify the image. Update on main window.
        
        Arguments:
            (arg1) xPix (int) : number of pixels to downsize horizontally
            (arg2) yPix (int) : number of pixels to downsize vertically
            (arg3) cropping (string) : formatted string with croppng details
        """
        
        #Modify the image
        self.img_pil_mod = imagemodification.convert_grey_downsize(self.file, xPix, yPix, True)
        self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        if cropping.capitalize() != 'none'.capitalize() and cropping != '':
            self.img_pil_mod = imagemodification.crop_image(cropping, self.img_pil_mod)
            self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        #The main window cannot handle images larger than 200x200
        if xPix > 200 and yPix <= 200:
            img_temp = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=200, newY=yPix, convert=True))
        elif yPix > 200 and xPix <= 200:
            img_temp = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=xPix, newY=200, convert=True))
        elif xPix > 200 and yPix > 200:
            img_temp = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=xPix, newY=200, convert=True))
        else:
            img_temp = self.img_tk_mod
        #Update on screen
        self.label_img_mod.configure(image=img_temp)
        self.label_img_lbl_mod.configure(text='Modified Image')
            
    def time_estimation(self, img_as_arr, exposure_arr, xPix, yPix, hologram_width, hologram_height):
        """
        Create a rough time estimation for the length of the experiment.
        
        Arguments:
            (arg1) img_as_arr (list[list[int]]) : the image converted into an array
            (arg2) exposure_arr (list[int]) : mapping of pixel values to exposure time
            (arg3) xPix (int) : number of pixels in horizontal direction
            (arg4) yPix (int) : number of pixels in vertical direction
            (arg5) hologram_width (float) : width of the hologram
            (arg6) hologram_height (float) : height of the hologram
            
        Returns:
            (ret1) run_time (float) : duration of experiment in seconds
        """
        
        run_time = 0
        #Loop through every potential grating on hologram
        for i in range (yPix):
            visited_row = False
            farthest_x = 0
            #Calculate exposure time
            for j in range (xPix):
                add = exposure_arr[img_as_arr[j][i]]
                if add != 0:
                    visited_row = True
                    farthest_x = j
                    run_time += add
            #Calculate travel time in x direction
            if visited_row == True:
                run_time += ((farthest_x / xPix) * hologram_width / .001)
        #Calculate travel time in x direction
        run_time += hologram_height / .001
        return run_time
    
    def run_experiment(self, hologram_width, hologram_height, xPix, yPix, config_shutter, config_motor, img_as_arr, exposure_arr):
        """
        Run the experiment by moving the motor and opening and closing the shutter.
        
        Arguments:
            (arg1) hologram_width (float) : width of the hologram
            (arg2) hologram_height (float) : height of the hologram
            (arg3) xPix (int) : number of pixels in horizontal direction
            (arg4) yPix (int) : number of pixels in vertical direction
            (arg5) config_shutter (tuple) : serial configurations for the shutter
            (arg6) config_motor (tuple) : serial configurations for the motor
            (arg7) img_as_arr (list[list[int]]) : the image converted into an array
            (arg8) exposure_arr (list[int]) : mapping of pixel values to exposure time
        """
        
        self.listbox.activate(0)
        
        #Capture the screen?
            
        #Record the start time of the experiment and compute dot separation
        self.label_start_time.configure(text = 'Start Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.listbox.activate(0)
        xDelta = 1.0 * hologram_width / xPix
        yDelta = 1.0 * hologram_height / yPix
        
        #Initialize the motor and shutter
        try:
            motor = Motor(config_motor)
            motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
            motor.configureAxis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
        except Exception as e:
            message = 'Something went wrong with setting up a connection with the motor.\n'
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
        try:
            shutter = Shutter(config_shutter)
        except Exception as e:
            message = 'Something went wrong with setting up a connection with the shutter.\n'
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
            
        #Movement and exposure procedure
        try:
            #Read greyscale image, move as needed
            for i in range(0, yPix):
                onRow = False #indicates the motor is already at a row
                for j in range(0, xPix):
                    #Handle pause or abort
                    while self.listbox.curselection != 0:
                        if self.listbox.curselection == 1:
                            time.sleep(1)
                        if self.listbox.curselection == 2:
                            raise Exception
                    #Movement and exposure
                    self.label_position.configure(text='Current Pixel (x,y): ' + str(j) + ',' + str(i))
                    cur_pix = img_as_arr[j][i]
                    if exposure_arr[cur_pix] != 0:
                        if onRow == False:
                            motor.moveAbsolute(axis=2, goToPos=i*yDelta*1000)
                        motor.moveAbsolute(axis=1, goToPos=j*xDelta*1000)
                        onRow = True
                        shutter.toggle_shutter(exposure_arr[cur_pix])
        except Exception as e:
            message = 'Something went wrong with the motion and exposure process.\n'
            self.text_communication.insert(tk.END, '\n' + message + '\n' + str(e) + '\n')
            return
        finally:
            #Ensure all serial ports are closed ect
            message = 'Closing the serial port connections with the motor and shutter\n'
            self.text_communication.insert(tk.END, '\n' + message + '\n')
            motor.ser.close()
            shutter.ser.close()
        
        #Print the time the experiment finished
        self.label_end_time.configure(text = 'Experiment End Time: ' + 
                            datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))

#MainLoop
root = tk.Tk()
app = SingleImageCreator(root)
root.mainloop()