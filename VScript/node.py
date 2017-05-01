def init():
    global NODE_ID
    NODE_ID = 0

def get_node_id():
    global NODE_ID
    NODE_ID += 1
    return NODE_ID - 1

class Head_node(object):
    def __init__(self, name, args, types, return_type, tabs = 0):
        #Initializations
        self.name = name
        self.args = args
        self.types = types
        self.tabs = 0
        self.return_type = return_type
        self.id = get_node_id()

    def get_name(self):
        return self.name
    
    def get_arguments(self):
        return self.args[::]
    
    def get_types(self):
        return self.types[::]
    
    def get_return_type(self):
        return self.return_type
    
    def get_id(self):
        return self.id
    
    def set_tabs(self, tabs):
        self.tabs = tabs
    
    def has_return(self):
        return False
    
    def is_head(self):
        return True
    
    def __str__(self):
        #Add function declaration
        code = "\t" * self.tabs
        code += self.return_type + " " + self.name + "("
        #Add arguments
        for i in range(len(self.args) - 1):
            code += self.types[i] + " " + self.args[i] + ", "
        if len(self.args) > 0 :
            code += self.types[-1] + " " + self.args[-1]
        #Add open brace
        code += ")\n" + "\t" * self.tabs + "{\n"
        return code

class Node(object):
    def __init__(self, args, snippet, name = "", tabs = 0):
        self.args = args[::]
        self.snippet = snippet
        self.vars = args[::]
        self.ret_val = None
        self.tabs = tabs
        self.name = name
        self.id = get_node_id()
    
    def get_name(self):
        return self.name
    
    def get_arguments(self):
        return self.args[::]
    
    def get_id(self):
        return self.id
    
    def get_snippet(self):
        return self.snippet[::]
    
    def argument(self, index, arg):
        self.vars[index] = arg
    
    def get_arguments(self):
        return self.args[::]
    
    def get_types(self):
        return self.types[::]
    
    def get_vars(self):
        return self.vars[::]
    
    def return_value(self, name):
        self.ret_val = name
    
    def get_return(self):
        return self.ret_val
    
    def set_tabs(self, tabs):
        self.tabs = tabs
    
    def get_tabs(self):
        return self.tabs
    
    def has_return(self):
        return self.snippet.find("([return])") >= 0
    
    def is_head(self):
        return False
    
    def __str__(self):
        #Add base snippet
        code = "\t" * self.tabs + self.snippet
        
        #Replace arguments with values
        for i in range(len(self.args)):
            arg = "([" + self.args[i] + "])"
            var = self.vars[i]
            code = code.replace(arg, var);
        
        #add return value
        if self.ret_val:
            code = code.replace("([return])", self.ret_val)
        
        code.replace("\n", "\n" + "\t" * self.tabs)
        code += "\n"
        return code
    
    def _eq_(self, other):
        return self.id == other.id

def copy_node(node):
    n = Node(node.get_arguments(), node.get_snippet(), node.get_name(), node.get_tabs())
    n.return_value(node.get_return())
    return n

if __name__ == "__main__":
    #Test code
    init()
    head = Head_node("add", ["x", "y"], ["int", "int"], "int") 
    node = Node(["x", "y"], "([return]) = ([x]) + ([y]);", 1)
    node.argument(0, "a")
    node.argument(1, "b")
    node.return_value("c")
    print(head, end = "")
    print(node, end = "")
    print("}\n")