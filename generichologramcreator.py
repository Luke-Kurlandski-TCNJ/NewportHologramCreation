# -*- coding: utf-8 -*-

"""
Create images upon a hologram.

Created on 10/1/19
Updated on 11/1/19

Copyright 2019, Luke Kurlandski, All rights reserved.

GenericImageCreator is designed to provide a simple, user interface to facilitate
the creation of image holograms upon a film. This program inherits from App.

This program was written by Luke Kurlandski and is his intellectual property. 

Luke Kurlandski recieved assistence from Matthew VanSoelen and Daniel Stolz. 

Dr. David McGee has permission to use this code in whatever way he sees fit.
"""

#Graphical User Interface tools
import tkinter as tk
from tkinter import ttk

#Communication with serial ports
import serial 
import serial.tools.list_ports 

#Support image processing
import imagemodification
import numpy

from app import App

class GenericImageCreator(App):
    """
    Create various kinds of images on a hologram.
    
    Notes:
        Parent class
        Place Tkinter stuff at the top. This will eventually be moved into its
            own class.
    """
    
    def __init__(self, root, window_width, window_height, window_title):
        """
        Constructor for generic image creation process.
        
            Arguments:
                (arg1) root (Tk.Tk) : main window
                (arg2) window_width (int) : width of the main window
                (arg3) window_height (int) : height of the main window
                (arg4) window_title (string) : title of the main window
        """
        
        #Use App's constructor
        super().__init__(root, window_width, window_height, window_title)
        #Error window with textbox filling window
        self.window_communication = self.pop_up_window(self.root, 'Communication Window', 660, 425, True, -200, -20) 
        self.set_up_menu(self.window_communication)
        self.text_communication = tk.Text(self.window_communication)
        self.text_communication.grid(sticky = tk.N+tk.S+tk.E+tk.W)
        self.window_communication.grid_columnconfigure(0, weight = 1)
        self.window_communication.grid_rowconfigure(0, weight = 1)
        self.apply_scrollbars(self.window_communication, self.text_communication, True, True)
        #Default laser settings
        self.laser_maximum = -1
        self.laser_pause = 0
    
    def image_as_array(self, window, img_pil, title):
        """
        Convert an image into an array and display array in a new window.
        
        Arguments:
            (arg1) window (tk.Toplevel)  : window to open new window off of
            (arg2) img_pil (Pil image) : image to process into an array and display as array
            (arg3) title (string) : what the new window should be called
            
        Returns:
            (ret) img_as_arr (list[list[int]]) : the image converted into an array
        """
        
        #Configure array window, display, and scrollbars
        array_window = tk.Toplevel(window)
        text_arr = tk.Text(array_window)
        text_arr.grid(sticky=tk.N + tk.S + tk.E + tk.W)
        array_window.grid_columnconfigure(0, weight = 1)
        array_window.grid_rowconfigure(0, weight = 1)
        self.set_up_menu(array_window)
        self.apply_scrollbars(array_window, text_arr, True, True)
        
        #Print the array to screen
        img_as_arr_ret = imagemodification.get_image_array(img_pil)
        img_as_arr = numpy.transpose(img_as_arr_ret)
        for i in img_as_arr:
            for j in i:
                spaces = '   '
                if j > 9:
                    spaces = '  '
                if j > 99:
                    spaces = ' '
                text_arr.insert(tk.END, str(j)+spaces)
            text_arr.insert(tk.END,'\n')
        array_window.configure(width=100, height=100)
        return img_as_arr_ret
    
    def generate_exposure_details(self, exposure, ignore, laser):
        """
        Generate the arrays to describe laser exposure lengths.
        
        Arguments:
            (arg1) exposure (list[string]) : special strings containing exposure details
            (arg2) ignore (list[string]) : special strings containing ignore details
            (arg3) laser (list[string]) : special string containing laser details
            
        Return:
            (ret1) exposure_arr (list[int]) : mapping of pixel values to exposure time
            (ret2) laser_arr (list[int]) : mapping of pixel values to laser intensity
        """
        
        #Generate the exposure array and process exposure
        exposure_arr = []
        for i in range(0,256):
            exposure_arr.append(0)
        for line in exposure:
            comma = line.find(',')
            bracket = line.find(']')
            start = int(line[1:comma])
            end = int(line[comma+1:bracket])
            x = line.find('x')
            if x == -1:
                expos_time = float(line[bracket+2:len(line)])
                for i in range(start, end):
                    exposure_arr[i] = expos_time
            else:
                mlt_fctr = float(line[bracket+2:x])
                for i in range(start,end):
                    exposure_arr[i] = round(mlt_fctr*i,2)
                    
        #Modify exposure array and process ignore
        for line in ignore:
            comma = line.find(',')
            bracket = line.find(']')
            start = int(line[1:comma])
            end = int(line[comma+1:bracket])
            for i in range(start,end):
                exposure_arr[i] = 0
                
        #Generate laser array and process laser
        laser_arr = []
        for i in range(0,256):
            laser_arr.append(0)
        for line in laser:
            comma = line.find(',')
            bracket = line.find(']')
            start = int(line[1:comma])
            end = int(line[comma+1:bracket])
            x = line.find('x')
            if x == -1:
                expos_power = float(line[bracket+2:len(line)])
                for i in range(start, end):
                    laser_arr[i] = expos_power
            else:
                mlt_fctr = float(line[bracket+2:x])
                for i in range(start,end):
                    laser_arr[i] = round(mlt_fctr*i,2)
        return exposure_arr, laser_arr
    
    def setup_serial_port(self, port_name):
        """
        Set up the serial port menu and write configurations to a file. 
        
        Notes:
            Writes user choices in: 'Serial Port Congifurations ' + port_name + '.txt'
            
        Arguments:
            (arg1) port_name (string) : machinery the port is controlling
        """
    
        def serial_save():
            """
            Save the user selected configurations in a .txt file.
            
            Notes: 
                Nested function allows for elegant access of the combo boxes
                Nested functions may cause problems with inheritence
            """
            
            port = cb_port.get()
            baudrate = cb_baudrate.get()
            timeout = cb_timeout.get()
            stopbits = cb_stopbits.get()
            bytesize = cb_bytesize.get()
            parity = cb_parity.get()
            #Creating a file for the serial port values
            file = open('Serial Port Congifurations ' + port_name + '.txt', 'w')
            file.write(port + '\n' + baudrate + '\n' + timeout + '\n' + stopbits + '\n' + bytesize + '\n' + parity)
            file.close()
            serialport_window.destroy()
            
        #Create serial port window
        serialport_window = tk.Toplevel(self.root) 
        serialport_window.title('Serial Port: ' + port_name)
        serialport_window.resizable(False, False)  
        serialport_window_height = 200
        serialport_window_width = 280
        screen_width = serialport_window.winfo_screenwidth()
        screen_height = serialport_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (serialport_window_width/2))
        y_cordinate = int((screen_height/2) - (serialport_window_height/2))
        serialport_window.geometry("{}x{}+{}+{}".format(serialport_window_width, serialport_window_height, x_cordinate, y_cordinate))
        
        #Create a menu bar in the serial port window
        self.set_up_menu(serialport_window)
        
        #Create labels for the port window
        tk.Label(serialport_window, text="Port:", font=('Arial', 12)).grid(row=0, column=0)
        tk.Label(serialport_window, text="Baudrate:", font=('Arial', 12)).grid(row=1, column=0)
        tk.Label(serialport_window, text="Timeout:", font=('Arial', 12)).grid(row=2, column=0) 
        tk.Label(serialport_window, text="Stopbits:", font=('Arial', 12)).grid(row=3, column=0)
        tk.Label(serialport_window, text="Bytesize:", font=('Arial', 12)).grid(row=4, column=0)
        tk.Label(serialport_window, text="Parity:", font=('Arial', 12)).grid(row=5, column=0)

        #Construct the users choices for serial configurations
        data_port = []
        comlist = serial.tools.list_ports.comports()
        for i in comlist:
            data_port.append(i.device)
        data_baudrate = ("75", "110", "134", "150", "300", "600", "1200", "1800", "2400", "4800", "7200", "9600", "14400", "19200", "38400", "57600", "115200", "128000")
        data_timeout = ("0.1", "0.5", "1", "1.5", "2")
        data_stopbits = ("1", "1.5", "2")
        data_bytesize = ("4", "5", "6", "7", "8")
        data_parity = ("None", "Even", "Odd", "Space", "Mark")
        
        #Create combo boxes for the user to select options from
        cb_port=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_port)
        cb_port.grid(row=0, column=1)
        cb_baudrate=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_baudrate)
        cb_baudrate.grid(row=1, column=1)
        cb_timeout=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_timeout)
        cb_timeout.grid(row=2, column=1)
        cb_stopbits=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_stopbits)
        cb_stopbits.grid(row=3, column=1)
        cb_bytesize=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_bytesize)
        cb_bytesize.grid(row=4, column=1)
        cb_parity=ttk.Combobox(serialport_window, width = 12, font=('Arial', 12), values=data_parity)
        cb_parity.grid(row=5, column=1)
        
        #Get the previous serial configurations from the file and print to combo boxes
        try: 
            file = open('Serial Port Congifurations ' + port_name + '.txt', 'r')
            lines = file.readlines()
            cb_port.set(lines[0].rstrip())
            cb_baudrate.set(lines[1].rstrip())
            cb_timeout.set(lines[2].rstrip())
            cb_stopbits.set(lines[3].rstrip())
            cb_bytesize.set(lines[4].rstrip())
            cb_parity.set(lines[5].rstrip())
        except FileNotFoundError as e:
            message = '\nCannot find a previous instance of: \'Serial Port Congifurations ' + port_name + '.txt\''
            message += str(e) 
            self.text_communication.insert(tk.END, message)
            
        #Create a Save-Button in the serial port window
        save_button = tk.Button(serialport_window, text='Save', font=('Arial', 12), command=serial_save)
        save_button.grid(row=8, column=1, sticky='n', pady=4)
        
        #Run the serial port window
        serialport_window.mainloop()
            
    def get_serial_config(self, port_name):
        """
        Read correct file to get serial configuations for a device. 
        
        Arguments:
            (arg1) port_name (string) : name of the port to be configured.

        Returns:
            (ret1) port (int) : port number to appended to COM
            (ret2) baudrate : baudrate of the affiliated serial port
            (ret3) timeout : timeout of the affiliated serial port
            (ret4) stopbits : stopbits of the affiliated serial port
            (ret5) bytesize : bytesize of the affiliated serial port
            (ret6) parity : parity of the affiliated serial port
        """
        
        #Read the file and read the data line by line
        try:
            file = open('Serial Port Congifurations ' + port_name + '.txt', "r")
            lines = file.readlines() 
            port = lines[0].rstrip() 
            baudrate = int(lines[1].rstrip()) 
            timeout = float(lines[2].rstrip())
            stopbits = float(lines[3].rstrip())
            bytesize = int(lines[4].rstrip())
            parity = lines[5].rstrip()
            file.close()
            return (port, baudrate, timeout, stopbits, bytesize, parity)
        except FileNotFoundError:
            raise FileNotFoundError('\nYou have not specified any serial port information for the ' 
                + port_name + ' and there is no record of information from a prior experiment.\n')
        except Exception as e:
            file.close()
            raise e
    
    def store_previous_data(self, file_name, subjects, datas):
        """
        Store data entered on the main screen in a txt file for later use.
        
        Arguments:
            (arg1) file_name (string) : name of txt file
            (arg2) subjects (list[string]) : subject headers to proceed data in file
            (arg3) datas (list[string]) : the data pulled from the UI
        """
        
        with open(file_name, 'w') as file:
            for i,j in zip(subjects,datas):
                file.write(str(i).rstrip() + '\n')
                file.write(str(j).rstrip() + '\n')
    
    def laser_settings(self):
        """
        Saves the laser settings into a file.
        
        Notes:
            Easily expandable to include more settings.
            Modify get_laser_settings as needed.
        
        Arguments:
            (arg1) previous (float) : the maximum power from previous experiment, overwritten
        """
        
        def laser_save():
            """
            Saves the laser settings.
            """
            
            self.text_communication.insert(tk.END, '\tSaving the laser settings.\n')
            laser_subjects = ['Laser Power', 'Power Change Pause']
            laser_data = [entry_power.get(), entry_pause.get()]
            self.store_previous_data('Laser Settings.txt', laser_subjects, laser_data)
            window.destroy()
        
        #Laser setting options
        window = self.pop_up_window(self.root, 'Laser Settings', 100, 250)
        self.set_up_menu(window)
        tk.Label(window, text = 'Maximum Laser Power (mW):').grid(row=0, column=0)
        entry_power = tk.Entry(window, width=10)
        entry_power.grid(row=0, column=1, sticky = tk.W)
        tk.Label(window, text = 'Power Change Pause:').grid(row=1, column=0)
        entry_pause = tk.Entry(window, width=10)
        entry_pause.grid(row=1, column=1, sticky = tk.W)
        #Get previous configurations and fill
        try:
            self.text_communication.insert(tk.END, 'Getting previous experiment\'s laser settings.\n')
            file = open('Laser Settings.txt', 'r')
            lines = file.readlines()
            entry_power.insert(0, lines[1])
            entry_pause.insert(0, lines[3])
            file.close()
        except FileNotFoundError:
            self.text_communication.insert(tk.END, '\tNo previous laser settings detected.\n')
        except Exception:
            file.close()
            self.text_communication.insert(tk.END, '\tPrevious laser setting were incomplete.\n')
        #Warning and save button
        button_save = tk.Button(window, text = 'Save Correct Settings', command = laser_save)
        button_save.grid(row=2, column=0, columnspan=2)
    
    def shutter_settings(self):
        """
        FIXME: implement
        """
        
        self.pop_up_window(self.root, 'Shutter Settings')
        tk.Label(text='Shutter Settings are coming soon!')
        
    def motor_settings(self):
        """
        FIXME: implement
        """ 
        
        self.pop_up_window(self.root, 'Motor Settings')
        tk.Label(text='Motor Settings are coming soon!')
    
    def get_laser_settings(self): #FIXME: modify into a general, get settings
        """
        Get the laser settings from a file.
        
        Returns:
            (ret1) lines[1] (float) : the maximum power read from the file
            (ret2) None (None) : placeholder for more settings to be implemented
        """
        
        try:
            file = open('Laser Settings.txt', 'r')
            lines = file.readlines()
            file.close()
            return float(lines[1].rstrip()), float(lines[3].rstrip())
        except FileNotFoundError:
            raise FileNotFoundError('You have not specified any settings for the laser and there is no record of information from a prior experiment.\n')
        except Exception:
            file.close()
        



