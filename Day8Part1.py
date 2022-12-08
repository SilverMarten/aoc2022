'''How many trees are visible from outside the grid?'''

visible = set()

with open('inputs/Day8 sample.txt') as input:
    lines = input.read().splitlines()

    for y in range(len(lines)):
        for x in range(len(lines[y])):
            pass


print(f'{len(visible)} trees are visible from outside the grid.')