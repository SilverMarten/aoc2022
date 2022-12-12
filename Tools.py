import random
'''
Useful methods
'''

def sign(number):
    '''
    Return the sign of the given number, or 0 if the input in 0.
    See: https://note.nkmk.me/en/python-sign-copysign/
    '''

    return (number > 0) - (number < 0 )

def isDivisible(number, divisor):
    '''
        Using rules, determine if a number is evenly divisible by a given divisor.
        Only covers 2, 3, 5, 7, 11, 13, 17, and 19. Returns None otherwise.
        See: https://en.wikipedia.org/wiki/Divisibility_rule#Divisibility_rules_for_numbers_1%E2%80%9330
    '''

    if number < 1_000:
        return number % divisor == 0

    numberString = str(number)
    divisible = None
    match(divisor):
        case 2:
            divisible = numberString[-1] in ['0', '2', '4', '6', '8']
        case 3:
            # divisible = isDivisible(sum([int(n) for n in numberString]), 3)
            # Subtract the quantity of the digits 2, 5, and 8 in the number from 
            # the quantity of the digits 1, 4, and 7 in the number.
            divisible = isDivisible(sum([1 for n in numberString if n in ['2', '5', '8']])\
                                    - sum([1 for n in numberString if n in ['1', '4', '7']]), 3)
        case 5:
            divisible = numberString[-1] in ['0','5']
        case 7:
            # Subtracting 2 times the last digit from the rest gives a multiple of 7.
            divisible = isDivisible(int(numberString[:-1]) - int(numberString[-1]) * 2, 7)
        case 11:
            # Form the alternating sum of the digits, or equivalently sum(odd) - sum(even).
            divisible = isDivisible(sum([int(numberString[n]) * (-1 if n%2 == 0 else 1) \
                                         for n in range(len(numberString))]), 11)
        case 13:
            # Subtract the last two digits from four times the rest.
            divisible = isDivisible(int(numberString[:-2]) * 4 - int(numberString[-2:]), 13)
        case 17:
            # Subtract the last two digits from two times the rest.
            divisible = isDivisible(int(numberString[:-2]) * 2 - int(numberString[-2:]), 17)
        case 19:
            # Add 4 times the last two digits to the rest.
            divisible = isDivisible(int(numberString[:-2]) + int(numberString[-2:]) * 4, 19)
        case _:
            pass
    
    return divisible


def testIsDivisible():
    valid = {2: 1_294,
             3: 16_499_205_854_376,
             5: 423_295,
             7: 1_369_851,
             7: 483_595,
             7: 204_540,
             11: 918_082,
             11: 14_179,
             13: 2_911_272,
             17: 4_675,
             19: 6_935}

    for validCombo in valid.items():
        assert isDivisible(validCombo[1], validCombo[0]), f'{validCombo[1]} divide by {validCombo[0]}'

    for i in range(1_000_000):
        for divisor in [2,3,5,7,11,13,19]:
            number = random.randint(1_000_000_000, 1_000_000_000_000) * random.randint(1_000_000_000, 1_000_000_000_000)
            assert isDivisible(number*divisor, divisor), f'{number*divisor} divide by {divisor}'

if __name__ == "__main__":
    testIsDivisible()
    print('Pass')