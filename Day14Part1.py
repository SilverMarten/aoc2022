import logging, Colorer
from tqdm import tqdm

'''
How many units of sand come to rest before sand starts flowing into the abyss below?
'''

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day14 sample.txt') as input:
    lines = input.read().splitlines()

# Parse the input
minX = 1_000_000
minY = 1_000_000
maxX = 0
maxY = 0
rockLines = []
for line in lines:
    rockLine = [(int(coordinates[0]), int(coordinates[1])) for coordinates in [pair.split(',') for pair in line.split(' -> ')]]
    rockLines.append(rockLine)
    log.debug(rockLine)
    for coordinate in rockLine:
        if coordinate[0] > maxX: maxX = coordinate[0]
        if coordinate[0] < minX: minX = coordinate[0]
        if coordinate[1] > maxY: maxY = coordinate[1]
        if coordinate[1] < minY: minY = coordinate[1]

log.debug(f'X: {minX} - {maxX}, Y: {minY} - {maxY}')

print(f'{0} units of sand come to rest before sand starts flowing into the abyss below.')

