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
import os #Allows for file writing
#import movement #package which drives motor and shutter
import imagework #package to support image modification
from serialcontrol import Motor, Shutter #Allows communication with machinery

class MyGUI:
    def __init__(self, root):
        '''
        Constructor for myGUI class
        Arguments:
            (arg1) root : the root object (tkinter object)
        '''
        
        #Set up root
        self.root = root
        root_window_height = 600
        root_window_width = 1200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (root_window_width/2))
        y_cordinate = int((screen_height/2) - (root_window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(root_window_width, 
                           root_window_height, x_cordinate, y_cordinate))
        self.root.title('Main Hologram Creation')
        #Set up menu
        self.menu = tk.Menu(self.root)
        self.menu.add_command(label='Quit', command=self.root.destroy)
        self.menu.add_command(label='Motor Serial', command=lambda: self.setup_serial_port('Motor'))
        self.menu.add_command(label='Shutter Serial', command=lambda: self.setup_serial_port('Shutter'))
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
        #Set up timing/position information
        self.label_start_time = tk.Label(self.frame_0x3, text='Start Time: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_start_time.pack()
        self.label_end_time = tk.Label(self.frame_0x3, text='Experiment End Time: In Progress')
        self.label_end_time.pack()
        self.label_end_time_est = tk.Label(self.frame_0x3, text='End Time Estimate: '+ datetime.now().strftime('%H:%M:%S -- %d/%m/%Y'))
        self.label_end_time_est.pack()
        self.label_position = tk.Label(self.frame_0x3, text='Current Pixel (x,y): (x,y)')
        self.label_position.pack()
        #Set up run button and pause/abort box
        self.button_run = tk.Button(self.frame_0x3, text = 'Run Experiment', command=self.run_experiment)
        self.button_run.pack()
        self.listbox = tk.Listbox(self.frame_0x3, height=3)
        self.listbox.pack()
        self.listbox.insert(1, "Run-Mode")
        self.listbox.insert(2, "Pause-Mode")
        self.listbox.insert(3, "Abort")
        self.listbox.activate(1)
    
    def setup_serial_port(self, port_name):
        '''
        Sets up the serial port menu.
            @author Daniel Stolz and Luke Kurlandski
        Arguments:
            (arg1) port_name (string) : machinery the port is controlling
        '''
        
        # Creating a serial port window
        serialport_window = tk.Toplevel(self.root) 
        serialport_window.title(port_name + ' Serial-Port')
        # Center the window on the screen
        serialport_window.resizable(False, False)  
        serialport_window_height = 200
        serialport_window_width = 280
        screen_width = serialport_window.winfo_screenwidth()
        screen_height = serialport_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (serialport_window_width/2))
        y_cordinate = int((screen_height/2) - (serialport_window_height/2))
        serialport_window.geometry("{}x{}+{}+{}".format(serialport_window_width, serialport_window_height, x_cordinate, y_cordinate))
        
        # Function to fill in a Help Menu for users
        def open_help():
            global help_window #FIXME
            help_window = tk.Toplevel(self.root) 
            help_window.title("Help")
            # Help-Window, centering on the screen
            help_window.resizable(False, False)  # This code helps to disable windows from resizing
            help_window_height = 150
            help_window_width = 200
            screen_width = help_window.winfo_screenwidth()
            screen_height = help_window.winfo_screenheight()
            x_cordinate = int((screen_width/2) - (help_window_width/2))
            y_cordinate = int((screen_height/2) - (help_window_height/2))
            help_window.geometry("{}x{}+{}+{}".format(help_window_width, help_window_height, x_cordinate, y_cordinate))
            # Label in the Help-Window
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
            # End of the Help-Window
            help_window.mainloop()
        
        # Creating a help menubar in the serial port window
        serialport_window_menubar = tk.Menu(serialport_window)
        serialport_window_menubar.add_command(label="Help", command=open_help)
        serialport_window.config(menu=serialport_window_menubar)        
        
        # Function for creating a Save-File with dummy entries for the Serial-Port values 
        def create_file():
            file = open(port_name + " Serial Port Values.txt","w")
            file.write("str" + "\n" + "int" + "\n" + "int" + "\n" + "float" + "\n" + "str" + "\n" + "float")
            file.close()
        
        # Function for reading a Save-File
        def read_file():
            '''
            Arguments:
                (arg1) is_digit (boolean) : if true, returns boolean values
            Returns:
                (ret) tuple (int) : the port, baudrate, stopbits, parity, and timeout
                
            '''
            file = open(port_name + ' Serial Port Values.txt', 'r')
            lines = file.readlines()
            #".rstrip()"method removes any trailing characters
            #".isdigit()"method runs True if all characters in the string are digits
            port = lines[0].rstrip() 
            baudrate = lines[1].rstrip()
            bytesize = lines[2].rstrip()
            stopbits = lines[3].rstrip()
            parity = lines[4].rstrip()     
            timeout = lines[5].rstrip()
            file.close()
            return (port, baudrate, timeout, stopbits, bytesize, parity)
    
        # Function for creating text input boxes (comboboxes) in the Serialport-Window
        def create_entry():
            # Gets a list of all COM ports
            comlist = serial.tools.list_ports.comports()
            connected = []
            for element in comlist:
                connected.append(element.device)
            # Sets up user's choices for serial options
            data_port = (connected)
            data_baudrate = ("75", "110", "134", "150", "300", "600", "1200", "1800", "2400", "4800", "7200", "9600", "14400", "19200", "38400", "57600", "115200", "128000")
            data_bytesize = ("4", "5", "6", "7", "8")
            data_stopbits = ("1", "1.5", "2")
            data_parity = ("N", "E", "O", "S", "M")
            data_timeout = ("0.1", "0.5", "1", "1.5", "2")
            # Sets up combo boxes to display user's choices
            global cb_port
            cb_port=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_port)
            cb_port.grid(row=0, column=1)
            global cb_baudrate
            cb_baudrate=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_baudrate)
            cb_baudrate.grid(row=1, column=1)
            global cb_bytesize
            cb_bytesize=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_bytesize)
            cb_bytesize.grid(row=2, column=1)
            global cb_stopbits
            cb_stopbits=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_stopbits)
            cb_stopbits.grid(row=3, column=1)
            global cb_parity
            cb_parity=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_parity)
            cb_parity.grid(row=4, column=1)
            global cb_timeout
            cb_timeout=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_timeout)
            cb_timeout.grid(row=5, column=1)
        
        # Function for creating the labels in the Serialport-Window       
        def create_label():
            label_port = tk.Label(serialport_window, text="Port:", font=('Arial', 12))
            label_port.grid(row=0, column=0)
            label_baudrate = tk.Label(serialport_window, text="Baud rate:", font=('Arial', 12))
            label_baudrate.grid(row=1, column=0) 
            label_bytesize = tk.Label(serialport_window, text="Byte size:", font=('Arial', 12))
            label_bytesize.grid(row=2, column=0)
            label_stopbits = tk.Label(serialport_window, text="Stop bits:", font=('Arial', 12))
            label_stopbits.grid(row=3, column=0)
            label_parity = tk.Label(serialport_window, text="Parity:", font=('Arial', 12))
            label_parity.grid(row=4, column=0)
            label_timeout = tk.Label(serialport_window, text="Timeout:", font=('Arial', 12))
            label_timeout.grid(row=5, column=0)    
        
        try:
            # Get the port ect from file
            port, baudrate, timeout, stopbits, bytesize, parity = read_file()
        except: 
            print('Going to have to create a new file')
        
        # Function for setting the comboboxes
        def set_combobox():
            cb_port.set(port)
            cb_baudrate.set(baudrate)
            cb_bytesize.set(bytesize)
            cb_stopbits.set(stopbits)
            cb_parity.set(parity)
            cb_timeout.set(timeout)
     
        # Prevent input errors
        if os.path.isfile(port_name + " Serial Port Values.txt"):
            # Number of lines in the text file 
            count = len(open(port_name + " Serial Port Values.txt").readlines()) 
            # If not 6 lines, create a new file
            if count != 6:
                create_file()
                read_file()
                create_label()
                create_entry()
                
            read_file()
            # Check data
            if (port.isdigit() == True or baudrate.isdigit() == False or bytesize.isdigit() == False or
                stopbits.replace('.', '').isdigit() == False  or parity.isdigit() == True or 
                    timeout.replace('.', '').isdigit() == False):  
                create_file()
                read_file()
                create_label()
                create_entry()  
            else:
                read_file()
                create_label()
                create_entry()
                set_combobox()
        #If the file is not found, create a file        
        else:
            create_file()
            read_file()
            create_label()
            create_entry()
            
        # Function for saving of the values of the Serial-Port in a .txt-file
        def save():
            a = cb_port.get()
            b = cb_baudrate.get()
            c = cb_bytesize.get()
            d = cb_stopbits.get()
            e = cb_parity.get()
            f = cb_timeout.get()
            # Creating a Save-File for the Serial-Port values
            file = open(port_name + " Serial Port Values.txt","w")
            file.write(a + "\n" + b + "\n" + c + "\n" + d + "\n" + e + "\n" + f )
            file.close()
            serialport_window.destroy()
            help_window.destroy()
            
        # Creating a Save-Button in the Serialport-Window
        save_button = tk.Button(serialport_window, text='Save', font=('Arial', 12), command=save)
        save_button.grid(row=8, column=1, sticky='n', pady=4)
        # End of the Serialport-Window
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
        
        try:
            xPix = int(self.entry_Xpix.get())
            yPix = int(self.entry_Ypix.get())
            self.img_pil_mod = imagework.convert_grey_downsize(self.file, xPix, yPix, True)
            self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        except:
            xPix = self.img_pil.width
            yPix = self.img_pil.height
            print('Using default image size')
        cropping = self.entry_crop.get()
        if cropping != 'none':
            self.img_pil_mod = imagework.crop_image(cropping, self.img_pil_mod)
            self.img_tk_mod = ImageTk.PhotoImage(self.img_pil_mod)
        else:
            print('No cropping occured')
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
app = MyGUI(root)
root.mainloop()