import logging, Colorer
from queue import PriorityQueue

'''
Work out the steps to release the most pressure in 30 minutes.
What is the most pressure you can release?
'''

class Valve:
    def __init__(self, label, flowRate, neighbourLabels) -> None:
        self.label = label
        self.flowRate = flowRate
        self.value = 0
        self.neighbourLabels = neighbourLabels
        self.neighbours = []

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self) -> str:
        return f'{self.label} {self.flowRate} ({self.value}) {self.neighbourLabels}'

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day16 sample.txt') as input:
    lines = input.read().splitlines()

valves = {}
# Parse the input
for line in lines:
    label = line[6:8]
    flowRate = int(line.split(';')[0][23:])
    neighbourLabels = line.split('valve')[1].replace('s', '').strip().split(', ')
    valves[label] = Valve(label, flowRate, neighbourLabels)
    
log.debug('\n'.join([str(valve) for valve in valves.values()]))

exit(0)
# Build the graph


graph[start].distance = 0

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