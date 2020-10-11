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


#I want to keep track of what direction I took to get into the room (keep stack)
stack = []
    
visited = {player.current_room.id}

#exploring all unexplored rooms
#will create stack, traversal path, and a visted set     
while True:
    #finding unexplored exit
    for direction in player.current_room.get_exits():
        if get_room_in_direction(player, direction) not in visited:
            player.travel(direction)
            traversal_path.append(direction)
            stack.append(direction)
            visited.add(player.current_room.id)
            break
    #otherwise backtrack
    else:
        if not stack: #when you can no longer backtrack anymore
            break
        direction = opposite_direction(stack.pop()) #backtrack to reach earlier unexplored exits
        player.travel(direction)
        traversal_path.append(direction)


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
