import logging, Colorer
from Tools import sign

'''
Find the signal strength during the 20th, 60th, 100th, 140th, 180th, and 220th cycles.
What is the sum of these six signal strengths?
'''

logging.basicConfig(format='%(message)s', level=logging.INFO)

with open('inputs/Day10.txt') as input:
    lines = input.read().splitlines()

registerValues = [1]

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

relevantCycles = [20, 60, 100, 140, 180, 220]
answer = sum([cycle * registerValues[cycle-1] for cycle in relevantCycles])
print(f'The sum of the six signal strengths is {answer}')