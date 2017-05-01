from tkinter import*
from tkinter import ttk
from node import *
from vec2 import *
from guinode import *
import compiler
import time

class Script_graph(object):
    def __init__(self, canvas, head):
        self.nodes = set([head])
        self.edges = set([])
        self.head = head
        self.active = None
        self.condition = False
        head.set_manager(self.activate)
        head.set_delete(self.remove_node)
        self.canvas = canvas
    
    def destroy(self):
        #Destroy all nodes
        for node in list(self.nodes):
            node.destroy()
    
    def add_node(self, node):
        #Add new nde
        if not node in self.nodes:
            self.nodes.add(node)
    
    def remove_node(self, node):
        #Check if attempting to remove head
        if node is self.head:
            return
        
        #Check if the node is in the graph
        if not node in self.nodes:
            return
        
        #Remove the node
        self.nodes.remove(node)
        
        #Remove the edges connected to the node
        to_remove = []
        for edge in self.edges:
            if edge[0] is node or edge[1] is node:
                to_remove.append(edge)
        
        for edge in to_remove:
            self.edges.remove(edge)
    
    def add_edge(self, node1, node2, condition = False):
        #Add the edge if it doens't exist
        edge = (node1, node2, condition)
        if not edge in self.edges:
            self.edges.add(edge)
            return True
            
        return False
    
    def unlink_active(self, condition = False):
        #Remove any edges that start at the current node with the same condition
        for edge in self.edges:
            if edge[0] == self.active and edge[2] == condition:
                self.edges.remove(edge)
                return True
        
        return False
    
    def activate(self, node, condition = False):
        #Set current node
        self.condition = condition
        self.active = node
        
        #Set cancel callback
        self.active.set_cancel(self.cancel_edge)
        
        #Unlnk current node
        self.unlink_active(condition)
        
        #Set all nodes to active mode
        for node in self.nodes:
            node.active_mode(self.process_edge)
    
    def process_edge(self, node2):
        #Add node2 if it is not already in the graph
        self.add_node(node2)
        
        #Add the edge from the active node
        self.add_edge(self.active, node2, self.condition)
        
        #Cleanup after the edge
        self.cancel_edge()
    
    def cancel_edge(self):
        #Cleanup active node
        self.active.set_cancel(skip)
        self.active = None
        self.condition = False
        
        #Set nodes to passive mode
        for node in self.nodes:
            node.passive_mode()
    
    def gen_graph_data(self):
        nodes = {}
        adjacency = {}
        
        #Generate the dictionary of nodes
        for node in self.nodes:
            nodes[node.get_node().get_id()] = node.get_node()
            adjacency[node.get_node().get_id()] = []
        
        #generate the adjacency List
        for edge in self.edges:
            node_id = edge[0].get_node().get_id()
            if edge[2]:
                adjacency[node_id].insert(0, edge[1].get_node().get_id())
            else:
                adjacency[node_id].append(edge[1].get_node().get_id())
        
        #Check to see there is a single sink
        empty = 0
        for key in adjacency.keys():
            if len(adjacency[key]) == 0:
                empty += 1
        
        if empty <= 1:
            return nodes, adjacency, self.head.get_node()
        
        #Create sink node
        return_value = ";\n"
        if self.head.get_node().get_return_type() != "void":
            return_value = " {};\n"
        
        #set empty links to sink node
        safety = Node([], "return" + return_value, "Safety", 1)
        nodes[safety.get_id()] = safety
        for key in adjacency.keys():
            if len(adjacency[key]) == 0:
                adjacency[key] = [safety.get_id()]
        
        adjacency[safety.get_id()] = []
        
        return nodes, adjacency, self.head.get_node()
    
    def draw(self):
        #Clear edges
        self.canvas.delete("all")
        
        #Draw all edges
        for e in self.edges:
            x0 = e[0].get_x() + e[0].get_width() // 2
            x1 = e[1].get_x() + e[1].get_width() // 2
            y0 = e[0].get_y() + e[0].get_height() - 5
            y1 = e[1].get_y() + 5
            if e[0].is_conditional():
                if e[2]:
                    x0 = e[0].get_x() + e[0].get_true_width() // 2
                else:
                    x0 = e[0].get_x() + e[0].get_width() - e[0].get_false_width() // 2
            self.canvas.create_line(x0, y0, x0, y0 + 20, x1, y1 - 20, x1, y1, arrow = LAST)   
    
if __name__ == "__main__":
    init()
    root = Tk()
    window = Canvas(root, width = 480, height = 480)
    window.pack(fill = BOTH, expand = YES)
    ttk.Style().configure("TFrame", background = "#0000ff")
    ttk.Style().configure("TLabel", background = "#ffffff")
    
    head = Head_node("main", ["argc", "argv"], ["int", "char**"], "int")
    node = Node(["message"], "printf(\"([message])\");\n\n\treturn 0;\n", "Body", 1)
    cond = Node(["expr"], "if(([expr]))", "Conditional", 1)
    
    gui_head = Gui_node(window, head, skip, skip, 0, 0)
    sg = Script_graph(window, gui_head)
    
    gui_node = Gui_node(window, node, sg.activate, sg.remove_node, 100, 240)
    sg.add_node(gui_node)
    
    gui_cond = Gui_conditional(window, cond, sg.activate, sg.remove_node, 100, 120)
    sg.add_node(gui_cond)
    
    last_time = time.clock()
    while True:
        try:
            root.update_idletasks()
            root.update()
            sg.draw()
            time.sleep(max(0, 1/60 - (time.clock() - last_time)))
            last_time = time.clock()
        except:
            break
    nodes, adjacency, head = sg.gen_graph_data()
    print(compiler.gen_source(nodes, adjacency, head, ["<cstdio>"]))
    sg.destroy()