
maxCalories = 0
maxElf = 0

calories = 0
elf = 1

with open('inputs/Day1.txt') as input:
    for line in input.readlines():
        # print(line)
        if line == '\n':
            if calories > maxCalories:
                maxElf = elf
                maxCalories = calories
            
            calories = 0
            elf += 1
        else:
            calories += int(line)

print(f'The elf with the most calories is #{maxElf} with {maxCalories} calories.')