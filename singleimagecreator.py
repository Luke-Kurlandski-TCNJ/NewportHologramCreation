# -*- coding: utf-8 -*-
"""
Create a single image upon a hologram.

Created on 9/22/19
Updated on 11/1/19

@author: Luke Kurlandski

SingleImageCreator is designed to provide a simple, user interface to facilitate
the creation of single-image holograms upon a film. This program inherits from
GenericImageCreator. 

The program functions as follows:
    
    1) determine the size of the hologram to create;
    2) modify an image according to user specifications and convert into an
        array of pixel values for each pixel in the image;
    3) process user input to determine how long and at what power level to expose
        each particular pixel value;
    4) control the motor, shutter, and laser to create the image upon the film.
    
The program is not a masterpiece. Functionality is more important than perfection.
Luke Kurlandski wrote this program with his focus on creating beautiful holograms,
not beautiful code.

Any and all modifications to this program in the future should be performed upon
a copy. This version should at no time ever be modified by anyone other than Luke
Kurlandski. 

This program was written by Luke Kurlandski and is his intellectual property. 
Dr. David McGee, The College of New Jersey Physics Department, has unlimited access 
to this program.
"""

#Graphical User Interface tools
import tkinter as tk 
from tkinter import filedialog 
from PIL import ImageTk 

#Experiment timing tools
from datetime import datetime 
from datetime import timedelta 
import time 

