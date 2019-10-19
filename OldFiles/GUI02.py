# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 15:48:08 2019

@author: laserlab
"""

import tkinter as tk
from tkinter import filedialog

#Set up root
root = tk.Tk()
root.attributes('-fullscreen' ,True)
#Set up menu
menu = tk.Menu(root)
menu.add_command(label='Quit', command=root.destroy)
root.config(menu=menu)
#Set up labels and entry
tk.Label(root, text='Film Selection').grid(column=0, row=0, sticky=tk.W+tk.E)
tk.Label(root, text='Enter width of image on film (m)').grid(column = 0, row = 1)
entry_1 = tk.Entry(root, width = 10)
entry_1.grid(column = 0, row = 2)
tk.Label(root, text='Enter height of image on film (m)').grid(column = 0, row = 3)
entry_2 = tk.Entry(root, width = 10)
entry_2.grid(column = 0, row = 4)

tk.Label(root, text='Image Selection').grid(column=0, row=5, pady = 20, sticky=tk.W+tk.E)
button_chsIMG = tk.Button(root, text='Select an Image')
button_chsIMG.grid(column=0, row=6)

#Set up canvas
canvas = tk.Canvas(root, width=300, height=300)
canvas.grid(column = 1, row=0, columnspan=300, rowspan=300, padx=100)
img = tk.PhotoImage(file=filedialog.askopenfilename())
canvas.create_image(20,20, anchor=tk.NW, image=img)

#MainLoop
tk.mainloop()