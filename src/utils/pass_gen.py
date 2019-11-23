from random import choice
from string import ascii_letters, digits, punctuation


def gen_password() -> str:
    strs = ascii_letters + digits + punctuation
    return ''.join([choice(strs) for _ in range(10)])
