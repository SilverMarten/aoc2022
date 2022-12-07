'''
Find all of the directories with a total size of at most 100000.
What is the sum of the total sizes of those directories?
'''

fileSystem = {}

pwd = []

with open('inputs/Day7 sample.txt') as input:
    lines = input.read().splitlines()

    for i in len(lines):
        line = lines[i]
        # print(line)
        
        # Go back up one in the path
        if line.startswith('$ cd ..'):
            pwd.pop()
        elif line.startswith('$ cd'):
            dir = line[6:]

            pwd.append(dir)

print(f'The first start-of-packet marker is detected after {i+1} characters.')