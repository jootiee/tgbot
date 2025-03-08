from random import choice
from string import ascii_letters 

def gen_url() -> str:
    return ''.join([choice(ascii_letters) for _ in range(16)])