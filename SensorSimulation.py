import tkinter as tk
from tkinter import messagebox
from functools import partial
import json

class Obj:
	"""docstring for Obj"""
	poz_x = None
	poz_y = None
	name = None
	circle = None
	button = None
	colour = None

	def __init__(self, name, i):
		self.name = name
		self.colour = self.get_Colour(i)

	def get_Colour(self, i):
		colours = {0 : 'Red', 1 : 'Yellow', 2 : 'Green', 3 : 'Blue'}
		return colours[i]

class Window(tk.Frame):
	objects_button = []
	objects = []
	types = ('Glass', 'Key', 'Phone', 'Pen')
	selected_object = -1

	app = App()

	def __init__(self, master=None):
		super().__init__(master)

		for i in range(0,4):
			self.objects.append(Obj(self.types[i], i))
		#BluePrint and control panels
		self.configure(background='dark slate gray')
		self.f1 = tk.Frame(self, bg = 'dark slate gray', bd = 5)
		f2 = tk.Frame(self, bg = 'dark slate gray', bd = 1, pady = 1)
		self.f2 = tk.Frame(f2, bg = 'gray16', bd = 1, pady = 1)
		f3 = tk.Frame(self, bg = 'dark slate gray', bd = 1, pady = 1)
		self.f3 = tk.Frame(f3, bg = 'gray16', bd = 1, pady = 1)
		
		#Set blueprint image
		self.bckg_img = tk.PhotoImage(file="blueprint.gif")
		self.canvas = tk.Canvas(self.f1, width=390, height=440, bd = 1, bg = 'black')
		self.draw_BP(self.canvas)
		self.f1.pack(side = 'left')

		self.canvas.bind("<Button-1>", self.draw_Circle)
		
		#Set controls options eg. filters
		tk.Label(self.f2, text = 'Filter:', bg = 'gray16', fg = 'white', anchor = 'w').pack(fill = 'x')
		for i in range(0,4):
			helper = partial(self.select_Object, i)
			self.objects[i].button = tk.Button(self.f2, text = self.objects[i].name, \
				bg = self.objects[i].colour, width = 10, command = helper)
			self.objects[i].button.pack(padx = 2, pady = 0)

		deselect_button = tk.Button(self.f3, text = 'Deselect', width = 10, command = self.Deselect)
		deselect_button.pack(padx = 2, pady = 0)

		send_button = tk.Button(self.f3, text = 'Send', width = 10, command = self.Send)
		send_button.pack(padx = 2, pady = 0)
		
		tk.Label(f2, text = 'IoT indoor positioning system for disabled people', \
			bg = 'dark slate gray', fg = 'white', anchor = 'w', wraplength = 100, bd = 5).grid(row = 0, column = 0)
		self.f2.grid(row = 1, column = 0)
		f2.pack(padx = 5)

		self.f3.grid(row = 2, column = 0)
		f3.pack(padx = 5)

		self.pack()

	def draw_BP(self,canv):
		canv.create_image(198, 224, image=self.bckg_img)
		canv.pack(fill = 'both')

	def Deselect(self):
		self.selected_object = -1;

	def select_Object(self, i):	
		if self.selected_object != -1:
			self.objects[self.selected_object].button.config(state = 'normal');
		self.selected_object = i
		self.objects[i].button.config(state = 'disabled')

	def draw_Circle(self,event):
		if self.selected_object != -1:
			if self.objects[self.selected_object].circle != None:
				self.canvas.delete(self.objects[self.selected_object].circle)
			self.objects[self.selected_object].circle = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, \
				fill = self.objects[self.selected_object].colour)
			self.objects[self.selected_object].poz_x = event.x;
			self.objects[self.selected_object].poz_y = event.y;

	def get_distant(self, o):
		dist = []
		dist.append(sqrt((power(s.poz_x,2)+power(s.poz_y,2))))
		dist.append(sqrt((power((s.poz_x-198),2)+power(s.poz_y,2))))
		dist.append(sqrt((power(s.poz_x,2)+power((s.poz_y-224),2))))
		return dist

	def make_json(self):
		json_data = {}
		for i in range(0:4):
			if objects[i].poz_x != None:
				json_data[objects[i].name] = dist
		
		json_object = json.dump(json_data)
		print(json_object)

	def send(self):
		print("Connecting to server...")
		print("Connected")
		print("Sending data...")
		print("Successful")


		

		
root=tk.Tk()
win = Window(master = root)
win.mainloop()
