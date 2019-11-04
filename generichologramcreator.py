# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:35:26 2019

@author: Luke Kurlandski
"""

import tkinter as tk #GUI library
from tkinter import ttk #GUI library extension
import serial #Communication with serial ports
import serial.tools.list_ports #Listing the COM ports
import imagemodification #package to support image modification

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
        
        #Error Box
        self.window_communication = self.pop_up_window(self.root, 'Communication Window', 660, 425, True, -200, -20) 
        self.text_communication = tk.Text(self.window_communication, width=50, height=40)
        self.text_communication.grid()
        self.apply_scrollbars(self.window_communication, self.text_communication, True, True)
        
        #Configure the root
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate+200, y_cordinate-40))
        self.root.title(window_title)
        
        #Default maximum laser power
        self.laser_maximum = 0.0
    
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
        menu.add_command(label='Close', command=window.destroy)
        return menu
    
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
        img_as_arr = imagemodification.get_image_array(img_pil)
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
    
    def generate_exposure_details(self, exposure, ignore, laser, max_power):
        """
        Generate the arrays to describe laser exposure lengths.
        
        Arguments:
            (arg1) exposure (list[string]) : special strings containing exposure details
            (arg2) ignore (list[string]) : special strings containing ignore details
            (arg3) laser (list[string]) : special string containing laser details
            (arg4) max_power (float) : the maximum power the laser is capable of handling
            
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
                    exposure_arr[i] = mlt_fctr*i
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
                    laser_arr[i] = mlt_fctr*i
        #Ensure the laser array does not violate max_power, then return data
        for i in laser_arr:
            if i > max_power:
                raise Exception('Tried to use a laser power greater than allowed which is, ' + str(max_power))
        return exposure_arr, laser_arr
        
    def save_experiment(self):
        """
        Save the inputs on an experiment.
        """
    
    def open_experiment(self):
        """
        Open a previous experiment.
        """
    
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
        
        #Create a menu bar in te serial port window
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
                file.write(str(i) + '\n')
                file.write(str(j) + '\n')
            
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
    
    def error_window(self, window, message):
        """
        Launch an error window on the affiliated window
        
        Arguments:
            (arg1) window (tk.Toplevel) : master window the error window is attatched to
            (arg2) title (string) : title of the pop-up window
            
        Returns:
            (ret1) error_window (tk.Toplevel) : the error window
        """
        
        error_window = self.pop_up_window(window, 'Error', resizable = True, window_height=200)
        tk.Label(error_window, text=message).pack()
        return error_window
    
    def help_window(self, window, subject, window_height=400, window_width=800):
        """
        Create a 'help me' pop up window for any window based upon the instructions from file.
        
        Arguments:
            (arg1) window (tk.Toplevel) : window to apply help window to
            (arg2) subject (string) : subject user requires assistence with
            (arg3) help_window_height (int) : size of window in y direction
            (arg4) help_window_width (int) : size of window in x direction
            
        Returns:
            (ret1) help_window (tk.Toplevel) : the help window
        """
        
        try:
            file = open('Help ' + subject + '.txt', 'r')
        except FileNotFoundError as e:
            message = '\nThe help document ' + subject + ' cannot be found.\n'
            message+= str(e) + '\n'
            self.text_communication.insert(tk.END, message)
            return
        help_window = self.pop_up_window(window, 'Help', window_height, window_width, resizable = True)
        text = tk.Text(help_window, width=95, height=22)
        text.grid()
        text.insert(tk.INSERT, file.read())
        self.apply_scrollbars(help_window, text, True, True)
        file.close()
        return help_window
    
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
            laser_subjects = ['Laser Power']
            laser_data = [entry_power.get()] 
            self.store_previous_data('Laser Settings.txt', laser_subjects, laser_data)
            window.destroy()
        
        #Laser setting options
        window = self.pop_up_window(self.root, 'Laser Settings', 100, 200)
        self.set_up_menu(window)
        tk.Label(window, text = 'Maximum Laser Power (mW):').grid(row=0, column=0)
        entry_power = tk.Entry(window, width=10)
        entry_power.grid(row=0, column=1, sticky = tk.W)
        #Get previous configurations and fill
        try:
            self.text_communication.insert(tk.END, 'Getting previous experiment\'s laser settings.\n')
            file = open('Laser Settings.txt', 'r')
            lines = file.readlines()
            entry_power.insert(0, lines[1])
            file.close()
        except FileNotFoundError:
            self.text_communication.insert(tk.END, '\tNo previous laser settings detected.\n')
        #Warning and save button
        tk.Label(window, text = 'Using incorrect settings\ncould destroy the laser.').grid(row=1, column=0, columnspan=2)
        button_save = tk.Button(window, text = 'These are the\n Correct Settings', command = laser_save)
        button_save.grid(row=2, column=0, columnspan=2)
        
    def get_laser_settings(self):
        """
        Get the laser settings from a file.
        
        Returns:
            (ret1) lines[1] (float) : the maximum power read from the file
        """
        
        try:
            file = open('Laser Settings.txt', 'r')
            lines = file.readlines()
            print(lines)
            file.close()
            return float(lines[1].rstrip())
        
        except FileNotFoundError:
            raise FileNotFoundError('You have not specified any settings for the ' 
                'laser and there is no record of information from a prior experiment.\n')
        
        
    
    def pop_up_window(self, window, title='Message', window_height=150, window_width=200, resizable = True, x_move=0, y_move=0):
        """
        Launch an pop up window on the affiliated window. Centers on Screen.
        
        Arguments:
            (arg1) window (tk.Toplevel) : master window the error window is attatched to
            (arg2) title (string) : title of the pop-up window
            (arg3) window_height (int) : height of the pop-up window
            (arg4) window_width (int) : width of the pop-up window
            (arg5) resizable (boolean) : if the user can modify the window size
            (arg6) x_move (int) : a slight shift in the x location of window
            (arg7) y_move (int) : a slight shift in the y location of window
            
        Retuns:
            (ret1) pop_up_window (tk.Toplevel) : pop-up window
        """
        
        pop_up_window = tk.Toplevel(window) 
        pop_up_window.title(title)
        pop_up_window.resizable(resizable, resizable)
        screen_width = pop_up_window.winfo_screenwidth()
        screen_height = pop_up_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2)) + x_move
        y_cordinate = int((screen_height/2) - (window_height/2)) + y_move
        
        #pop_up_window
        
        #pop_up_window.geometry(str(window_height)+'x'+str(window_width)+' + '+str(x_cordinate)+' + '+str(y_cordinate))
        
        pop_up_window.geometry("{}x{}+{}+{}".format(window_width, window_height, 
            (x_cordinate+x_move), (y_cordinate+y_move)))
        return pop_up_window
    
    
        
        
        
        