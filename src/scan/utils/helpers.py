from string import ascii_letters

def is_letter(char):
    return char in ascii_letters
def is_number(char):
    return char in list(map(str, range(0,10)))
