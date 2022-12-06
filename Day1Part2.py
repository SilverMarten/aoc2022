
calories = [0]

with open('inputs/Day1.txt') as input:
    for line in input.readlines():
        if line == '\n':
            calories.append(0)
        else:
            calories[-1] += int(line)

top3Calories = sorted(calories, reverse=True)[:3]

print(f'The top three most calories is #{top3Calories} with a sum of {sum(top3Calories)} calories.')