import logging, Colorer
from collections import deque
from sympy import symbols, solve

class Monkey:
    def __init__(self, name, job) -> None:
        self.name = name
        self.job = job
        self.value = None
        self.operation = None
        self.dependsOn = []
        self.parseJob()

    def parseJob(self):
        '''Parse the job string into a value, or an operation'''
        if self.job.isnumeric():
            self.value = self.job
        else:
            values = self.job.split()
            self.operation = values[1]
            self.dependsOn = [values[0], values[2]]

    def computeValue(self, monkeys):
        if self.value != None:
            return self.value
        elif monkeys[self.dependsOn[0]].value != None \
            and monkeys[self.dependsOn[1]].value != None:
            self.value = f'({monkeys[self.dependsOn[0]].value} {self.operation} {monkeys[self.dependsOn[1]].value})'
            return self.value
        
        return None

    def __str__(self) -> str:
        return f'{self.name}: {self.job} ({self.value})'

'''
What number do you yell to pass root's equality test?
'''

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()
CR = '\n'

with open('inputs/Day21.txt') as fileInput:
    lines = fileInput.read().splitlines()

monkeys = {}

# Parse lines
for line in lines:
    name = line.split(': ')[0]
    monkey = Monkey(name, line.split(': ')[1])
    monkeys[name] = monkey

monkeys['root'].operation = '=='
monkeys['humn'].value = 'x'

# Start from root, and add dependencies to the queue
queue = deque()
queue.append(monkeys['root'])

while queue:
    monkey = queue.pop()

    # If its value can't been computed
    if monkey.computeValue(monkeys) == None:
        # Put it back on the queue, along with it's dependencies
        queue.append(monkey)
        queue.extend([monkeys[dependsOn] for dependsOn in monkey.dependsOn])
    
    # Otherwise, it can stay off the queue
    log.debug(f'Queue: {[monkey.name for monkey in queue]}')

log.debug(f'Final values:{CR}{CR.join([str(monkey) for monkey in monkeys.values()])}{CR}')

equation = monkeys['root'].value
log.debug(f'Final equation: {equation}')

x = symbols('x')
lhs = equation.split('==')[0]
rhs = equation.split('==')[1]
solution = int(solve(eval(f'{lhs} - {rhs}'))[0])

print(f'The number you need to yell is {solution}')
