import logging, Colorer
from tqdm import tqdm
from collections import deque

'''
What is the surface area of your scanned lava droplet (without pockets)?
'''

def isPocket(coordinates, droplets):
    '''There a contained pocket here.'''
    x,y,z = coordinates
    dropletCount = 0
    for delta in [-1,1]:
        if (x+delta, y, z) in droplets: 
            dropletCount += 1
        if (x, y+delta, z) in droplets: 
            dropletCount += 1
        if (x, y, z+delta) in droplets: 
            dropletCount += 1

    return dropletCount == 6

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day18.txt') as inputFile:
    lines = inputFile.read().splitlines()

droplets = deque()
for line in lines:
    droplets.append(eval(f'({line})'))

allDroplets = set(droplets)
totalDroplets = len(droplets)
contiguousFaces = 0
pockets = set()

while droplets:
    x,y,z = droplets.pop()
    # Check neighbours, count contiguous faces
    for delta in [-1,1]:
        if (x+delta, y, z) in droplets: 
            contiguousFaces += 1
        elif isPocket((x+delta, y, z), allDroplets):
            pockets.add((x+delta, y, z))
        if (x, y+delta, z) in droplets: 
            contiguousFaces += 1
        elif isPocket((x, y+delta, z), allDroplets):
            pockets.add((x, y+delta, z))
        if (x, y, z+delta) in droplets: 
            contiguousFaces += 1
        elif isPocket((x, y, z+delta), allDroplets):
            pockets.add((x, y, z+delta))

log.debug(f'{len(pockets)} at: {sorted(pockets)}')

area = 6 * totalDroplets - 2 * contiguousFaces - 6 * len(pockets)
print(f'The surface area of the lava droplet is: {area}')