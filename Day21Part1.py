import logging, Colorer
from collections import deque

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
            self.value = int(self.job)
        else:
            values = self.job.split()
            self.operation = values[1]
            self.dependsOn = [values[0], values[2]]

    def computeValue(self, monkeys):
        if self.value != None:
            return self.value
        # elif self.dependsOn[0] in monkeys.keys() \
        #     and self.dependsOn[1] in monkeys.keys():
        elif monkeys[self.dependsOn[0]].value != None \
            and monkeys[self.dependsOn[1]].value != None:
            self.value = eval(f'int({monkeys[self.dependsOn[0]].value}) {self.operation} int({monkeys[self.dependsOn[1]].value})')
            return self.value
        
        return None

    def __str__(self) -> str:
        return f'{self.name}: {self.job} ({self.value})'

'''
What number will the monkey named root yell?
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

print(f'The monkey named root will yell {monkeys["root"].value}')
