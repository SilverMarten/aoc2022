import logging, Colorer, math, re
import time
startTime = time.time()

'''
--- Day 23: Unstable Diffusion ---
Simulate the Elves' process and find the smallest 
rectangle that contains the Elves after 10 rounds. 
How many empty ground tiles does that rectangle contain?
'''

class Grid:
    number: str
    start: tuple[int, int]
    cells: list[list[str]]
    size: int
    connections: list["Grid"]

    def __init__(self,number:str, start:tuple[int, int], size:int, cells:list[list[str]]) -> None:
        self.number = number
        self.start = start
        self.size = size
        self.cells = cells
        self.connections = [None for _ in range(4)]

    def __str__(self) -> str:
        return f'{self.number} {self.start}' + CR + '\n'.join([''.join(row) for row in self.cells])

sample = True
logging.basicConfig(format='%(message)s', level=logging.DEBUG if sample else logging.INFO)
log = logging.getLogger()
CR = '\n'

with open(f"inputs/Day23{' sample' if sample else ''}.txt") as fileInput:
    lines = fileInput.read().splitlines()

# Parse lines
elfPositions:set[tuple[int, int]] = set()
for y, line in enumerate(lines):
    for x, character in enumerate(line):
        if character == '#':
            elfPositions.add((x,y))


log.debug(f'Elves: {elfPositions}')

# Follow the directions

# Count the empty tiles
maxX:int = max([x for x,y in elfPositions])
minX:int = min([x for x,y in elfPositions])
maxY:int = max([y for x,y in elfPositions])
minY:int = min([y for x,y in elfPositions])

emptyTiles = (maxX - minX + 1) * (maxY - minY + 1) - len(elfPositions)
print(f'{CR}The number of empty ground tiles is {emptyTiles}')

log.info('Final map:')
for y in range(minY, maxY+1):
    line = ''
    for x in range(minX, maxX+1):
        line += '#' if (x,y) in elfPositions else '.'
    log.info(line)

log.warning(f'Took {(time.time() - startTime) * 1000}ms')