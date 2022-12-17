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
        self.neighbourLabels = neighbourLabels
        self.neighbours = []

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self) -> str:
        return f'{self.label} {self.flowRate} {self.neighbourLabels}'

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

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()

with open('inputs/Day16 sample.txt') as inputFile:
    lines = inputFile.read().splitlines()

valves = {}
# Parse the input
for line in lines:
    label = line[6:8]
    flowRate = int(line.split(';')[0][23:])
    neighbourLabels = line.split('valve')[1].replace('s', '').strip().split(', ')
    valves[label] = Valve(label, flowRate, neighbourLabels)
    
log.info('\n'.join([str(valve) for valve in valves.values()]))

# Build the graph
for valve in valves.values():
    valve.neighbours.extend([valves[neighbour] for neighbour in valve.neighbourLabels])

toGml(valves.values())

start = valves['AA']
maxTime = 30
openableValves = [openable for openable in valves.values() if openable.flowRate > 0]

# Visit nodes
# See: https://www.techiedelight.com/maximum-cost-path-graph-source-destination/
 
# Create a queue for doing BFS (avoids stack overflow)
queue = deque()

# Add source vertex to list and enqueue it
path = list([start])

# Append state:
# (current vertex, current path cost, minutes elapsed, current path)
queue.append((start, 0, 0, path, set(openableValves)))

# Store maximum cost of a path from the source
maxPressure = -1
maxPath = []

paths = set()

# Loop till queue is empty
while queue:

    # Dequeue front node (current state)
    valve, pressure, time, path, remainingValves = queue.popleft()

    # Check if this path has already been covered
    if ''.join([node.label for node in path]) in paths: continue

    log.debug(f'From {valve.label}: pressure released {pressure}, {time} minutes, ({[node.label for node in path]})')

    # Do for every adjacent edge of `v`
    for destNode in valve.neighbours:
        # Setup new state for visiting node
        newTime = time + 1
        newRemainingValves = set(remainingValves)    # Make a copy for the next itteration
        # If the node has an unopened valve, and there's time, open it
        pressureReleased = 0
        if destNode.flowRate > 0 and destNode in newRemainingValves and newTime < maxTime:
            newRemainingValves.remove(destNode)
            pressureReleased = destNode.flowRate * (maxTime - newTime - 1)
            newTime += 1

        # If all valves are open, or maxTime is reached, 
        # check if this is the new max pressure, save the path, then continue
        if len(newRemainingValves) == 0 or newTime >= maxTime:
            paths.add(''.join([node.label for node in path]))
            if pressure + pressureReleased > maxPressure:
                maxPressure = pressure + pressureReleased
                maxPath = list(path)
                maxPath.append(destNode)
                log.info(f'New max pressure: {maxPressure} in {newTime} minutes: ({[node.label for node in maxPath]})')
            else:
                log.info(f'Done after {newTime} minutes: max pressure: {maxPressure} on path ({[node.label for node in maxPath]})')
            continue
            

        # If the next node would be the same we just came from,
        # and a valve was not opened, skip it
        # if newTime == time + 1 and len(path) > 1 and destNode == path[-2]:
        #     continue 

        # Push the new state onto the queue

        newPath = list(path)
        newPath.append(destNode)
        queue.append((destNode, pressure + pressureReleased, newTime, newPath, newRemainingValves))

    if log.level == logging.DEBUG:
        input()


print(f'The maximum pressure released is {maxPressure}')