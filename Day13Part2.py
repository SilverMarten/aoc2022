import logging, Colorer
from Tools import sign
from functools import cmp_to_key

'''
Organize all of the packets into the correct order.
What is the decoder key for the distress signal?
'''

def compare(left, right):
    # Both ints
    if isinstance(left, int) and isinstance(right, int):
        return sign(right - left)
    
    # Both list
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            result = compare(left[i], right[i])
            if result != 0:
                return result
        
        return sign(len(right) - len(left))

    # One int, one list
    if isinstance(left, list):
        return compare(left, [right])
    else:
        return compare([left], right)

logging.basicConfig(format='%(message)s', level=logging.INFO)
log = logging.getLogger()

with open('inputs/Day13.txt') as input:
    lines = input.read().splitlines()

# Add divider packets
divider1 = '[[2]]'
lines.append(divider1)
divider2 = '[[6]]'
lines.append(divider2)

# Parse the packets
packets = [eval(line) for line in lines if line != '']
log.debug('Unsorted: \n' + '\n'.join([str(packet) for packet in packets]))

packets = sorted(packets, key=cmp_to_key(compare), reverse=True)

log.debug('Sorted: \n' + '\n'.join([str(packet) for packet in packets]))

dividerPackets = [packets.index(eval(divider1))+1, packets.index(eval(divider2))+1]
log.debug(f'The divider packets are at: {dividerPackets}')

print(f'The decoder key for the distress signal: {dividerPackets[0] * dividerPackets[1]}')

