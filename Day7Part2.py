
'''
Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update.
What is the total size of that directory?
'''
TOTAL_DISK_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000

class Node:
    '''A node in a file system'''
    def __init__(self, name, type, parent = None, bytes = 0):
        self.name = name
        self.type = type
        self.contents = {}
        self.parent = parent
        self.bytes = int(bytes)
        
    def __str__(self):
        return f'{self.bytes} {self.name}' if self.type == 'file' else \
               f'{self.type} {self.name}\n' + \
               '\n'.join([str(dir) for dir in self.contents.values()])

    def size(self):
        '''Compute the size of the node based on its type'''
        if self.type == 'file': return self.bytes

        return sum([dir.size() for dir in self.contents.values()])

root = Node('/', 'dir')

pwd = root

with open('inputs/Day7.txt') as input:
    lines = input.read().splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        # print(line)
        
        # Handle the commands
        if line.startswith('$ cd /'):
            # print('Switching to root.')
            pwd = root
        elif line.startswith('$ cd ..'):
            # print('Switching to parent.')
            pwd = pwd.parent
        elif line.startswith('$ cd'):
            dir = line[5:]
            # print(f'Switching to {dir}.')
            pwd = pwd.contents[dir]
        elif line.startswith('$ ls'):
            # Parse each line of the directory listing
            node = None
            while i+1 < len(lines) and not lines[i+1].startswith('$'):
                i += 1
                line = lines[i].split()
                name = line[1]
                if line[0] == 'dir':
                    node = Node(name, 'dir', pwd)
                    # print(f'Creating directory {name}')
                else:
                    node = Node(name, 'file', pwd, line[0])
                    # print(f'Creating file {node}')
                pwd.contents[name] = node

        i += 1

# print(root)

freeSpace = TOTAL_DISK_SPACE - root.size()
neededSpace = REQUIRED_SPACE - freeSpace

print(f'There are {freeSpace} bytes free. An additional {neededSpace} bytes are needed.')

# Work out the size of each directory, keep those over the needed space
candidates = {}
directoriesToCheck = [root]
while len(directoriesToCheck) > 0:
    dir = directoriesToCheck.pop(0)
    dirSize = dir.size()
    if dirSize >= neededSpace:
        candidates[dir] = dirSize
    
    directoriesToCheck.extend([dir for dir in dir.contents.values() if dir.type == 'dir'])

smallest = sorted(candidates.items(), key=lambda i: i[1])[0][0]


print(f'The size of the smallest directory that, if deleted, would free up enough space on the filesystem to run the update is {smallest.name} ({smallest.size()}).') 