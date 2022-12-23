prioritySum = 0

compartments = ['','']

with open('inputs/Day3.txt') as input:
    for line in input.readlines():
        line = line.strip('\n\r')
        compartments[0], compartments[1] = line[:int(len(line)/2)], line[int(len(line)/2):]
        # print(compartments)
        # https://www.geeksforgeeks.org/python-intersection-two-lists/
        intersection = list(set(compartments[0]) & set(compartments[1]))[0]
        # print(intersection)
        priority = ord(intersection) - (ord('a') - 1 if intersection.islower() else ord('A') - 27)
        # print(priority)
        prioritySum += priority

print(f'The sum of the item priorities is {prioritySum}.')