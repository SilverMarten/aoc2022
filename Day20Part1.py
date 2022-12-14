import logging, Colorer
from collections import deque

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.round = 0

    def __str__(self) -> str:
        return f'{self.value} ({self.round})'

'''
The grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers
after the value 0, wrapping around the list as necessary.
What is the sum of the three numbers that form the grove coordinates?
'''

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()
CR = '\n'

with open('inputs/Day20.txt') as fileInput:
    lines = fileInput.read().splitlines()

values = deque([Node(int(value)) for value in lines])
numValues = len(values)
log.debug(f'Initial arrangement:{CR}{", ".join([str(value.value) for value in values])}{CR}')

round = 1
i = 0
zero = None
while i < numValues:
    node = values[i]
    if node.value == 0:
        zero = node
        i += 1
    elif node.round != round:
        del values[i]
        node.round = round
        newIndex = (i + node.value) % (numValues - 1)
        if newIndex == 0:
            newIndex = numValues - 1
            
        values.insert(newIndex, node)

        log.debug(f'{node.value} moves between {values[(newIndex - 1) % numValues].value} and {values[(newIndex + 1) % numValues].value}:' +\
                  f'{CR}{", ".join([str(value.value) for value in values])}{CR}')
    else:
        i += 1




log.debug(f'Final arrangement:{CR}{", ".join([str(value.value) for value in values])}{CR}')

offset = values.index(zero)
coordinates = (values[(1000 + offset)%numValues].value, 
               values[(2000 + offset)%numValues].value, 
               values[(3000 + offset)%numValues].value)
sum = sum(coordinates)
print(f'The sum of the three numbers that form the grove coordinates {coordinates} is {sum}')
