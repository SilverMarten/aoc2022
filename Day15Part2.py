import logging, Colorer
from tqdm import tqdm
from Tools import between

def printMap(map):
    mapString = ''#f'    {minX}\n'
    for y in range(len(map)):
        mapString += f'{y:7}' + ' ' + ''.join(map[y]) + '\n'

    return mapString

def manhattanDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def inRange(cell, sensors):
    for sensor in sensors:
        if manhattanDistance(cell, sensor.location) <= sensor.range:
            return True
    return False

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
Find the only possible position for the distress beacon. What is its tuning frequency?
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

max = 20 if maxY < 2_000_000 else 4_000_000

# Check around each sensor's range for a cell not covered by another sensor
missingBeacon = None
for sensor in tqdm(sensors):
    x = sensor.location[0] - sensor.range - 1
    y = sensor.location[1]
    yDirection = -1
    xDirection = 1
    while x <= sensor.location[0] + sensor.range + 1:
        if between(x, 0, max) and between(y, 0, max) and not inRange((x,y), sensors):
            missingBeacon = (x,y)
            break
        if x == 0:
            yDirection *= -1
        x += xDirection
        y += yDirection

    xDirection *= -1
    while x >= sensor.location[0] - sensor.range - 1:
        if between(x, 0, max) and between(y, 0, max) and not inRange((x,y), sensors):
            missingBeacon = (x,y)
            break
        if x == 0:
            yDirection *= -1
        x += xDirection
        y += yDirection
    
    if missingBeacon != None:
        break
    
if missingBeacon == None:
    log.error('Missing beacon not found!')
    exit(1)

tuningFrequency = missingBeacon[0] * 4_000_000 + missingBeacon[1]
print(f'The tuning frequency of the beacon at {missingBeacon} is {tuningFrequency}.')
