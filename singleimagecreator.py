# -*- coding: utf-8 -*-
"""
Master GUI class

Created on 9/22/19

@author: Luke Kurlandski and Daniel Stolz
"""

import tkinter as tk #GUI library
from tkinter import ttk #GUI library extension
from tkinter import filedialog #file selection of image
from PIL import ImageTk #Pil and Tk image compatability
from datetime import datetime #Assist with displaying run time
from datetime import timedelta #Assist with displaying run time
import time #Assist with pausing and waiting
import serial #Communication with serial ports
import serial.tools.list_ports #Listing the COM ports
#import os #Allows for file writing
#import movement #package which drives motor and shutter
import imagework #package to support image modification
from serialcontrol import Motor, Shutter #Allows communication with machinery
from generichologramcreator import GenericImageCreator

class SingleImageCreator(GenericImageCreator):
    def __init__(self, root):
        '''
        Constructor for myGUI class
        Arguments:
            (arg1) root (Tk) : the root window
        '''
        
        #Set up the main window (700x650), frames (3x4), and the main menu
        super().__init__(root, 700, 650, 'Single Hologram Creation')
        self.frames = self.set_up_frames(self.root, 3, 5)
        self.frames[0][1].grid(row=0, column=1, pady=10, rowspan=200, columnspan=200, sticky='NW')
        self.frames[1][1].grid(row=1, column=1, pady=10, rowspan=200, columnspan=200, sticky='W')
        self.frames[0][2].grid(row=0, column=2, pady=10, rowspan=200, columnspan=200, sticky='NW', padx=250)
        self.menu = self.set_up_menu(self.root)
        self.menu.add_command(label='Motor Serial', command=lambda: self.setup_serial_port('Motor'))
        self.menu.add_command(label='Shutter Serial', command=lambda: self.setup_serial_port('Shutter'))
        
        #Set up Film Size
        tk.Label(self.frames[0][0], text='1) Film Information', font="bold").pack()
        tk.Label(self.frames[0][0], text='Enter width of image on film (m)').pack()
        self.entry_width = tk.Entry(self.frames[0][0], width = 10, text=.02)
        self.entry_width.pack()
        self.entry_width.insert(1,'0.02')
        tk.Label(self.frames[0][0], text='Enter height of image on film (m)').pack()
        self.entry_height = tk.Entry(self.frames[0][0], width = 10)
        self.entry_height.pack()
        self.entry_height.insert(1,'0.02')
        
        #Set up Image Selection
        tk.Label(self.frames[1][0], text='2) Image Selection', font="bold").pack()
        self.button_chsIMG = tk.Button(self.frames[1][0], text='Select an Image', command=self.image_select)
        self.button_chsIMG.pack()
        #Set up Image Modification
        tk.Label(self.frames[2][0], text='3) Image Modification', font='bold').pack()
        tk.Label(self.frames[2][0], text='Enter desired gratings in horizontal direction').pack()
        self.entry_Xpix = tk.Entry(self.frames[2][0], width = 10)
        self.entry_Xpix.pack()
        self.entry_Xpix.insert(1,'100')
        tk.Label(self.frames[2][0], text='Enter desired gratings in vertical direction').pack()
        self.entry_Ypix = tk.Entry(self.frames[2][0], width = 10)
        self.entry_Ypix.pack()
        self.entry_Ypix.insert(1,'100')
        tk.Label(self.frames[2][0],text='Optional Cropping (see \'Help\')').pack()
        self.entry_crop = tk.Entry(self.frames[2][0], width = 10)
        self.entry_crop.pack()
        self.entry_crop.insert(1, 'none')
        
        #Set up Default Images
        self.label_img_lbl = tk.Label(self.frames[0][1], text = 'Sample Image')
        self.label_img_lbl.pack()
        self.img_pil = imagework.convert_grey_downsize('DefaultImage.png')
        self.img_tk = ImageTk.PhotoImage(self.img_pil)
        self.label_img = tk.Label(self.frames[0][1], image=self.img_tk)
        self.label_img.pack()
        self.img_pil_mod = imagework.convert_grey_downsize('DefaultImage.png', convert=True)
        self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        self.label_img_lbl_mod = tk.Label(self.frames[1][1], text = 'Modified Sample Image')
        self.label_img_lbl_mod.pack()
        self.label_img_mod = tk.Label(self.frames[1][1], image=self.img_tk_mod)
        self.label_img_mod.pack()
        
        #Set up Exposure Information
        tk.Label(self.frames[0][2], text='4) Exposure Information', font="bold").pack()
        tk.Label(self.frames[0][2],text='Exposure details (see \'Help\')').pack()
        self.exposure_details = tk.Text(self.frames[0][2], width=20, height=17)
        self.exposure_details.pack(side='top')
        self.exposure_details.insert(tk.END, '[0,50]:1\n[50,100]:1.5\n[100,150]:2\n[150,200]:2.5\n[200,255]:3')
        tk.Label(self.frames[0][2],text='Ignore details (see \'Help\')').pack()
        self.ignore_details = tk.Text(self.frames[0][2], width=20, height=17)
        self.ignore_details.pack(side='top')
        self.ignore_details.insert(tk.END, '[0,0]\n[255,255]')
        
        #Set up Prepare Experiment
        tk.Label(self.frames[3][0], text='5) Prepare for Experiment', font="bold").pack()
        self.button_update = tk.Button(self.frames[3][0], text = 'Update all Information', command=self.update_all)
        self.button_update.pack()
        
        #Set up Running Experiment
        tk.Label(self.frames[4][0], text='6) Running an Experiment', font="bold").pack()
        self.button_run = tk.Button(self.frames[4][0], text = 'Run Experiment', command=self.run_experiment)
        self.button_run.pack()
        self.listbox = tk.Listbox(self.frames[4][0], height=3)
        self.listbox.pack()
        self.listbox.insert(1, "Run-Mode")
        self.listbox.insert(2, "Pause-Mode")
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
    
    def setup_serial_port(self, port_name):
        '''
        Sets up the serial port menu.
            @author Daniel Stolz and Luke Kurlandski
        Arguments:
            (arg1) port_name (string) : machinery the port is controlling
        '''
        
        def serial_save():
            '''
            Saves the user's selected configurations in a .txt file
            '''
            
            port = cb_port.get()
            baudrate = cb_baudrate.get()
            bytesize = cb_bytesize.get()
            stopbits = cb_stopbits.get()
            parity = cb_parity.get()
            timeout = cb_timeout.get()
            #Creating a file for the serial port values
            file = open(port_name + " Serial Port Values.txt","w")
            file.write(port + "\n" + baudrate + "\n" + bytesize + "\n" + stopbits + "\n" + parity + "\n" + timeout )
            file.close()
            serialport_window.destroy()
        
        def serial_help():
            '''
            Creates a help window specifically for the serial port window
            '''
            
            help_window = self.help_me(serialport_window)
            #Label in the Help-Window
            label_COM_Port = tk.Label(help_window, text="Timeout Values:", font=('Arial', 12))
            label_COM_Port.grid(row=0, column=0, sticky='w')
            label_COM_Port = tk.Label(help_window, text="Unit [s]", font=('Arial', 12))
            label_COM_Port.grid(row=0, column=1, sticky='w')
            label_COM_Port = tk.Label(help_window, text="Parity Values:", font=('Arial', 12))
            label_COM_Port.grid(row=1, column=0, sticky='w')
            label_COM_Port = tk.Label(help_window, text="N (None)", font=('Arial', 12))
            label_COM_Port.grid(row=1, column=1, sticky='w')
            label_COM_Port = tk.Label(help_window, text="E (Even)", font=('Arial', 12))
            label_COM_Port.grid(row=2, column=1, sticky='w')
            label_COM_Port = tk.Label(help_window, text="O (Odd)", font=('Arial', 12))
            label_COM_Port.grid(row=3, column=1, sticky='w')
            label_COM_Port = tk.Label(help_window, text="S (Space)", font=('Arial', 12))
            label_COM_Port.grid(row=4, column=1, sticky='w')
            label_COM_Port = tk.Label(help_window, text="M (Mark)", font=('Arial', 12))
            label_COM_Port.grid(row=5, column=1, sticky='w')
            #Activate the help window
            help_window.mainloop()
        
        def get_proper_file_info():
            '''
            Tries to open the file containing previous configurations and returns
                those configurations. Handles incorrect files. Recursive method.
                Returns:
                    (ret) tuple : port, baudrate, timeout, stopbits, bytesize, parity  
            '''
            
            try:
                #Try and open the file
                file = open(port_name + ' Serial Port Values.txt', 'r')
                #Get the number of lines in file
                lines = file.readlines()
                count = len(lines)
                #If there are not 6 lines, the file is of improper format
                if count != 6:
                    raise Exception
                #Remove trailing characters
                port = lines[0].rstrip();  
                baudrate = lines[1].rstrip(); 
                bytesize = lines[2].rstrip()
                stopbits = lines[3].rstrip()
                parity = lines[4].rstrip()     
                timeout = lines[5].rstrip()
                #Test the data to ensure correct types
                if (port.isdigit() or not baudrate.isdigit() or not bytesize.isdigit() or
                        not stopbits.replace('.', '').isdigit() or parity.isdigit() or 
                                not timeout.replace('.', '').isdigit()):
                    raise Exception
                #Return Correct Information
                return (port, baudrate, timeout, stopbits, bytesize, parity)
            except FileNotFoundError or Exception:
                #Create the file and fill with sample values
                file = open(port_name + " Serial Port Values.txt","w")
                file.write("str" + "\n" + "int" + "\n" + "int" + "\n" + "float" + "\n" + "str" + "\n" + "float")
                file.close()
                #Recursive Call to get the right information
                return get_proper_file_info()
            finally:
                file.close()
        
        #Get the previous serial configurations from the file
        port, baudrate, timeout, stopbits, bytesize, parity = get_proper_file_info()
        
        #Create serial port window
        serialport_window = tk.Toplevel(self.root) 
        serialport_window.title(port_name + ' Serial-Port')
        serialport_window.resizable(False, False)  
        serialport_window_height = 200
        serialport_window_width = 280
        screen_width = serialport_window.winfo_screenwidth()
        screen_height = serialport_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (serialport_window_width/2))
        y_cordinate = int((screen_height/2) - (serialport_window_height/2))
        serialport_window.geometry("{}x{}+{}+{}".format(serialport_window_width, serialport_window_height, x_cordinate, y_cordinate))
        
        #Create a menu bar in te serial port window
        serialport_window_menubar = self.set_up_menu(serialport_window)
        serialport_window_menubar.add_command(label="Help", command=serial_help)
        
        #Create labels for the port window
        tk.Label(serialport_window, text="Port:", font=('Arial', 12)).grid(row=0, column=0)
        tk.Label(serialport_window, text="Baud rate:", font=('Arial', 12)).grid(row=1, column=0) 
        tk.Label(serialport_window, text="Byte size:", font=('Arial', 12)).grid(row=2, column=0)
        tk.Label(serialport_window, text="Stop bits:", font=('Arial', 12)).grid(row=3, column=0)
        tk.Label(serialport_window, text="Parity:", font=('Arial', 12)).grid(row=4, column=0)
        tk.Label(serialport_window, text="Timeout:", font=('Arial', 12)).grid(row=5, column=0) 

        #Get the users choices for serial configurations
        data_baudrate = ("75", "110", "134", "150", "300", "600", "1200", "1800", "2400", "4800", "7200", "9600", "14400", "19200", "38400", "57600", "115200", "128000")
        data_bytesize = ("4", "5", "6", "7", "8")
        data_stopbits = ("1", "1.5", "2")
        data_parity = ("N", "E", "O", "S", "M")
        data_timeout = ("0.1", "0.5", "1", "1.5", "2")
        data_port = []
        comlist = serial.tools.list_ports.comports()
        for i in comlist:
            data_port.append(i.device)
            
        #Create combo boxes for the user to select options from
        cb_port=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_port)
        cb_port.grid(row=0, column=1)
        cb_port.set(port)
        cb_baudrate=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_baudrate)
        cb_baudrate.grid(row=1, column=1)
        cb_baudrate.set(baudrate)
        cb_bytesize=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_bytesize)
        cb_bytesize.grid(row=2, column=1)
        cb_bytesize.set(bytesize)
        cb_stopbits=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_stopbits)
        cb_stopbits.grid(row=3, column=1)
        cb_stopbits.set(stopbits)
        cb_parity=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_parity)
        cb_parity.grid(row=4, column=1)
        cb_parity.set(parity)
        cb_timeout=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_timeout)
        cb_timeout.grid(row=5, column=1)
        cb_timeout.set(timeout)
            
        #Create a Save-Button in the serial port window
        save_button = tk.Button(serialport_window, text='Save', font=('Arial', 12), command=serial_save)
        save_button.grid(row=8, column=1, sticky='n', pady=4)
        
        #Run the serial port window
        serialport_window.mainloop()
    
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
        
        #Get the new image size
        try:
            xPix = int(self.entry_Xpix.get())
            yPix = int(self.entry_Ypix.get())
            self.img_pil_mod = imagework.convert_grey_downsize(self.file, xPix, yPix, True)
            self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        except:
            xPix = self.img_pil.width
            yPix = self.img_pil.height
            print('Using default image size')
            
        #Crop image if nessecary
        cropping = self.entry_crop.get()
        if cropping != 'none':
            self.img_pil_mod = imagework.crop_image(cropping, self.img_pil_mod)
            self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        self.label_img_mod.configure(image=self.img_tk_mod)
        self.label_img_lbl_mod.configure(text='Modified Image')
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
        self.exposeArr = []
        for i in range(0,256):
            self.exposeArr.append(0)
        #Parse through the user's entry based upon comma and bracket location
        lines=self.exposure_details.get('1.0','end-1c').splitlines()
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
        lines = self.ignore_details.get('1.0','end-1c').splitlines()
        for s in lines:
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
        self.label_end_time_est.configure(text='Estimated End Time: ' + 
                    (datetime.now() + exp).strftime('%H:%M:%S -- %d/%m/%Y'))
    
    def get_serial_config(self, port_name):
        '''
        Gets the serial aconfigurations for a particular device. 
        Arguments:
            (arg1) port_name (string) : name of the port to be configured
        Returns:
            (ret1) port, baudrate, bytesize, stopbits, parity, timeout (tuple)
        '''
        
        file = open(port_name + " Serial Port Values.txt", "r")
        lines = file.readlines() #reads line by line
        port = lines[0].rstrip() #".rstrip()"method removes any trailing characters (characters at the end of a string)
        baudrate = int(lines[1]) #"lines[]" reads only one specific line
        bytesize = int(lines[2])
        stopbits = float(lines[3])
        parity = lines[4].rstrip()
        timeout = float(lines[5])
        file.close()
        return (port, baudrate, timeout, stopbits, bytesize, parity)
    
    def run_experiment(self):
        '''
        Runs the experiment by controlling motor and shutter.
        '''
        
        self.label_start_time.configure(text = 'Start Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.listbox.activate(0)
        #Number of pixels size of image on hologram, distance each movement
        width = float(self.entry_width.get())
        height = float(self.entry_height.get())
        xPix = len(self.img_as_arr) 
        yPix = len(self.img_as_arr[0]) 
        xDelta = 1.0 * width / xPix
        yDelta = 1.0 * height / yPix
        #Serial Configurations
        cfg_sht = self.get_serial_config('Shutter')
        cfg_mtr = self.get_serial_config('Motor')
        #Movement
        try:
            #Motor, Shutter control
            shutter = Shutter(cfg_sht[0],cfg_sht[1],cfg_sht[2],cfg_sht[3],cfg_sht[4])
            motor = Motor(cfg_mtr[0],cfg_mtr[1],cfg_mtr[2],cfg_mtr[3],cfg_mtr[4])
            motor.configureAxis(axis=1, velocity=1.0, acceleration=4, moveHome=True)
            motor.configureAxis(axis=2, velocity=1.0, acceleration=4, moveHome=True)
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
                    cur_pix = self.img_as_arr[j][i]
                    if self.expose_arr[cur_pix] != 0:
                        if onRow == False:
                            motor.moveAbsolute(axis=2, goToPos=i*yDelta*1000)
                        motor.moveAbsolute(axis=1, goToPos=j*xDelta*1000)
                        onRow = True
                        shutter.toggle_shutter(self.expose_arr[cur_pix])
        except:
            print('An error has occured:')
        finally:
            #Ensure all serial ports are closed ect
            print('Closing the shutter and all serial ports')
            shutter.ser.close()
            motor.ser.close()
            shutter.ser.close()
        
        #Print the time the experiment finished
        self.label_end_time.configure(text = 'Experiment End Time: ' + datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
            

#MainLoop
root = tk.Tk()
app = SingleImageCreator(root)
root.mainloop()