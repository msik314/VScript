from tkinter import*
from tkinter import ttk
from tkinter import filedialog
from node import *
from vec2 import *
from guinode import *
from scriptgraph import *
import compiler
import graphstarter

class App(object):
    def __init__(self, root, canvas, standard, custom, reqs):
        #Initialize members
        self.standard = standard
        self.custom = custom
        self.reqs = reqs
        self.conditional = Node(["expr"], "if(([expr]))", "If/Else")
        self.canvas = canvas
        self.root = root
        
        #Create head
        starter = graphstarter.Starter()
        starter.start_graph(root, canvas)
        head = starter.gen_node()
        starter.destroy()
        self.sg = Script_graph(canvas, head)
        
        #Create menu bar
        self.menu_bar = Menu(root)
        menu_file = Menu(self.menu_bar)
        menu_file.add_command(label = "New", command = self.restart)
        
        menu_mods = Menu(self.menu_bar)
        menu_std = Menu(menu_mods)
        for i in range(len(self.standard)):
            menu_std.add_command(label = self.standard[i].get_name(), command = lambda s = i: self.add_node(self.standard[s]))
        
        menu_ctm = Menu(menu_mods)
        for i in range(len(self.custom)):
            menu_ctm.add_command(label = self.custom[i].get_name(), command = lambda c = i: self.add_node(self.custom[c]))
        
        menu_mods.add_cascade(menu = menu_std, label = "Standard")
        menu_mods.add_cascade(menu = menu_ctm, label = "Custom")
        menu_mods.add_command(label = "If/Else", command = self.add_conditional)
        
        self.menu_bar.add_cascade(menu = menu_file, label = "File")
        self.menu_bar.add_cascade(menu = menu_mods, label = "Module")
        self.menu_bar.add_command(label = "Compile", command = self.comp)
        
        self.root["menu"] = self.menu_bar
    
    def restart(self):
        #Detroy menu
        self.menu_bar.destroy()
        
        #Restart graph
        self.sg.destroy()
        sg.draw()
        starter = graphstarter.Starter()
        starter.start_graph(self.root, self.canvas)
        head = starter.gen_node()
        starter.destroy()
        self.sg = Script_graph(self.canvas, head)
        
        #Recreate menu
        self.menu_bar = Menu(self.root)
        menu_file = Menu(self.menu_bar)
        menu_file.add_command(label = "New", command = self.restart)
        
        menu_mods = Menu(self.menu_bar)
        menu_std = Menu(menu_mods)
        for i in range(len(self.standard)):
            menu_std.add_command(label = self.standard[i].get_name(), command = lambda: self.add_node(self.standard[i]))
        
        menu_ctm = Menu(menu_mods)
        for i in range(len(self.standard)):
            menu_ctm.add_command(label = self.custom[i].get_name(), command = lambda: self.add_node(self.custom[i]))
        
        menu_mods.add_cascade(menu = menu_std, label = "Standard")
        menu_mods.add_cascade(menu = menu_ctm, label = "Custom")
        menu_mods.add_command(label = "If/Else", command = self.add_conditional)
        
        self.menu_bar.add_cascade(menu = menu_file, label = "File")
        self.menu_bar.add_cascade(menu = menu_mods, label = "Module")
        self.menu_bar.add_command(label = "Compile", command = self.comp)
        
        self.root["menu"] = self.menu_bar
    
    def comp(self):
        #Open save dialog
        filename = filedialog.asksaveasfilename()
        if filename == "":
            return
        
        #Compile the program
        nodes, adjacency, head = self.sg.gen_graph_data()
        code = compiler.gen_source(nodes, adjacency, head, self.reqs)
        
        #Write output to file
        file = open(filename, 'w')
        file.write(code)
        file.close()
    
    def add_node(self, node):
        gn = Gui_node(self.canvas, copy_node(node), self.sg.activate, self.sg.remove_node, 20, 20)
        self.sg.add_node(gn)
    
    def add_conditional(self):
        gc = Gui_conditional(self.canvas, copy_node(self.conditional), self.sg.activate, self.sg.remove_node, 20, 20)
        self.sg.add_node(gc)
    
    def draw(self):
        self.sg.draw()