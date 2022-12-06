
calories = {1:0}
elf = 1

with open('inputs/Day1.txt') as input:
    for line in input.readlines():
        # print(line)
        if line == '\n':
            elf += 1
            calories[elf] = 0
        else:
            calories[elf] += int(line)

# top3Calories = sorted(calories, key=calories.get, reverse=True)[:3]
top3Calories = dict(sorted(calories.items(), key=lambda item: item[1], reverse=True)[:3])

print(f'The top three most calories is #{top3Calories} with a sum of {sum(top3Calories.values())} calories.')