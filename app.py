# -*- coding: utf-8 -*-

"""
Create graphical user interface apps with tkinter.

Created on 10/1/19
Updated on 11/1/19

Copyright 2019, Luke Kurlandski, All rights reserved.

App is designed to provide a simple framework to create a variety of GUI programs.

This program was written by Luke Kurlandski and is his intellectual property. 

Dr. David McGee has permission to use this code in whatever way he sees fit.
"""

import tkinter as tk #GUI library
from tkinter import ttk #GUI library extension

class App:

	def __init__(self, root, window_width, window_height, window_title):
	    """
	    Constructor for generic image creation process.
	    
	        Arguments:
	            (arg1) root (Tk.Tk) : main window
	            (arg2) window_width (int) : width of the main window
	            (arg3) window_height (int) : height of the main window
	            (arg4) window_title (string) : title of the main window
	    """
	    
	    self.root = root 
	    screen_width = self.root.winfo_screenwidth()
	    screen_height = self.root.winfo_screenheight()
	    x_cordinate = int((screen_width/2) - (window_width/2))
	    y_cordinate = int((screen_height/2) - (window_height/2))
	    self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate+200, y_cordinate-40))
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
	    wigit.configure(yscrollcommand = yscrollcommand, xscrollcommand = xscrollcommand, wrap = tk.NONE)
	    
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
	        raise FileNotFoundError(message)
	    help_window = self.pop_up_window(window, 'Help', window_height, window_width, resizable = True)
	    text = tk.Text(help_window, width=95, height=22)
	    text.grid()
	    text.insert(tk.INSERT, file.read())
	    self.apply_scrollbars(help_window, text, True, True)
	    file.close()
	    return help_window

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