import logging, Colorer
from collections import deque
from Tools import sign
from tqdm import tqdm

class Node:
    def __init__(self, value, index) -> None:
        self.value = value
        self.index = index

    def __str__(self) -> str:
        return f'{self.value} ({self.round})'

'''
The grove coordinates can be found by looking at the 1000th, 2000th, and 3000th numbers
after the value 0, wrapping around the list as necessary.
What is the sum of the three numbers that form the grove coordinates?
'''

logging.basicConfig(format='%(message)s', level=logging.WARN)
log = logging.getLogger()
CR = '\n'

with open('inputs/Day20.txt') as fileInput:
    lines = fileInput.read().splitlines()

decryptionKey = 811589153
values = deque()
for i in range(len(lines)):
    values.append(Node(int(lines[i]) * decryptionKey, i))

originalOrder = list(values)
numValues = len(values)
log.info(f'Initial arrangement:{CR}{", ".join([str(value.value) for value in values])}{CR}')

zero = None
for round in tqdm(range(10)):
    for node in originalOrder:
        if node.value == 0:
            zero = node
        else:
            del values[node.index]
            newIndex = (node.index + node.value) % (numValues - 1)
            if newIndex == 0:
                newIndex = numValues - 1
            
            values.insert(newIndex, node)

            # Update all the indices
            for i in range(numValues):
                values[i].index = i

            log.debug(f'{node.value} moves between {values[(newIndex - 1) % numValues].value} and {values[(newIndex + 1) % numValues].value}:' +\
                    f'{CR}{", ".join([str(value.value) for value in values])}{CR}')

    log.info(f'After {round+1} rounds of mixing:{CR}{", ".join([str(value.value) for value in values])}{CR}')

offset = zero.index
coordinates = (values[(1000 + offset)%numValues].value, 
               values[(2000 + offset)%numValues].value, 
               values[(3000 + offset)%numValues].value)
sum = sum(coordinates)
print(f'The sum of the three numbers that form the grove coordinates {coordinates} is {sum}')
