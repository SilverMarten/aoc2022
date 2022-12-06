prioritySum = 0

with open('inputs/Day3.txt') as input:
    lines = input.read().splitlines()
    for i in range(int(len(lines)/3)):
        # https://www.geeksforgeeks.org/python-intersection-two-lists/
        intersection = list(set(lines[i*3]) & set(lines[i*3+1]) & set(lines[i*3+2]))[0]
        # print(intersection)
        priority = ord(intersection) - (ord('a') - 1 if intersection.islower() else ord('A') - 27)
        # print(priority)
        prioritySum += priority

print(f'The sum of the item priorities is {prioritySum}.')