from random import choice
from string import ascii_letters, digits, punctuation


def gen_password() -> str:
    '''
    Utility function for generating a random password made up of
    alphanumeric characters and punctuation.\n
    Params: None\n
    Returns: A 10 character long, randomly generated string.
    '''
    strs = ascii_letters + digits + punctuation
    return ''.join([choice(strs) for _ in range(10)])

