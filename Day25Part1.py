import logging, Colorer, time, numpy

startTime = time.time()

'''
--- Day 25: Full of Hot Air ---
What SNAFU number do you supply to Bob's console?
'''

def toSnafuNumber(decimalNumber:int) -> str:
    values:dict[int, str] = dict(zip([0,1,2,3,4],'012=-'))
    
    base5String = numpy.base_repr(decimalNumber, 5)

    # Adjust from the right
    snafuString = ''
    digits = [int(n) for n in base5String]
    carry = 0
    while digits:
        digit = int(digits.pop()) + carry
        carry = (digit+2) // 5 if digit > 2  else 0
        snafuString = values[digit % 5] + snafuString

    log.debug(f'{decimalNumber} => {base5String} => {snafuString}')
    return snafuString.lstrip('0')

def fromSnafuNumber(snafuNumber:str) -> int:
    values:dict[str, int] = dict(zip('=-012',[-2,-1,0,1,2]))
    return sum([values[digit] * 5 ** power for power, digit in enumerate(reversed(snafuNumber))])

sample = False
logging.basicConfig(format='%(message)s', level=logging.DEBUG if sample else logging.WARN)
log = logging.getLogger()
CR = '\n'

with open(f"inputs/Day25{' sample' if sample else ''}.txt") as fileInput:
    lines = fileInput.read().splitlines()

# Parse lines
fuelRequirements = [fromSnafuNumber(snafuNumber) for snafuNumber in lines]
log.info(f'Fuel requirements:{CR}{CR.join([f"{snafu:>6} {dec:>7}" for snafu, dec in zip(lines, fuelRequirements)])}')

fuelSum = sum(fuelRequirements)
log.warning(f'Fuel requirement sum: {fuelSum}')


snafuNumber = toSnafuNumber(fuelSum)
if fromSnafuNumber(snafuNumber) != fuelSum:
    log.error(f'{snafuNumber} != {fuelSum}')
    exit(1)

print(f'{CR}The number to enter is {snafuNumber}')

log.warning(f'Took {(time.time() - startTime) * 1000}ms')