from node import *

def get_builtins():
    b = []
    b.append(Node([], ";", "End"))
    b.append(Node(["type", "variable"], "([type]) ([variable]);", "Declaration"))
    b.append(Node(["variable", "value"], "([variable]) = ([value]);", "Assignment"))
    b.append(Node(["value"], "return ([value]);", "Return"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) + ([op2]);", "Add"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) - ([op2]);", "Subtract"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) * ([op2]);", "Multiply"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) / ([op2]);", "Divide"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) % ([op2]);", "Modulus"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) && ([op2]);", "And"))
    b.append(Node(["op1", "op2"], "([return]) = ([op1]) || ([op2]);", "Or"))
    
    return b