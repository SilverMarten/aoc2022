'''How many characters need to be processed before the first start-of-packet marker is detected?'''


with open('inputs/Day6.txt') as input:
    lines = input.read().splitlines()

    for line in lines:
        # print(line)
        for i in range(len(line)):
            # if i > 3: print(line[i-3:i+1])
            if i > 3 and len(set(line[i-3:i+1])) == 4: break

        print(f'The first start-of-packet marker is detected after {i+1} characters.')