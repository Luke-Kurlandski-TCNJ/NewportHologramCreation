### Python libraries ###
# Monitor packages
# from screeninfo import get_monitors # Screen Information (screeninfo) is a package to fetch location and size of physical screens.
# Window packages 
from tkinter import Toplevel, Tk, Label # Graphical User Interface (GUI) package
from PIL import Image, ImageTk # Python Imaging Librarier (PIL) package
# Processing packages
import re # Regular Expression (re) is a package to check, if a string contains the specified search pattern.
import numpy as np # Scientific computing package (NumPy)

class SLM_window():

	def __init__(self, master):
		### Monitor controlling 
		# Finds the resolution of all monitors that are connected.
		# active_monitors = get_monitors() # "monitor(screenwidth x screenheight + startpixel x + startpixel y)"


		# Separates all numbers from a string
		# monitor_values=re.findall('([0-9]+)', str(active_monitors))
		# print(monitor_values)

		# Assign the separated digits of the string to a variable
		# begin_monitor_horizontal = monitor_values[0]
		# begin_monitor_vertical = monitor_values[1]
		# begin_slm_horizontal = monitor_values[5]
		# begin_slm_vertical = monitor_values[6]


		begin_monitor_horizontal = 100
		begin_monitor_vertical = 100
		begin_slm_horizontal = 20
		begin_slm_vertical = 20


		width = 1920
		height = 1152

		array = np.zeros((height, width), dtype = np.uint16)
		image = Image.fromarray(array)
		image = image.convert('L')

		# Create a window environment on the computer
		
		# self.image_window = Tk()
		self.image_window = master
		

		# # Window requieres no frame
		# self.image_window.attributes("-alpha", 0.0)
		# self.image_window.iconify()

		# Create a window on the screen of the SLM monitor
		self.window_slm = Toplevel(self.image_window)
		self.window_slm_geometry = str("{:}".format(width) + 'x' + "{:}".format(height) + '+' + "{:}".format(begin_slm_horizontal) + '+' + "{:}".format(begin_slm_vertical))
		
		self.window_slm.geometry(self.window_slm_geometry)
		self.window_slm.overrideredirect(1)

		grating = ImageTk.PhotoImage(image)

		# Load the opened image into the window of the SLM monitor
		# self.window_slm_label = Label(self.window_slm, image=grating)
		# self.window_slm_label.pack()

		self.test_label = Label(self.window_slm, text='John')
		self.test_label.pack()

		# Termination command for the code
		self.window_slm.bind("<Escape>", lambda e: self.window_slm.destroy())
		# self.image_window.bind("<E>", lambda e: self.image_window.destroy())

		# self.image_window.mainloop()

	def change_text(self, msg):
		self.test_label.config(text= msg)

	def display(self,grating):
		self.window_slm_label.config(image=grating)

	def close_window(self):
		print("pressed")
		self.window_slm.destroy()
		self.window_slm.update()





