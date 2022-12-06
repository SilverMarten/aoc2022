'''In how many assignment pairs do the ranges overlap?'''

count = 0

with open('inputs/Day4.txt') as input:
    for line in input.read().splitlines():
        assignments = [set(range(int(assignment.split('-')[0]), int(assignment.split('-')[1]) + 1))
                       for assignment in line.split(',')]
        overlap = assignments[0] & assignments[1]
        if len(overlap) > 0:
            count += 1

print(f'There are {count} assignment pairs that overlap at all.')