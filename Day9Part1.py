import logging
from Tools import sign

'''How many positions does the tail of the rope visit at least once?'''

logging.basicConfig(format='%(message)s', level=logging.INFO)

with open('inputs/Day9.txt') as input:
    lines = input.read().splitlines()

headPosition = (0,0)
tailPosition = (0,0)
visitedPositions = set()

for line in lines:
    logging.debug(line)
    for move in range(int(line[2:])):
        # Move head
        match line[0]:
            case 'U':
                headPosition = (headPosition[0], headPosition[1] + 1)
            case 'D':
                headPosition = (headPosition[0], headPosition[1] - 1)
            case 'R':
                headPosition = (headPosition[0] + 1, headPosition[1])
            case 'L':
                headPosition = (headPosition[0] - 1, headPosition[1])

        logging.debug(f'Head: {headPosition}')
        # Move tail
        deltaX = headPosition[0]-tailPosition[0]
        deltaY = headPosition[1]-tailPosition[1]

        if abs(deltaX) > 1 or abs(deltaY) > 1:
            tailPosition = (tailPosition[0] + sign(deltaX), tailPosition[1] + sign(deltaY))
        
        visitedPositions.add(tailPosition)
        logging.debug(f'Tail: {tailPosition}')

print(f'The tail of the rope visits {len(visitedPositions)} positions.')