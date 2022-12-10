import logging, Colorer
from Tools import sign

'''How many positions does the tail of the rope visit at least once?'''

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

with open('inputs/Day9 sample.txt') as input:
    lines = input.read().splitlines()

rope = [(0,0) for i in range(10)]
visitedPositions = set()

for line in lines:
    logging.debug(line)
    for move in range(int(line[2:])):
        for i in range(len(rope)-1):
            headPosition = rope[i]
            tailPosition = rope[i+1]
            if i == 0:
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

            logging.info(f'Rope {i}: {headPosition}')
            # Move tail
            deltaX = headPosition[0]-tailPosition[0]
            deltaY = headPosition[1]-tailPosition[1]

            if abs(deltaX) > 1 or abs(deltaY) > 1:
                tailPosition = (tailPosition[0] + sign(deltaX), tailPosition[1] + sign(deltaY))
            
            rope[i] = headPosition
            rope[i+1] = tailPosition

        visitedPositions.add(rope[-1])
        logging.info(f'Tail: {rope[-1]}')

print(f'The tail of the rope visits {len(visitedPositions)} positions.')