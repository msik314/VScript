class vec2(object):
    #This is a basic 2D vector
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return vec2(x + other.x, y + other.y)
    
    def __sub__(self, other):
        return vec2(x - other.x, y - other.y)
    
    def __eq__(self, other):
        return x == other.x and y == other.y
    
    def __neq__(self, other):
        return not (self == other)