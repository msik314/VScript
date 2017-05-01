from node import*
from queue import Queue

def explore(node, adjacency, nodes, visited):
    visited[node.get_id()] += 1
    if visited[node.get_id()] > 1:
        return
    #Depth first search to find branches and joining nodes.
    for i in adjacency[node.get_id()]:
        explore(nodes[i], adjacency, nodes, visited)

def gen_source(nodes, adjacency, head, requires):
    #Setup code generation
    code = ""
    for r in requires:
        code += "#include " + r + "\n"
    code += "\n"
    
    visited = {}
    for i in nodes.keys():
        visited[i] = 0
    explore(head, adjacency, nodes, visited)

    
    blocks = []
    block = []
    node = head
    block_index = 0
    indices = {}
    unchecked = []
    checked = set([])
    
    #Pass over nodes to find blocks.
    while node:
        put = False
        checked.add(node)
        if node in unchecked: unchecked.remove(node)
        
        #Check for joining paths
        if visited[node.get_id()] > 1:
            blocks.append(block[::])
            block = [node]
            block_index += 1
            indices[node.get_id()] = block_index
            put = True
        
        #Check for brancing paths
        if len(adjacency[node.get_id()]) > 1:
            if not put:
                block.append(node)
                indices[node.get_id()] = block_index
            block_index += 1
            blocks.append(block[::])
            block = []
            put = True
        
        #Get next node to process
        candidates = []
        for n in adjacency[node.get_id()]:
            if nodes[n] in checked:
                continue
                
            candidates.append(nodes[n])
        
        if len(candidates) < 1:
            if not put:
                block.append(node)
                indices[node.get_id()] = block_index
            
            blocks.append(block[::])
            block_index += 1
            block = []
            if len(unchecked):
                node = unchecked.pop(0)
            
            else:
                node = None
        
        elif len(candidates) == 1:
            if not put:
                block.append(node)
                indices[node.get_id()] = block_index
            node = candidates[0]
            
        else:
            if not put:
                block.append(node)
                indices[node.get_id()] = block_index
            
            for n in candidates[1::]:
                unchecked.append(n)
            
            node = candidates[0]
    
    #Pass over blocks to generate code
    written_blocks = set()
    q = Queue()
    q.put(blocks[0], False)
    branch = False
    while not q.empty():
        #Process blocks in breadth first order
        current_block = q.get(False)
        if tuple(current_block) in written_blocks:
            branch = False
            continue
        written_blocks.add(tuple(current_block))
        
        #Add block label
        if current_block[0].get_id() != head.get_id():
            code += "Block" + str(indices[current_block[0].get_id()]) + ":\n"
        
        #Write block code
        for n in current_block:
            code += str(n)        
        
        next_block_list = adjacency[current_block[-1].get_id()]
        
        #Process the end of a block or a branch
        for i in range(len(next_block_list)):
            if i > 0:
                code += "else\n"
            
            code += "goto Block" + str(indices[next_block_list[i]]) + ";\n"
            next_block = blocks[indices[next_block_list[i]]]
            if tuple(next_block) in written_blocks:
                continue
                
            q.put(next_block, False)
    return code + "}\n"
    
if __name__ == "__main__":
    filename = input("Enter output file: ")
    init()
    reqs = ["<cstdio>"]
    head = Head_node("main", ["argc", "argv"], ["int", "char**"], "int")
    cond = Node(["expr"], "if(([expr]) > 1)")
    cond.argument(0, "argc")
    true = Node([], "printf(\"Extra arguments given\\n\");")
    false = Node([], "printf(\"Hello World!\\n\");")
    tg = Node([], "printf(\"Joined back up!\\n\");")
    ret = Node([], "return 0;")
    
    nodes = {}
    nodes[head.get_id()] = head
    nodes[cond.get_id()] = cond
    nodes[true.get_id()] = true
    nodes[false.get_id()] = false
    nodes[tg.get_id()] = tg
    nodes[ret.get_id()] = ret
    
    adj = {}
    adj[head.get_id()] = [cond.get_id()]
    adj[cond.get_id()] = [true.get_id(), false.get_id()]
    adj[true.get_id()] = [tg.get_id()]
    adj[false.get_id()] = [tg.get_id()]
    adj[tg.get_id()] = [ret.get_id()]
    adj[ret.get_id()] = []
    
    code = gen_source(nodes, adj, head, reqs)
    print(code, file = open(filename, "w"), end = "")