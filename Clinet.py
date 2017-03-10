import tkinter as tk
from PIL import Image
import rethinkdb as r
from tkinter import messagebox

class Client(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.f1 = tk.Frame(self)
        self.f2 = tk.Frame(self)

        self.bckg_img = tk.PhotoImage(file="blueprint.gif")
        self.canvas = tk.Canvas(self.f1, width=390, height=440, bd = 3, bg = 'black')
        self.draw_BP(self.canvas)

        self.f1.pack()
        self.pack()

        try:
            r.connect( "localhost", 28015)
        except r.ReqlDriverError as e:
            self.db_exception_handler()

        l1 = tk.Label(f2,'Filter')
        self.refresh_objects()

        self.f2.pack()
        self.pack()

    def draw_BP(self,canvas):
        canvas.create_image(198, 224, image=self.bckg_img)
        canvas.pack(fill = 'both')

    def db_exception_handler(self):
        if(tk.messagebox.askretrycancel('ERROR','ERROR: Unable to connect to the database.')):
            try:
                r.connect( "localhost", 28015)
            except r.ReqlDriverError as e:
                self.db_exception_handler()
        else:
            try:
                root.destroy()
            except:
                pass 

    def refresh_objects():
        self.objects = r.table("objects").changes().run()
        for object in objects:
            print(object)



def main():
    root = tk.Tk()
    root.title("IOT_LPS_Client")
    cln = Client(master=root)
    cln.mainloop()
    try:
        root.destroy()
    except:
        pass 

if __name__ == '__main__':
    main()