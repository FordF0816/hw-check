# A correct solution — every rule should pass.

def sum_even_digits(n):
    total = 0
    while n > 0:
        n, r = divmod(n, 10)
        if r % 2 == 0:
            total = total + r
    return total


class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h
