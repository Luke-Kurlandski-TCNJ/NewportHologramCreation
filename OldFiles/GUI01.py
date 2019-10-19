# -*- coding: utf-8 -*-
"""
GUI devlopment with tkinter

Created on 9/20/19

@author: Luke Kurlandski
"""

import tkinter as tk
from tkinter import filedialog

def chooseImage():
    imgFile = filedialog.askopenfilename()
    print('File:\n' + imgFile)
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    img = tk.PhotoImage(file=filedialog.askopenfilename())
    canvas.create_image(20,20, anchor=tk.NW, image=img)
    
def f1():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    img = tk.PhotoImage(file='Earth.png')
    canvas.create_image(20,20, anchor=tk.NW, image=img)
    tk.mainloop()

def f2():    
    root = tk.Tk()
    
    image1 = tk.PhotoImage('Earth.png')
    '''
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.create_image(20,20, anchor=tk.NW, image = image) 
    canvas.pack()
    '''
    '''
    frame = tk.Frame(root, width=400, height=300)
    frame.pack()
    '''
    button = tk.Button(root, text = 'Choose Image', image = image1, command = chooseImage, width=100, height = 100)
    button.pack()
    
    menu = tk.Menu(root)
    menu.add_command(label='Quit', command=root.destroy)
    root.config(menu=menu)
    
    root.mainloop()
    '''
    menu = tk.Menu(root)
    root.config(menu=menu)
    fileMenu = tk.Menu(menu)
    menu.add_cascade(label = 'File', menu=fileMenu)
    fileMenu.add_command(label = 'Exit', command = root.quit)
    imgButton = tk.Button(root, text='Choose an Image')
    imgButton.grid(column = 0)
    '''
    root.mainloop()



def f3():
    #Set up root
    global root
    root = tk.Tk()
    #Set up menu
    menu = tk.Menu(root)
    menu.add_command(label='Quit', command=root.destroy)
    root.config(menu=menu)
    #Set up canvas
    '''
    canvas = tk.Canvas(root, width=300, height=300)
    canvas.pack()
    '''
    #Set up button
    button = tk.Button(root, text = 'Choose Image', command = chooseImage)
    button.pack()
    
    
    
    tk.mainloop()

f3()
