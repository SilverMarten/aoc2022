'''After the rearrangement procedure completes, what crate ends up on top of each stack?'''

stacks = [[] for i in range(9)]

with open('inputs/Day5.txt') as input:
    lines = input.read().splitlines()

    # Read the starting conditions
    for line in lines:
        # print(line)
        if line == '' or line.startswith(' 1'): break

        for i in range(int((len(line)+1)/4)):
            box = line[i * 4 + 1]
            if box.isalpha(): stacks[i].append(box)

    for stack in stacks: stack.reverse() 
    # print(stacks)

    # Read the instructions and process them
    for line in lines:
        if not line.startswith('move'): continue

        toStack = int(line[-1])
        fromStack = int(line[-6])
        howMany = int(line[5:-12])
        # print(f'move {howMany} from {fromStack} to {toStack}')
        for i in range(howMany):
            stacks[toStack - 1].append(stacks[fromStack - 1].pop())
        
        # print(stacks)

print(f'After the rearrangement procedure, the top of the stacks are: {[box[-1] for box in stacks if len(box) > 0]}')