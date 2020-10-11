from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
#I want to keep track of what direction I took to get into the room (keep stack)
#list of spots I want to visit
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

def opposite_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def get_room_in_direction(player, direction):
    player.travel(direction)
    neighbor_id  = player.current_room.id
    player.travel(opposite_direction(direction))
    return neighbor_id

def dft(graph, starting_room):

    stack = Stack()
        
        visited = set()
        
        stack.push(direction)
        
        while stack.size() > 0:
            for direction in player.current_room.get_exits():
                if get_room_in_direction(player, direction) not in visited:
                    player.travel(direction)
                    stack.push(direction)

            current_direction = stack.pop()
            
            if current_direction not in visited:
                
                visited.add(current_node)
                print(current_node)
                
                
                edges = self.get_neighbors(current_node)
                
                for edge in edges:
                    stack.push(edge)
    return None


while len(graph) < len(room_graph):
    current_roomid = player.current_room.id
    if current_roomid not in graph:
        graph[current_roomid] = {}
        for exit in player.current_room.get_exits():
            graph[current_roomid][exit] = "?"
    for direction in graph[current_roomid]:
        if direction not in graph[current_roomid]:
            break
        if graph[current_roomid][direction] == '?':
            roomExit = direction
            if roomExit is not None:
                traversal_path.append(roomExit)
                player.travel(roomExit)
                new_room_id = player.current_room.id


                if new_room_id not in graph:
                    graph[new_room_id] = {}
                    for exit in player.current_room.get_exits():
                        graph[new_room_id][exit] = '?'

            graph[current_roomid][roomExit] = new_room_id
            graph[new_room_id][opposite_direction(roomExit)] = current_roomid
            current_roomid = new_room_id

    room_paths = dft(graph, player.current_room.id)
    print(room_paths)

    if room_paths is not None:
        for room in room_paths:
            for exit in graph[current_roomid]:
                print(f"{graph[current_roomid]}")
                if graph[current_roomid][exit] == room:
                    traversal_path.append(exit)
                    player.travel(exit)


    current_roomid = player.current_room.id

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
