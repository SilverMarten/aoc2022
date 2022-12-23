import logging, Colorer, math
import time
startTime = time.time()

'''
Figure out which monkeys to chase by counting how many items they inspect over 20 rounds.
What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans?
'''

class Monkey:
    def __init__(self, items, operation, test, trueMonkey, falseMonkey):
        self.items = items
        self.operation = operation
        self.test = test
        self.trueMonkey = trueMonkey
        self.falseMonkey = falseMonkey
        self.inspected = 0

    def __str__(self):
        return f'  Starting items: {self.items}\n' +\
               f'  Operation: {self.operation}\n' +\
               f'  Test: divisible by {self.test}\n' +\
               f'    If true: throw to monkey {self.trueMonkey}\n' +\
               f'    If false: throw to monkey {self.falseMonkey}\n'


logging.basicConfig(format='%(message)s', level=logging.ERROR)
log = logging.getLogger()

with open('inputs/Day11.txt') as input:
    lines = input.read().splitlines()

monkeys = []

# Setup the monkeys
for i in range(0, len(lines), 7):
    items = [int(i) for i in lines[i+1][18:].split(", ")]
    operation = lines[i+2][19:]
    test = int(lines[i+3][21:])
    trueMonkey = int(lines[i+4][-1])
    falseMonkey = int(lines[i+5][-1])
    monkeys.append(Monkey(items, operation, test, trueMonkey, falseMonkey))

for monkey in monkeys:
    log.debug(str(monkey))

# simulate 10,000 rounds
for round in range(10_000):
    # if round > 0 and log.level == logging.DEBUG:
    #     log.setLevel(logging.INFO)

    log.info(f'Round {round+1}:')

    primeProduct = math.prod([2,3,5,7,11,13,17,19,23])
    i = 0
    for monkey in monkeys:
        log.debug(f'Monkey {i}:')

        while len(monkey.items) > 0:
            old = monkey.items.pop(0)
            log.debug(f'  Monkey inspects an item with a worry level of {old}.')
            log.debug(f'    Operation: {monkey.operation}')
            new = eval(monkey.operation)
            log.debug(f'    New worry level: {new}.')
            # new = math.floor(new / 3)
            new = new % primeProduct
            log.debug(f'    Monkey gets bored with item. Worry level is modded by {primeProduct} to {new}.')
            if new % monkey.test == 0:
                log.debug(f'    Current worry level is divisible by {monkey.test}.')
                monkeys[monkey.trueMonkey].items.append(new)
                log.debug(f'    Item with worry level {new} is thrown to monkey {monkey.trueMonkey}.')
                log.info(f'M{i}: {old} -> {new} % {monkey.test} -> M{monkey.trueMonkey}')
            else:
                log.debug(f'    Current worry level is not divisible by {monkey.test}.')
                monkeys[monkey.falseMonkey].items.append(new)
                log.debug(f'    Item with worry level {new} is thrown to monkey {monkey.falseMonkey}.')
                log.info(f'M{i}: {old} -> {new} !% {monkey.test} -> M{monkey.falseMonkey}')
            monkey.inspected += 1
    
        i += 1

    if round+1 in [1,20] or (round+1)%1000 == 0\
        or round in range(20):
        log.warning(f'\nRound {round+1}:')
        # i = 0
        for monkey in range(len(monkeys)):
            log.warning(f'Monkey {monkey} inspected items {monkeys[monkey].inspected} times')
            # i += 1

monkeys = sorted(monkeys, key=lambda m: m.inspected, reverse=True)
monkeyBusiness = monkeys[0].inspected * monkeys[1].inspected
assert monkeyBusiness > 2570891260, f'{monkeyBusiness} is too low!'
print(f'The level of monkey business after 10,000 rounds is {monkeyBusiness}')

# 2570891260 is too low


log.error(f'Took {(time.time() - startTime) * 1000}ms')