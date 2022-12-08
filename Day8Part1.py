
'''How many trees are visible from outside the grid?'''

visible = set()

with open('inputs/Day8.txt') as input:
    lines = input.read().splitlines()

trees = []
for line in lines:
    trees.append([int(tree) for tree in line])
# print(trees)

# Keep track of the highest trees in each column
highestFromTop = dict([(x,-1) for x in range(len(trees[0]))])
highestFromBottom = dict([(x,-1) for x in range(len(trees[0]))])
for y in range(len(trees)):
    # The highest trees in this row
    highestFromLeft = -1
    highestFromRight = -1
    rowLength = len(trees[y])
    for x in range(rowLength):
        # print(f'({x},{y})')
        if trees[y][x] > highestFromLeft:
            # print(f'({x},{y}) is visible from the left.')
            highestFromLeft = trees[y][x]
            visible.add((x,y))
        if trees[y][rowLength-x-1] > highestFromRight:
            # print(f'({rowLength-x-1},{y}) is visible from the right.')
            highestFromRight = trees[y][rowLength-x-1]
            visible.add((rowLength-x-1,y))
        if trees[y][x] > highestFromTop[x]:
            # print(f'({x},{y}) is visible from the top.')
            highestFromTop[x] = trees[y][x]
            visible.add((x,y))
        if trees[len(trees)-y-1][x] > highestFromBottom[x]:
            # print(f'({x},{len(trees)-y-1}) is visible from the bottom.')
            highestFromBottom[x] = trees[len(trees)-y-1][x]
            visible.add((x,len(trees)-y-1))
        pass

# print(f'Visible trees: {sorted(visible)}')

print(f'{len(visible)} trees are visible from outside the grid.')