import logging, Colorer
from queue import PriorityQueue

'''
What is the fewest steps required to move from your current position to the location that should get the best signal?
'''

class Node:
    def __init__(self, value, coordinates) -> None:
        self.value = value
        self.coordinates = coordinates
        self.distance = 1_000_000
        self.neighbours = []

    def __lt__(self, other):
        return self.distance < other.distance

    def __str__(self) -> str:
        return f'{self.coordinates} {self.value} ({self.distance}) {[neighbour.coordinates for neighbour in self.neighbours]}'

logging.basicConfig(format='%(message)s', level=logging.WARN)
log = logging.getLogger()

with open('inputs/Day12.txt') as input:
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
graph = {}

for y in range(len(map)):
    for x in range(len(map[y])):
        node = Node(map[y][x], (x,y))
        graph[(x,y)] = node

# Map neighbours
for y in range(len(map)):
    for x in range(len(map[y])):
        node = graph[(x,y)]
        # elevation of the destination square can be at most one higher than the elevation of your current square
        if x + 1 < len(map[y]) and map[y][x + 1] <= node.value + 1:
            node.neighbours.append(graph[(x + 1, y)])

        if y + 1 < len(map) and map[y + 1][x] <= node.value + 1:
            node.neighbours.append(graph[(x, y + 1)])

        if y - 1 >= 0 and map[y - 1][x] <= node.value + 1:
            node.neighbours.append(graph[(x, y - 1)])

        if x - 1 >= 0 and map[y][x - 1] <= node.value + 1:
            node.neighbours.append(graph[(x - 1, y)])

graph[start].distance = 0
log.debug('\n'.join([f'{vertex}' for vertex in graph.values()]))

# Visit nodes
unvisited = PriorityQueue()
unvisited.put(graph[start])
visited = []
predecessor = {}

while unvisited.qsize() > 0:
    bestVertex = unvisited.get()
    log.debug(f'Best vertex: {bestVertex}')
    visited.append(bestVertex)

    for neighbour in bestVertex.neighbours:
        if neighbour not in visited:
            distance = bestVertex.distance + 1
            if distance < neighbour.distance:
                neighbour.distance = distance
                log.debug(f'Put {neighbour} in queue with distance {distance}')
                unvisited.put(neighbour)
                predecessor[neighbour] = bestVertex
    
# Find the shortest path
path = []
nextNode = graph[end]
while nextNode in predecessor.keys():
    path.append(nextNode)
    nextNode = predecessor[nextNode]

log.info(f'Path: {[str(node.coordinates) for node in reversed(path)]}')

print(f'The fewest steps required is {graph[end].distance}')