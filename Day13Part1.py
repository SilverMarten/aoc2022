import logging, Colorer
from tqdm import tqdm
from Tools import sign

'''
Determine which pairs of packets are already in the right order.
What is the sum of the indices of those pairs?
'''

def compare(left, right):
    # Both ints
    if isinstance(left, int) and isinstance(right, int):
        return sign(right - left)
    
    # Both list
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            result = compare(left[i], right[i])
            if result != 0:
                return result
        
        return sign(len(right) - len(left))

    # One int, one list
    if isinstance(left, list):
        return compare(left, [right])
    else:
        return compare([left], right)

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()

with open('inputs/Day13.txt') as input:
    lines = input.read().splitlines()

orderedLines = []

# Parse the map
for i in range(0, len(lines), 3):
    logging.debug(f'Comparing {lines[i]} and {lines[i+1]}.')
    left = eval(lines[i])
    right = eval(lines[i+1])
    if compare(left, right) > 0:
        log.debug('They are in the right order.')
        orderedLines.append(int(i/3 + 1))
    else:
        log.debug('They are not in the right order.')

log.info(f'The pairs in the right order are: {orderedLines}')

print(f'The sum of the indicies of the correctly ordered pairs is: {sum(orderedLines)}')

