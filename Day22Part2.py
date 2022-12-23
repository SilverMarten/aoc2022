import logging, Colorer, math, re
import time
startTime = time.time()

'''
--- Day 22: Monkey Map ---
Follow the path given in the monkeys' notes. 
What is the final password?
'''

class Grid:
    number: int
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

sample = False
logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()
CR = '\n'

with open(f"inputs/Day22{' sample' if sample else ''}.txt") as fileInput:
    lines = fileInput.read().splitlines()

# Parse lines
# The last line is the directions, and the seconsd to last line is blank
directionsLine = lines.pop()
lines.pop()
distances = [int(distance) for distance in re.split('\D+', directionsLine)]
turns = [-1 if turn == 'L' else 1 for turn in re.split('\d+', directionsLine)[1:-1]]
log.debug(f'Distances: {distances}{CR}Turns: {turns}')

map:dict[tuple[int,int], Grid] = {}
grids:dict[str, Grid] = {}

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
        grids[grid.number] = grid


# log.debug('Map:\n' + '\n'.join([f'{grid[0][1] * mapWidth + grid[0][0]} ' + str(grid[0]) + ":\n" + str(grid[1]) for grid in map.items()]))
log.debug('Map:\n' + '\n'.join([str(grid) for grid in map.values()]))

# Connect the grids
translations: dict[tuple, tuple] = {}
if sample:
    neighbours = grids[2].connections
    neighbours[0] = grids[11]
    translations[(2,11)] = ('x', 'squareSize - y - 1', 2)
    neighbours[1] = grids[6]
    translations[(2,6)] = ('x', '0', 1)
    neighbours[2] = grids[5]
    translations[(2,5)] = ('y', '0', 1)
    neighbours[3] = grids[4]
    translations[(2,4)] = ('squareSize - x - 1', '0', 1)
    
    neighbours = grids[4].connections
    neighbours[0] = grids[5]
    translations[(4,5)] = ('0', 'y', 0)
    neighbours[1] = grids[10]
    translations[(4,10)] = ('squareSize - x - 1', 'squareSize - 1', 3)
    neighbours[2] = grids[11]
    translations[(4,11)] = ('squareSize - y - 1', 'squareSize - 1', 3)
    neighbours[3] = grids[2]
    translations[(4,2)] = ('squareSize - x - 1', '0', 1)

    neighbours = grids[5].connections
    neighbours[0] = grids[6]
    translations[(5,6)] = ('0', 'y', 0)
    neighbours[1] = grids[10]
    translations[(5,10)] = ('0', 'squareSize - x - 1', 0)
    neighbours[2] = grids[4]
    translations[(5,4)] = ('squareSize - 1', 'y', 2)
    neighbours[3] = grids[2]
    translations[(5,2)] = ('0', 'x', 0)

    neighbours = grids[6].connections
    neighbours[0] = grids[11]
    translations[(6,11)] = ('squareSize - y - 1', '0', 1)
    neighbours[1] = grids[10]
    translations[(6,10)] = ('x', '0', 1)
    neighbours[2] = grids[5]
    translations[(6,5)] = ('squareSize - 1', 'y', 2)
    neighbours[3] = grids[2]
    translations[(6,2)] = ('x', 'squareSize - 1', 3)

    neighbours = grids[10].connections
    neighbours[0] = grids[11]
    translations[(10,11)] = ('0', 'y', 0)
    neighbours[1] = grids[4]
    translations[(10,4)] = ('squareSize - x - 1', 'squareSize - 1', 3)
    neighbours[2] = grids[5]
    translations[(10,5)] = ('squareSize - y - 1', 'squareSize - 1', 3)
    neighbours[3] = grids[6]
    translations[(10,6)] = ('x', 'squareSize - 1', 3)
    
    neighbours = grids[11].connections
    neighbours[0] = grids[2]
    translations[(11,2)] = ('x', 'squareSize - y - 1', 2)
    neighbours[1] = grids[4]
    translations[(11,4)] = ('0', 'squareSize - x - 1', 0)
    neighbours[2] = grids[10]
    translations[(11,10)] = ('squareSize - 1', 'y', 2)
    neighbours[3] = grids[6]
    translations[(11,6)] = ('squareSize - 1', 'squareSize - x - 1', 2)
