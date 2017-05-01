from tkinter import *
from tkinter import ttk
from node import *
from vec2 import *

def skip():
    pass

class Gui_node(object):
    def __init__(self, parent, node,  manage_function, delete_function, x = 0, y = 0):
        #Initialize members
        self.node = node
        num_args = len(node.get_arguments())
        
        #Create the frame, name, and delete buttons
        self.pos = vec2(x,y)
        self.frame = ttk.Frame(parent, relief = "solid", borderwidth = 2)
        self.name_label = ttk.Label(self.frame, text = node.get_name())
        self.name_label.grid(column = 0 , row = 0, sticky = (N, W, S))
        self.name_label.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        delete_button = ttk.Button(self.frame, text = "X", width = 1, command = self.destroy)
        delete_button.grid(row = 0, column = 1, sticky = (N, E, S))
        self.frame.place(x = self.pos.x, y = self.pos.y, anchor = NW)
        self.frame.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        self.frame.bind("<1>", lambda e: skip())
        self.name_label.bind("<1>", lambda e: skip())
        
        #Set callbacks
        self.manage_function = manage_function
        self.delete_function = delete_function
        
        if(node.is_head()):
            #Display arguments
            self.vars = []
            delete_button.state(["disabled"])
            for i in range(len(node.get_arguments())):
                self.vars.append(StringVar())
                self.vars[i].set(node.get_types()[i] + " " + node.get_arguments()[i])
                label = ttk.Label(self.frame, width = 20, textvariable = self.vars[i])
                label.grid(column = 0, columnspan = 2, sticky = (E, W))
        else:
            #Display arguments
            self.vars = []
            for i in range(len(node.get_arguments())):
                self.vars.append(StringVar())
                arg = node.get_arguments()[i]
                label = ttk.Label(self.frame, text = arg)
                label.grid(row = i + 1, column = 0, sticky = (E, W))
                entry = ttk.Entry(self.frame, width = 18 - len(arg), textvariable = self.vars[i])
                entry.bind("<Return>", lambda e, n = i: self.node.argument(n, self.vars[n].get()))
                entry.bind("<FocusOut>", lambda e, n = i: self.node.argument(n, self.vars[n].get()))
                entry.grid(row = i + 1, column = 1, sticky = (E, W))
            
            #Display return value
            if node.has_return():
                self.return_val = StringVar()
                label = ttk.Label(self.frame, text = "return").grid(row = num_args + 1, column = 0, sticky = (E,W))
                entry = ttk.Entry(self.frame, width = 12, textvariable = self.return_val)
                entry.bind("<Return>", lambda e: self.node.return_value(self.return_val.get()))
                entry.bind("<FocusOut>", lambda e: self.node.return_value(self.return_val.get()))
                entry.grid(row = num_args + 1, column = 1, sticky = (E, W))
        
        ttk.Button(self.frame, text = "Next", command = self.manage).grid(column = 0, columnspan = 2, sticky = (E, W))
    
    def place(self, x, y):
        #Set the position of the widget
        self.pos.x += x
        self.pos.y += y
        self.frame.place(x = self.pos.x, y = self.pos.y, anchor = NW)
        
    def destroy(self):
        #Cleanup the widget
        self.frame.destroy()
        self.delete_function(self)
    
    def manage(self):
        self.manage_function(self)
    
    def active_mode(self, manage_function):
        #Disable movement and enable clicking
        self.frame.bind("<B1-Motion>", lambda e: skip())
        self.name_label.bind("<B1-Motion>", lambda e: skip())
        self.frame.bind("<1>", lambda e: manage_function(self))
        self.name_label.bind("<1>", lambda e: manage_function(self))
        
        #Disable buttons
        for i in range(1, len(self.frame.winfo_children())):
            self.frame.winfo_children()[i].state(["disabled"])
        
    
    def passive_mode(self):
        #Enable movement and disable clicking
        self.frame.bind("<1>", lambda e: skip())
        self.name_label.bind("<1>", lambda e: skip())
        self.frame.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        self.name_label.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        
        #Enable buttons
        if not self.node.is_head():
            self.frame.winfo_children()[1].state(["!disabled"])
        for i in range(2, len(self.frame.winfo_children())):
            self.frame.winfo_children()[i].state(["!disabled"])
    
    def is_conditional(self):
        return False
    
    def get_node(self):
        return self.node
    
    def get_x(self):
        return self.pos.x
    
    def get_y(self):
        return self.pos.y
    
    def get_width(self):
        return self.frame.winfo_width()
    
    def get_height(self):
        return self.frame.winfo_height()
    
    def set_manager(self, manage_function):
        self.manage_function = manage_function
    
    def set_delete(self, delete_function):
        self.delete_function = delete_function
    
    def set_cancel(self, cancel_function):
        self.frame.winfo_children()[-1].bind("<Escape>", lambda e:cancel_function())