#My own programs
import imagemodification
from serialcontrol import Motor, Shutter, Laser
from generichologramcreator import GenericImageCreator

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
        self.menu = tk.Menu(self.root)
        self.root.config(menu = self.menu)
        #File Menu
        submenu_file = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=submenu_file)
        submenu_file.add_command(label='Quit', command=self.root.destroy)
        submenu_file.add_command(label='Save', command=self.save_experiment)
        submenu_file.add_command(label='Open', command=self.open_experiment)
        #Serial Menu
        submenu_serial = tk.Menu(self.menu)
        self.menu.add_cascade(label='Serial Configurations', menu=submenu_serial)
        submenu_serial.add_command(label='Serial Motor', command=lambda: self.setup_serial_port('Motor'))
        submenu_serial.add_command(label='Serial Shutter', command=lambda: self.setup_serial_port('Shutter'))
        submenu_serial.add_command(label='Serial Laser', command=lambda: self.setup_serial_port('Laser'))
        submenu_serial.add_command(label='Laser Settings', command=self.laser_settings)
        #Help Menu
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
        self.entry_crop = tk.Entry(self.frames[2][0], width = 15)
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
        #Exposure Details
        sub_frame_1 = tk.Frame(self.frames[0][2])
        sub_frame_1.pack()
        tk.Label(sub_frame_1, text='Exposure Details').grid(row=0, column=0)
        self.exposure_details = tk.Text(sub_frame_1, width=20, height=10)
        self.exposure_details.grid(row=1, column=0)
        self.apply_scrollbars(sub_frame_1, self.exposure_details, x=True, y=True, yrow=1, ycol=1, xrow=2, xcol=0)
        #Ignore Details
        sub_frame_2 = tk.Frame(self.frames[0][2])
        sub_frame_2.pack()
        tk.Label(sub_frame_2, text='Ignore Details').grid(row=0, column=0)
        self.ignore_details = tk.Text(sub_frame_2, width=20, height=10)
        self.ignore_details.grid(row=1, column=0)
        self.apply_scrollbars(sub_frame_2, self.ignore_details, x=True, y=True, yrow=1, ycol=1, xrow=2, xcol=0)
        #Laser Details
        sub_frame_3 = tk.Frame(self.frames[0][2])
        sub_frame_3.pack()
        tk.Label(sub_frame_3, text='Laser Power').grid(row=0, column=0)
        self.laser_details = tk.Text(sub_frame_3, width=20, height=10)
        self.laser_details.grid(row=1, column=0)
        self.apply_scrollbars(sub_frame_3, self.laser_details, x=True, y=True, yrow=1, ycol=1, xrow=2, xcol=0)
        
        #Set up Initialize Experiment
        tk.Label(self.frames[3][0], text='5) Initialize Experiment', font="bold").pack()
        self.button_update = tk.Button(self.frames[3][0], text = 'Update all Information', command=self.get_data)
        self.button_update.pack()
        self.button_run = tk.Button(self.frames[3][0], text = 'Run Experiment', command=lambda: self.run_experiment(self.hologram_width, self.hologram_height, self.xPix, self.yPix, self.config_shutter, self.config_motor, self.config_laser, self.img_as_arr, self.exposure_arr, self.laser_arr, self.laser_settings))
        self.button_run.pack()
        
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
        
        #Fill main window with values from previous experiment
        self.text_communication.insert(tk.END, 'Retrieving previous experiment data.\n')
        with open('Prior Experiment Data Single Image Creation.txt', 'r') as file:
            try:
                lines = file.readlines()
                self.entry_width.insert(1, lines[1].rstrip())
                self.entry_height.insert(1, lines[3].rstrip())
                self.entry_Xpix.insert(1, lines[5].rstrip())
                self.entry_Ypix.insert(1, lines[7].rstrip())
                self.entry_crop.insert(1, lines[9].rstrip())
                self.laser_maximum = float(lines[11].rstrip())
                cont = 13
                for i in range(13, lines.index('Ignore Lines\n')):
                    self.exposure_details.insert(tk.END, lines[i].rstrip() + '\n')
                    cont = i
                for i in range(cont+2, lines.index('Laser Lines\n')):
                    self.ignore_details.insert(tk.END, lines[i].rstrip() + '\n')
                    cont = i
                for j in range(cont+2, len(lines)):
                    self.laser_details.insert(tk.END, lines[j].rstrip() + '\n') 
            except Exception as e:
                error_message = 'Something went wrong with retrieving data from the previous experiment.'
                error_message += '\t' + str(e) + '\n'
                self.text_communication.insert(tk.END, error_message)                
    
    def image_select(self):
        """
        Get image from user, downsize automatically, and display.
        """
        
        #Store original PIL image
        self.text_communication.insert(tk.END, 'Finding and storing your image.\n')
        self.file = filedialog.askopenfilename()
        self.img_pil = imagemodification.convert_grey_downsize(self.file, newX=None, newY=None, convert=False)
        
        #Print an appropriately downsized image to the main window
        self.img_tk = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=200, newY=200, convert=False))
        self.label_img.configure(image=self.img_tk)
        self.label_img_lbl.configure(text='Original Image')
        
    def get_data(self):
        """
        Get data from main window and drives next processes in program.
        
        Notes:
            Provides basic feedback to user if processes go wrong.
        """
        
        try:
            #Get hologram size, image modifcations
            self.text_communication.insert(tk.END, 'Getting all raw user data from main window.\n')
            error_message = 'Something went wrong getting the hologram width/height.'
            self.hologram_width = float(self.entry_width.get())
            self.hologram_height = float(self.entry_height.get())
            error_message = 'Something went wrong getting the hologram horizontal/vertical pixels.'
            if self.entry_Xpix.get().rsplit() != '':
                self.xPix = int(self.entry_Xpix.get())
            else:
                self.xPix = self.img_pil_mod.width
            if self.entry_Ypix.get().rsplit() != '':
                self.yPix = int(self.entry_Ypix.get())
            else:
                self.yPix = self.img_pil_mod.height
            error_message = 'Something went wrong getting the cropping information.'
            cropping = self.entry_crop.get()
            
            #Get exposure/ignore/laser details
            error_message = 'Something went wrong acquiring the unprocessed exposure, ignore, and/or laser details.'
            self.exposure_lines = self.exposure_details.get('1.0','end-1c').rstrip().splitlines()
            self.ignore_lines = self.ignore_details.get('1.0','end-1c').rstrip().splitlines()
            self.laser_lines = self.laser_details.get('1.0','end-1c').rstrip().splitlines()
            
            #Store all the user data in a file
            self.text_communication.insert(tk.END, 'Storing all raw data in a file for the next experiment.\n')
            error_message = 'Something went wrong storing your input into a file.'
            subjects = ['HologramWidth', 'Hologram Height', 'xPix', 'yPix', 'Cropping', 'Laser Maximum Power', 'Exposure Lines', 'Ignore Lines', 'Laser Lines']
            datas = [self.hologram_width, self.hologram_height, self.xPix, self.yPix, cropping, self.laser_maximum, self.exposure_details.get('1.0','end-1c').rstrip(), self.ignore_details.get('1.0','end-1c').rstrip(), self.laser_details.get('1.0','end-1c').rstrip()]
            self.store_previous_data('Prior Experiment Data Single Image Creation.txt', subjects, datas)
            
            #Process exposure/ignore/laser details
            self.text_communication.insert(tk.END, 'Processing the exposure, ignore, and laser details.\n')
            error_message = 'Something went wrong processing the exposure, ignore, and/or laser details.'
            self.exposure_arr, self.laser_arr = self.generate_exposure_details(self.exposure_lines, self.ignore_lines, self.laser_lines, self.laser_maximum)
            
            #Configure the Serial Ports
            self.text_communication.insert(tk.END, 'Retrieving serial port configurations from file.\n')
            error_message = 'Something went wrong getting previous configurations for the Shutter.'
            self.config_shutter = self.get_serial_config('Shutter')
            error_message = 'Something went wrong getting previous configurations for the Motor.'
            self.config_motor = self.get_serial_config('Motor')
            error_message = 'Something went wrong getting previous configurations for the Laser.'
            self.config_laser = self.get_serial_config('Laser')
            
            #Modify the image, convert into an array, update xPix and yPix (cropping)
            self.text_communication.insert(tk.END, 'Modifying the image and processing into an array.\n')
            error_message = 'Something went wrong while modifying the image.'
            self.xPix, self.yPix = self.modify_image(self.xPix, self.yPix, cropping)
            error_message = 'Something went wrong while processing the image into an array.'
            self.img_as_arr = self.image_as_array(self.root, self.img_pil_mod, 'Modified Image')
            
            #Generate runtime estimation and display on main window
            self.text_communication.insert(tk.END, 'Generating a run-time estimation.\n')
            error_message = 'Something went wrong while generating a run-time estimation.'
            run_time = self.time_estimation(self.img_as_arr, self.exposure_arr, self.xPix, self.yPix, self.hologram_width, self.hologram_height)
            exp = timedelta(seconds = run_time)
            self.label_end_time_est.configure(text='Estimated End Time: ' + (datetime.now() + exp).strftime('%H:%M:%S -- %d/%m/%Y'))
            error_message = 'All data processed correctly.'
            
            #Get the laser settings from the file
            self.text_communication.insert(tk.END, 'Getting up to date laser settings.\n')
            self.laser_settings = self.get_laser_settings()
            
        except Exception as e:
            self.text_communication.insert(tk.END, '\t' + str(e) + '\n')
            return
        
        finally:
            self.text_communication.insert(tk.END, error_message + '\n')
        
    def modify_image(self, xPix, yPix, cropping):
        """
        Modify the original image and update on main window.
        
        Arguments:
            (arg1) xPix (int) : number of pixels to downsize horizontally
            (arg2) yPix (int) : number of pixels to downsize vertically
            (arg3) cropping (string) : formatted string with croppng details
            
        Returns:
            (arg1) new_xPix (int) : number of pixels horizontally after cropping
            (arg2) new_yPix (int) : number of pixels vertically after cropping
        """
        
        #Modify the image, redefine the number of pixels in image
        self.text_communication.insert(tk.END, '\tDownsizing the original image with your new dimentions.\n')
        self.img_pil_mod = imagemodification.convert_grey_downsize(self.file, xPix, yPix, True)
        if cropping != '':
            self.text_communication.insert(tk.END, '\tApplying your cropping to the downsized image.\n')
            self.img_pil_mod = imagemodification.crop_image(cropping, self.img_pil_mod)
        self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod) 
        new_xPix = self.img_pil_mod.width
        new_yPix = self.img_pil_mod.height
        
        #Update on screen, downsize screen image if larger than 200x200
        if new_xPix > 200 or new_yPix > 200:
            self.text_communication.insert(tk.END, '\tYour image is too big for the main window. Downsizing it again, but only for display.\n')
            if xPix > 200 and yPix <= 200:
                img_temp = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=200, newY=yPix, convert=True))
            if yPix > 200 and xPix <= 200:
                img_temp = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=xPix, newY=200, convert=True))
            if xPix > 200 and yPix > 200:
                img_temp = ImageTk.PhotoImage(imagemodification.convert_grey_downsize(self.file, newX=200, newY=200, convert=True))
        else:
            img_temp = self.img_tk_mod
        self.label_img_mod.configure(image=img_temp)
        self.label_img_lbl_mod.configure(text='Modified Image')
        
        return new_xPix, new_yPix
            
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
    
    #FIXME: incorporate the laser
    def run_experiment(self, hologram_width, hologram_height, xPix, yPix, 
        config_shutter, config_motor, config_laser, img_as_arr, exposure_arr, 
        laser_arr, laser_settings):
        """
        Run the experiment by moving the motor and opening and closing the shutter.
        
        Arguments:
            (arg1) hologram_width (float) : width of the hologram
            (arg2) hologram_height (float) : height of the hologram
            (arg3) xPix (int) : number of pixels in horizontal direction
            (arg4) yPix (int) : number of pixels in vertical direction
            (arg5) config_shutter (tuple) : serial configurations for the shutter
            (arg6) config_motor (tuple) : serial configurations for the motor
            (arg7) config_laser (tuple) : serial configurations for the shutter
            (arg8) img_as_arr (list[list[int]]) : the image converted into an array
            (arg9) exposure_arr (list[float]) : mapping of pixel values to exposure time
            (arg10) laser_arr (list[float]) : mapping of pixel values to laser power
            (arg11) laser_settings (list) : settings for the laser such as maximum power
        """
        
        #FIXME: take a screen shot and save it to a folder            
        #Record the start time of the experiment and compute dot separation
        self.label_start_time.configure(text = 'Start Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.listbox.activate(0)
        xDelta = 1.0 * hologram_width / xPix
        yDelta = 1.0 * hologram_height / yPix
        
        try:
            #Set up the serial connections
            self.text_communication.insert(tk.END, 'Establishing serial connections with devices.\n')
            error_message = 'Something went wrong establishing a serial connection with the motor.'
            motor = Motor.from_arguments(config_motor)
            error_message = 'Something went wrong establishing a serial connection with the shutter.'
            shutter = Shutter.from_arguments(config_shutter)
            error_message = 'Something went wrong establishing a serial connection with the laser.'
            laser = Laser.from_arguments(config_laser) #FIXME
            
            #turn on and configure the laser #FIXME
            laser.configure_settings(laser_settings)
            laser.read_power() 
            
            #Configure each axis, move home
            self.text_communication.insert(tk.END, 'Configuring the axes and moving home.\n')
            error_message = 'Something went wrong configuring the stages.'
            motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
            motor.configureAxis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
            
            #Move stages and exposure according to pixel value at that location
            self.text_communication.insert(tk.END, 'Printing the image.\n')
            for i in range(0, yPix):
                onRow = False 
                for j in range(0, xPix):
                    #Handle pause or abort
                    error_message = 'Something went wrong printing the image at ' + i + ',' + j + '.'
                    while self.listbox.curselection != 0:
                        if self.listbox.curselection == 1:
                            time.sleep(1)
                        if self.listbox.curselection == 2:
                            raise Exception('User terminated experiment')
                    #Movement and exposure
                    self.label_position.configure(text='Current Pixel (x,y): ' + str(j) + ',' + str(i))
                    cur_pix = img_as_arr[j][i]
                    if exposure_arr[cur_pix] != 0:
                        if onRow == False:
                            motor.moveAbsolute(axis=2, goToPos=i*yDelta*1000)
                        motor.moveAbsolute(axis=1, goToPos=j*xDelta*1000)
                        onRow = True
                        shutter.toggle_shutter(exposure_arr[cur_pix])
                        
            error_message = 'All experimental procedures executed properly'
                        
        except Exception as e:
            self.text_communication.insert(tk.END, '\t' + str(e) + '\n')
            self.text_communication.insert(tk.END, 'Closing all serial ports due to malfunction.\n')
            motor.ser.close()
            shutter.ser.close()
            laser.ser.close() #FIXME
            return
        
        finally:
            self.text_communication.insert(tk.END, error_message + '\n')
        
        #Final processes before program termination
        self.text_communication.insert(tk.END, 'Closing all serial ports due to malfunction.\n')
        motor.ser.close()
        shutter.ser.close()
        laser.ser.close() #FIXME
        self.label_end_time.configure(text = 'Experiment End Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))

#MainLoop
root = tk.Tk()
app = SingleImageCreator(root)
root.mainloop()