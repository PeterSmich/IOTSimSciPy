import tkinter as tk
from tkinter import messagebox

class Obj:
	"""docstring for Obj"""
	poz_x = -1
	poz_y = -1
	name = "Kecske"
	circle = None
	button = None
	colour = 'Red'
	def __init__(self, x, y, name, circle, button, color):
		print("kecske")

	def __init__(self, name, i):
		self.name = name
		self.colour = self.get_Colour(i)

	def get_Colour(self, i):
		colours = {0 : 'Red', 1 : 'Yellow', 2 : 'Green', 3 : 'Blue'}
		return colours[i]

class Sensor:
	"""docstring for Sensor"""
	poz_x = 0
	poz_y = 0
	def __init__(self, x, y):
		self.poz_y = y
		self.poz_x = x

	def obj_dist(s):
		return sqrt((power((s.poz_x-self.poz_x),2)+power((s.poz_y-self.poz_y),2)))

	def get_dist(objects):
		dist = []
		for s in objects:
			dist.push(obj_dist(s))
		return dist
		
class App:
	"""docstring for App"""
	ip = 0
	port = 0
	sensors = []

	def __init__(self):
		print("kecske")

	def add_object():
		print("kecske")

	def connect():
		print("kecske")

	def send():
		for s in sensors:
			s.get_dist(objects)

		send_to()
	def send_to(json):
		print("kecske")

	def disconnect():
		print("kecske")


class Window(tk.Frame):
	objects_button = []
	objects = []
	types = ('Glass', 'Key', 'Phone', 'Pen')
	selected_object = None;

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
		
		#Set blueprint image
		self.bckg_img = tk.PhotoImage(file="blueprint.gif")
		self.canvas = tk.Canvas(self.f1, width=390, height=440, bd = 1, bg = 'black')
		self.draw_BP(self.canvas)
		self.f1.pack(side = 'left')

		self.canvas.bind("<Button-1>", self.draw_Circle)
		
		#Set controls options eg. filters
		tk.Label(self.f2, text = 'Filter:', bg = 'gray16', fg = 'white', anchor = 'w').pack(fill = 'x')
		for i in range(0,4):
			self.objects[i].button = tk.Button(self.f2, text = self.objects[i].name, \
				bg = self.objects[i].colour, width = 10, command = self.select_Object(i))
			self.objects[i].button.pack(padx = 2, pady = 0)
		

		tk.Label(f2, text = 'IoT indoor positioning system for disabled people', \
			bg = 'dark slate gray', fg = 'white', anchor = 'w', wraplength = 100, bd = 5).grid(row = 0, column = 0)
		self.f2.grid(row = 1, column = 0)
		f2.pack(padx = 5)
		self.pack()

	def draw_BP(self,canv):
		canv.create_image(198, 224, image=self.bckg_img)
		canv.pack(fill = 'both')

	def set_changes(self):
		self.changes = True

	def select_Object(self, i):
		self.selected_object = i
		print(self.selected_object)

	def draw_Circle(self,event):
		self.objects[self.selected_object].circle = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, \
			fill = self.objects[self.selected_object].colour)
		

		
root=tk.Tk()
win = Window(master = root)
win.mainloop()
