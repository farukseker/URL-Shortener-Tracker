import string, random


def generate_short_code(length: int = 6):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=length))
