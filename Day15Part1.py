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

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()

with open('inputs/Day15.txt') as input:
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
# Sample: X: -2 - 25, Y: 0 - 22
# Real: X: -893678 - 3999864, Y: -690123 - 3975025

row = 10 if maxY < 2_000_000 else 2_000_000

# Check how much each sensor projects onto the given line
covered = set()
for sensor in sensors:
    distance = abs(sensor.location[1]-row)
    log.debug(f'Sensor at {sensor.location} is {distance} away from row {row}, with a range of {sensor.range}.')
    if distance < sensor.range:
        coverage = (sensor.range - distance) * 2 + 1
        fromX = sensor.location[0] - int(coverage/2)
        toX = sensor.location[0] + int(coverage/2)
        log.debug(f'{coverage} cells are covered, from {fromX} to {toX}.')
        for x in range(fromX, toX):
            covered.add((x,row))

blankPositions = (maxX - minX) - len(covered)

print(f'{len(covered)} positions cannot contain a beacon.')
assert len(covered) < 5942321, 'Answer is too high!'
