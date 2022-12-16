import logging, Colorer
from collections import deque

'''
Work out the steps to release the most pressure in 30 minutes.
What is the most pressure you can release?
'''

class Valve:
    def __init__(self, label, flowRate, neighbourLabels) -> None:
        self.label = label
        self.flowRate = flowRate
        self.value = 0
        self.distance = 0
        self.neighbourLabels = neighbourLabels
        self.neighbours = []

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self) -> str:
        return f'{self.label} {self.flowRate} ({self.value}) {self.neighbourLabels}'

def toGml(valves):

    gmlString = 'graph ['

    # Nodes
    nodes = {}
    i = 0
    for valve in valves:
        gmlString += '\nnode [ ' + \
                     f'id {i} label "{valve.label}"' + \
                     f' graphics [type "{"ellipse" if valve.flowRate == 0 else "roundrectangle"}" ' + \
                     f' fill "{"#CC99FF" if valve.label != "AA" else "#990099"}"]' + \
                     ']'
        nodes[valve.label] = i
        i += 1

    # Edges
    connected = []
    for valve in valves:
        for neighbour in valve.neighbourLabels:
            if not neighbour in connected:
                gmlString += '\nedge [ ' + \
                             f'source {nodes[valve.label]} target {nodes[neighbour]}' +\
                             ' ]'
        connected.append(valve.label)

    gmlString += ']'
    
    with open('Day16.gml', mode='w') as output:
        output.write(gmlString)

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day16.txt') as input:
    lines = input.read().splitlines()

valves = {}
# Parse the input
for line in lines:
    label = line[6:8]
    flowRate = int(line.split(';')[0][23:])
    neighbourLabels = line.split('valve')[1].replace('s', '').strip().split(', ')
    valves[label] = Valve(label, flowRate, neighbourLabels)
    
log.debug('\n'.join([str(valve) for valve in valves.values()]))

# Build the graph
for valve in valves.values():
    valve.neighbours.extend([valves[neighbour] for neighbour in valve.neighbourLabels])

toGml(valves.values())

start = valves['AA']
maxDistance = 30

# Visit nodes
# See: https://www.techiedelight.com/maximum-cost-path-graph-source-destination/
 
# create a queue for doing BFS
queue = deque()

# add source vertex to set and enqueue it
vertices = set([start])

# (current vertex, current path cost, set of nodes visited so far in
# the current path)
queue.append((start, 0, 1, vertices))

# stores maximum cost of a path from the source
maxcost = -1

# loop till queue is empty
while queue:

    # dequeue front node
    valve, cost, distance, vertices = queue.popleft()


    # do for every adjacent edge of `v`
    for dest in valve.neighbours:

        # check for a cycle
        # if not dest in vertices:
            log.debug(f'Move to {dest.label}.')
            distance += 1

            # add current node to the path
            path = set(vertices)
            path.add(dest)

            # push every vertex (discovered or undiscovered) into
            # the queue with a cost equal to the
            # parent's cost plus the current edge's weight
            pressureReleased = 0
            if dest.flowRate > 0 and not dest in vertices:
                pressureReleased = dest.flowRate * (maxDistance - distance)
                distance += 1
                log.debug(f'At {distance}, opening valve {dest.label} (will release {pressureReleased} total pressure)')
            queue.append((dest, cost + pressureReleased, distance + 1, path))

    # if the destination is reached and BFS depth is equal to `m`,
    # update the minimum cost calculated so far
    if distance >= maxDistance:
        maxcost = max(maxcost, cost)
        continue

print(f'The maximum pressure released is {maxcost}')