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
        #Get Data     
        try:
            #self.types = r.table("objects").with_fields('type').distinct(index = 'type')changes().run(self.db)
            self.objects = r.table("objects").changes().run(self.db)
        except r.ReqlDriverError as e:
            t = threading.Thread(target = self.db_exception_handler)
            t.setDaemon(True)
            t.start()
            
        print(type(self.objects))
        #set filter gui
        '''
        self.f3 = tk.Frame(self.f2)
        self.f3.grid(row = 0, column = 1)
        self.types_checkbox = [];
        self.filter = [];
        generate_types_checkbox()
        '''
	'''
    def generate_types_checkbox():
        for tc in self.types_checkbox:
            tc.pack_forget()
            del tc
        self.type_c_value = []
        for tc in range(0, length(types)):
            v = IntVar()
            c = tk.Checkbutton(self.f3, text = tc, command = self.set_filter, variable = v)
            c.select()
            c.pack(side = 'right')
            self.types_checkbox.append(c)
            self.type_c_value.append(v)
	'''
    def connect(self):
        try:
            self.db = r.connect( "localhost", 28015)
            self.refresh_objects()
        except r.ReqlDriverError as e:
            self.db_exception_handler()

    def db_exception_handler(self):
        if(tk.messagebox.askretrycancel('ERROR','ERROR: Unable to connect to the database.')):
            try:
                r.connect( "localhost", 28015)
            except r.ReqlDriverError as e:
                self.db_exception_handler()
        else:
            self.master.event_generate("<<CancelEvent>>", when = "tail")
            
    def draw_BP(self,canvas):
        canvas.create_image(198, 224, image=self.bckg_img)
        canvas.pack(fill = 'both')
	'''
    def set_filter():
        for i in range(0,length(self.types_checkbox)):
            if(self.type_c_value[i]){
                self.filter.append(self.types_checkbox(i).getText())
            }
	
    def set_query(self):
        try:
            self.objects = r.table("objects").filter(r.row["type"] in self.filter).changes().run(self.db)
        except r.ReqlDriverError as e:
            t = threading.Thread(target = self.db_exception_handler)
            t.setDaemon(True)
            t.start()
	'''
    def refresh_objects(self):
        #set_query() 
        for object in self.objects:
            draw_Circle(object[cordinates][0],object[cordinates][1])
           
    def draw_Circle(self, x, y):
		self.canves.create_circle(x, y, 10)

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
