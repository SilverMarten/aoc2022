import math
'''What is the highest scenic score possible for any tree?'''

highestScenicScore = 0

with open('inputs/Day8.txt') as input:
    lines = input.read().splitlines()
trees = []
for line in lines:
    trees.append([int(tree) for tree in line])
# print(trees)

for y in range(1,len(trees)-1):
    rowLength = len(trees[y])
    for x in range(1, rowLength-1):
        # print(f'({x},{y})')
        tree = trees[y][x]
        viewingDistances = [0,0,0,0]
        # Check up
        for i in range(y-1,-1,-1):
            viewingDistances[0] += 1
            if trees[i][x] >= tree:
                break
        # Check left
        for i in range(x-1,-1,-1):
            viewingDistances[1] += 1
            if trees[y][i] >= tree:
                break
        # Check right
        for i in range(x+1,rowLength):
            viewingDistances[2] += 1
            if trees[y][i] >= tree:
                break
        # Check down
        for i in range(y+1,len(trees)):
            viewingDistances[3] += 1
            if trees[i][x] >= tree:
                break

        scenicScore = math.prod(viewingDistances)
        if scenicScore > highestScenicScore: highestScenicScore = scenicScore

        # print(f'Scenic score: {scenicScore}\tViewing distances: {viewingDistances}')

# print(f'Visible trees: {sorted(visible)}')

print(f'The highest scenic score is {highestScenicScore}')