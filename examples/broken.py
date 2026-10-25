# A deliberately broken solution — every rule should fire.

def um_even_digits(n):
    total = 0
    while n > 0:
        n, r = divmod(n, 10)
        if r % 2 == 0:
            total = r + total
    print("the answer is", total)
    return total


class Counter:
    def __init__(self, name):
        name = name
        return name
