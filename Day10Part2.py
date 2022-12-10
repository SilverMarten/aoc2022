import logging, Colorer
from Tools import sign

'''
Render the image given by your program.
What eight capital letters appear on your CRT?
'''

logging.basicConfig(format='%(message)s', level=logging.INFO)

with open('inputs/Day10.txt') as input:
    lines = input.read().splitlines()

registerValues = [1]

# Calculate register values
for line in lines:
    logging.debug(line)
    match line[:4]:
        case 'addx':
            registerValues.append(registerValues[-1])
            registerValues.append(int(line[5:]) + registerValues[-1])
            pass
        case 'noop':
            registerValues.append(registerValues[-1])
            pass

logging.debug(registerValues)

for i in range(240):
    if i % 40 == 0:
        print()

    if abs(registerValues[i] - i % 40) <= 1:
        print('#', end='')
    else:
        print('.', end='')
