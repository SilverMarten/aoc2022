
outcomes = {'A': {'X': 4, 'Y': 8, 'Z': 3},
            'B': {'X': 1, 'Y': 5, 'Z': 9},
            'C': {'X': 7, 'Y': 2, 'Z': 6}}

score = 0

with open('inputs/Day2.txt') as input:
    for line in input.readlines():
        throws = line.strip('\n\r').split(' ')
        score += outcomes[throws[0]][throws[1]]

print(f'The total score is {score}.')