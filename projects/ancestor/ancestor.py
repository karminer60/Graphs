class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = set()

    def add_edge(self, v1, v2):
        
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            print("That vertex does not exist")


def earliest_ancestor(ancestors, starting_node):
    
    graph = Graph()
    for pair in ancestors:
        graph.add_vertex(pair[0])
        graph.add_vertex(pair[1])
        
        graph.add_edge(pair[1], pair[0])
    
    max_path_len = 1
    earliest_ancestor = -1
    
    q = Queue()
    q.enqueue([starting_node])
    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        
        if (len(path) >= max_path_len and v < earliest_ancestor) or (len(path) > max_path_len):
            earliest_ancestor = v
            max_path_len = len(path)
        for neighbor in graph.vertices[v]:
            path_copy = list(path)
            path_copy.append(neighbor)
            q.enqueue(path_copy)
    
    return earliest_ancestor
        