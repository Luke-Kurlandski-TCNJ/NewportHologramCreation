# -*- coding: utf-8 -*-

"""
Create a single image upon a hologram.

Created on 9/22/19
Updated on 11/1/19

Copyright 2019, Luke Kurlandski, All rights reserved.

SingleImageCreator is designed to provide a simple, user interface to facilitate
the creation of single-image holograms upon a film. This program inherits from
GenericImageCreator. 

This program was written by Luke Kurlandski and is his intellectual property. 

Luke Kurlandski recieved assistence from Matthew VanSoelen and Daniel Stolz. 

Dr. David McGee has permission to use this code in whatever way he sees fit.
"""

#Graphical User Interface tools
import tkinter as tk 
from tkinter import filedialog 
from PIL import ImageGrab, ImageTk
#Experiment timing tools
from datetime import datetime 
from datetime import timedelta 
import time 
#Support image processing, equipment, inheritence
import imagemodification
from serialcontrol import Motor, Shutter, Laser
from generichologramcreator import GenericImageCreator

class SingleImageCreator(GenericImageCreator):
    """
    Create a single dot matrix image on a hologram.
    
    Notes:
        Child class, derives from GenericImageCreator. During execution, this 
            program will become unresponsive due to the movement of stages.
    """
    
    def __init__(self, root):
        """
        Constructor for creating a single image.
            
        Arguments:
            (arg1) root (Tk) : the root window
        """
        
        #Call parent constructor
        super().__init__(root, 700, 700, 'Single Hologram Creation. Copyright 2019, Luke Kurlandski, all rights reserved.')

        #Set up the frames: x=4 , y=5
        self.frames = self.set_up_frames(self.root, 4, 5)
        self.frames[0][1].grid(row=0, column=1, pady=10, rowspan=200, columnspan=200, sticky='NW')
        self.frames[1][1].grid(row=1, column=1, pady=10, rowspan=200, columnspan=200, sticky='W')
        self.frames[0][2].grid(row=0, column=2, pady=10, rowspan=200, columnspan=200, sticky='NW', padx=250)
        self.data_colleted = False #only collect data once

        #Set up main menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu = self.menu)
        #File Menu
        submenu_file = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=submenu_file)
        submenu_file.add_command(label='Quit', command=self.root.destroy)
        submenu_file.add_command(label='Save As', command=self.save_experiment)
        submenu_file.add_command(label='Open Experiment', command=self.open_experiment)
        submenu_file.add_command(label='Open Previous', command=lambda: self.open_experiment('SingleImageCreator/Experiments/Previous Experiment Single Image.txt'))
        submenu_file.add_command(label='Open Sample', command=lambda: self.open_experiment('SingleImageCreator/Experiments/Sample Experiment Single Image.txt'))
        submenu_file.add_command(label='Clear Inputs', command=self.clear_inputs)
        #Serial Menu: 
        #FIXME: I have observed some extremely bizarre behavior here,possible source of FileNotFoundError
        submenu_serial = tk.Menu(self.menu)
        self.menu.add_cascade(label='Serial Configurations', menu=submenu_serial)
        submenu_serial.add_command(label='Serial Motor', command=lambda: self.setup_serial_port('Motor', 'SingleImageCreator/Equipment/Serial Port Congifurations Motor.txt'))
        submenu_serial.add_command(label='Serial Shutter', command=lambda: self.setup_serial_port('Shutter', 'SingleImageCreator/Equipment/Serial Port Congifurations Shutter.txt'))
        submenu_serial.add_command(label='Serial Laser', command=lambda: self.setup_serial_port('Laser','SingleImageCreator/Equipment/Serial Port Congifurations Laser.txt'))
        #Equipment Menu
        submenu_equipment = tk.Menu(self.menu)
        self.menu.add_cascade(label='Equipment Settings', menu=submenu_equipment)
        submenu_equipment.add_command(label='Motor', command=self.motor_settings)
        submenu_equipment.add_command(label='Shutter', command=self.shutter_settings)
        submenu_equipment.add_command(label='Laser', command=self.laser_settings)
        #Help Menu
        submenu_help = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=submenu_help)
        drcty = 'SingleImageCreator/Help/'
        submenu_help.add_command(label='General Instructions', command=lambda: self.help_window(self.root, drcty + 'General Instructions.txt'))
        submenu_help.add_command(label='Film Information', command=lambda: self.help_window(self.root, drcty + 'Film Information.txt'))
        submenu_help.add_command(label='Image Selection', command=lambda: self.help_window(self.root, drcty + 'Image Selection.txt'))
        submenu_help.add_command(label='Exposure Information', command=lambda: self.help_window(self.root, drcty + 'Exposure Information.txt'))
        submenu_help.add_command(label='Initialize Experiment', command=lambda: self.help_window(self.root, drcty + 'Initialize Experiment.txt'))
        submenu_help.add_command(label='While Running', command=lambda: self.help_window(self.root, drcty + 'While Running.txt'))
        
        #Set up Film Information
        tk.Label(self.frames[0][0], text='Film Information', font="bold").pack()
        tk.Label(self.frames[0][0], text='Image Width on Film (m)').pack()
        self.entry_width = tk.Entry(self.frames[0][0], width = 10)
        self.entry_width.pack()
        tk.Label(self.frames[0][0], text='Image Height on Film (m)').pack()
        self.entry_height = tk.Entry(self.frames[0][0], width = 10)
        self.entry_height.pack()
        tk.Label(self.frames[0][0], text='Estimate Spot Size (\u03BCm) (opt)').pack()
        self.entry_spot = tk.Entry(self.frames[0][0], width = 10)
        self.entry_spot.pack()
        
        #Set up Image Selection
        tk.Label(self.frames[1][0], text='Image Selection', font='bold').pack()
        self.button_chsIMG = tk.Button(self.frames[1][0], text='Select an Image', command=self.image_select)
        self.button_chsIMG.pack()
        tk.Label(self.frames[1][0], text='Desired Horizontal Gratings (opt)').pack()
        self.entry_Xpix = tk.Entry(self.frames[1][0], width = 10)
        self.entry_Xpix.pack()
        tk.Label(self.frames[1][0], text='Desired Vertical Gratings (opt)').pack()
        self.entry_Ypix = tk.Entry(self.frames[1][0], width = 10)
        self.entry_Ypix.pack()
        tk.Label(self.frames[1][0],text='Cropping (opt)').pack()
        self.entry_crop = tk.Entry(self.frames[1][0], width = 15)
        self.entry_crop.pack()
        
        #Set up Default Images and get default image size
        self.file = 'Images/Sample Image.png'
        self.label_img_lbl = tk.Label(self.frames[0][1])
        self.label_img_lbl.pack()
        self.label_img = tk.Label(self.frames[0][1])
        self.label_img.pack()
        self.image_select(self.file)
        self.label_img_lbl_mod = tk.Label(self.frames[1][1], text = 'Modified Sample Image')
        self.label_img_lbl_mod.pack()
        self.label_img_mod = tk.Label(self.frames[1][1])
        self.label_img_mod.pack()     
        self.xPix, self.yPix = self.modify_image(200, 200, '')

        #Set up Exposure Information
        tk.Label(self.frames[0][2], text='Exposure Information', font="bold").pack()
        #Exposure Details
        sub_frame_1 = tk.Frame(self.frames[0][2])
        sub_frame_1.pack()
        tk.Label(sub_frame_1, text='Exposure Details (s)').grid(row=0, column=0)
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
        tk.Label(sub_frame_3, text='Laser Power (mW)').grid(row=0, column=0)
        self.laser_details = tk.Text(sub_frame_3, width=20, height=10)
        self.laser_details.grid(row=1, column=0)
        self.apply_scrollbars(sub_frame_3, self.laser_details, x=True, y=True, yrow=1, ycol=1, xrow=2, xcol=0)
        
        #Set up Initialize Experiment
        tk.Label(self.frames[2][0], text='Initialize Experiment', font="bold").pack()
        self.button_update = tk.Button(self.frames[2][0], text = 'Update all Information', command=self.get_data)
        self.button_update.pack()
        self.label_resolution = tk.Label(self.frames[2][0], text='Image Resolution (dpi): ?')
        self.label_resolution.pack()
        self.button_run = tk.Button(self.frames[2][0], text = 'Run Experiment', command=lambda: self.run_experiment(self.hologram_width, self.hologram_height, self.xPix, self.yPix, self.config_shutter, self.config_motor, self.config_laser, self.img_as_arr, self.exposure_arr, self.laser_arr, self.laser_settings))
        self.button_run.pack()
        
        #Set up Running Experiment
        tk.Label(self.frames[3][0], text='While Running', font="bold").pack()
        self.listbox = tk.Listbox(self.frames[3][0], height=3)
        self.listbox.pack()
        self.listbox.insert(1, "Run")
        self.listbox.insert(2, "Pause")
        self.listbox.insert(3, "Abort")
        self.listbox.activate(1)
        
        #Timing and location information
        self.label_start_time = tk.Label(self.frames[3][0], text='Start Time: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_start_time.pack()
        self.label_end_time = tk.Label(self.frames[3][0], text='Experiment End Time: In Progress')
        self.label_end_time.pack()
        self.label_end_time_est = tk.Label(self.frames[3][0], text='End Time Estimate: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_end_time_est.pack()
        self.label_position = tk.Label(self.frames[3][0], text='Current Location (x,y) : (x,y)')
        self.label_position.pack() 
        self.label_details = tk.Label(self.frames[3][0], text='Details (pxl,pwr,time) : (p,mW,s)')
        self.label_details.pack() 
    
    def image_select(self, img_file=None):
        """
        Get image from user, downsize version displayed on main window.
        
        Notes:
            Additionally updates the self.xPix and self.yPix
        
        Arguments:
            (arg1) img_file (string) : optionally specifiy an image file
        """
        
        #Get original PIL image
        self.text_communication.insert(tk.END, 'Finding and storing your image.\n\n')
        if img_file == None:
            self.file = filedialog.askopenfilename(initialdir = 'Images', title = "Select Image",filetypes = (("png images","*.png"),("jpeg images","*.jpeg"),("All files","*.*")))
        else:
            self.file = img_file
        img_pil = imagemodification.convert_grey_downsize(self.file, newX=None, newY=None, convert=False)
        self.xPix, self.yPix = img_pil.size
        #Get a TK image to print to main window
        self.img_tk = imagemodification.image_for_window(200, 200, img_pil, self.file)
        self.label_img.configure(image = self.img_tk)
        self.label_img_lbl.configure(text='Original Image')

    def get_data(self):
        """
        Gets data from main window and processes the data to prepare for runtime.
        
        Notes:
            Provides basic feedback to user if processes go wrong. Alters an 
                error_message which will be printed if an exception is thrown.
                Prints information to the text_communication to update the user.
        """
        
        self.text_communication.insert(tk.END, 'Beginning Data Pocessing\n\n')
        
        try:
            #Get hologram size, image modifcations
            self.text_communication.insert(tk.END, 'Getting all raw user data from main window.\n\n')
            error_message = 'Something went wrong getting the hologram width/height.'
            self.hologram_width = float(self.entry_width.get())
            self.hologram_height = float(self.entry_height.get())
            error_message = 'Something went wrong getting the hologram horizontal/vertical pixels.'
            if self.entry_Xpix.get().rstrip() != '':
                self.xPix = int(self.entry_Xpix.get())
            else:
                self.xPix = self.img_pil_mod.width
            if self.entry_Ypix.get().rstrip() != '':
                self.yPix = int(self.entry_Ypix.get())
            else:
                self.yPix = self.img_pil_mod.height
            error_message = 'Something went wrong getting the cropping information.'
            self.cropping = self.entry_crop.get()
            
            #Get exposure/ignore/laser 
            self.text_communication.insert(tk.END, 'Getting the exposure, ignore, and laser details.\n\n')
            error_message = 'Something went wrong acquiring the unprocessed exposure, ignore, and/or laser details.'
            self.exposure_lines = self.exposure_details.get('1.0','end-1c').rstrip().splitlines()
            self.ignore_lines = self.ignore_details.get('1.0','end-1c').rstrip().splitlines()
            self.laser_lines = self.laser_details.get('1.0','end-1c').rstrip().splitlines()
            
            #Process exposure/ignore/laser details
            self.text_communication.insert(tk.END, 'Processing the exposure, ignore, and laser details.\n\n')
            error_message = 'Something went wrong processing the exposure, ignore, and/or laser details.'
            self.exposure_arr, self.laser_arr = self.generate_exposure_details(self.exposure_lines, self.ignore_lines, self.laser_lines)
            
            #Configure the Serial Ports
            self.text_communication.insert(tk.END, 'Retrieving serial port configurations from file.\n\n')
            error_message = 'Something went wrong getting previous configurations for the Shutter.'
            self.config_shutter = self.get_serial_config('SingleImageCreator/Equipment/Serial Port Congifurations Shutter.txt')
            error_message = 'Something went wrong getting previous configurations for the Motor.'
            self.config_motor = self.get_serial_config('SingleImageCreator/Equipment/Serial Port Congifurations Motor.txt')
            error_message = 'Something went wrong getting previous configurations for the Laser.'
            self.config_laser = self.get_serial_config('SingleImageCreator/Equipment/Serial Port Congifurations Laser.txt')
            
            #Modify the image, convert into an array, update xPix and yPix (cropping), dots per inch
            self.text_communication.insert(tk.END, 'Modifying the image and processing into an array.\n\n')
            error_message = 'Something went wrong while modifying the image.'
            self.xPix, self.yPix = self.modify_image(self.xPix, self.yPix, self.cropping)
            error_message = 'Something went wrong while processing the image into an array.'
            self.img_as_arr = self.image_as_array(self.root, self.img_pil_mod, 'Modified Image')
            dots_per_inch = self.xPix / (39.3 * self.hologram_width)
            self.label_resolution.configure(text='Image Resolution (dpi): ' + str(int(dots_per_inch)))
            
            #Generate runtime estimation and display on main window
            self.text_communication.insert(tk.END, 'Generating a run-time estimation.\n\n')
            error_message = 'Something went wrong while generating a run-time estimation.'
            run_time = self.time_estimation(self.img_as_arr, self.exposure_arr, self.xPix, self.yPix, self.hologram_width, self.hologram_height)
            exp = timedelta(seconds = run_time)
            self.label_end_time_est.configure(text='Estimated End Time: ' + (datetime.now() + exp).strftime('%H:%M:%S -- %d/%m/%Y'))
            
            #Get the laser settings from the file
            self.text_communication.insert(tk.END, 'Getting up to date laser settings.\n\n')
            error_message = 'Something went wrong while retrieving laser settings from the file.'
            self.laser_settings = self.get_laser_settings('SingleImageCreator/Equipment/Settings Laser.txt')
            self.text_communication.insert(tk.END, 'Storing all raw data in: Previous Experiment Single Image.txt\n\n')
            subjects = ['HologramWidth', 'Hologram Height', 'xPix', 'yPix', 'Cropping', 'Laser Maximum Power', 'Laser Pause Period', 'Exposure Lines', 'Ignore Lines', 'Laser Lines']
            datas = [self.hologram_width, self.hologram_height, self.xPix, self.yPix, self.cropping, self.laser_maximum, self.laser_pause, self.exposure_details.get('1.0','end-1c').rstrip(), self.ignore_details.get('1.0','end-1c').rstrip(), self.laser_details.get('1.0','end-1c').rstrip()]
            self.store_previous_data('SingleImageCreator/Experiments/Previous Experiment Single Image.txt', subjects, datas)
            
            #The data is processed correctly
            error_message = 'All data processed correctly.\n'
            
        except Exception as e:
            self.text_communication.insert(tk.END, str(e) + '\n\n')
            return
        
        finally:
            self.text_communication.insert(tk.END, error_message + '\n')
        self.text_communication.insert(tk.END, '\n')
        
    def modify_image(self, xPix, yPix, cropping):
        """
        Convert the original image to greyscale, downsize, and update on main window.
        
        Notes:
            The main window is only capable of handling 200x200 images. The user
                may print images larger than that, however, only a 200x200 version
                will appear on the main window.
        
        Arguments:
            (arg1) xPix (int) : number of pixels to downsize horizontally
            (arg2) yPix (int) : number of pixels to downsize vertically
            (arg3) cropping (string) : formatted string with croppng details
            
        Returns:
            (arg1) new_xPix (int) : number of pixels horizontally after cropping
            (arg2) new_yPix (int) : number of pixels vertically after cropping
        """
        
        #Modify the image, redefine the number of pixels in image
        self.text_communication.insert(tk.END, 'Downsizing the original image with your new dimentions.\n\n')
        self.img_pil_mod = imagemodification.convert_grey_downsize(self.file, xPix, yPix, True)
        if cropping != '':
            self.text_communication.insert(tk.END, 'Applying your cropping to the downsized image.\n\n')
            self.img_pil_mod = imagemodification.crop_image(cropping, self.img_pil_mod) 
        new_xPix = self.img_pil_mod.width
        new_yPix = self.img_pil_mod.height
        #Update on screen, downsize screen image if larger than 200x200
        self.img_tk_mod = imagemodification.image_for_window(200, 200, self.img_pil_mod, self.file)
        self.label_img_mod.configure(image = self.img_tk_mod)
        self.label_img_lbl_mod.configure(text='Modified Image')
        #Return the updated image dimentions
        return new_xPix, new_yPix
            
    def time_estimation(self, img_as_arr, exposure_arr, xPix, yPix, hologram_width, hologram_height):
        """
        Create a time estimation for the length of the experiment.
        
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
    
    def run_experiment(self, hologram_width, hologram_height, xPix, yPix, config_shutter, config_motor, config_laser, img_as_arr, exposure_arr, laser_arr, laser_settings):
        """
        Run the experiment by mcontrolling laboratory equipment and reading
            the processed user input.
        
        Notes:
            self.root.update() and self.root.update_idletasks() are used to keep
                the user interface responsive. However, the interface will still
                become unresponsive. The only solution to this problem would be 
                to implement threading.
        
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
                   
        #Record the start time of the experiment and compute dot separation
        self.text_communication.insert(tk.END, 'Beginning Run-Time Processes (program may become \'unresponsive\'.)\n\n')
        self.label_start_time.configure(text = 'Start Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.listbox.selection_set(0)
        xDelta = 1.0 * hologram_width / xPix
        yDelta = 1.0 * hologram_height / yPix
        
        #Printing image process, prone to exceptions
        try:
            #Set up the serial connections
            self.text_communication.insert(tk.END, 'Establishing serial connections with devices.\n\n')
            error_message = 'Something went wrong establishing a serial connection with the motor.'
            motor = Motor.from_arguments(config_motor)
            error_message = 'Something went wrong establishing a serial connection with the shutter.'
            shutter = Shutter.from_arguments(config_shutter)
            error_message = 'Something went wrong establishing a serial connection with the laser.'
            laser = Laser.from_arguments(config_laser) 
            self.root.update_idletasks()
            #Turn on and configure the laser 
            self.text_communication.insert(tk.END, 'Configuring the laser.\n\n')
            self.root.update_idletasks()
            error_message = 'Something went wrong initializing the laser'
            laser.configure_settings(laser_settings)
            #Configure each axis, move home
            self.text_communication.insert(tk.END, 'Configuring the axes and moving home.\n\n')
            self.root.update_idletasks()
            error_message = 'Something went wrong initializing the stages.'
            motor.configure_axis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
            motor.configure_axis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
            #Move stages and exposure according to pixel value at that location
            self.text_communication.insert(tk.END, 'Printing the image.\n\n')
            self.root.update_idletasks()
            prev_pix = None
            for i in range(0, yPix):
                onRow = False 
                for j in range(0, xPix):
                    self.root.update()
                    #Handle pause or abort
                    error_message = 'Something went wrong printing the image at ' + str(i) + ',' + str(j) + '.'
                    while self.listbox.curselection()[0] != 0:
                        if 1 in self.listbox.curselection():
                            time.sleep(1)
                            self.root.update()
                        if 2 in self.listbox.curselection():
                            raise Exception('User terminated the experiment') #FIXME: test this
                    #Movement and exposure
                    cur_pix = img_as_arr[j][i]
                    if exposure_arr[cur_pix] != 0:
                        self.label_position.configure(text='Location (x,y) : (' + str(j) + ',' + str(i) + ')') 
                        self.label_details.configure(text='Details (pxl,pwr,time) : (' + str(cur_pix) + ',' + str(laser_arr[cur_pix]) + ',' + str(exposure_arr[cur_pix]) + ')')
                        #Ensure laser is on and change power if nessecary
                        #laser.turn_on_off(True) #FIXME: is this nessecary?
                        if (prev_pix != None and not (laser_arr[prev_pix] -.05 < laser_arr[cur_pix] < laser_arr[prev_pix] + .05)):
                            laser.change_power(laser_arr[cur_pix])
                        #Move y-axis if nessecary
                        if onRow == False:
                            motor.move_absolute(axis=2, goToPos=i*yDelta*1000)
                        #Move x-axis
                        motor.move_absolute(axis=1, goToPos=j*xDelta*1000)
                        onRow = True
                        shutter.toggle_shutter(exposure_arr[cur_pix])
                    prev_pix = cur_pix
            error_message = 'All experimental procedures executed properly.'
                        
        except Exception as e:
            self.text_communication.insert(tk.END, str(e) + '\n\n')
            self.text_communication.insert(tk.END, 'Closing all serial ports due to malfunction.\n\n')
            motor.ser.close()
            shutter.ser.close()
            laser.ser.close() 
            return
        
        finally:
            self.text_communication.insert(tk.END, error_message + '\n\n')
        
        #Final processes before program termination: close serial ports, update save-file (new screenshot!)
        self.text_communication.insert(tk.END, 'Closing all serial ports as part of closing procedures.\n\n')
        motor.ser.close()
        shutter.ser.close()
        laser.ser.close() 
        self.label_end_time.configure(text = 'Experiment End Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.save_experiment(self.file_save)
        
    def save_experiment(self, file=None):
        """
        Save the experiment inputs in a text file from a file dialogue box or
            from a specific file as argument and takes a screenshot.

        Arguments:
            (arg1) file (string) : optionally include a file to open, rather than letting user choose file
        """
        #Update all data from main window if nessecary
        if self.data_collected == False:
            self.get_data()
        #Get the location and name of file from user
        if file==None:
            self.file_save = filedialog.asksaveasfilename(initialdir = 'SingleImageCreator/Experiments', title = 'Format: \'(mm-dd-yy)[name]\'', filetypes = (("txt files","*.txt"),("All Files","*.*")), defaultextension = '.txt')
        else:
            self.file_save = file
        #Save the data
        self.text_communication.insert(tk.END, 'Storing all raw data in: ' + self.file_save + '\n\n')
        subjects = ['HologramWidth', 'Hologram Height', 'xPix', 'yPix', 'Cropping', 'Laser Maximum Power', 'Laser Pause Period', 'Exposure Lines', 'Ignore Lines', 'Laser Lines']
        datas = [self.hologram_width, self.hologram_height, self.entry_Xpix.get(), self.entry_Ypix.get(), self.cropping, self.laser_maximum, self.laser_pause, self.exposure_details.get('1.0','end-1c').rstrip(), self.ignore_details.get('1.0','end-1c').rstrip(), self.laser_details.get('1.0','end-1c').rstrip()]
        self.store_previous_data(self.file_save, subjects, datas)
        #Take screenshot and save in same place
        x1 = self.root.winfo_x()
        y1 = self.root.winfo_y()
        x2 = x1 + self.root.winfo_width()
        y2 = y1 + self.root.winfo_height()
        myScreenshot = ImageGrab.grab((x1,y1,x2,y2))
        myScreenshot.save(self.file_save.replace('.txt','.png'))

    def open_experiment(self, file=None):
        """
        Open a previous experiment with either a file dialogue box or specific 
            file as argument.

        Arguments:
            (arg1) file (string) : optionally include a file to open, rather than letting user choose file
        """
        
        #Let the user choose which file to open
        if file == None:
            file_open = filedialog.askopenfilename(initialdir = 'SingleImageCreator/Experiments', title = "Open Experiment", filetypes = (("txt files","*.txt"),("All files","*.*")))
        else:
            file_open = file  
        #Clear all user input
        self.clear_inputs()
        #Fill main window with values from previous experiment
        self.text_communication.insert(tk.END, 'Retrieving experiment data.\n\n')
        try:
            file = open(file_open, 'r')
            lines = file.readlines()
            self.entry_width.insert(1, lines[1].rstrip())
            self.entry_height.insert(1, lines[3].rstrip())
            self.entry_Xpix.insert(1, lines[5].rstrip())
            self.entry_Ypix.insert(1, lines[7].rstrip())
            self.entry_crop.insert(1, lines[9].rstrip())
            self.laser_maximum = float(lines[11].rstrip())
            self.laser_pause = float(lines[13].rstrip())
            cont = 15
            for i in range(cont, lines.index('Ignore Lines\n')):
                self.exposure_details.insert(tk.END, lines[i].rstrip() + '\n')
                cont = i
            for i in range(cont+2, lines.index('Laser Lines\n')):
                self.ignore_details.insert(tk.END, lines[i].rstrip() + '\n')
                cont = i
            for j in range(cont+2, len(lines)):
                self.laser_details.insert(tk.END, lines[j].rstrip() + '\n') 
        except Exception as e:
            error_message = 'Something went wrong with retrieving data from the previous experiment.'
            error_message += '\t' + str(e) + '\n\n'
            self.text_communication.insert(tk.END, error_message) 
        finally:
            file.close()

    def clear_inputs(self):
        """
        Clear all input from the main window.
        """

        self.entry_width.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)
        self.entry_Xpix.delete(0, tk.END)
        self.entry_Ypix.delete(0, tk.END)
        self.entry_crop.delete(0, tk.END)
        self.exposure_details.delete(1.0, tk.END)
        self.ignore_details.delete(1.0, tk.END)
        self.laser_details.delete(1.0, tk.END)
        
#MainLoop
root = tk.Tk()
app = SingleImageCreator(root)
root.mainloop()