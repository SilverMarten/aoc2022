import logging, Colorer
from tqdm import tqdm

def printMap(map):
    mapString = ''#f'    {minX}\n'
    for y in range(len(map)):
        mapString += f'{y:7}' + ' ' + ''.join(map[y]) + '\n'

    return mapString

def manhattanDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

class Sensor:
    def __init__(self, location, beacon) -> None:
        self.location = location
        self.beacon = beacon
        self.range = manhattanDistance(location, beacon)

    def __str__(self) -> str:
        return f'Sensor at x={self.location[0]}, y={self.location[1]}: ' +\
                 f'closest beacon is at x={self.beacon[0]}, y={self.beacon[1]} ' +\
                 f'(distance={self.range})'
        
'''
In the row where y=2000000, how many positions cannot contain a beacon?
'''

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day15 sample.txt') as input:
    lines = input.read().splitlines()

# Parse the input
minX = 1_000_000
minY = 1_000_000
maxX = 0
maxY = 0

sensors = []
for line in lines:
    sensorString = line.split(':')[0]
    location = (int(sensorString.split(', y')[0][sensorString.find('=')+1:]), \
                int(sensorString.split(', y')[1][1:]))
    beaconString = line.split(':')[1]
    beacon = (int(beaconString.split(', y')[0][beaconString.find('=')+1:]), \
              int(beaconString.split(', y')[1][1:]))
    sensor = Sensor(location, beacon)
    log.debug(sensor)

    sensors.append(Sensor(location, beacon))
    for coordinate in [location, beacon]:
        if coordinate[0] > maxX: maxX = coordinate[0]
        if coordinate[0] < minX: minX = coordinate[0]
        if coordinate[1] > maxY: maxY = coordinate[1]
        if coordinate[1] < minY: minY = coordinate[1]

log.info(f'X: {minX} - {maxX}, Y: {minY} - {maxY}')
# Sample: X: 494 - 503, Y: 4 - 9
# Real: X: 483 - 557, Y: 13 - 170
exit()
# Create/draw the map
minX -= 1
map = [['.' for x in range(minX, maxX+1)] for y in range(maxY+1)]
# log.debug(printMap(map))

for line in rockLines:
    # log.debug(line)
    for i in range(len(line)-1):
        fromPoint = line[i]
        toPoint = line[i+1]
        if(fromPoint[0] == toPoint[0]):
            # Vertical
            x = fromPoint[0] - minX
            for y in range(min(fromPoint[1],toPoint[1]), max(fromPoint[1],toPoint[1])+1):
                map[y][x] = '#'
        else:
            # Horizontal
            for x in range(min(fromPoint[0],toPoint[0]), max(fromPoint[0],toPoint[0])+1):
                map[fromPoint[1]][x - minX] = '#'

sandStart = 500 - minX
map[0][sandStart] = '+'
log.debug(f'  {minX}\n' + printMap(map))

# Simulate sand
unitsOfSand = 0
sandLimit = (maxX-minX)*maxY
while unitsOfSand < sandLimit:
    x = sandStart
    topOfSand = min([y for y in range(maxY+1) if map[y][x] not in ['.', '+']]) - 1 
    if topOfSand == maxY:
        break

    while map[topOfSand + 1][x-1] == '.' or map[topOfSand + 1][x+1] == '.' or map[topOfSand + 1][x] == '.':
        if map[topOfSand + 1][x] == '.':
            pass
        elif map[topOfSand + 1][x-1] == '.':
            x -= 1
        elif map[topOfSand + 1][x+1] == '.':
            x += 1

        topOfSand += 1
        if topOfSand >= maxY:
            sandLimit = unitsOfSand
            break
    
    map[topOfSand][x] = 'o'
    unitsOfSand += 1
    if unitsOfSand in [1, 2, 3, 5, 22]:
        log.debug(f'{unitsOfSand}:\n  {minX}\n' + printMap(map))

log.info(f'{unitsOfSand}:\n  {minX}\n' + printMap(map))
print(f'{unitsOfSand-1} units of sand come to rest before sand starts flowing into the abyss below.')

