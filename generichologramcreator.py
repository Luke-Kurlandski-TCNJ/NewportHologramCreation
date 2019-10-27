# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:35:26 2019

@author: Luke Kurlandski
"""

import tkinter as tk #GUI library
from tkinter import ttk #GUI library extension
import serial #Communication with serial ports
import serial.tools.list_ports #Listing the COM ports
import imagework #package to support image modification

class GenericImageCreator:
    """
    Create various kinds of images on a hologram.
    
    Notes:
        Parent class
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
        
        #Set up the root
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2) - 50)
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.root.title(window_title)
        
    def set_up_frames(self, window, frames_horizontal, frames_vertical):
        """
        Create and orgainze a set of frames for any window.
        
        Arguments:
            (arg1) window (tk.Toplevel) : window to apply help window to
            (arg2) frames_horizontal (int) : number of frames to create in x direction
            (arg3) frames_vertical (int) : number of frames to create in y direction
            
        Returns:
            (ret1) frames (list[list[tk.Frame]]) : 2-D list of frames 
        """
    
        frames = []
        for i in range (0, frames_vertical):
            temp = []
            for j in range (0, frames_horizontal):
                frame = tk.Frame(window)
                frame.grid(row = i, column = j, pady = 10)
                temp.append(frame)
            frames.append(temp)
        return frames
    
    def apply_scrollbars(self, master, wigit, x=False, y=False, xrow=1, xcol=0, yrow=0, ycol=1):
        """
        Apply scrollbars to a master tk widgit or window ect.
        
        Notes:
            Not thoroughly tested for strong flexibility. 
        
        Arguments:
            (arg1) master (tk wigit) : container for the widgit to recieve scroll bars
            (arg2) wigit (tk wigit) : wigit to recieve the scroll bars
            (arg3) x (boolean) : apply scrollbar in x direction
            (arg4) y (boolean) : apply scrollbar in y direction
            (arg5) xrow (int) : row to use with the grid() placement for xscrollbar
            (arg6) xcol (int) : column to use with the grid() placement for xscrollbar
            (arg7) yrow (int) : row to use with the grid() placement for y scrollbar
            (arg8) ycol (int) : column to use with the grid() placement for y scrollbar
        """
        
        yscrollcommand = None
        xscrollcommand = None
        if x == True:
            scrollbar_x = tk.Scrollbar(master, orient = tk.HORIZONTAL, command = wigit.xview)
            scrollbar_x.grid(row=xrow, column=xcol, sticky = tk.W + tk.E)
            xscrollcommand = scrollbar_x.set
        if y == True:
            scrollbar_y = tk.Scrollbar(master, orient = tk.VERTICAL, command = wigit.yview)
            scrollbar_y.grid(row=yrow, column=ycol, sticky = tk.N + tk.S)
            yscrollcommand = scrollbar_y.set
        wigit.configure(yscrollcommand = yscrollcommand, 
                         xscrollcommand = xscrollcommand, wrap = tk.NONE)
        
    def set_up_menu(self, window):
        """
        Create a standard menu bar for any window.
        
        Arguments:
            (arg1) window (tk.Toplevel) : window to apply help window to
            
        Returns:
            (ret) menu (tk.Menu) : the newly created menu widgit
        """
        
        menu = tk.Menu(window)
        window.config(menu=menu)
        menu.add_command(label='Quit Window', command=window.destroy)
        return menu
    
    def main_help(self, window, subject):
        """
        Read the instructions from a file and print on a popup window.
        
        Arguments:
            (arg1) window (tk.Toplevel) : window to apply help window to
            (arg2) subject (string) : subject user requires assistence with
        """
        
        help_window = self.help_me(window, 'Help : ' + subject, 400, 800)
        try:
            file = open('Help ' + subject + '.txt', 'r')
        except:
            print('Not found')
            tk.Label(help_window, text = 'Nothing to help you with at the moment').pack()
            return
        text = tk.Text(help_window, width=95, height=22)
        text.grid()
        text.insert(tk.INSERT, file.read())
        self.apply_scrollbars(help_window, text, True, True)
        file.close()
        
    def help_me(self, window, title='Help', help_window_height=150, help_window_width=200):
        """
        Create a 'help me' pop up window for any window.
        
        Arguments:
            (arg1) window (tk.Toplevel) : window to apply help window to
            (arg2) title (string) : name for the window
            (arg3) help_window_height (int) : size of window in y direction
            (arg4) help_window_width (int) : size of window in x direction
            
        Returns:
            (ret1) help_window (tk.Toplevel) : the help window
        """
        
        help_window = tk.Toplevel(window) 
        self.set_up_menu(help_window)
        help_window.title(title)
        help_window.resizable(True, True)
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (help_window_width/2))
        y_cordinate = int((screen_height/2) - (help_window_height/2))
        help_window.geometry("{}x{}+{}+{}".format(help_window_width, help_window_height, x_cordinate, y_cordinate))
        return help_window
    
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
        xPix = img_pil.width
        yPix = img_pil.height
        array_window = tk.Toplevel(window)
        self.set_up_menu(array_window)
        tk.Label(array_window, text = title).pack(side = tk.TOP)
        scrollbar_y = tk.Scrollbar(array_window)
        scrollbar_y.pack(side = tk.RIGHT, fill = tk.Y)
        scrollbar_x = tk.Scrollbar(array_window, orient = tk.HORIZONTAL)
        scrollbar_x.pack(side = tk.BOTTOM, fill = tk.X)
        text_arr = tk.Text(array_window, yscrollcommand = scrollbar_y.set, 
                xscrollcommand = scrollbar_x.set, width = xPix*4, height = yPix, wrap = tk.NONE)
        text_arr.pack()
        scrollbar_y.configure(command = text_arr.yview)
        scrollbar_x.configure(command = text_arr.xview)
        #Print the array to screen
        img_as_arr = imagework.get_image_array(img_pil)
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
        return img_as_arr
    
    def generate_exposure_details(self, exposure, ignore):
        """
        Generate the arrays to describe laser exposure lengths.
        
        Arguments:
            (arg1) exposure (list[string]) : special strings containing exposure details
            (arg2) ignore (list[string]) : special strings containing ignore details
            
        Return:
            (ret) exposure_arr (list[int]) : mapping of pixel values to exposure time
        """
        
        #Generate the exposure array
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
                    exposure_arr[i] = mlt_fctr*i
        #Override with 0s, for the ignore array
        for line in ignore:
            comma = line.find(',')
            bracket = line.find(']')
            start = int(line[1:comma])
            end = int(line[comma+1:bracket])
            for i in range(start,end):
                exposure_arr[i] = 0
        return exposure_arr
    
    def setup_serial_port(self, port_name):
        """
        Set up the serial port menu and write configurations to a file. 
        
        Notes:
            Writes user choices into file: port_name + " Serial Port Values.txt"
            
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
            bytesize = cb_bytesize.get()
            stopbits = cb_stopbits.get()
            parity = cb_parity.get()
            timeout = cb_timeout.get()
            #Creating a file for the serial port values
            file = open(port_name + " Serial Port Values.txt","w")
            file.write(port + "\n" + baudrate + "\n" + bytesize + "\n" + stopbits + "\n" + parity + "\n" + timeout )
            file.close()
            serialport_window.destroy()
        
        #Get the previous serial configurations from the file
        port, baudrate, timeout, stopbits, bytesize, parity = self.get_proper_file_info(port_name)
        
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
        serialport_window_menubar.add_command(label="Help", command=lambda: self.serial_help(serialport_window))
        
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
        
    def get_proper_file_info(self, port_name):
        """
        Open the file containing previous configurations and read.
        
        Notes:
            Handles incorrect file format or file not found with recursive calls
            May have logical errors in Exception handling
        
        Arguments:
            (arg1) port_name (string) : machinery the port is controlling
        
        Returns:
            (ret1) port (int) : port number to appended to COM
            (ret2) baudrate : baudrate of the affiliated serial port
            (ret3) bytesize : bytesize of the affiliated serial port
            (ret4) stopbits : stopbits of the affiliated serial port
            (ret5) parity : parity of the affiliated serial port
            (ret6) timeout : timeout of the affiliated serial port
        """
        
        try:
            #Open file and ensure proper format
            file = open(port_name + ' Serial Port Values.txt', 'r')
            lines = file.readlines()
            count = len(lines)
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
            return (port, baudrate, timeout, stopbits, bytesize, parity)
        except FileNotFoundError:
            #Create the file and fill with sample values
            file = open(port_name + " Serial Port Values.txt","w")
            file.write("str" + "\n" + "int" + "\n" + "int" + "\n" + "float" + "\n" + "str" + "\n" + "float")
            file.close()
            return self.get_proper_file_info(port_name)
        except Exception:
            #Incorrect format
            file.close()
            file = open(port_name + " Serial Port Values.txt","w")
            file.write("str" + "\n" + "int" + "\n" + "int" + "\n" + "float" + "\n" + "str" + "\n" + "float")
            file.close()
            return self.get_proper_file_info(port_name)
        
    def serial_help(self, serialport_window):
        """
        Create a help window specifically for the serial port window.
        
        Arguments:
            (arg1) serialport_window (tk.Toplevel) : window of the serial port
        """
        
        help_window = self.help_me(serialport_window, False)
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
        
    def get_serial_config(self, port_name):
        """
        Read correct file to get serial configuations for a device. 
        
        Arguments:
            (arg1) port_name (string) : name of the port to be configured.

        Returns:
            (ret1) port (int) : port number to appended to COM
            (ret2) baudrate : baudrate of the affiliated serial port
            (ret3) bytesize : bytesize of the affiliated serial port
            (ret4) stopbits : stopbits of the affiliated serial port
            (ret5) parity : parity of the affiliated serial port
            (ret6) timeout : timeout of the affiliated serial port
        """
        
        #Read the file and read the data line by line
        try:
            file = open(port_name + " Serial Port Values.txt", "r")
        except FileNotFoundError:
            self.error_window(self.root, 'You have not specified serial port information.')
        lines = file.readlines() 
        port = lines[0].rstrip() 
        baudrate = int(lines[1]) 
        bytesize = int(lines[2])
        stopbits = float(lines[3])
        parity = lines[4].rstrip()
        timeout = float(lines[5])
        file.close()
        return (port, baudrate, timeout, stopbits, bytesize, parity)
    
    def error_window(self, window, message):
        """
        Launch an error window on the affiliated screen.
        
        Arguments:
            (arg1) window (tk.Toplevel) : window the error window is attatched to
            (arg2) message (string) : error message to display on screen
        """
        
        error_window = tk.Toplevel(window) 
        error_window.title("Error")
        error_window.resizable(False, False)
        error_window_height = 150
        error_window_width = 200
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (error_window_width/2))
        y_cordinate = int((screen_height/2) - (error_window_height/2))
        error_window.geometry("{}x{}+{}+{}".format(error_window_width, error_window_height, x_cordinate, y_cordinate))
        tk.Label(text = message, font = 'Bold').pack()