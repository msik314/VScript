from tkinter import*
from tkinter import ttk
from node import *
from vec2 import *
from guinode import *
import time

class Starter(object):
    def __init__(self):
        #Initialize members to nothing
        self.vars = []
        self.types = []
        self.ret = StringVar()
        self.name = StringVar()
        self.var = StringVar()
        self.type = StringVar()
        self.running = False
        self.frame = None
        self.row = 0
        self.next_button = None
        self.back_button = None
        self.next_type = None
        self.next_var = None
        self.done_button = None
        self.parent = None
    
    def gen_node(self):
        head = Head_node(self.name.get(), self.vars, self.types, self.ret.get())
        return Gui_node(self.parent, head, lambda n: skip(), lambda n: skip(), 20, 20)
    
    def destroy(self):
        self.frame.destroy()
    
    def start_graph(self, root, parent):
        #Setup Tk
        self.parent = parent
        ttk.Style().configure("Start.TFrame", background = "#808080")
        
        #Set up user interface
        self.ret.set("Return type")
        self.name.set("Function name")
        self.type.set("Variable type")
        self.var.set("Variable name")
        self.frame = ttk.Frame(parent, style = "Start.TFrame", relief = "solid", borderwidth = 2)
        self.frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        ttk.Entry(self.frame, textvariable = self.ret).grid(row = 0, column = 0, sticky = (S, E, W))
        ttk.Entry(self.frame, textvariable = self.name).grid(row = 0, column = 1, sticky = (S, E, W))
        self.next_button = ttk.Button(self.frame, text = "Next", command = self.add_var)
        self.next_button.grid(row = 2, column = 1, sticky = (E, W))
        self.back_button = ttk.Button(self.frame, text = "Back", command = self.remove_var)
        self.back_button.grid(row = 2, column = 0, sticky = (E, W))
        self.next_type = ttk.Entry(self.frame, textvariable = self.type)
        self.next_type.grid(row = 1, column = 0, sticky = (E, W))
        self.next_var = ttk.Entry(self.frame, textvariable = self.var)
        self.next_var.grid(row = 1, column = 1, sticky = (E, W))
        self.done_button = ttk.Button(self.frame, text = "Done", command = self.stop_loop)
        self.done_button.grid(row = 3, column = 1, sticky = (E, W))
        
        #Update Tk
        last_time = time.clock()
        self.running = True
        while self.running:
            try:
                root.update_idletasks()
                root.update()
            
                time.sleep(max(0, 1/60 - (time.clock() - last_time)))
                last_time = time.clock()
            except:
                return
            
        self.frame.destroy()
    
    def stop_loop(self):
        self.running = False
    
    def add_var(self):
        #Add a new variable and type to the lists
        self.vars.append(self.var.get())
        self.types.append(self.type.get())
        self.type.set("")
        self.var.set("")
        
        #Move the bottom of the dialog down
        self.row += 1
        self.next_type.grid(row = self.row + 1, column = 0, sticky = (E, W))
        self.next_var.grid(row = self.row + 1, column = 1, sticky = (E, W))
        self.next_button.grid(row = self.row + 2, column = 1, sticky = (E, W))
        self.back_button.grid(row = self.row + 2, column = 0, sticky = (E, W))
        self.done_button.grid(row = self.row + 3, column = 1, sticky = (E, W))
        
        #Add new labels
        ttk.Label(self.frame, text = self.types[-1]).grid(row = self.row, column = 0, sticky = (E, W))
        ttk.Label(self.frame, text = self.vars[-1]).grid(row = self.row, column = 1, sticky = (E, W))
    
    def remove_var(self):
        #Avoid underflowing the lists
        if self.row == 0:
            return
        
        #Pop the last variable and type from the lists
        self.var.set(self.vars.pop())
        self.type.set(self.types.pop())
        
        #Destroy the last two labels
        self.frame.winfo_children()[-1].destroy()
        self.frame.winfo_children()[-1].destroy()
        
        #Move the bottom of the dialog up
        self.row -= 1
        self.next_type.grid(row = self.row + 1, column = 0, sticky = (E, W))
        self.next_var.grid(row = self.row + 1, column = 1, sticky = (E, W))
        self.next_button.grid(row = self.row + 2, column = 1, sticky = (E, W))
        self.back_button.grid(row = self.row + 2, column = 0, sticky = (E, W))
        self.done_button.grid(row = self.row + 3, column = 1, sticky = (E, W))