from tkinter import*
from tkinter import ttk
from node import *
from app import *
import time
import builtinloader

def read_module(filename):
    file = open(filename)
    #Read name
    name = file.readline().strip()
    
    #Read dependencies
    reqs = file.readline().split(' ')
    for i in range(len(reqs) - 1, -1, -1):
        if(reqs[i] == ""):
            reqs.pop(i)
            continue
        
        reqs[i] = reqs[i].strip()
        
    reqs = set(reqs)
    
    #Read arguments
    args = file.readline().split(' ')
    for i in range(len(args) - 1, -1, -1):
        if(args[i] == ""):
            args.pop(i)
            continue
        
        args[i] = args[i].strip()
    
    #Read snippet
    snippet = file.read()
    
    file.close()
    return reqs, Node(args, snippet, name)

def load_modules():
    mods = []
    reqs = set([])
    file = open("modules.txt")
    
    #Read all the modules listed
    for line in file:
        line = line.strip()
        r, m = read_module(line)
        mods.append(m)
        reqs |= r
    
    file.close()
    return mods, reqs

def startup():
    init()
    b = builtinloader.get_builtins()
    m, r = load_modules()
    
    return b, m, r


if __name__ == "__main__":
    #Load modules
    standard, custom, reqs = startup()
    
    #Start Tk
    root = Tk()
    root.option_add("*tearOff", FALSE)
    
    ttk.Style().configure("TFrame", background = "#0000ff")
    ttk.Style().configure("TLabel", background = "#ffffff")
    canvas = Canvas(root, width = 1280, height = 720)
    canvas.pack(expand = True, fill = BOTH)
    
    #Start application
    application = App(root, canvas, standard, custom, reqs)
    
    #Upadte apllication
    last_time = time.clock()
    while True:
        try:
            root.update_idletasks()
            root.update()
            
            application.draw()
            
            time.sleep(max(0, 1/60 - (time.clock() - last_time)))
            last_time = time.clock()
        except:
            break