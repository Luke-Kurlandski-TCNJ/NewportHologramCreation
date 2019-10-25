# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:35:26 2019

@author: laserlab
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
import imagework #package to support image modification
from serialcontrol import Motor, Shutter #Allows communication with machinery

class GenericImageCreator:
    
    def __init__(self, root, window_width, window_height, window_title):
        '''
        Constructor.
            Arguments:
                (arg1) root (Tk.Tk) : main window
                (arg2) window_width (int) : width of the main window
                (arg3) window_height (int) : height of the main window
                (arg4) window_title (string) : title of the main window
        '''
        
        #Set up the root
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2) - 50)
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.root.title(window_title)
        
    def set_up_frames(self, window, frames_horizontal, frames_vertical):
        '''
        Create and orgainze the frames for any window.
            Arguments:
                (arg1) window (tk.Toplevel) : window to apply help window to
                (arg2) frame_horizontal (int) : number of frames in x direction
                (arg3) frame_vertical (int) : number of frames in y direction
            Returns:
                (ret) frames (list[list[tk.Frame]]) : 2-D list of frames 
        '''
    
        frames = []
        for i in range (0, frames_vertical):
            temp = []
            for j in range (0, frames_horizontal):
                frame = tk.Frame(window)
                frame.grid(row = i, column = j, pady = 10)
                temp.append(frame)
            frames.append(temp)
        return frames
    
    def set_up_menu(self, window):
        '''
        Creates a menu bar for any window.
            Arguments:
                (arg1) window (tk.Toplevel) : window to apply help window to
            Returns:
                (ret) menu (tk.Menu) : the newly created menu widgit
        '''
        
        menu = tk.Menu(window)
        menu.add_command(label='Quit', command=window.destroy)
        #menu.add_command(label='Help', command=lambda: self.help_me(window))
        window.config(menu=menu)
        return menu
    
    def help_me(self, window):
        '''
        Creates a 'help me' pop up window for any window.
            Arguments:
                (arg1) window (tk.Toplevel) : window to apply help window to.
            Returns:
                (ret) help_window (tk.Toplevel) : the help window
        '''
        
        help_window = tk.Toplevel(window) 
        help_window.title("Help")
        help_window.resizable(False, False)
        help_window_height = 150
        help_window_width = 200
        screen_width = help_window.winfo_screenwidth()
        screen_height = help_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (help_window_width/2))
        y_cordinate = int((screen_height/2) - (help_window_height/2))
        help_window.geometry("{}x{}+{}+{}".format(help_window_width, help_window_height, x_cordinate, y_cordinate))
        return help_window
    
    def image_as_array(self, xPix, yPix, img_pil, title):
        '''
        Converts the image into an array. Displays array in a new window.
            Arguments:
                (arg1) xPix (int) : number of pixels horizontally
                (ret2) yPix (int) : number rof pixels vertically
                (arg3) img_pil (Pil image) : the image to convert into array
                (arg4) title (string) : title of the image
            Returns:
                (ret) image_as_array (list[list[int]]) : the image converted into an array
        '''
        
        #Configure array window, display, and scrollbars
        array_window = tk.Toplevel(self.root)
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
        img_as_array = imagework.get_image_array(img_pil)
        for i in img_as_array:
            for j in i:
                spaces = '   '
                if j > 9:
                    spaces = '  '
                if j > 99:
                    spaces = ' '
                text_arr.insert(tk.END, str(j)+spaces)
            text_arr.insert(tk.END,'\n')
        array_window.configure(width=100, height=100)
        return img_as_array