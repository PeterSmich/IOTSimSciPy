import tkinter as tk
from PIL import Image
import rethinkdb as r
from tkinter import messagebox
import threading
import sys

class Client(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #BluePrint and contorl panels
        self.f1 = tk.Frame(self)
        self.f2 = tk.Frame(self, height = 443)
        #Set blueprint image
        self.bckg_img = tk.PhotoImage(file="blueprint.gif")
        self.canvas = tk.Canvas(self.f1, width=390, height=440, bd = 3, bg = 'black')
        self.draw_BP(self.canvas)

        self.f1.grid(row = 0, column = 0)
        self.pack()
        #Set controls options
        '''
        l1 = tk.Label(self.f2, text = 'Filter')
        l1.grid(row = 0, column = 0)
        '''
        self.f2.grid(row = 0, column = 1, sticky = 'n')
        #Chack for database connection
        t = threading.Thread(target = self.connect)
        t.setDaemon(True)
        t.start()

    def connect(self):
        try:
            self.db = r.connect( "localhost", 28015).repl()
        except r.ReqlDriverError as e:
            self.db_exception_handler()
            return
        self.run()

    def db_exception_handler(self):
        if(tk.messagebox.askretrycancel('ERROR','ERROR: Unable to connect to the database.')):
            self.connect()
        else:
            self.master.event_generate("<<CancelEvent>>", when = "tail")
            
    def draw_BP(self,canvas):
        canvas.create_image(198, 224, image=self.bckg_img)
        canvas.pack(fill = 'both')
    '''
    def refresh_objects(self):
        for object in self.objects:
            draw_Circle(object[cordinates][0],object[cordinates][1])
    '''   
    def draw_Circle(self, x, y):
        self.canves.create_circle(x, y, 10)

    def refresh_objects(self):        
        try:
            self.objects = r.db('IoT').table('objects').run()
        except r.ReqlDriverError as e:
            t = threading.Thread(target = self.db_exception_handler)
            t.setDaemon(True)
            t.start()
            return 1
        return 0

    def run(self):
        if(self.refresh_objects()): return
        print(type(self.objects))
        for object in self.objects:
           print(object)
        self.objects = r.db('IoT').table('objects').changes().run()        
        for object in self.objects:
           print(object)

def main():
    root = tk.Tk()

    def exit_gui(*args):
        root.destroy()

    root.bind("<<CancelEvent>>", exit_gui)
    root.title("IOT_LPS_Client")
    cln = Client(master=root)
    cln.mainloop()
    try:
        root.destroy()
    except:
        pass 

if __name__ == '__main__':
    main()
