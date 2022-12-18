import logging, Colorer
from tqdm import tqdm
from collections import deque

'''
What is the surface area of your scanned lava droplet?
'''

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
log = logging.getLogger()

with open('inputs/Day18.txt') as inputFile:
    lines = inputFile.read().splitlines()

droplets = deque()
for line in lines:
    droplets.append(eval(f'({line})'))

totalDroplets = len(droplets)
contiguousFaces = 0

while droplets:
    x,y,z = droplets.pop()
    # Check neighbours, count contiguous faces
    for delta in [-1,1]:
        if (x+delta, y, z) in droplets: contiguousFaces += 1
        if (x, y+delta, z) in droplets: contiguousFaces += 1
        if (x, y, z+delta) in droplets: contiguousFaces += 1

    
area = 6 * totalDroplets - 2 * contiguousFaces
print(f'The surface area of the lava droplet is: {area}')