import tkinter as tk

class Obj:
	"""docstring for Obj"""
	poz_x = 0
	poz_y = 0
	id = 0
	def __init__(self, x, y, id):

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
	objects = []

	def __init__(self):

	def add_object():

	def connect():

	def send():
		for s in sensors:
			s.get_dist(objects)

		send_to()
	def send_to(json):

	def disconnect():


class Window(tk.Frame):
	obj_type = ['Phone', 'Remooter', 'Mug', 'Key']
	buttons = []
	app = App()
	def __init__(self, master=None):
		super().__init__(master)
		f1 = tk.Frame(self)
		f2 = tk.Frame(self, )
		for ot in self.obj_type:
			self.buttons.append(tk.Button(f1, text = ot))
		for i in range(1,len(self.buttons)):
			self.buttons[i].grid(row = i, column = 0, padx = 2, pady = 2)
		f1.grid(row = 0, column = 1, padx = 2, pady = 2)
		f2.grid(row = 0, column = 0, padx = 2, pady = 2)
		self.pack()
		

		
root=tk.Tk()
win = Window(master = root)
win.mainloop()
