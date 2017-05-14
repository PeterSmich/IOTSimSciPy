import tkinter as tk
#from PIL import Image
from tkinter import messagebox
import threading
import os
'''
class Client(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		server_isrunning = False
		db_isrunning = False
		client_isrunning = False
		
		self.server_button = tk.Button(master, text = 'Start server', command = self.start_server)
		self.db_button = tk.Button(master, text = 'Start db', command = self.start_db)
		self.client_button = tk.Button(master, text = 'Start client', command = self.start_client)
		
		self.server_label = tk.Label(master, text = 'Server not running')
		self.db_label = tk.Label(master, text = 'DB not running')
		self.client_label = tk.Label(master, text = 'Client not running')
		
		self.exit_button = tk.Button(master, text = 'Exit', command = self.master.quit)
		
		self.db_button.grid(row = 0, column = 0, sticky = 'w'+'e')
		self.server_button.grid(row = 1, column = 0, sticky = 'w'+'e')
		self.client_button.grid(row = 2, column = 0, sticky = 'w'+'e')
		self.db_label.grid(row = 0, column = 1, sticky = 'w'+'e')
		self.server_label.grid(row = 1, column = 1, sticky = 'w'+'e')
		self.client_label.grid(row = 2, column = 1, sticky = 'w'+'e')
		self.exit_button.grid(row = 3, column = 0, columnspan = 2)
		
	def start_server(self):
		pass
		
	def start_server(self):
		pass
		
	def start_server(self):
		pass
'''
def main():
	exec('C:\\Users\\kovac\\OneDrive\\Egyetem\\MSc\\SciPy\\rethinkdb.exe')
	print('Database was started')
	exec('Server.py')
	print('Server was started')
	exec('SensorSimulation.pyw')
	print('Sensor simulation was started')
	exec('Client.py')
	print('Client was started')

if __name__ == '__main__':
	main()