else: # Real data
    neighbours = grids[1].connections
    neighbours[0] = grids[2]
    translations[(1,2)] = ('0', 'y', 0)
    neighbours[1] = grids[4]
    translations[(1,4)] = ('x', '0', 1)
    neighbours[2] = grids[6]
    translations[(1,6)] = ('0', 'squareSize - y - 1', 0)
    neighbours[3] = grids[9]
    translations[(1,9)] = ('0', 'x', 0)
    
    neighbours = grids[2].connections
    neighbours[0] = grids[7]
    translations[(2,7)] = ('squareSize - 1', 'squareSize - y - 1', 2)
    neighbours[1] = grids[4]
    translations[(2,4)] = ('squareSize - 1', 'x', 2)
    neighbours[2] = grids[1]
    translations[(2,1)] = ('squareSize - 1', 'y', 2)
    neighbours[3] = grids[9]
    translations[(2,9)] = ('x', 'squareSize - 1', 3)

    neighbours = grids[4].connections
    neighbours[0] = grids[2]
    translations[(4,2)] = ('y', 'squareSize - 1', 3)
    neighbours[1] = grids[7]
    translations[(4,7)] = ('x', '0', 1)
    neighbours[2] = grids[6]
    translations[(4,6)] = ('y', '0', 1)
    neighbours[3] = grids[1]
    translations[(4,1)] = ('x', 'squareSize - 1', 3)

    neighbours = grids[6].connections
    neighbours[0] = grids[7]
    translations[(6,7)] = ('0', 'y', 0)
    neighbours[1] = grids[9]
    translations[(6,9)] = ('x', '0', 1)
    neighbours[2] = grids[1]
    translations[(6,1)] = ('0', 'squareSize - y - 1', 0)
    neighbours[3] = grids[4]
    translations[(6,4)] = ('0', 'x', 0)

    neighbours = grids[7].connections
    neighbours[0] = grids[2]
    translations[(7,2)] = ('squareSize - 1', 'squareSize - y - 1', 2)
    neighbours[1] = grids[9]
    translations[(7,9)] = ('squareSize - 1', 'x', 2)
    neighbours[2] = grids[6]
    translations[(7,6)] = ('squareSize - 1', 'y', 2)
    neighbours[3] = grids[4]
    translations[(7,4)] = ('x', 'squareSize - 1', 3)
    
    neighbours = grids[9].connections
    neighbours[0] = grids[7]
    translations[(9,7)] = ('y', 'squareSize - 1', 3)
    neighbours[1] = grids[2]
    translations[(9,2)] = ('x', '0', 1)
    neighbours[2] = grids[1]
    translations[(9,1)] = ('y', '0', 1)
    neighbours[3] = grids[6]
    translations[(9,6)] = ('x', 'squareSize - 1', 3)

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
while move > 0: #and len(moves) < 50:
    x = column + movement[facing][0]
    y = row + movement[facing][1]
    newFacing = facing
    newGrid:Grid = grid

    # if not between(newColumn, grid.start[0], grid.start[0] + squareSize, inclusive=False) or\
    #    not between(newRow, grid.start[1], grid.start[1] + squareSize, inclusive=False):
    #     newGrid = grid.connections[facing]
    # if not between(newColumn, 0, squareSize - 1) or\
    #    not between(newRow, 0, squareSize - 1):
    if x not in range(squareSize) or\
       y not in range(squareSize):
        newGrid = grid.connections[facing]
        # Apply transformation
        transX, transY, newFacing = translations[(grid.number, newGrid.number)]
        x, y = x % squareSize, y % squareSize
        x, y = eval(transX), eval(transY)

    # Does it hit a wall?
    if newGrid.cells[y][x] == '#':
        move = 0
    else:
        move -= 1
        column, row, facing, grid = x, y, newFacing, newGrid
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

if password >= 134056: log.error(f'Answer is too high! ({password})')
if password <= 3337: log.error(f'Answer is too low! ({password})')
log.warning(f'Took {(time.time() - startTime) * 1000}ms')