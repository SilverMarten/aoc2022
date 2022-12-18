import logging, Colorer
from tqdm import tqdm
from collections import deque
from Tools import between

'''
What is the surface area of your scanned lava droplet (without pockets)?
'''

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day18.txt') as inputFile:
    lines = inputFile.read().splitlines()

droplets = set()
for line in lines:
    droplets.add(eval(f'({line})'))

# Eureka!
# Create a volume of steam around the chunk of lava and calculate its surface area

minCoordinate = min([min(x,y,z) for x,y,z in droplets]) - 1
maxCoordinate = max([max(x,y,z) for x,y,z in droplets]) + 1

log.debug(f'Checking from {minCoordinate} to {maxCoordinate}.')

# Figure out the locations of the steam droplets
start = (minCoordinate,minCoordinate,minCoordinate)
steam = set()
steam.add(start)
toCheck = deque()
toCheck.append(start)

while toCheck:
    x,y,z = toCheck.pop()
    
    # Check neighbours, add steam to queue and set
    for delta in [-1,1]:
        neighbour = (x+delta, y, z)
        if between(x+delta, minCoordinate, maxCoordinate) and\
             neighbour not in droplets and neighbour not in steam: 
            steam.add(neighbour)
            toCheck.append(neighbour)
        neighbour = (x, y+delta, z)
        if between(y+delta, minCoordinate, maxCoordinate) and\
             neighbour not in droplets and neighbour not in steam: 
            steam.add(neighbour)
            toCheck.append(neighbour)
        neighbour = (x, y, z+delta)
        if between(z+delta, minCoordinate, maxCoordinate) and\
             neighbour not in droplets and neighbour not in steam: 
            steam.add(neighbour)
            toCheck.append(neighbour)

# Find the surface area of the steam
contiguousFaces = 0
steamDroplets = deque(steam)
while steamDroplets:
    x,y,z = steamDroplets.pop()
    # Check neighbours, count contiguous faces
    for delta in [-1,1]:
        if (x+delta, y, z) in steamDroplets: 
            contiguousFaces += 1
        if (x, y+delta, z) in steamDroplets: 
            contiguousFaces += 1
        if (x, y, z+delta) in steamDroplets: 
            contiguousFaces += 1

area = 6 * len(steam) - 2 * contiguousFaces - 6 * (maxCoordinate - minCoordinate + 1) ** 2
print(f'The surface area of the lava droplet is: {area}')