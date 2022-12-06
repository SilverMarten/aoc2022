
outcomes = {'A': {'X': 3, 'Y': 4, 'Z': 8},
            'B': {'X': 1, 'Y': 5, 'Z': 9},
            'C': {'X': 2, 'Y': 6, 'Z': 7}}

score = 0

with open('inputs/Day2.txt') as input:
    for line in input.readlines():
        throws = line.strip('\n\r').split(' ')
        score += outcomes[throws[0]][throws[1]]

print(f'The total score is {score}.')