class Gui_conditional(object):
    def __init__(self, parent, node,  manage_function, delete_function, x = 0, y = 0):
        #Initialize members
        self.node = node
        num_args = len(node.get_arguments())
        
        #Create the frame, name, and delete buttons
        self.pos = vec2(x,y)
        self.frame = ttk.Frame(parent, relief = "solid", borderwidth = 2)
        self.name_label = ttk.Label(self.frame, text = node.get_name())
        self.name_label.grid(column = 0 , row = 0, sticky = (N, W, S))
        self.name_label.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        delete_button = ttk.Button(self.frame, text = "X", width = 1, command = self.destroy)
        delete_button.grid(row = 0, column = 1, sticky = (N, E, S))
        self.frame.place(x = self.pos.x, y = self.pos.y, anchor = NW)
        self.frame.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        self.frame.bind("<1>", lambda e: skip())
        self.name_label.bind("<1>", lambda e: skip())
        
        #Set callbacks
        self.manage_function = manage_function
        self.delete_function = delete_function
        
        #Display arguments
        self.vars = []
        for i in range(len(node.get_arguments())):
            self.vars.append(StringVar())
            arg = node.get_arguments()[i]
            label = ttk.Label(self.frame, text = arg)
            label.grid(row = i + 1, column = 0, sticky = (E, W))
            entry = ttk.Entry(self.frame, width = 18 - len(arg), textvariable = self.vars[i])
            entry.bind("<Return>", lambda e, n = i: self.node.argument(n, self.vars[n].get()))
            entry.bind("<FocusOut>", lambda e, n = i: self.node.argument(n, self.vars[n].get()))
            entry.grid(row = i + 1, column = 1, sticky = (E, W))
        
        #Display return value
        if node.has_return():
            self.return_val = StringVar()
            label = ttk.Label(self.frame, text = "return").grid(row = num_args + 1, column = 0, sticky = (E,W))
            entry = ttk.Entry(self.frame, width = 12, textvariable = self.return_val)
            entry.bind("<Return>", lambda e: self.node.return_value(self.return_val.get()))
            entry.bind("<FocusOut>", lambda e: self.node.return_value(self.return_val.get()))
            entry.grid(row = num_args + 1, column = 1, sticky = (E, W))
        
        ttk.Button(self.frame, text = "True", command = lambda: self.manage(True)).grid(column = 0, row = num_args + 2, sticky = (E, W))
        ttk.Button(self.frame, text = "False", command = lambda: self.manage(False)).grid(column = 1, row = num_args + 2, sticky = (E, W))
    
    def place(self, x, y):
        #Set the position of the widget
        self.pos.x += x
        self.pos.y += y
        self.frame.place(x = self.pos.x, y = self.pos.y, anchor = NW)
        
    def destroy(self):
        #Cleanup the widget
        self.frame.destroy()
        self.delete_function(self)
    
    def manage(self, conditional):
        self.manage_function(self, conditional)
    
    def active_mode(self, manage_function):
        #Disable movement and enable clicking
        self.frame.bind("<B1-Motion>", lambda e: skip())
        self.name_label.bind("<B1-Motion>", lambda e: skip())
        self.frame.bind("<1>", lambda e: manage_function(self))
        self.name_label.bind("<1>", lambda e: manage_function(self))
        
        #Disable buttons
        for i in range(1, len(self.frame.winfo_children())):
            self.frame.winfo_children()[i].state(["disabled"])
        
    
    def passive_mode(self):
        #Enable movement and disable clicking
        self.frame.bind("<1>", lambda e: skip())
        self.name_label.bind("<1>", lambda e: skip())
        self.frame.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        self.name_label.bind("<B1-Motion>", lambda e: self.place(e.x, e.y))
        
        #Enable buttons
        if not self.node.is_head():
            self.frame.winfo_children()[1].state(["!disabled"])
        for i in range(2, len(self.frame.winfo_children())):
            self.frame.winfo_children()[i].state(["!disabled"])
    
    def is_conditional(self):
        return True
    
    def get_node(self):
        return self.node
    
    def get_x(self):
        return self.pos.x
    
    def get_y(self):
        return self.pos.y
    
    def get_width(self):
        return self.frame.winfo_width()
    
    def get_height(self):
        return self.frame.winfo_height()
        
    def get_false_width(self):
        return self.frame.winfo_children()[-1].winfo_width()
    
    def get_true_width(self):
        return self.frame.winfo_children()[-2].winfo_width()
    
    def set_manager(self, manage_function):
        self.manage_function = manage_function
    
    def set_delete(self, delete_function):
        self.delete_function = delete_function
    
    def set_cancel(self, cancel_function):
        self.frame.winfo_children()[-1].bind("<Escape>", lambda e:cancel_function())

if __name__ == "__main__":
    init()
    root = Tk()
    window = Canvas(root, width = 480, height = 480).pack(fill = BOTH, expand = YES)
    ttk.Style().configure("TFrame", background = "#0000ff")
    ttk.Style().configure("TLabel", background = "#ffffff")
    
    head = Head_node("main", ["argc", "argv"], ["int", "char**"], "int")
    node = Node(["msg1", "msg2"], "printf(\"([msg1])\"\"([msg2])\");\n\nreturn 0;\n", "Body", 1)
    
    gui_head = Gui_node(window, head, lambda n: print(n.get_node()), lambda n: print("d head"), 240, 200)
    gui_node = Gui_node(window, node, lambda n: print(n.get_node()), lambda n: print("d node"), 240, 280)
    root.mainloop()
    