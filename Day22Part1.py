import logging, Colorer, math, re
import time
startTime = time.time()

'''
--- Day 22: Monkey Map ---
Follow the path given in the monkeys' notes. 
What is the final password?
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

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()
CR = '\n'

with open('inputs/Day22.txt') as fileInput:
    lines = fileInput.read().splitlines()

# Parse lines
# The last line is the directions, and the seconsd to last line is blank
directionsLine = lines.pop()
lines.pop()
distances = [int(distance) for distance in re.split('\D+', directionsLine)]
turns = [-1 if turn == 'L' else 1 for turn in re.split('\d+', directionsLine)[1:-1]]
log.debug(f'Distances: {distances}{CR}Turns: {turns}')

map:dict[tuple[int,int], Grid] = {}

# The map is in fact a series of connected squares
squareSize = int(math.sqrt(sum([len(line.lstrip()) for line in lines]) / 6))
mapWidth = max([len(line) for line in lines]) // squareSize
mapHeight = len(lines) // squareSize

grid = [[[] for c in range(mapWidth)] for r in range(mapHeight)]
for gridRow in range(mapHeight):
    for gridColumn in range(mapWidth):
        x, y = gridColumn * squareSize, gridRow * squareSize
        # If it's out of range, or just blank squares, continue
        if y >= len(lines) or x >= len(lines[y]) or lines[y][x] == ' ':
            continue

        gridStart = (x,y)
        cells = [line[x:x+squareSize] for line in lines[y:y+squareSize]]
        grid = Grid(y * mapWidth // squareSize + x // squareSize, gridStart, squareSize, cells)
        map[(x // squareSize, y // squareSize)] = grid


# log.debug('Map:\n' + '\n'.join([f'{grid[0][1] * mapWidth + grid[0][0]} ' + str(grid[0]) + ":\n" + str(grid[1]) for grid in map.items()]))
log.debug('Map:\n' + '\n'.join([str(grid) for grid in map.values()]))

# Connect the grids
for mapEntry in map.items():
    x,y = mapEntry[0]
    grid:Grid = mapEntry[1]
    n = 1
    while ((x + n)%mapWidth, y) not in map.keys():
        n += 1
    grid.connections[0] = map[((x + n)%mapWidth, y)]
    n = 1
    while ((x - n)%mapWidth, y) not in map.keys():
        n += 1    
    grid.connections[2] = map[((x - n)%mapWidth, y)]
    n = 1
    while (x, (y + n)%mapHeight) not in map.keys():
        n += 1
    grid.connections[1] = map[(x, (y + n)%mapHeight)]
    n = 1
    while (x, (y - n)%mapHeight) not in map.keys():
        n +=1
    grid.connections[3] = map[(x, (y - n)%mapHeight)]

log.info('\n'.join([f'Grid {grid.number} neighbours: {[neighbour.number for neighbour in grid.connections]}'\
                     for grid in map.values()]))

# Get on the grid
startColumn = min([grid.start[0] for grid in map.values() if grid.start[1] == 0])
grid:Grid = map[(startColumn // squareSize, 0)]

# Follow the directions
movement = [(1,0), (0,1), (-1,0), (0, -1)]
column = 0
row = 0
facing = 0
move = distances.pop(0)

log.info(f'Starting at {(column + grid.start[0] + 1, row +  grid.start[1] + 1)} with {move} moves.')

# Move on the grids
moves = [(column + grid.start[0] + 1, row +  grid.start[1] + 1)]
facings = [0]
while move > 0: # and len(moves) < 100:
    newColumn = column + movement[facing][0]
    newRow = row + movement[facing][1]
    newGrid:Grid = grid
    # if not between(newColumn, grid.start[0], grid.start[0] + squareSize, inclusive=False) or\
    #    not between(newRow, grid.start[1], grid.start[1] + squareSize, inclusive=False):
    #     newGrid = grid.connections[facing]
    # if not between(newColumn, 0, squareSize - 1) or\
    #    not between(newRow, 0, squareSize - 1):
    if newColumn not in range(squareSize) or\
       newRow not in range(squareSize):
        newGrid = grid.connections[facing]

    # Does it hit a wall?
    if newGrid.cells[newRow % squareSize][newColumn % squareSize] == '#':
        move = 0
    else:
        move -= 1
        column, row, grid = newColumn % squareSize, newRow % squareSize, newGrid
        moves.append((column + grid.start[0] + 1, row +  grid.start[1] + 1))
        facings.append(facing)

    if move <= 0:
        if not turns or not distances:
            break

        # Turn
        facing += turns.pop(0)
        facing %= 4
        facings.pop()
        facings.append(facing)

        move = distances.pop(0)

log.debug(f'Moves: {moves}')
absoluteColumn = column + grid.start[0] + 1
absoluteRow = row + grid.start[1] + 1
log.info(f'Final location: {(absoluteColumn, absoluteRow)}')

passwordString = f'1000 * {absoluteRow} + 4 * {absoluteColumn} + {facing}'

password = eval(passwordString)
print(f'{CR}The final password is {passwordString}: {password}')

# Check the moves
for column, row in moves:
    if lines[row - 1][column - 1] != '.':
        log.error(f'{move} is not a valid move; there is a {lines[row - 1][column - 1]} there!')

# Output the final map
directionsChars = ['>', 'v', '<', '^']
charMap = [list(line) for line in lines]
for move, facing in zip(moves, facings):
    column, row = move[0] - 1, move[1] - 1
    charMap[row][column] = directionsChars[facing]

charMap[row][column] = 'X'
with open('Day22 - output.txt', 'w') as outputFile:
    outputFile.writelines('\n'.join([''.join(line) for line in charMap]))

if password <= 32492: log.error(f'Answer is too low! ({password})')
log.warning(f'Took {(time.time() - startTime) * 1000}ms')