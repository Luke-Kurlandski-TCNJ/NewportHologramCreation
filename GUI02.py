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
tk.Label(root, text='Enter width of image on film (m)').grid(column = 0, row = 0)
entry_1 = tk.Entry(root, width = 10)
entry_1.grid(column = 0, row = 10)

tk.Label(root, text='Enter height of image on film (m)').grid(column = 0, row = 30)
entry_2 = tk.Entry(root, width = 10)
entry_2.grid(column = 0, row = 40)

button_chsIMG = tk.Button(root, text='Select an Image')
button_chsIMG.grid(column=0, row=70)

#Set up canvas
canvas = tk.Canvas(root, width=300, height=300)
canvas.grid(column = 1000, row = 1000, columnspan=300, rowspan=300)
img = tk.PhotoImage(file=filedialog.askopenfilename())
canvas.create_image(20,20, anchor=tk.NW, image=img)
#MainLoop
tk.mainloop()