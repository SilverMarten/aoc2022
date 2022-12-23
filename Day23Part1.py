import logging, Colorer, operator
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

def printMap(elves:set[tuple[int, int]]) -> str:
    maxX:int = max([x for x,y in elves])
    minX:int = min([x for x,y in elves])
    maxY:int = max([y for x,y in elves])
    minY:int = min([y for x,y in elves])

    map = ''
    for y in range(minY, maxY+1):
        line = ''
        for x in range(minX, maxX+1):
            line += '#' if (x,y) in elves else '.'
        map += line + CR

    return map

def isEmptyAround(checkPosition:tuple[int,int], elfPositions:set[tuple[int, int]]) -> bool:
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            if x == 0 and y == 0:
                continue

            if tuple(map(operator.add, checkPosition, (x,y))) in elfPositions:
                return False
    return True

def isEmptyInDirection(checkPosition:tuple[int,int], offsets:list[tuple[int,int]], elfPositions:set[tuple[int, int]]) -> bool:
    for offset in offsets:
        if tuple(map(operator.add, checkPosition, offset)) in elfPositions:
            return False
    return True

sample = False
logging.basicConfig(format='%(message)s', level=logging.DEBUG if sample else logging.WARN)
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
# N, S, W, E (times two)
directions:list[list[tuple[int,int]]] = [[(-1,-1),(0,-1),(1,-1)], \
                                         [(-1,1),(0,1),(1,1)], \
                                         [(-1,-1),(-1,0),(-1,1)], \
                                         [(1,-1),(1,0),(1,1)], \
                                         [(-1,-1),(0,-1),(1,-1)], \
                                         [(-1,1),(0,1),(1,1)], \
                                         [(-1,-1),(-1,0),(-1,1)], \
                                         [(1,-1),(1,0),(1,1)]]
directionIndex = 0
propsedMoves:dict[tuple[int,int], list[tuple[int,int]]] = {}

log.info('== Initial State ==' + CR + printMap(elfPositions))

for round in range(1, 11):
    # Propose new positions
    propsedMoves.clear()
    for elf in elfPositions:
        if isEmptyAround(elf, elfPositions): continue

        for offsets in directions[directionIndex:directionIndex+4]:
            # Check for elves
            if isEmptyInDirection(elf, offsets, elfPositions):
                propsedDirection = tuple(map(operator.add, elf, offsets[1]))
                if propsedDirection in propsedMoves.keys():
                    propsedMoves[propsedDirection].append(elf)
                else:
                    propsedMoves[propsedDirection] = [elf]
                break
    log.debug(f'Proposed directions:{CR}{CR.join([str(item) for item in propsedMoves.items()])}')

    # Move to allowed positions
    for newPosition, elves in propsedMoves.items():
        if len(elves) == 1:
            elfPositions.remove(elves[0])
            elfPositions.add(newPosition)

    log.info(f'== End of Round {round} ==' + CR + printMap(elfPositions))
    directionIndex = (directionIndex + 1) % 4


# Count the empty tiles
maxX:int = max([x for x,y in elfPositions])
minX:int = min([x for x,y in elfPositions])
maxY:int = max([y for x,y in elfPositions])
minY:int = min([y for x,y in elfPositions])

emptyTiles = (maxX - minX + 1) * (maxY - minY + 1) - len(elfPositions)
print(f'{CR}The number of empty ground tiles is {emptyTiles}')

# log.info('Final map:')
# for y in range(minY, maxY+1):
#     line = ''
#     for x in range(minX, maxX+1):
#         line += '#' if (x,y) in elfPositions else '.'
#     log.info(line)

log.warning(f'Took {(time.time() - startTime) * 1000}ms')