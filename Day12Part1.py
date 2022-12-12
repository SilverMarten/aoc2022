import logging, Colorer
from queue import PriorityQueue

'''
What is the fewest steps required to move from your current position to the location that should get the best signal?
'''

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.distance = 1_000_000
        self.neighbours = {}

    def __str__(self) -> str:
        return f'{self.value} ({self.distance}) {self.neighbours.keys()}'

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day12 sample.txt') as input:
    lines = input.read().splitlines()

map = []
start = None
end = None

# Parse the map
for i in range(len(lines)):
    line = lines[i]
    logging.debug(line)
    if 'S' in line:
        start = (line.find('S'),i)
        line = line.replace('S', 'a')
    if 'E' in line:
        end = (line.find('E'),i)
        line = line.replace('E', 'z')
    
    map.append([ord(height)-ord('a') for height in line])

log.debug(f'Start: {start}')
log.debug(f'End: {end}')
for row in map:
    log.debug(' '.join([f'{i:2}' for i in row]))

# Build the graph
graph = {start: Node(0), end: Node(25)}


for y in range(len(map)):
    for x in range(len(map[y])):
        node = Node(map[y][x])
        graph[(x,y)] = node

        # elevation of the destination square can be at most one higher than the elevation of your current square
        if x + 1 < len(map[y]) and map[y][x + 1] <= node.value + 1:
            node.neighbours[(x + 1, y)] = Node(map[y][x + 1]) if (x + 1, y) in graph.keys() else graph[(x + 1, y)]

        if y + 1 < len(map) and map[y + 1][x] <= node.value + 1:
            node.neighbours[(x, y + 1)] = Node(map[y + 1][x]) if (x, y + 1) in graph.keys() else graph[(x, y + 1)]

        if y - 1 > 0 and map[y - 1][x] <= node.value + 1:
            node.neighbours[(x, y - 1)] = Node(map[y - 1][x]) if (x, y - 1) in graph.keys() else graph[(x, y - 1)]

        if x - 1 > 0 and map[y][x - 1] <= node.value + 1:
            node.neighbours[(x - 1, y)] = Node(map[y][x - 1]) if (x - 1, y) in graph.keys() else graph[(x - 1, y)]

graph[start].distance = 0
log.debug('\n'.join([f'{vertex[0]}: {vertex[1]}' for vertex in graph.items()]))

# Visit nodes
unvisited = PriorityQueue()
unvisited.put((0, graph[start]))
visited = []
predecessor = {}

while not unvisited.empty():
    # log.debug(f'Unvisited: {unvisited}')
    bestVertex = unvisited.get()[1]
    visited.append(bestVertex)

    for neighbour in bestVertex.neighbours.values():
        if neighbour not in visited:
            distance = bestVertex.distance + 1
            if distance < neighbour.distance:
                neighbour.distance = distance
                unvisited.put((distance, neighbour))
                predecessor[neighbour] = bestVertex
    
# Find the shortest path
path = []
nextNode = graph[end]
while nextNode in predecessor.keys():
    path.append(nextNode)
    nextNode = predecessor[nextNode]

log.debug(f'Path: {path}')

print(f'The fewest steps required is {graph[end].distance}')