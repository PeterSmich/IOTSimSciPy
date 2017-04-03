import tkinter as tk
import time
import rethinkdb as r
from tkinter import messagebox
import threading
import sys

class Client(tk.Frame):
    obj_change = False
    objects = {}
    types = {'glass' : 'red', 'key' : 'green', 'phone' : 'blue', 'pen' : 'yellow'}

    def __init__(self, master=None):
        super().__init__(master)

        master.bind("<<RefreshMap>>", self.refresh_map)
        #BluePrint and contorl panels
        self.f1 = tk.Frame(self)
        self.f2 = tk.Frame(self, height = 443)
        #Set blueprint image
        self.bckg_img = tk.PhotoImage(file="blueprint.gif")
        self.canvas = tk.Canvas(self.f1, width=390, height=440, bd = 3, bg = 'black')
        self.draw_BP(self.canvas)

        self.f1.grid(row = 0, column = 0)
        #Set controls options eg. filters
        self.types_filter = {'glass' : tk.BooleanVar(), 'key' : tk.BooleanVar(), 'phone' : tk.BooleanVar(), 'pen' : tk.BooleanVar()}
        self.check_Glass = tk.Checkbutton(self.f2, text = 'Glasses', variable = self.types_filter['glass'], bg = self.types['glass'], width = 20, command = self.set_changes)
        self.check_Key = tk.Checkbutton(self.f2, text = 'Keys', variable = self.types_filter['key'], bg = self.types['key'], width = 20, command = self.set_changes)
        self.check_Phone = tk.Checkbutton(self.f2, text = 'Phones', variable = self.types_filter['phone'], bg = self.types['phone'], width = 20, command = self.set_changes)
        self.check_Pen = tk.Checkbutton(self.f2, text = 'Pens', variable = self.types_filter['pen'], bg = self.types['pen'], width = 20, command = self.set_changes)
        
        self.check_Glass.select()
        self.check_Key.select()
        self.check_Phone.select()
        self.check_Pen.select()

        self.check_Glass.pack()
        self.check_Key.pack()
        self.check_Phone.pack()
        self.check_Pen.pack()

        self.f2.grid(row = 0, column = 1, sticky = 'n')
        self.pack()
        #Chack for database connection
        t = threading.Thread(target = self.connect)
        t.setDaemon(True)
        t.start()

    def set_changes(self):
        self.changes = True

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
            
    def draw_BP(self,canv):
        canv.create_image(198, 224, image=self.bckg_img)
        canv.pack(fill = 'both')

    def draw_Circle(self, x, y, color = None):
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill = color)

    def refresh_cursor(self):        
        try:
            self.cursor = r.db('IoT').table('objects').run()
        except r.ReqlDriverError as e:
            t = threading.Thread(target = self.db_exception_handler)
            t.setDaemon(True)
            t.start()
            return 1
        return 0

    def refresh_object(self, obj):
        if (obj['old_val'] is not None):
            del self.objects[obj['old_val']['id']]
        if (obj['new_val'] is not None):        
            self.objects[obj['new_val']['id']] = {'type' : obj['new_val']['type'], 'cord' : obj['new_val']['coordinates ']}

    def refresh_map(self, *args):
        self.changes = False
        self.draw_BP(self.canvas)
        for i, d in self.objects.items():
            if (self.types_filter[d['type']].get()):
                self.draw_Circle(d['cord']['x'],d['cord']['y'], self.types[d['type']])


    def run(self):
        if(self.refresh_cursor()): return
        for obj in self.cursor:
           self.objects[obj['id']] = {'type' : obj['type'], 'cord' : obj['coordinates ']}
        self.refresh_map()


        t = threading.Thread(target = self.refresh_notifyer)
        t.setDaemon(True)
        t.start()

        self.cursor = r.db('IoT').table('objects').changes().run()        
        for object in self.cursor:
            self.changes = True
            self.refresh_object(object)

    def refresh_notifyer(self):
        while (True):
            try:
                time.sleep(0.5)
                if (self.changes):
                    self.master.event_generate("<<RefreshMap>>", when = "tail")
            except Exception as e:
                pass


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
