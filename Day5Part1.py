'''After the rearrangement procedure completes, what crate ends up on top of each stack?'''

stacks = []

with open('inputs/Day5 sample.txt') as input:
    # Read the starting conditions
    for line in input.read().splitlines():
        if line == '': break

    # Read the instructions and process them
    for line in input.read().splitlines():
        fromStack = line.split(' from' )[0]

print(f'After the rearrangement procedure, the top of the stacks are: {[box[0] for box in stacks]}')