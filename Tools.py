'''
Useful methods
'''

class bcolors:
    '''See: https://stackoverflow.com/a/287944'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

LogColours = {
    'DEBUG': '\033[32m',
    'INFO': '\033[34m',
    'WARN': '\033[33m',
    'ERROR': '\033[31m',
    'CRITICAL': '\033[91m'
}


def sign(number):
    '''
    Return the sign of the given number, or 0 if the input in 0.
    See: https://note.nkmk.me/en/python-sign-copysign/
    '''

    return (number > 0) - (number < 0 )