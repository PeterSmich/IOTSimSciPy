import tkinter as tk
from tkinter import messagebox
from functools import partial
import json
import socket
import math

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
		f4 = tk.Frame(self, bg = 'dark slate gray', bd = 1, pady = 1)
		self.f4 = tk.Frame(f4, bg = 'gray16', bd = 1, pady = 1)
		
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
				bg = self.objects[i].colour, width = 15, command = helper)
			self.objects[i].button.pack(padx = 2, pady = 0)

		deselect_button = tk.Button(self.f3, text = 'Deselect', width = 15, command = self.Deselect)
		deselect_button.pack(padx = 2, pady = 0)

		delete_sel_button = tk.Button(self.f3, text = 'Delete selected', width = 15, command = self.del_sel)
		delete_sel_button.pack(padx = 2, pady = 0)

		delete_all_button = tk.Button(self.f3, text = 'Delete All', width = 15, command = self.del_all)
		delete_all_button.pack(padx = 2, pady = 0)

		send_button = tk.Button(self.f4, text = 'Send', width = 15, command = self.send)
		send_button.pack(padx = 2, pady = 0)
		
		tk.Label(f2, text = 'IoT indoor positioning system for disabled people', \
			bg = 'dark slate gray', fg = 'white', anchor = 'w', wraplength = 100, bd = 5).grid(row = 0, column = 0)
		self.f2.grid(row = 1, column = 0)
		f2.pack(padx = 5)

		self.f3.grid(row = 2, column = 0)
		f3.pack(padx = 5)

		self.f4.grid(row = 2, column = 0)
		f4.pack(padx = 5)

		self.pack()

	def draw_BP(self,canv):
		canv.create_image(198, 224, image=self.bckg_img)
		canv.pack(fill = 'both')

	def Deselect(self):
		if self.selected_object != -1:
			self.objects[self.selected_object].button.config(state = 'normal');
		self.selected_object = -1;

	def select_Object(self, i):	
		if self.selected_object != -1:
			self.objects[self.selected_object].button.config(state = 'normal');
		self.selected_object = i
		self.objects[i].button.config(state = 'disabled')

	def draw_Circle(self,event):
		if self.selected_object != -1:
			self.canvas.delete(self.objects[self.selected_object].circle)
			self.objects[self.selected_object].circle = self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, \
				fill = self.objects[self.selected_object].colour)
			self.objects[self.selected_object].poz_x = event.x;
			self.objects[self.selected_object].poz_y = event.y;

	def del_sel(self):
		if self.selected_object != -1:
			self.canvas.delete(self.objects[self.selected_object].circle)
			self.objects[self.selected_object].poz_x = None
			self.objects[self.selected_object].poz_y = None

	def del_all(self):
		for i in range(0,4):
			self.canvas.delete(self.objects[i].circle)
			self.objects[i].poz_x = None
			self.objects[i].poz_y = None


	def get_distant(self, o):
		dist = []
		dist.append(math.sqrt((pow(o.poz_x,2)+pow(o.poz_y,2))))
		dist.append(math.sqrt((pow((o.poz_x-390),2)+pow(o.poz_y,2))))
		dist.append(math.sqrt((pow(o.poz_x,2)+pow((o.poz_y-440),2))))
		return dist

	def make_json(self):
		json_data = {}
		for i in range(0,4):
			if self.objects[i].poz_x != None:
				json_data[self.objects[i].name] = self.get_distant(self.objects[i])
		
		json_object = json.dumps(json_data) #separators = (', ',': ')
		return json_object

	def send(self):
		socket.setdefaulttimeout(3)
		s = socket.socket()
		#host = '192.168.0.101'
		host = 'localhost'
		port = 12345
		print("Connecting to server...")
		try:
			s.connect((host, port))
		except socket.timeout:
			print("Connection timed out, server not responding")
		else:
			print("Successfully connected")
			print(s.recv(1024).decode())
			data = self.make_json()
			s.sendto(data.encode(),(host, port))
		s.close()


		

		
root=tk.Tk()
win = Window(master = root)
win.mainloop()
