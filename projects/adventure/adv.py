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


graph = {}

def bfs(graph, starting_room):

    q = Queue()

    visited_set = set()

    q.enqueue([starting_room])

    while q.size() > 0:
        path = q.dequeue()
        check_room = path[-1]

        if check_room not in visited_set:
            visited_set.add(check_room)

            for room in graph[check_room]:
                if graph[check_room][room] == '?':
                    return path

            for e_exit in graph[check_room]:
                neighbor = graph[check_room][e_exit]
                path_copy = list(path)
                path_copy.append(neighbor)
                q.enqueue(path_copy)
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
                newRoomID = player.current_room.id


                if newRoomID not in graph:
                    graph[newRoomID] = {}
                    for exit in player.current_room.get_exits():
                        graph[newRoomID][exit] = '?'

            graph[current_roomid][roomExit] = newRoomID
            graph[newRoomID][opposite_direction(roomExit)] = current_roomid
            current_roomid = newRoomID

    pathOfRooms = bfs(graph, player.current_room.id)
    print(pathOfRooms)

    if pathOfRooms is not None:
        for room in pathOfRooms:
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
