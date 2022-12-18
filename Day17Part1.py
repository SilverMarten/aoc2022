import logging, Colorer
from Rocks import *
from tqdm import tqdm

def printRoom(room):
    return '\n'.join(reversed([''.join(line) for line in room]))

'''
How many units tall will the tower of rocks be after 2022 rocks have stopped falling?
'''

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()

with open('inputs/Day17.txt') as inputFile:
    directions = inputFile.read()

lineLength = len(directions)
directionIndex = 0

rocks = [Line, Plus, Corner, Column, Box]
numRocks = len(rocks)

room = [list('+-------+')]

height = 0

# Drop 2022 rocks
for n in range(2022):
    # Start the rock so that its left edge is two units away from the left wall
    # and its bottom edge is three units above the highest rock
    rock = rocks[n % numRocks]()
    x = 3 # Count the left wall...
    y = height + 3 + rock.height

    # Add rows, if needed
    for _ in range(height + rock.height + 4 - len(room)):
        room.append(list('|.......|'))

    # While the rock is not stopped, move it, then lower it (or stop it)
    stopped = False
    while not stopped:
        if directions[directionIndex] == '<' and rock.canMoveLeft(room, (x,y)):
            x -= 1
        elif directions[directionIndex] == '>' and rock.canMoveRight(room, (x,y)):
            x += 1
        directionIndex += 1
        directionIndex %= lineLength

        if rock.canMoveDown(room, (x,y)):
            y -= 1
        else:
            rock.stop(room, (x,y))
            stopped = True
    if n < 10:
        log.debug(f'\nRock {n}:' + '\n' + printRoom(room))
        # if log.level == logging.DEBUG: input()

    # Adjust height
    for row in range(height, len(room)):
        if ''.join(room[row]) == '|.......|':
            height = row - 1
            break

with open('Day17 - tower.txt', 'w') as fileOutput:
    fileOutput.write(printRoom(room))

print(f'After 2022 rounds the tower is {height} units tall.')
assert height > 2847, 'Answer is too low!'